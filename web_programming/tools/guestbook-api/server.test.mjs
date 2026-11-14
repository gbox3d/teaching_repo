import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { createGuestbookServer } from './server.mjs';

async function fixture(t) {
  const directory = mkdtempSync(path.join(tmpdir(), 'classroom-rest-test-'));
  let server;
  let base;
  async function start() {
    server = createGuestbookServer({ directory });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    base = `http://127.0.0.1:${server.address().port}/rest/v1/guestbook`;
  }
  async function stop() { await new Promise(resolve => server.close(resolve)); }
  await start();
  t.after(async () => { await stop(); rmSync(directory, { recursive: true, force: true }); });
  const keys = JSON.parse(readFileSync(path.join(directory, 'local-edit-keys.json'), 'utf8'));
  async function request(method = 'GET', query = '', body, key, extras = {}) {
    return fetch(base + query, {
      method,
      headers: { apikey: 'classroom-local', 'Content-Type': 'application/json', Prefer: 'return=representation', ...(key ? { 'X-Edit-Key': key } : {}), ...extras },
      ...(body === undefined ? {} : { body: typeof body === 'string' ? body : JSON.stringify(body) })
    });
  }
  return { request, keys, info: (route, options = {}) => fetch(new URL(route, base), options), restart: async () => { await stop(); await start(); } };
}

test('소개·도움말은 공개 키로 조회하고 쓰기 요청은 거부한다', async t => {
  const { request, info } = await fixture(t);
  const headers = { apikey: 'classroom-local' };
  const before = await (await request()).json();
  const response = await info('/rest/v1/about', { headers });
  assert.equal(response.status, 200);
  assert.match(response.headers.get('content-type'), /application\/json/);
  const [about] = await response.json();
  assert.equal(about.version, 'v1');
  assert.equal(about.help_path, '/rest/v1/help');
  const listed = await info(about.help_path + '?order=step.asc', { headers });
  assert.equal(listed.status, 200);
  const help = await listed.json();
  assert.deepEqual(help.map(row => row.method), ['GET', 'GET', 'GET', 'POST', 'PATCH', 'DELETE']);
  assert.deepEqual(help.map(row => row.step), [1, 2, 3, 4, 5, 6]);
  for (const route of ['/rest/v1/about', '/rest/v1/help']) {
    assert.equal((await info(route)).status, 401);
    assert.equal((await info(route, { headers: { apikey: 'wrong' } })).status, 401);
    for (const method of ['POST', 'PATCH', 'DELETE']) {
      assert.equal((await info(route, { method, headers })).status, 405);
    }
    const preflight = await info(route, { method: 'OPTIONS' });
    assert.equal(preflight.status, 204);
    assert.equal(preflight.headers.get('access-control-allow-origin'), '*');
  }
  assert.deepEqual(await (await request()).json(), before);
});

test('CRUD, 재시작 후 유지, 다른 학생 키의 변경 거부', async t => {
  const { request, keys, restart } = await fixture(t);
  const query = '?book_id=eq.student01&order=id.desc&select=id,name,message,created_at&limit=50';
  assert.equal((await request('OPTIONS')).status, 204);
  const posted = await request('POST', '', { book_id: 'student01', name: '연습', message: '<b>안녕하세요</b>' });
  assert.equal(posted.status, 201);
  const [row] = await posted.json();
  const byId = `?book_id=eq.student01&id=eq.${row.id}`;
  assert.equal((await (await request('GET', query)).json())[0].message, '<b>안녕하세요</b>');
  assert.equal((await (await request('GET', query)).json())[0].book_id, undefined);
  assert.deepEqual(await (await request('PATCH', byId, { message: 'wrong' }, keys.student02)).json(), []);
  assert.equal((await request('DELETE', byId, undefined, keys.student02)).status, 204);
  assert.equal((await (await request('GET', byId)).json()).length, 1);
  const patched = await request('PATCH', byId, { message: '수정 완료' }, keys.student01);
  assert.equal(patched.status, 200);
  assert.equal((await patched.json())[0].message, '수정 완료');
  await restart();
  assert.equal((await (await request('GET', byId)).json())[0].message, '수정 완료');
  const removed = await request('DELETE', byId, undefined, keys.student01);
  assert.equal(removed.status, 204);
  assert.equal(await removed.text(), '');
  assert.deepEqual(await (await request('GET', byId)).json(), []);
});

test('입력 제한, 잘못된 JSON, 보호된 필드, CORS', async t => {
  const { request, keys } = await fixture(t);
  const cases = [
    ['POST', '', '{bad'],
    ['POST', '', { book_id: 'student01', name: '', message: 'x' }],
    ['POST', '', { book_id: 'student01', name: '\t\n', message: 'x' }],
    ['POST', '', { book_id: 'student01', name: ' '.repeat(30) + 'x', message: 'x' }],
    ['POST', '', { book_id: 'student01', name: 'x', message: 'x'.repeat(501) }],
    ['POST', '', { book_id: 'student01', name: 'x', message: 'x' + ' '.repeat(500) }],
    ['POST', '', { book_id: '__proto__', name: 'x', message: 'x' }],
    ['POST', '', { book_id: 'student01', name: 'x', message: 'x', id: 3 }],
    ['PATCH', '?book_id=eq.student01&id=eq.1', { book_id: 'student02' }],
    ['DELETE', '?book_id=eq.student01'],
    ['GET', '?limit=NaN'],
    ['GET', '?book_id=like.student%'],
    ['GET', '?select=edit_key_hash']
  ];
  for (const [method, query, body] of cases) {
    const response = await request(method, query, body, keys.student01);
    assert.equal(response.status, 400, `${method} ${query}`);
  }
  assert.equal((await request('GET', '', undefined, undefined, { apikey: 'wrong' })).status, 401);
  assert.equal((await request('POST', '', 'x'.repeat(8193))).status, 413);
  assert.equal((await request('POST', '', { book_id: 'student01', name: '연습', message: 'x' }, undefined, { 'Content-Type': 'application/json-invalid' })).status, 415);
  const preflight = await request('OPTIONS');
  assert.match(preflight.headers.get('access-control-allow-headers'), /x-edit-key/);
  assert.equal(preflight.headers.get('access-control-allow-origin'), '*');
});

test('편집 키가 없거나 대상 방명록이 다르면 글을 변경하지 않는다', async t => {
  const { request, keys } = await fixture(t);
  const byId = '?book_id=eq.student02&id=eq.2';
  const before = await (await request('GET', byId)).json();
  for (const key of [undefined, 'not-an-edit-key', keys.student01]) {
    assert.deepEqual(await (await request('PATCH', byId, { message: '변경 시도' }, key)).json(), []);
    assert.equal((await request('DELETE', byId, undefined, key)).status, 204);
    assert.deepEqual(await (await request('GET', byId)).json(), before);
  }
  for (const body of [{ id: 99 }, { book_id: 'student01' }, { created_at: '2000-01-01' }]) {
    assert.equal((await request('PATCH', byId, body, keys.student02)).status, 400);
  }
  assert.deepEqual(await (await request('GET', byId)).json(), before);
});

test('이름과 메시지 길이는 공백을 포함하고 한글·이모지는 문자로 센다', async t => {
  const { request } = await fixture(t);
  const response = await request('POST', '', { book_id: 'student01', name: '가'.repeat(30), message: '🙂'.repeat(500) });
  assert.equal(response.status, 201);
  const [row] = await response.json();
  assert.equal([...row.name].length, 30);
  assert.equal([...row.message].length, 500);
  assert.equal((await request('POST', '', { book_id: 'student01', name: '가'.repeat(31), message: 'x' })).status, 400);
});

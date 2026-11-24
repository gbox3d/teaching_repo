import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
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
  async function request(method = 'GET', query = '', body, extras = {}) {
    return fetch(base + query, {
      method,
      headers: { apikey: 'classroom-local', 'Content-Type': 'application/json', Prefer: 'return=representation', ...extras },
      ...(body === undefined ? {} : { body: typeof body === 'string' ? body : JSON.stringify(body) })
    });
  }
  return { request, info: (route, options = {}) => fetch(new URL(route, base), options), restart: async () => { await stop(); await start(); } };
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
  assert.deepEqual(help.map(row => row.method), ['GET', 'GET', 'POST', 'GET', 'PATCH', 'DELETE']);
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

test('공용 키로 글 한 건 생성·조회·수정·삭제, 서버 재시작 후 내용 유지', async t => {
  const { request, restart } = await fixture(t);
  const query = '?book_id=eq.student01&order=id.desc&select=id,name,message,created_at&limit=50';
  assert.equal((await request('OPTIONS')).status, 204);
  const posted = await request('POST', '', { book_id: 'student01', name: '연습', message: '<b>안녕하세요</b>' });
  assert.equal(posted.status, 201);
  const [row] = await posted.json();
  const byId = `?book_id=eq.student01&id=eq.${row.id}`;
  assert.equal((await (await request('GET', query)).json())[0].message, '<b>안녕하세요</b>');
  assert.equal((await (await request('GET', query)).json())[0].book_id, undefined);
  const patched = await request('PATCH', byId, { message: '수정 완료' });
  assert.equal(patched.status, 200);
  assert.equal((await patched.json())[0].message, '수정 완료');
  await restart();
  assert.equal((await (await request('GET', byId)).json())[0].message, '수정 완료');
  const removed = await request('DELETE', byId);
  assert.equal(removed.status, 204);
  assert.equal(await removed.text(), '');
  assert.deepEqual(await (await request('GET', byId)).json(), []);
});

test('입력 제한, 잘못된 JSON, 보호된 필드, CORS', async t => {
  const { request } = await fixture(t);
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
    ['GET', '?select=unknown']
  ];
  for (const [method, query, body] of cases) {
    const response = await request(method, query, body);
    assert.equal(response.status, 400, `${method} ${query}`);
  }
  assert.equal((await request('GET', '', undefined, { apikey: 'wrong' })).status, 401);
  assert.equal((await request('POST', '', 'x'.repeat(8193))).status, 413);
  assert.equal((await request('POST', '', { book_id: 'student01', name: '연습', message: 'x' }, { 'Content-Type': 'application/json-invalid' })).status, 415);
  const preflight = await request('OPTIONS');
  assert.equal(preflight.headers.get('access-control-allow-headers'), 'apikey, content-type, prefer');
  assert.equal(preflight.headers.get('access-control-allow-origin'), '*');
});

test('태그와 글 번호가 모두 일치해야 한 건만 변경되고 보호 열은 유지된다', async t => {
  const { request } = await fixture(t);
  const target = '?book_id=eq.student02&id=eq.2';
  const wrongTag = '?book_id=eq.student01&id=eq.2';
  const neighbor = '?book_id=eq.student01&id=eq.1';
  const original = await (await request('GET', target)).json();
  const untouched = await (await request('GET', neighbor)).json();

  assert.deepEqual(await (await request('PATCH', wrongTag, { message: '수정 시도' })).json(), []);
  assert.equal((await request('DELETE', wrongTag)).status, 204);
  assert.deepEqual(await (await request('GET', target)).json(), original);
  for (const body of [{ id: 99 }, { book_id: 'student01' }, { created_at: '2000-01-01' }]) {
    assert.equal((await request('PATCH', target, body)).status, 400);
  }
  for (const method of ['PATCH', 'DELETE']) {
    const body = method === 'PATCH' ? { message: '수정 시도' } : undefined;
    assert.equal((await request(method, target, body, { apikey: 'wrong' })).status, 401);
  }
  await request('DELETE', target);
  assert.deepEqual(await (await request('GET', target)).json(), []);
  assert.deepEqual(await (await request('GET', neighbor)).json(), untouched);
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

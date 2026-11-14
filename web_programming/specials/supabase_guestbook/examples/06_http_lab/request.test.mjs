import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';
import { walk, checkFile } from '../../../home_iot_http/examples/simulator/check_ui_copy.mjs';

const source = name => readFileSync(new URL(name, import.meta.url), 'utf8');

test('HTTP 실험 화면의 한국어 문구가 작성 규칙을 따른다', () => {
  const findings = walk(fileURLToPath(new URL('../', import.meta.url)))
    .filter(file => !file.endsWith('config.example.js'))
    .flatMap(file => checkFile(file));
  assert.deepEqual(findings, []);
});

function context(extra = {}) {
  const ctx = vm.createContext({ URL, API_BASE_URL: 'http://127.0.0.1:8787', API_PUBLIC_KEY: 'classroom-local', BOOK_ID: 'student01', ...extra });
  vm.runInContext(source('request.js'), ctx);
  return ctx;
}

test('PATCH와 DELETE는 글 ID 없이는 보내지 않는다', () => {
  const ctx = context();
  assert.throws(() => ctx.buildRequest('DELETE', 'student01', '', '', 'key'));
  assert.throws(() => ctx.buildRequest('PATCH', 'student01', '', '{}', 'key'));
  assert.throws(() => ctx.buildRequest('DELETE', 'student01', '1&book_id=eq.student02', '', 'key'));
  const req = ctx.buildRequest('DELETE', 'student01', '41', '', 'key');
  const url = new URL(req.url);
  assert.equal(url.searchParams.get('book_id'), 'eq.student01');
  assert.equal(url.searchParams.get('id'), 'eq.41');
  assert.equal(req.options.headers['X-Edit-Key'], 'key');
  assert.equal(req.options.body, undefined);
});

test('POST와 PATCH는 JSON 객체, GET은 읽기 필터를 사용한다', () => {
  const ctx = context();
  assert.throws(() => ctx.buildRequest('POST', 'student01', '', '[]', ''));
  assert.throws(() => ctx.buildRequest('PATCH', 'student01', '41', 'not json', 'key'));
  const post = ctx.buildRequest('POST', 'student01', '', '{"book_id":"student01","name":"연습","message":"값"}', '');
  assert.equal(post.options.headers['Content-Type'], 'application/json');
  assert.equal(post.options.headers.Prefer, 'return=representation');
  assert.equal(JSON.parse(post.options.body).book_id, 'student01');
  const get = ctx.buildRequest('GET', 'student01', '', '', '');
  assert.equal(get.options.headers['X-Edit-Key'], undefined);
  assert.equal(new URL(get.url).searchParams.get('limit'), '50');
});

function fakePage() {
  const elements = {};
  for (const id of ['request-form', 'method', 'book', 'id', 'body', 'edit-key', 'send', 'notice', 'api-address', 'sample', 'response-status', 'response-body', 'request-summary', 'observation']) {
    elements['#' + id] = { value: '', textContent: '', disabled: false, events: {}, addEventListener(name, fn) { this.events[name] = fn; } };
  }
  return { elements, document: { querySelector: id => elements[id] } };
}

test('204 응답 표시, 편집 키 입력·요약 비노출, 버튼 복구', async () => {
  const page = fakePage();
  let sent;
  const ctx = context({ document: page.document, fetch: async (url, options) => { sent = { url, options }; return new Response(null, { status: 204 }); } });
  vm.runInContext(source('exercise.js'), ctx);
  vm.runInContext(source('app.js'), ctx);
  page.elements['#method'].value = 'DELETE';
  page.elements['#id'].value = '41';
  page.elements['#edit-key'].value = 'never-print-this-edit-key';
  await page.elements['#request-form'].events.submit({ preventDefault() {} });
  assert.equal(sent.options.headers['X-Edit-Key'], 'never-print-this-edit-key');
  assert.equal(page.elements['#edit-key'].value, '');
  assert.equal(page.elements['#response-body'].textContent, '(본문 없음)');
  assert.match(page.elements['#response-status'].textContent, /204/);
  assert.equal(page.elements['#send'].disabled, false);
  for (const element of Object.values(page.elements)) assert.ok(!element.textContent.includes('never-print-this-edit-key'));
});

test('요청 오류를 안내하고 다음 요청 버튼을 복구한다', async () => {
  const page = fakePage();
  const ctx = context({ document: page.document, fetch: async () => { throw new Error('connection failed'); } });
  vm.runInContext(source('exercise.js'), ctx);
  vm.runInContext(source('app.js'), ctx);
  page.elements['#method'].value = 'GET';
  await page.elements['#request-form'].events.submit({ preventDefault() {} });
  assert.match(page.elements['#notice'].textContent, /요청 실패/);
  assert.equal(page.elements['#send'].disabled, false);
});

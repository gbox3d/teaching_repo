import test from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { fileURLToPath } from 'node:url';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { createSimulator } from './server.mjs';
import { walk, checkFile } from './check_ui_copy.mjs';

async function start(t) {
  const server = createSimulator();
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  t.after(() => new Promise((resolve) => { server.closeAllConnections(); server.close(resolve); }));
  const base = 'http://127.0.0.1:' + server.address().port;
  return {
    base,
    get: (url) => fetch(base + url),
    patch: (url, body, extra = {}) => fetch(base + url, { method: 'PATCH', headers: { 'Content-Type': 'application/json', ...extra }, body: JSON.stringify(body) })
  };
}

test('GET과 PATCH가 전등·선풍기·온도 상태를 공유한다', async (t) => {
  const api = await start(t);
  let state = await (await api.get('/api/state')).json();
  assert.deepEqual(state.light, { on: false, brightness: 60 });
  assert.equal(state.environment.temperature, 24);
  assert.equal((await api.patch('/api/devices/light', { on: true, brightness: 40 })).status, 200);
  assert.equal((await api.patch('/api/devices/fan', { on: true })).status, 200);
  assert.equal((await api.patch('/api/environment', { temperature: 29.5 })).status, 200);
  state = await (await api.get('/api/state')).json();
  assert.deepEqual(state.light, { on: true, brightness: 40 });
  assert.equal(state.fan.on, true);
  assert.equal(state.environment.temperature, 29.5);
  assert.equal(state.revision, 3);
  assert.equal(state.log.length, 3);
});

test('부분 변경은 다른 상태를 보존하고 가상 팬이 온도를 바꾸지 않는다', async (t) => {
  const api = await start(t);
  await api.patch('/api/devices/light', { brightness: 0 });
  await api.patch('/api/devices/light', { on: true });
  await api.patch('/api/devices/fan', { on: true });
  const state = await (await api.get('/api/state')).json();
  assert.deepEqual(state.light, { on: true, brightness: 0 });
  assert.equal(state.environment.temperature, 24);
});

test('잘못된 값은 400이고 상태가 바뀌지 않는다', async (t) => {
  const api = await start(t);
  for (const body of [{ on: 'true' }, { brightness: 101 }, { brightness: 3.5 }, { mystery: true }, {}, [], null]) {
    assert.equal((await api.patch('/api/devices/light', body)).status, 400);
  }
  assert.equal((await api.patch('/api/environment', { temperature: 41 })).status, 400);
  assert.equal((await api.patch('/api/environment', { temperature: '28' })).status, 400);
  const state = await (await api.get('/api/state')).json();
  assert.equal(state.revision, 0);
  assert.deepEqual(state.light, { on: false, brightness: 60 });
});

test('JSON 형식·본문 크기·메서드·존재하지 않는 경로를 구분한다', async (t) => {
  const api = await start(t);
  let response = await fetch(api.base + '/api/devices/light', { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: '{' });
  assert.equal(response.status, 400);
  response = await fetch(api.base + '/api/devices/light', { method: 'PATCH', body: '{}' });
  assert.equal(response.status, 415);
  assert.equal((await api.patch('/api/devices/light', { value: 'x'.repeat(5000) })).status, 413);
  assert.equal((await api.get('/api/devices/light')).status, 405);
  assert.equal((await api.patch('/api/state', { on: true })).status, 405);
  assert.equal((await api.get('/api/devices/unknown')).status, 404);
});

test('다른 사이트의 제어 요청과 서버 소스 접근을 거절한다', async (t) => {
  const api = await start(t);
  assert.equal((await api.patch('/api/devices/light', { on: true }, { Origin: 'https://example.com' })).status, 403);
  assert.equal((await api.get('/server.mjs')).status, 404);
  assert.equal((await api.get('/examples/ex01/%2e%2e%2f%2e%2e%2fsimulator/server.mjs')).status, 404);
  assert.equal((await api.get('/examples/ex01/%2e%2e%2fex02/app.js')).status, 404);
  assert.equal((await (await api.get('/api/state')).json()).light.on, false);
});

test('대시보드와 모든 실습 화면·코드를 제공한다', async (t) => {
  const api = await start(t);
  const exerciseFiles = ['ex01', 'ex02', 'ex03', 'student', 'reference'].flatMap((name) => ['/examples/' + name + '/', '/examples/' + name + '/app.js']);
  exerciseFiles.push('/examples/automatic/', '/examples/automatic/policy.js', '/examples/automatic/runner.js', '/examples/automatic_student/', '/examples/automatic_student/policy.js');
  for (const url of ['/', '/styles.css', '/app.js', ...exerciseFiles]) {
    const response = await api.get(url);
    assert.equal(response.status, 200, url);
    assert.equal(response.headers.get('cache-control'), 'no-store');
  }
});

test('요청 기록은 최근 12건까지만 보관한다', async (t) => {
  const api = await start(t);
  for (let i = 0; i < 15; i++) await api.patch('/api/devices/light', { brightness: i });
  const state = await (await api.get('/api/state')).json();
  assert.equal(state.log.length, 12);
  assert.equal(state.log[0].body.brightness, 14);
  assert.equal(state.log[11].body.brightness, 3);
});

test('학생 화면과 서버 응답의 한국어 문구가 작성 규칙을 따른다', () => {
  const directory = fileURLToPath(new URL('../', import.meta.url));
  const findings = walk(directory).flatMap((file) => checkFile(file));
  assert.deepEqual(findings, []);
});

function controllerFixture(fetch) {
  const nodes = new Map();
  function element() {
    return {
      value: '', textContent: '', disabled: false, children: [],
      addEventListener() {},
      prepend(child) { this.children.unshift(child); child.remove = () => this.children.splice(this.children.indexOf(child), 1); },
      get lastElementChild() { return this.children.at(-1); }
    };
  }
  const document = { querySelector(id) { if (!nodes.has(id)) nodes.set(id, element()); return nodes.get(id); }, createElement: element };
  for (const [id, value] of Object.entries({ mode: 'single', threshold: '27.5', low: '26', high: '29', interval: '2000' })) document.querySelector('#' + id).value = value;
  const timers = new Map();
  let timerId = 0;
  const context = vm.createContext({ document, window: { addEventListener() {} }, fetch, AbortController, Date, JSON, Error, Number, Math, URL, Blob,
    setTimeout(fn, delay) { const id = ++timerId; timers.set(id, { fn, delay }); return id; },
    clearTimeout(id) { timers.delete(id); }
  });
  for (const file of ['policy.js', 'runner.js']) vm.runInContext(readFileSync(new URL('../automatic/' + file, import.meta.url), 'utf8'), context);
  return { nodes, timers, context, start: () => context.startControl(), stop: () => context.stopControl(), fire(delay) { const entry = [...timers.entries()].find(([, timer]) => timer.delay === delay); assert.ok(entry, '예약 간격 ' + delay); timers.delete(entry[0]); entry[1].fn(); } };
}

const tick = () => new Promise(resolve => setImmediate(resolve));

test('단일 기준과 26/29도 히스테리시스는 같은 입력에서 다른 전환 수를 만든다', () => {
  const context = vm.createContext({});
  vm.runInContext(readFileSync(new URL('../automatic/policy.js', import.meta.url), 'utf8'), context);
  const single = { mode: 'single', threshold: 27.5, low: 26, high: 29 };
  const hysteresis = { ...single, mode: 'hysteresis' };
  assert.deepEqual([27.4, 27.6, 27.4, 27.6].map(value => context.decideFan(value, false, single)), [false, true, false, true]);
  assert.deepEqual([27.4, 27.6, 27.4, 27.6].map(value => context.decideFan(value, false, hysteresis)), [false, false, false, false]);
  assert.equal(context.decideFan(29, false, hysteresis), true);
  assert.equal(context.decideFan(27, true, hysteresis), true);
  assert.equal(context.decideFan(26, true, hysteresis), false);
});

test('시작을 반복해도 진행 중 GET을 겹치지 않고 완료 후 다음 검사를 예약한다', async () => {
  let resolveRequest;
  let calls = 0;
  const runner = controllerFixture(() => { calls += 1; return new Promise(resolve => { resolveRequest = resolve; }); });
  runner.start();
  runner.start();
  assert.equal(calls, 1);
  assert.deepEqual([...runner.timers.values()].map(timer => timer.delay), [3000]);
  resolveRequest({ ok: true, json: async () => ({ environment: { temperature: 24 }, fan: { on: false } }) });
  await tick();
  assert.deepEqual([...runner.timers.values()].map(timer => timer.delay), [2000]);
  runner.fire(2000);
  assert.equal(calls, 2);
  runner.stop();
});

test('통신 실패는 4/8/10초 대기 후 재시도하고 중지하면 예약을 취소한다', async () => {
  let calls = 0;
  const runner = controllerFixture(async () => { calls += 1; throw new Error('연결 실패'); });
  runner.start();
  await tick();
  for (const delay of [4000, 8000, 10000]) {
    assert.equal(runner.nodes.get('#notice').textContent, '재시도 대기 · ' + delay + 'ms');
    runner.fire(delay);
    await tick();
  }
  assert.equal(calls, 4);
  runner.stop();
  assert.equal(runner.timers.size, 0);
  assert.equal(runner.nodes.get('#notice').textContent, '중지됨 · 새 요청 없음');
});

test('중지 중 도착한 GET 응답은 PATCH나 다음 검사로 이어지지 않는다', async () => {
  let resolveRequest;
  let calls = 0;
  const runner = controllerFixture(() => { calls += 1; return new Promise(resolve => { resolveRequest = resolve; }); });
  runner.start();
  runner.stop();
  resolveRequest({ ok: true, json: async () => ({ environment: { temperature: 30 }, fan: { on: false } }) });
  await tick();
  assert.equal(calls, 1);
  assert.equal(runner.timers.size, 0);
  assert.equal(runner.nodes.get('#notice').textContent, '중지됨 · 새 요청 없음');
});

test('복구 후 정상 간격으로 돌아가고 상태가 다를 때만 PATCH를 보낸다', async () => {
  let available = false;
  let fanOn = false;
  const requests = [];
  const runner = controllerFixture(async (url, options = {}) => {
    requests.push({ url, method: options.method || 'GET' });
    if (!available) throw new Error('연결 실패');
    if (options.method === 'PATCH') fanOn = JSON.parse(options.body).on;
    return { ok: true, json: async () => ({ environment: { temperature: 29 }, fan: { on: fanOn } }) };
  });
  runner.start();
  await tick();
  available = true;
  runner.fire(4000);
  await tick();
  assert.equal(fanOn, true);
  assert.equal(requests.filter(request => request.method === 'PATCH').length, 1);
  assert.deepEqual([...runner.timers.values()].map(timer => timer.delay), [2000]);
  assert.match(runner.nodes.get('#counts').textContent, /연속 실패 0회/);
  runner.fire(2000);
  await tick();
  assert.equal(requests.filter(request => request.method === 'PATCH').length, 1);
  runner.stop();
});

test('미완성 학생 정책은 안내 후 중지하며 제어 요청을 보내지 않는다', async () => {
  let calls = 0;
  const runner = controllerFixture(async () => {
    calls += 1;
    return { ok: true, json: async () => ({ environment: { temperature: 29 }, fan: { on: false } }) };
  });
  vm.runInContext(readFileSync(new URL('../automatic_student/policy.js', import.meta.url), 'utf8'), runner.context);
  runner.start();
  await tick();
  assert.equal(calls, 1);
  assert.equal(runner.timers.size, 0);
  assert.equal(runner.nodes.get('#start').disabled, false);
  assert.match(runner.nodes.get('#notice').textContent, /TODO를 완성하세요/);
});

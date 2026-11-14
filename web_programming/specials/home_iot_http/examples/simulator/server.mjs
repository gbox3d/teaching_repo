// 제공 서버: 학생은 examples/ex01~ex03 및 student/app.js를 수정한다.
import http from 'node:http';
import { readFile, realpath } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const examples = path.dirname(here);
const publicRoot = path.join(here, 'public');
const pages = new Set(['ex01', 'ex02', 'ex03', 'student', 'reference', 'automatic', 'automatic_student']);
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8' };

function reply(res, status, body, type = 'application/json; charset=utf-8', extra = {}) {
  const text = type.startsWith('application/json') ? JSON.stringify(body) : body;
  res.writeHead(status, { 'Content-Type': type, 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', ...extra });
  res.end(text);
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    if (req.headers['content-type']?.split(';')[0].trim() !== 'application/json') {
      req.resume();
      reject({ status: 415, message: 'Content-Type을 application/json으로 지정하세요.' });
      return;
    }
    const chunks = [];
    let length = 0;
    req.on('data', (chunk) => {
      length += chunk.length;
      if (length <= 4096) chunks.push(chunk);
    });
    req.on('error', reject);
    req.on('end', () => {
      if (length > 4096) return reject({ status: 413, message: '요청 본문은 4096바이트 이하여야 합니다.' });
      try { resolve(JSON.parse(Buffer.concat(chunks).toString('utf8'))); }
      catch { reject({ status: 400, message: 'JSON 형식을 확인하세요.' }); }
    });
  });
}

function validate(body, target) {
  if (!body || typeof body !== 'object' || Array.isArray(body) || Object.keys(body).length === 0) return false;
  const fields = target === 'light' ? ['on', 'brightness'] : target === 'fan' ? ['on'] : ['temperature'];
  if (Object.keys(body).some((key) => !fields.includes(key))) return false;
  if ('on' in body && typeof body.on !== 'boolean') return false;
  if ('brightness' in body && (!Number.isInteger(body.brightness) || body.brightness < 0 || body.brightness > 100)) return false;
  if ('temperature' in body && (!Number.isFinite(body.temperature) || body.temperature < 10 || body.temperature > 40)) return false;
  return true;
}

export function createSimulator() {
  const state = { light: { on: false, brightness: 60 }, fan: { on: false }, environment: { temperature: 24 }, revision: 0, log: [] };
  const server = http.createServer(async (req, res) => {
    const port = server.address()?.port;
    const hosts = [`127.0.0.1:${port}`, `localhost:${port}`];
    if (!hosts.includes(req.headers.host) || (req.headers.origin && !hosts.some((host) => req.headers.origin === `http://${host}`))) {
      req.resume();
      return reply(res, 403, { error: '이 PC의 시뮬레이터 화면에서 요청하세요.' });
    }
    let pathname;
    try { pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname); }
    catch { return reply(res, 400, { error: '요청 주소를 확인하세요.' }); }
    if (pathname.startsWith('/api/')) {
      if (pathname === '/api/state' && req.method === 'GET') return reply(res, 200, state);
      const target = pathname === '/api/devices/light' ? 'light' : pathname === '/api/devices/fan' ? 'fan' : pathname === '/api/environment' ? 'environment' : null;
      if (!target && pathname !== '/api/state') return reply(res, 404, { error: '요청한 장치 또는 API가 없습니다.' });
      if (req.method !== 'PATCH' || pathname === '/api/state') {
        req.resume();
        return reply(res, 405, { error: '이 주소에서 허용한 HTTP 메서드를 확인하세요.' }, undefined, { Allow: pathname === '/api/state' ? 'GET' : 'PATCH' });
      }
      let body;
      let status = 200;
      let error;
      try {
        body = await readJson(req);
        if (!validate(body, target)) throw { status: 400, message: '값을 확인하세요. on은 true/false, brightness는 0~100 정수, temperature는 10~40 숫자입니다.' };
        Object.assign(state[target], body);
        state.revision += 1;
      } catch (failure) {
        status = failure.status || 400;
        error = failure.message || '요청 본문을 읽지 못했습니다.';
      }
      state.log.unshift({ time: new Date().toISOString(), method: 'PATCH', path: pathname, body: error ? null : body, status });
      state.log.length = Math.min(state.log.length, 12);
      return reply(res, status, error ? { error } : state);
    }
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      req.resume();
      return reply(res, 405, { error: '화면 파일은 GET으로 요청하세요.' }, undefined, { Allow: 'GET, HEAD' });
    }
    let root = publicRoot;
    let relative = pathname.slice(1) || 'index.html';
    const parts = pathname.split('/');
    if (parts[1] === 'examples' && pages.has(parts[2])) {
      if (parts.length === 3) return reply(res, 301, '', 'text/plain; charset=utf-8', { Location: pathname + '/' });
      root = path.join(examples, parts[2]);
      relative = parts.slice(3).join('/') || 'index.html';
    }
    const candidate = path.resolve(root, relative);
    if (!candidate.startsWith(root + path.sep) || !types[path.extname(candidate)]) return reply(res, 404, { error: '화면 파일을 찾을 수 없습니다.' });
    try {
      const actual = await realpath(candidate);
      if (!actual.startsWith(root + path.sep)) return reply(res, 404, { error: '화면 파일을 찾을 수 없습니다.' });
      const data = await readFile(actual);
      reply(res, 200, req.method === 'HEAD' ? '' : data, types[path.extname(candidate)]);
    } catch { reply(res, 404, { error: '화면 파일을 찾을 수 없습니다.' }); }
  });
  server.requestTimeout = 10_000;
  server.headersTimeout = 10_000;
  return server;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const port = Number(process.argv[2] || 8014);
  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    console.error('포트는 1~65535 정수로 지정하세요.');
    process.exit(1);
  }
  const server = createSimulator();
  server.on('error', (error) => {
    console.error(error.code === 'EADDRINUSE' ? `${port}번 포트 사용 중. node examples/simulator/server.mjs ${port + 1}` : error.message);
    process.exitCode = 1;
  });
  server.listen(port, '127.0.0.1', () => console.log(`홈 IoT 시뮬레이터: http://localhost:${port}/ (종료: Ctrl+C)`));
}

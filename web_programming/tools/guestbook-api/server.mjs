// 강의자 로컬 리허설용: 수업에서 쓰는 Supabase REST 요청만 구현한다.
import http from 'node:http';
import { createHash, randomBytes } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const hash = value => createHash('sha256').update(value).digest('hex');
const columns = ['id', 'book_id', 'name', 'message', 'created_at'];
const error = (status, message) => Object.assign(new Error(message), { status });
const validText = (value, limit) => typeof value === 'string' && value.trim().length > 0 && [...value].length <= limit;
// about-help.sql과 같은 수업용 읽기 전용 응답이다.
const about = [{ name: '수업용 REST API', version: 'v1', description: 'REST API 접속과 데이터 처리를 연습합니다.', help_path: '/rest/v1/help' }];
const help = [
  { step: 1, method: 'GET', path: '/rest/v1/about', description: '서버 소개와 API 버전을 확인합니다.' },
  { step: 2, method: 'GET', path: '/rest/v1/help', description: '사용 가능한 요청을 확인합니다.' },
  { step: 3, method: 'GET', path: '/rest/v1/guestbook?book_id=eq.student01', description: '태그별 방명록을 조회합니다.' },
  { step: 4, method: 'POST', path: '/rest/v1/guestbook', description: 'book_id, name, message를 JSON으로 보내 글을 저장합니다.' },
  { step: 5, method: 'PATCH', path: '/rest/v1/guestbook?book_id=eq.student01&id=eq.123', description: '해당 방명록 편집 키로 선택한 글을 수정합니다.' },
  { step: 6, method: 'DELETE', path: '/rest/v1/guestbook?book_id=eq.student01&id=eq.123', description: '해당 방명록 편집 키로 선택한 글을 삭제합니다.' }
];

export function createGuestbookServer({ directory = fileURLToPath(new URL('./.local/', import.meta.url)) } = {}) {
  mkdirSync(directory, { recursive: true });
  const filename = path.join(directory, 'local-data.json');
  let state;
  const save = () => {
    writeFileSync(filename + '.tmp', JSON.stringify(state, null, 2) + '\n', { mode: 0o600 });
    renameSync(filename + '.tmp', filename);
  };
  if (existsSync(filename)) {
    state = JSON.parse(readFileSync(filename, 'utf8'));
  } else {
    const keys = {};
    const books = {};
    const messages = [];
    for (let number = 1; number <= 30; number++) {
      const id = `student${String(number).padStart(2, '0')}`;
      keys[id] = randomBytes(32).toString('hex');
      books[id] = hash(keys[id]);
      messages.push({ id: number, book_id: id, name: '안내', message: '온라인 방명록에 오신 것을 환영합니다.', created_at: new Date().toISOString() });
    }
    state = { nextId: 31, books, messages };
    writeFileSync(path.join(directory, 'local-edit-keys.json'), JSON.stringify(keys, null, 2) + '\n', { mode: 0o600 });
    save();
  }

  return http.createServer(async (req, res) => {
    // 자격 증명 쿠키를 쓰지 않는 로컬 실습 API. 공개 예제의 origin을 모두 허용한다.
    const baseHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PATCH, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'apikey, content-type, prefer, x-edit-key',
      'Cache-Control': 'no-store',
      'X-Content-Type-Options': 'nosniff'
    };
    const send = (status, data) => {
      res.writeHead(status, { ...baseHeaders, 'Content-Type': 'application/json; charset=utf-8' });
      res.end(status === 204 ? undefined : JSON.stringify(data));
    };
    try {
      const url = new URL(req.url, 'http://localhost');
      if (!['/rest/v1/about', '/rest/v1/help', '/rest/v1/guestbook'].includes(url.pathname)) throw error(404, '요청 주소를 확인하세요.');
      if (req.method === 'OPTIONS') return send(204);
      if (req.headers.apikey !== 'classroom-local') throw error(401, '로컬 실습용 apikey를 확인하세요.');
      if (url.pathname === '/rest/v1/about' || url.pathname === '/rest/v1/help') {
        if (req.method !== 'GET') throw error(405, '소개·도움말은 GET으로 조회하세요.');
        for (const [key, value] of url.searchParams) {
          if (url.pathname !== '/rest/v1/help' || key !== 'order' || value !== 'step.asc') {
            throw error(400, '로컬 소개·도움말에서는 help의 order=step.asc만 지원합니다.');
          }
        }
        return send(200, url.pathname === '/rest/v1/about' ? about : help);
      }
      if (!['GET', 'POST', 'PATCH', 'DELETE'].includes(req.method)) throw error(405, '지원하지 않는 요청 메서드입니다.');
      for (const key of url.searchParams.keys()) {
        if (!['book_id', 'id', 'select', 'order', 'limit'].includes(key)) throw error(400, '실습에서 지원하는 조회 조건을 사용하세요.');
      }
      const equality = key => {
        const value = url.searchParams.get(key);
        if (value === null) return null;
        if (!value.startsWith('eq.')) throw error(400, '조건에는 eq.를 사용하세요.');
        return value.slice(3);
      };
      const bookId = equality('book_id');
      const rowId = equality('id');
      if (bookId !== null && !/^[a-z0-9_-]{1,40}$/.test(bookId)) throw error(400, '방명록 번호 형식을 확인하세요.');
      if (rowId !== null && !/^[1-9][0-9]*$/.test(rowId)) throw error(400, '글 번호 형식을 확인하세요.');
      const matches = row => (bookId === null || row.book_id === bookId) && (rowId === null || row.id === Number(rowId));
      if (req.method === 'GET') {
        const selected = url.searchParams.get('select')?.split(',') ?? columns;
        if (selected.some(name => !columns.includes(name))) throw error(400, '조회할 필드 이름을 확인하세요.');
        const order = url.searchParams.get('order') ?? 'id.asc';
        if (!['id.asc', 'id.desc'].includes(order)) throw error(400, '정렬에는 id.asc 또는 id.desc를 사용하세요.');
        const rawLimit = url.searchParams.get('limit') ?? '50';
        if (!/^[0-9]+$/.test(rawLimit) || Number(rawLimit) < 1 || Number(rawLimit) > 100) throw error(400, '조회 개수는 1~100 사이여야 합니다.');
        const rows = state.messages.filter(matches).sort((a, b) => order === 'id.desc' ? b.id - a.id : a.id - b.id).slice(0, Number(rawLimit));
        return send(200, rows.map(row => Object.fromEntries(selected.map(name => [name, row[name]]))));
      }
      let body;
      if (req.method === 'POST' || req.method === 'PATCH') {
        if (req.headers['content-type']?.split(';')[0].trim().toLowerCase() !== 'application/json') throw error(415, 'Content-Type을 application/json으로 지정하세요.');
        let size = 0;
        const chunks = [];
        for await (const chunk of req) {
          size += chunk.length;
          if (size > 8192) throw error(413, '요청 본문이 너무 큽니다.');
          chunks.push(chunk);
        }
        try { body = JSON.parse(Buffer.concat(chunks).toString('utf8')); }
        catch { throw error(400, 'JSON 형식을 확인하세요.'); }
        if (!body || typeof body !== 'object' || Array.isArray(body)) throw error(400, '글 한 개를 JSON 객체로 보내세요.');
        const allowed = req.method === 'POST' ? ['book_id', 'name', 'message'] : ['name', 'message'];
        if (!Object.keys(body).length || Object.keys(body).some(key => !allowed.includes(key))) throw error(400, '변경 가능한 필드 이름을 확인하세요.');
        if ((req.method === 'POST' || 'name' in body) && !validText(body.name, 30)) throw error(400, '이름은 1~30글자로 입력하세요.');
        if ((req.method === 'POST' || 'message' in body) && !validText(body.message, 500)) throw error(400, '메시지는 1~500글자로 입력하세요.');
      }
      if (req.method === 'POST') {
        if (typeof body.book_id !== 'string' || !Object.hasOwn(state.books, body.book_id)) throw error(400, '등록된 방명록 번호를 사용하세요.');
        const row = { id: state.nextId++, book_id: body.book_id, name: body.name, message: body.message, created_at: new Date().toISOString() };
        state.messages.push(row);
        save();
        return send(201, req.headers.prefer === 'return=representation' ? [row] : undefined);
      }
      if (bookId === null || rowId === null) throw error(400, '수정·삭제에는 방명록 번호와 글 번호를 함께 지정하세요.');
      const suppliedHash = hash(String(req.headers['x-edit-key'] ?? ''));
      const affected = state.messages.filter(row => matches(row) && state.books[row.book_id] === suppliedHash);
      if (req.method === 'PATCH') {
        for (const row of affected) Object.assign(row, body);
        save();
        if (req.headers.prefer === 'return=representation') return send(200, affected);
        return send(204);
      }
      state.messages = state.messages.filter(row => !affected.includes(row));
      save();
      return send(204);
    } catch (failure) {
      // 요청 본문과 키는 로그에 남기지 않는다.
      if (!res.headersSent && !res.destroyed) send(failure.status ?? 500, { message: failure.status ? failure.message : '서버 파일 저장에 실패했습니다.' });
    }
  });
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const port = Number(process.env.PORT ?? 8787);
  const server = createGuestbookServer();
  server.on('error', failure => { console.error(failure.code === 'EADDRINUSE' ? `${port}번 포트를 사용 중입니다.` : failure.message); process.exitCode = 1; });
  server.listen(port, '127.0.0.1', () => console.log(`방명록 리허설 API: http://127.0.0.1:${port}/rest/v1/guestbook\n편집 키 파일: .local/local-edit-keys.json (강의자만 확인)\n종료: Ctrl+C`));
}

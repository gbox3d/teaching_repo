// server.mjs — 수업용 정적 웹 서버. Node.js 기본 모듈만 쓴다(npm install 필요 없음).
//
// 사용: node server.mjs [폴더] [포트]
//   node server.mjs                → 지금 폴더를 http://localhost:8000/ 으로 연다
//   node server.mjs . 5500         → 포트만 바꾼다
//   node server.mjs ../web-week05  → 다른 폴더를 연다
// 멈추기: 서버를 띄운 터미널에서 Ctrl+C
//
// 터미널에는 요청이 한 줄씩 찍힌다(예: "200 GET /styles.css").
// 브라우저가 HTML 을 받은 뒤 그 안의 CSS·JS·그림을 따로 요청하는 것을 눈으로 볼 수 있다.

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(process.argv[2] ?? '.');           // 이 폴더 안의 파일만 내보낸다
const port = Number(process.argv[3] ?? process.env.PORT ?? 8000);
const host = process.env.HOST ?? '127.0.0.1';                  // 내 PC 에서만 열린다(README "휴대폰으로 보기" 참고)

// 확장자 → Content-Type. 브라우저는 이 값을 보고 받은 파일을 어떻게 읽을지 정한다.
const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
  '.md': 'text/plain; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.mp3': 'audio/mpeg',
  '.mp4': 'video/mp4',
};

// 응답 하나를 보내고 터미널에 한 줄 남긴다. Cache-Control: no-store → 고친 파일이 새로고침에 바로 보인다.
function send(req, res, status, body, type = 'text/html; charset=utf-8', extra = {}) {
  res.writeHead(status, { 'Content-Type': type, 'Cache-Control': 'no-store', ...extra });
  res.end(req.method === 'HEAD' ? undefined : body);
  console.log(`${status} ${req.method} ${req.url}`);
}

const escapeHtml = (s) => s.replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);

// index.html 이 없는 폴더는 파일 목록을 보여 준다(비교 예제 폴더를 열 때 편하다).
function listing(urlPath, dir) {
  const items = fs.readdirSync(dir, { withFileTypes: true })
    .filter((d) => !d.name.startsWith('.'))
    .sort((a, b) => Number(b.isDirectory()) - Number(a.isDirectory()) || a.name.localeCompare(b.name))
    .map((d) => {
      const name = d.name + (d.isDirectory() ? '/' : '');
      return `<li><a href="${encodeURIComponent(d.name)}${d.isDirectory() ? '/' : ''}">${escapeHtml(name)}</a></li>`;
    });
  const up = urlPath === '/' ? '' : '<li><a href="../">../</a></li>';
  return `<!doctype html><meta charset="utf-8"><title>${escapeHtml(urlPath)}</title>
<h1>${escapeHtml(urlPath)}</h1><ul>${up}${items.join('')}</ul>`;
}

const server = http.createServer((req, res) => {
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    return send(req, res, 405, '405 Method Not Allowed', 'text/plain; charset=utf-8', { Allow: 'GET, HEAD' });
  }

  let urlPath;
  try {
    urlPath = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);   // "%20" → " ", 한글 이름도
  } catch {
    return send(req, res, 400, '400 Bad Request', 'text/plain; charset=utf-8');
  }

  // 주소를 폴더 안의 파일 경로로 바꾼다. "../" 로 폴더 밖을 요청하면 막는다.
  const filePath = path.join(root, urlPath);
  if (filePath !== root && !filePath.startsWith(root + path.sep)) {
    return send(req, res, 403, '403 Forbidden', 'text/plain; charset=utf-8');
  }

  fs.stat(filePath, (err, stat) => {
    if (err) {
      return send(req, res, 404, `<!doctype html><meta charset="utf-8"><h1>404 Not Found</h1><p>${escapeHtml(urlPath)} 파일이 없습니다. 파일 이름과 대소문자를 확인하세요.</p>`);
    }
    if (stat.isDirectory()) {
      if (!urlPath.endsWith('/')) {       // "/week05" → "/week05/" 로 보내야 그 안의 상대 경로가 맞는다
        return send(req, res, 301, '', 'text/plain; charset=utf-8', { Location: encodeURI(urlPath + '/') });
      }
      const index = path.join(filePath, 'index.html');
      if (!fs.existsSync(index)) return send(req, res, 200, listing(urlPath, filePath));
      return sendFile(req, res, index);
    }
    sendFile(req, res, filePath);
  });
});

function sendFile(req, res, filePath) {
  const type = TYPES[path.extname(filePath).toLowerCase()] ?? 'application/octet-stream';
  fs.readFile(filePath, (err, data) => {
    if (err) return send(req, res, 500, '500 Internal Server Error', 'text/plain; charset=utf-8');
    send(req, res, 200, data, type);
  });
}

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`${port} 번 포트를 이미 다른 프로그램이 쓰고 있습니다. 다른 번호로 띄우세요: node server.mjs . ${port + 1}`);
  } else {
    console.error(err.message);
  }
  process.exit(1);
});

server.listen(port, host, () => {
  console.log(`폴더: ${root}`);
  console.log(`주소: http://localhost:${port}/   (멈추기: Ctrl+C)`);
});

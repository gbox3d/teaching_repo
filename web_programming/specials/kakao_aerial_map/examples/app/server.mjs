import { createReadStream, existsSync, readFileSync, statSync } from 'node:fs';
import { createServer } from 'node:http';
import { dirname, extname, join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

import { relayKakaoStaticImage } from './static-map-relay.mjs';

// fileURLToPath(new URL('.', ...)) keeps a trailing separator on Windows.
// Normalize it once so the containment check below is platform-independent.
const root = resolve(fileURLToPath(new URL('.', import.meta.url)));
const port = Number.parseInt(process.env.PORT ?? '3000', 10);

if (!Number.isInteger(port) || port < 1 || port > 65535) {
  throw new Error(`Invalid PORT: ${process.env.PORT}`);
}

const allowedHosts = new Set([`localhost:${port}`, `127.0.0.1:${port}`]);
const allowedOrigins = new Set(
  [...allowedHosts].map((host) => `http://${host}`),
);

function isAllowedHost(request) {
  return allowedHosts.has(String(request.headers.host ?? '').toLowerCase());
}

function isSameOriginApiRequest(request) {
  if (request.headers['sec-fetch-site'] !== 'same-origin') return false;

  try {
    const refererOrigin = new URL(String(request.headers.referer ?? '')).origin;
    if (!allowedOrigins.has(refererOrigin)) return false;
    const origin = request.headers.origin;
    return !origin || allowedOrigins.has(String(origin).toLowerCase());
  } catch {
    return false;
  }
}

function findWorkspaceConfig(startDirectory) {
  let directory = resolve(startDirectory);

  while (true) {
    if (existsSync(join(directory, '.git'))) {
      return join(directory, 'config.json');
    }

    const parent = dirname(directory);
    if (parent === directory) {
      throw new Error('Git workspace root not found.');
    }
    directory = parent;
  }
}

const workspaceConfigPath = findWorkspaceConfig(root);

function readRuntimeConfig() {
  let javascriptKey = process.env.KAKAO_JAVASCRIPT_KEY?.trim() ?? '';

  if (!javascriptKey && existsSync(workspaceConfigPath)) {
    const config = JSON.parse(readFileSync(workspaceConfigPath, 'utf8'));
    javascriptKey = config.kakaoMaps?.javascriptKey?.trim() ?? '';
  }

  const configured = Boolean(
    javascriptKey && !javascriptKey.includes('REPLACE_WITH_'),
  );

  return {
    kakaoJavaScriptKey: configured ? javascriptKey : null,
    setupRequired: !configured,
  };
}

const contentTypes = new Map([
  ['.html', 'text/html; charset=utf-8'],
  ['.css', 'text/css; charset=utf-8'],
  ['.js', 'text/javascript; charset=utf-8'],
  ['.mjs', 'text/javascript; charset=utf-8'],
  ['.json', 'application/json; charset=utf-8'],
  ['.svg', 'image/svg+xml'],
]);

function sendJson(response, statusCode, value) {
  response.writeHead(statusCode, {
    'cache-control': 'no-store',
    'content-type': 'application/json; charset=utf-8',
  });
  response.end(`${JSON.stringify(value)}\n`);
}

let staticMapRelayActive = false;
let lastStaticMapRelayAt = 0;

async function sendStaticMapImage(response, source) {
  const now = Date.now();
  if (staticMapRelayActive || now - lastStaticMapRelayAt < 500) {
    sendJson(response, 429, {
      error: '정적 지도 요청이 너무 빠릅니다. 잠시 후 다시 시도해 주세요.',
    });
    return;
  }

  staticMapRelayActive = true;
  lastStaticMapRelayAt = now;
  try {
    const image = await relayKakaoStaticImage(source);
    response.writeHead(200, {
      'cache-control': 'no-store',
      'content-length': image.body.length,
      'content-type': image.contentType,
      'cross-origin-resource-policy': 'same-origin',
      'x-content-type-options': 'nosniff',
    });
    response.end(image.body);
  } catch (error) {
    const clientError = error instanceof TypeError || error instanceof RangeError;
    sendJson(response, clientError ? 400 : 502, {
      error: error instanceof Error ? error.message : '정적 지도 이미지를 가져오지 못했습니다.',
    });
  } finally {
    staticMapRelayActive = false;
  }
}

const server = createServer((request, response) => {
  response.setHeader('x-content-type-options', 'nosniff');
  response.setHeader('referrer-policy', 'strict-origin-when-cross-origin');
  response.setHeader('cross-origin-resource-policy', 'same-origin');
  response.setHeader(
    'permissions-policy',
    'geolocation=(self)',
  );

  if (!isAllowedHost(request)) {
    sendJson(response, 421, { error: 'Misdirected request.' });
    return;
  }

  let requestUrl;
  let pathname;
  try {
    requestUrl = new URL(request.url ?? '/', 'http://localhost');
    pathname = decodeURIComponent(requestUrl.pathname);
  } catch {
    sendJson(response, 400, { error: 'Invalid request path.' });
    return;
  }
  if (pathname === '/runtime-config.json') {
    try {
      sendJson(response, 200, readRuntimeConfig());
    } catch {
      sendJson(response, 500, {
        error: 'The workspace config.json is not valid JSON.',
      });
    }
    return;
  }

  if (pathname === '/api/kakao-static-image') {
    if (request.method !== 'GET') {
      sendJson(response, 405, { error: 'Method not allowed.' });
      return;
    }
    if (!isSameOriginApiRequest(request)) {
      sendJson(response, 403, { error: 'Same-origin browser request required.' });
      return;
    }
    const sources = requestUrl.searchParams.getAll('source');
    if (sources.length !== 1) {
      sendJson(response, 400, { error: '정적 지도 이미지 주소가 필요합니다.' });
      return;
    }
    void sendStaticMapImage(response, sources[0]);
    return;
  }

  const relativePath = pathname === '/' ? 'index.html' : pathname.slice(1);
  const filename = resolve(root, relativePath);

  if (filename !== root && !filename.startsWith(`${root}${sep}`)) {
    sendJson(response, 403, { error: 'Forbidden path.' });
    return;
  }

  let file;
  try {
    file = statSync(filename);
  } catch {
    sendJson(response, 404, { error: `Not found: ${pathname}` });
    return;
  }

  if (!file.isFile()) {
    sendJson(response, 404, { error: `Not found: ${pathname}` });
    return;
  }

  response.writeHead(200, {
    'cache-control': pathname === '/index.html' ? 'no-cache' : 'public, max-age=60',
    'content-type': contentTypes.get(extname(filename)) ?? 'application/octet-stream',
  });
  createReadStream(filename).pipe(response);
});

server.listen(port, '127.0.0.1', () => {
  console.log(`Kakao aerial canvas lab: http://localhost:${port}/`);
  console.log(`Workspace config: ${workspaceConfigPath}`);
});

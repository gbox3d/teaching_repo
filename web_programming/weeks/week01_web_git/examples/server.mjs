import { createReadStream } from 'node:fs';
import { createServer } from 'node:http';
import { fileURLToPath } from 'node:url';

const port = Number.parseInt(process.env.PORT ?? '8000', 10);
const files = new Map([
  ['/', ['index.html', 'text/html; charset=utf-8']],
  ['/index.html', ['index.html', 'text/html; charset=utf-8']],
  ['/styles.css', ['styles.css', 'text/css; charset=utf-8']],
  ['/app.js', ['app.js', 'text/javascript; charset=utf-8']],
]);

const root = fileURLToPath(new URL('.', import.meta.url));

const server = createServer((request, response) => {
  const pathname = new URL(request.url ?? '/', 'http://localhost').pathname;
  const resource = files.get(pathname);

  if (!resource) {
    response.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
    response.end(`404 Not Found: ${pathname}\n`);
    return;
  }

  const [filename, contentType] = resource;
  response.writeHead(200, { 'content-type': contentType });
  createReadStream(`${root}${filename}`).pipe(response);
});

server.listen(port, '127.0.0.1', () => {
  console.log(`Open http://localhost:${port}/`);
});

import { createReadStream } from 'node:fs';
import { createServer } from 'node:http';
import { fileURLToPath } from 'node:url';

const port = Number.parseInt(process.env.PORT ?? '8000', 10);
const files = new Map([
  ['/broken-site/', ['broken-site/index.html', 'text/html; charset=utf-8']],
  ['/broken-site/index.html', ['broken-site/index.html', 'text/html; charset=utf-8']],
  ['/broken-site/assets/styles.css', ['broken-site/assets/styles.css', 'text/css; charset=utf-8']],
  ['/broken-site/assets/app.js', ['broken-site/assets/app.js', 'text/javascript; charset=utf-8']],
  ['/broken-site/assets/campus-mark.svg', ['broken-site/assets/campus-mark.svg', 'image/svg+xml']],
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
  console.log(`Open http://localhost:${port}/broken-site/`);
});

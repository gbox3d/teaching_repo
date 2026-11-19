import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { mkdtemp, mkdir, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

test('정적 파일과 설정 견본은 제공하고 로컬 비공개 파일은 차단한다', { timeout: 10000 }, async t => {
  const prefix = path.join(tmpdir(), 'web-static-test-');
  const directory = await mkdtemp(prefix);
  await mkdir(path.join(directory, 'localfiles'));
  await mkdir(path.join(directory, 'images'));
  await writeFile(path.join(directory, 'index.html'), '<h1>공개 예제</h1>');
  await writeFile(path.join(directory, '.env.example'), 'API_PUBLIC_KEY=classroom-local');
  await writeFile(path.join(directory, '.env'), 'API_PUBLIC_KEY=private-fixture');
  await writeFile(path.join(directory, 'localfiles', 'fixture.txt'), 'private-fixture');
  const child = spawn(process.execPath, [fileURLToPath(new URL('./server.mjs', import.meta.url)), directory, '0'], {
    env: { ...process.env, HOST: '127.0.0.1' }, windowsHide: true, stdio: ['ignore', 'pipe', 'pipe']
  });
  t.after(async () => {
    if (child.exitCode === null) {
      const closed = once(child, 'close');
      child.kill();
      await closed;
    }
    assert.ok(path.resolve(directory).startsWith(path.resolve(prefix)));
    await rm(directory, { recursive: true, force: true });
  });
  const base = await new Promise((resolve, reject) => {
    let output = '';
    child.once('error', reject);
    child.once('exit', code => reject(new Error(`server exited: ${code}`)));
    child.stdout.on('data', chunk => {
      output += chunk;
      const match = output.match(/http:\/\/localhost:(\d+)\//);
      if (match) resolve(`http://127.0.0.1:${match[1]}`);
    });
  });
  assert.equal((await fetch(base + '/')).status, 200);
  assert.equal((await fetch(base + '/.env.example')).status, 200);
  for (const suffix of ['/.env', '/.ENV', '/.env.local', '/%2eenv', '/localfiles/fixture.txt', '/.local/data.json', '/.git/config']) {
    const response = await fetch(base + suffix);
    assert.equal(response.status, 403, suffix);
    assert.ok(!(await response.text()).includes('private-fixture'));
  }
  const head = await fetch(base + '/index.html', { method: 'HEAD' });
  assert.equal(head.status, 200);
  assert.equal(await head.text(), '');
  assert.equal((await fetch(base + '/missing.html')).status, 404);
  assert.equal((await fetch(base + '/index.html', { method: 'POST' })).status, 405);
});

// node provision.mjs student01 student02 ... → 로컬 비공개 키/등록 SQL 생성
import { randomBytes, createHash } from 'node:crypto';
import { mkdirSync, writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ids = process.argv.slice(2);
if (!ids.length || ids.some(id => !/^[a-z0-9_-]{1,40}$/.test(id)) || new Set(ids).size !== ids.length) {
  console.error('사용법: node provision.mjs student01 student02 (영문 소문자·숫자·밑줄·붙임표)');
  process.exit(1);
}
const directory = fileURLToPath(new URL('./.local/', import.meta.url));
mkdirSync(directory, { recursive: true });
const keyPath = path.join(directory, 'cloud-edit-keys.json');
const sqlPath = path.join(directory, 'cloud-books.sql');
if (existsSync(keyPath) || existsSync(sqlPath)) {
  console.error('기존 배부 파일이 있습니다. 보관 위치를 바꾼 뒤 실행하세요. 자동으로 키를 교체하지 않습니다.');
  process.exit(1);
}
const keys = Object.fromEntries(ids.map(id => [id, randomBytes(32).toString('hex')]));
const sql = ids.map(id => {
  const hash = createHash('sha256').update(keys[id]).digest('hex');
  return `insert into private.classroom_books (book_id, edit_key_hash) values ('${id}', '${hash}');`;
}).join('\n');
writeFileSync(keyPath, JSON.stringify(keys, null, 2) + '\n', { mode: 0o600 });
writeFileSync(sqlPath, 'begin;\n' + sql + '\ncommit;\n', { mode: 0o600 });
console.log('등록 SQL: .local/cloud-books.sql\n개별 배부용 편집 키: .local/cloud-edit-keys.json\n키 파일은 공개 저장소와 화면 공유에서 제외하세요.');

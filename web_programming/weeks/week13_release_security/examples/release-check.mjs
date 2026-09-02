import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { resolve, join, relative } from "node:path";

const root = resolve(process.argv[2] ?? ".");
const ignored = new Set([".git", "node_modules", "dist"]);
const secretPatterns = [
  "sb_" + "secret_",
  "service" + "_" + "role",
  "SUPABASE_" + "SECRET"
];
const suspiciousNames = new Set([".env", ".env.local", "config.secret.js"]);
const findings = [];

function walk(directory) {
  for (const name of readdirSync(directory)) {
    if (ignored.has(name)) continue;
    const fullPath = join(directory, name);
    const item = statSync(fullPath);
    if (item.isDirectory()) {
      walk(fullPath);
      continue;
    }

    const shortPath = relative(root, fullPath);
    if (suspiciousNames.has(name)) {
      findings.push(["secret-file", shortPath]);
    }

    if (item.size > 1_000_000) continue;
    const text = readFileSync(fullPath, "utf8");
    for (const pattern of secretPatterns) {
      if (text.includes(pattern)) findings.push(["secret-pattern", shortPath]);
    }
    if (/\binnerHTML\b/.test(text)) findings.push(["review-innerHTML", shortPath]);
  }
}

for (const required of ["README.md", "index.html"]) {
  if (!existsSync(join(root, required))) findings.push(["missing", required]);
}

walk(root);

if (findings.length === 0) {
  console.log("기본 자동 점검에서 발견된 항목이 없습니다. 수동 RLS·접근성 검사를 계속하세요.");
} else {
  console.table(findings.map(([type, path]) => ({ type, path })));
  process.exitCode = 1;
}

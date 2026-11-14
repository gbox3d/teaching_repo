// 화면 문구 검사: korean-copy-style 스킬의 check_ui_copy.mjs에서 순수 검사 부분을 재사용한다.
// 훅·git·사용자 홈 경로는 필요하지 않으므로 포함하지 않는다.
import { readFileSync, readdirSync, statSync } from "node:fs";
import { basename, extname, join } from "node:path";

// ── 규칙 ───────────────────────────────────────────────────────────────────────
// 구어·비표준 어휘 → 표준 UI 용어. 왼쪽은 정규식(부분 일치), 오른쪽은 제안.
export const GLOSSARY = [
  [/쉬는 중/, "대기 중"],
  [/다 받았(다|음|습니다)|다 받음/, "다운로드 완료"],
  [/받는 중/, "다운로드 중"],
  [/^받음$/, "다운로드 완료"],
  [/차례 기다림|차례를 기다/, "순서 대기 중"],
  [/(?<!되)(돌리|돌린|돌릴|돌려|돌렸)/, "실행 (예: 돌린 작업 → 실행한 작업)"],
  [/띄우|띄운|띄울|띄워|띄웠/, "시작·실행"],
  [/고른 |고르기|고르는|골라/, "선택 (예: 고른 영상 → 선택한 영상)"],
  [/^끝$|^끝남$|끝맺음/, "완료·종료"],
  [/그만두|그만둔|그만둘|그만둡/, "중단"],
  [/^멈춤/, "중지됨"],
  [/안 돌렸|안 돌린/, "미실행"],
  [/들어와야|들어오세요|들어가기$/, "로그인"],
];
// 명사인데 '다'로 끝나는 것(해라체 오탐 방지)
const NOUN_ENDS_DA = /(람다|바다|판다|캐나다|아가다|가나다|사다리|오다|마다)$/;
// 문장 안에서 쪼개는 경계: 줄바꿈, 마침표+공백, 대시·가운뎃점·세로줄, 괄호 시작
const SPLIT_RE = /\n|(?<=[.!?。])\s+|\s[—–·|]\s|\s—|—\s|\s\(|\)\s/;

// 합쇼체 종결(…습니다 / ㅂ받침+니다: 입니다·합니다·됩니다). '아니다'·'다니다'는 해라체다.
const jong = (ch) => (ch.charCodeAt(0) - 0xac00) % 28;
const isPolite = (tail) => /습니다$/.test(tail) || (/[가-힣]니다$/.test(tail) && jong(tail.at(-3)) === 17);

export function judge(segment) {
  const out = [];
  const t = segment.replace(/\s+/g, " ").trim();
  if (!/[가-힣]/.test(t)) return out;
  // R1 해라체 종결: …다 / …다. / …다(괄호 설명) — 합쇼체와 '다'로 끝나는 명사는 제외
  const tail = t.replace(/\([^()]*\)?\s*$/, "").replace(/[\s.。!…?)\]'"」』»:]+$/g, "");
  if (/[가-힣]다$/.test(tail) && !isPolite(tail) && !NOUN_ENDS_DA.test(tail) && (tail.match(/[가-힣]/g) || []).length >= 2) {
    out.push({ rule: "해라체", text: t, hint: "명사형(…중/…완료) 또는 합쇼체(…입니다/…하세요)로" });
  }
  if (/(잖아|거든|더라|구나|냐)[.!?…]*$/.test(tail)) out.push({ rule: "구어 종결", text: t, hint: "합쇼체로" });
  // R2 어휘
  for (const [re, good] of GLOSSARY) {
    if (re.test(t)) out.push({ rule: "어휘", text: t, hint: `→ ${good}` });
  }
  return out;
}

// ── 추출: 문자열 조각 → [{line, text, ctx}] ───────────────────────────────────
const SINK_RE = /console\.(log|error|warn|info|debug)|logger\.|logging\.|\bprint\(|process\.std(out|err)|\[[a-z0-9-]+\]\s*`?\$?/i;
const PY_SINK_RE = /^\s*(raise\b|print\(|log(ger|ging)?\.|assert\b)|help=|description=|sys\.exit\(|SystemExit\(/;
const OK_MARK = /ui-copy:\s*ok/; // 그 줄에 이 주석이 있으면 고의로 둔 문구다

function pushSeg(acc, line, text, ctx) {
  for (const piece of text.split(SPLIT_RE)) {
    const p = piece.trim();
    if (p) acc.push({ line, text: p, ctx });
  }
}

// JS/TS: 주석을 걷고 문자열·템플릿 리터럴의 글만. 템플릿의 ${…} 안은 코드로 다시 본다.
export function extractJs(src, lineBase = 1, acc = []) {
  const lines = src.split("\n");
  let i = 0, line = lineBase;
  const ctxOf = (ln) => lines[ln - lineBase] ?? "";
  const n = src.length;
  while (i < n) {
    const c = src[i], d = src[i + 1];
    if (c === "\n") { line++; i++; continue; }
    if (c === "/" && d === "/") { while (i < n && src[i] !== "\n") i++; continue; }
    if (c === "/" && d === "*") { i += 2; while (i < n && !(src[i] === "*" && src[i + 1] === "/")) { if (src[i] === "\n") line++; i++; } i += 2; continue; }
    if (c === "'" || c === '"') {
      const q = c; const start = line; let j = i + 1, s = "";
      while (j < n && src[j] !== q) { if (src[j] === "\\") { s += src[j + 1] ?? ""; j += 2; continue; } if (src[j] === "\n") break; s += src[j]; j++; }
      pushSeg(acc, start, s, ctxOf(start)); i = j + 1; continue;
    }
    if (c === "`") {
      const start = line; let j = i + 1, s = "";
      while (j < n && src[j] !== "`") {
        if (src[j] === "\\") { s += src[j + 1] ?? ""; j += 2; continue; }
        if (src[j] === "$" && src[j + 1] === "{") {
          pushSeg(acc, line, s, ctxOf(start)); s = "";
          let depth = 1, k = j + 2; const exprStart = k, exprLine = line;
          while (k < n && depth > 0) { if (src[k] === "{") depth++; else if (src[k] === "}") depth--; else if (src[k] === "`") { k++; while (k < n && src[k] !== "`") { if (src[k] === "\\") k++; k++; } } if (depth > 0) k++; }
          extractJs(src.slice(exprStart, k), exprLine, acc);
          for (const ch of src.slice(j, k)) if (ch === "\n") line++;
          j = k + 1; continue;
        }
        if (src[j] === "\n") { pushSeg(acc, line, s, ctxOf(start)); s = ""; line++; }
        else s += src[j];
        j++;
      }
      pushSeg(acc, line, s, ctxOf(start)); i = j + 1; continue;
    }
    if (c === "/") { // 정규식 리터럴: 앞 토큰이 연산자·괄호면
      const prev = src.slice(0, i).trimEnd().slice(-1);
      if (prev === "" || "(,=:[!&|?{};+-*%<>~^".includes(prev)) {
        let j = i + 1, inClass = false;
        while (j < n && src[j] !== "\n") { if (src[j] === "\\") { j += 2; continue; } if (src[j] === "[") inClass = true; else if (src[j] === "]") inClass = false; else if (src[j] === "/" && !inClass) break; j++; }
        i = j + 1; continue;
      }
    }
    i++;
  }
  return acc;
}

// HTML: 주석 제거 → <script> 는 JS 로, <style> 은 버리고, 글 노드와 몇 가지 속성만.
export function extractHtml(src, acc = []) {
  const lineAt = (idx) => src.slice(0, idx).split("\n").length;
  let s = src.replace(/<!--[\s\S]*?-->/g, (m) => m.replace(/[^\n]/g, " "));
  s = s.replace(/<script\b[^>]*>([\s\S]*?)<\/script>/gi, (m, body, off) => { extractJs(body, lineAt(off + m.indexOf(body)), acc); return m.replace(/[^\n]/g, " "); });
  s = s.replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, (m) => m.replace(/[^\n]/g, " "));
  for (const m of s.matchAll(/\b(title|placeholder|alt|aria-label|value|label|data-label|content)\s*=\s*"([^"]*)"/g)) pushSeg(acc, lineAt(m.index), m[2], m[0]);
  for (const m of s.matchAll(/>([^<>]+)</g)) {
    const text = m[1].replace(/&nbsp;/g, " ").replace(/&[a-z]+;/g, "");
    if (/[가-힣]/.test(text)) pushSeg(acc, lineAt(m.index), text, "");
  }
  return acc;
}

// Python: 문자열 리터럴(접두사 허용), f-string 의 {…} 는 코드로, 주석 제외. HTML 을 담은 문자열은 HTML 로 본다.
export function extractPy(src, acc = [], { all = true } = {}) {
  const lines = src.split("\n");
  let i = 0, line = 1; const n = src.length;
  const ctxOf = (ln) => lines[ln - 1] ?? "";
  while (i < n) {
    const c = src[i];
    if (c === "\n") { line++; i++; continue; }
    if (c === "#") { while (i < n && src[i] !== "\n") i++; continue; }
    if (c === "'" || c === '"') {
      const triple = src.startsWith(c.repeat(3), i);
      const q = triple ? c.repeat(3) : c;
      const start = line; let j = i + q.length, s = "";
      while (j < n && !src.startsWith(q, j)) { if (src[j] === "\\") { s += src[j + 1] ?? ""; j += 2; continue; } if (src[j] === "\n") { line++; if (!triple) break; } s += src[j]; j++; }
      const ctx = ctxOf(start);
      if (!triple && !PY_SINK_RE.test(ctx)) { // 삼중따옴표는 docstring(개발자용) — 문구가 아니다
        const prefix = (src.slice(Math.max(0, i - 2), i).match(/[fFrRbBuU]+$/) || [""])[0];
        let text = s;
        if (/f/i.test(prefix)) text = s.replace(/\{[^{}]*\}/g, " ");
        if (/<[a-z][^>]*>/i.test(text)) extractHtml(text, acc); // acc 에 바로 쌓인다
        else if (all) { for (const [k, ln] of text.split("\n").entries()) pushSeg(acc, start + k, ln, ctx); }
      }
      i = j + q.length; continue;
    }
    i++;
  }
  return acc;
}

// ── 파일 ───────────────────────────────────────────────────────────────────────
const KIND = { ".html": "html", ".htm": "html", ".vue": "html", ".svelte": "html", ".js": "js", ".mjs": "js", ".cjs": "js", ".ts": "js", ".tsx": "js", ".jsx": "js", ".py": "py" };
const SKIP_DIR = /(^|\/)(node_modules|\.venv|venv|vendor|third_party|dist|build|\.git|__pycache__|test|tests|fixtures|_attic[^/]*)(\/|$)/;
const SKIP_FILE = /(\.min\.|\.test\.|\.spec\.|^test_|_test\.py$|\.d\.ts$|^check_ui_copy\.mjs$)/;
// Python 은 페이지를 만드는 파일(이름에 html·template·management·demo·report·page·site·web·ui)만 문자열 전부를 보고,
// 그 밖(개발자용 CLI·점검 도구)은 HTML 을 담은 문자열만 본다 — CLI 메시지는 저장소 관례(해라체)대로 둔다.
const PY_PAGE_RE = /(html|template|management|demo|report|page|site|web|ui)/i;
export const isUiFile = (p) => Boolean(KIND[extname(p).toLowerCase()]) && !SKIP_DIR.test(p) && !SKIP_FILE.test(basename(p));

export function extract(path, src) {
  const kind = KIND[extname(path).toLowerCase()];
  if (kind === "html") return extractHtml(src);
  if (kind === "py") return extractPy(src, [], { all: PY_PAGE_RE.test(basename(path)) });
  if (kind === "js") return extractJs(src);
  return [];
}

const lineOf = (src, n) => src.split("\n")[n - 1] ?? "";
export function checkText(path, src, onlyLines = null) {
  const findings = [];
  const seen = new Set();
  for (const seg of extract(path, src)) {
    if (onlyLines && !onlyLines.has(seg.line)) continue;
    if (SINK_RE.test(seg.ctx) || OK_MARK.test(seg.ctx) || OK_MARK.test(lineOf(src, seg.line))) continue;
    for (const f of judge(seg.text)) {
      const key = `${seg.line}|${f.rule}|${f.text}`;
      if (seen.has(key)) continue;
      seen.add(key);
      findings.push({ file: path, line: seg.line, ...f });
    }
  }
  return findings;
}

export function checkFile(path, onlyLines = null) {
  let src;
  try { src = readFileSync(path, "utf8"); } catch { return []; }
  return checkText(path, src, onlyLines);
}

export function walk(p, out = []) {
  let st;
  try { st = statSync(p); } catch { return out; }
  if (st.isDirectory()) { if (!SKIP_DIR.test(p + "/")) for (const e of readdirSync(p)) walk(join(p, e), out); }
  else if (isUiFile(p)) out.push(p);
  return out;
}

import { Marp } from "@marp-team/marp-core";
import { copyFile, mkdir, readFile, realpath, rm, stat, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const EXPECTED_NODE_MAJOR = 24;
const EXPECTED_DECKS = 46;
const EXPECTED_SLIDES = 927;
const REPOSITORY_BLOB_URL = "https://github.com/gbox3d/teaching_repo/blob/main";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const site = path.join(root, "site");
const dist = path.join(root, "dist");
const legacyDecksRoot = path.join(dist, "decks");
const catalogFile = path.join(site, "catalog.json");
const themeFile = path.join(site, "assets", "marp-theme.css");
const courseTemplateFile = path.join(site, "course.html");
const courseAssets = [
  "assets/library.css",
  "assets/course.css",
  "assets/course.js",
  "assets/deck.css",
  "assets/deck.js",
  "favicon.svg",
];
const publishedFiles = [
  [path.join(site, "index.html"), path.join(dist, "index.html")],
  [path.join(site, "assets", "library.css"), path.join(dist, "assets", "library.css")],
  [path.join(site, "assets", "library.js"), path.join(dist, "assets", "library.js")],
  [path.join(site, "assets", "deck.css"), path.join(dist, "assets", "deck.css")],
  [path.join(site, "assets", "deck.js"), path.join(dist, "assets", "deck.js")],
  [path.join(site, "favicon.svg"), path.join(dist, "favicon.svg")],
  [path.join(root, "LICENSE"), path.join(dist, "LICENSE")],
];

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function assertInside(parent, candidate, label) {
  const relative = path.relative(parent, candidate);
  assert(
    relative !== "" &&
      relative !== ".." &&
      !relative.startsWith(`..${path.sep}`) &&
      !path.isAbsolute(relative),
    `${label} 경로가 허용 범위를 벗어납니다: ${candidate}`,
  );
}

async function isFile(filename) {
  try {
    return (await stat(filename)).isFile();
  } catch (error) {
    if (error?.code === "ENOENT") return false;
    throw error;
  }
}

function assertIdentifier(value, label) {
  assert(
    typeof value === "string" && /^[a-z0-9][a-z0-9_-]*$/.test(value),
    `${label} 값이 안전한 식별자가 아닙니다: ${JSON.stringify(value)}`,
  );
}

function sourcePath(course, chapter) {
  if (course.id === "android" && chapter.type === "week") {
    return path.posix.join("android_programming", "weeks", chapter.id, "slides.md");
  }
  if (course.id === "web" && chapter.type === "week") {
    return path.posix.join("web_programming", "weeks", chapter.id, "slides.md");
  }
  if (course.id === "web" && chapter.type === "special") {
    return path.posix.join("web_programming", "specials", chapter.id, "slides.md");
  }
  if (course.id === "open-source-ai" && chapter.type === "week") {
    return path.posix.join("open_source_ai", "weeks", chapter.id, "slides.md");
  }
  throw new Error(`원고 위치를 결정할 수 없습니다: ${course.id}/${chapter.id}`);
}

function repositoryUrl(relative) {
  const encoded = relative.split("/").map(encodeURIComponent).join("/");
  return `${REPOSITORY_BLOB_URL}/${encoded}`;
}

function splitTarget(target) {
  const positions = [target.indexOf("?"), target.indexOf("#")].filter((index) => index >= 0);
  const splitAt = positions.length ? Math.min(...positions) : target.length;
  return { pathname: target.slice(0, splitAt), suffix: target.slice(splitAt) };
}

function mapOutsideInlineCode(line, mapText, mapCode = (value) => value) {
  let output = "";
  let cursor = 0;
  while (cursor < line.length) {
    const opening = line.indexOf("`", cursor);
    if (opening < 0) return output + mapText(line.slice(cursor));
    let size = 1;
    while (line[opening + size] === "`") size += 1;
    const delimiter = "`".repeat(size);
    const closing = line.indexOf(delimiter, opening + size);
    if (closing < 0) return output + mapText(line.slice(cursor));
    output += mapText(line.slice(cursor, opening));
    output += mapCode(line.slice(opening, closing + size));
    cursor = closing + size;
  }
  return output;
}

function markdownCode(content) {
  const longest = Math.max(0, ...(content.match(/`+/g) ?? []).map((run) => run.length));
  const delimiter = "`".repeat(longest + 1);
  return `${delimiter}${content}${delimiter}`;
}

function normalizeLegacyHtml(markdown, relativeSource) {
  const output = [];
  let fence = null;
  for (const [index, line] of markdown.split("\n").entries()) {
    const marker = line.match(/^( {0,3})(`{3,}|~{3,})(.*)$/);
    if (fence) {
      output.push(line);
      if (
        marker &&
        marker[2][0] === fence.character &&
        marker[2].length >= fence.length &&
        marker[3].trim() === ""
      ) {
        fence = null;
      }
      continue;
    }
    if (marker) {
      fence = { character: marker[2][0], length: marker[2].length };
      output.push(line);
      continue;
    }

    const rewritten = mapOutsideInlineCode(line, (text) =>
      text
        .replace(/<code>([^<>\r\n]*)<\/code>/gi, (_whole, content) => markdownCode(content))
        .replace(/<br\s*\/?>\s*$/i, "\\"),
    );
    const exposed = mapOutsideInlineCode(
      rewritten,
      (text) => text,
      (code) => " ".repeat(code.length),
    );
    const rawTag = exposed.match(/<\/?[a-z][a-z\d-]*(?:\s[^<>]*?)?\s*\/?>/i);
    assert(!rawTag, `${relativeSource}:${index + 1}: 허용되지 않은 raw HTML ${rawTag?.[0]}`);
    output.push(rewritten);
  }
  return output.join("\n");
}

function resolveRepositoryTarget(target, relativeSource) {
  const { pathname: targetPath, suffix } = splitTarget(target);
  if (!targetPath) return null;
  assert(
    !targetPath.startsWith("/") && !targetPath.includes("\\"),
    `${relativeSource}: 안전하지 않은 상대 URL ${target}`,
  );
  let decoded;
  try {
    decoded = decodeURIComponent(targetPath);
  } catch {
    throw new Error(`${relativeSource}: 잘못 인코딩된 URL ${target}`);
  }
  assert(
    !decoded.includes("\\") && !/[\u0000-\u001f\u007f]/.test(decoded),
    `${relativeSource}: 안전하지 않은 상대 URL ${target}`,
  );
  const relative = path.posix.normalize(
    path.posix.join(path.posix.dirname(relativeSource), decoded),
  );
  assert(
    relative !== ".." && !relative.startsWith("../") && !path.posix.isAbsolute(relative),
    `${relativeSource}: 저장소 밖 URL ${target}`,
  );
  return { relative, suffix };
}

function encodedRelativePath(relative) {
  return relative.split("/").map(encodeURIComponent).join("/");
}

function allowedExternalTarget(target, kind, relativeSource) {
  if (target.startsWith("//")) {
    throw new Error(`${relativeSource}: protocol-relative URL은 허용되지 않습니다: ${target}`);
  }
  const scheme = target.match(/^([a-z][a-z\d+.-]*):/i)?.[1].toLowerCase();
  if (!scheme) return false;
  if (kind === "link" && ["http", "https", "mailto", "tel"].includes(scheme)) return true;
  if (kind === "asset" && ["http", "https"].includes(scheme)) return true;
  if (kind === "asset" && scheme === "data" && /^data:image\//i.test(target)) return true;
  throw new Error(`${relativeSource}: 허용되지 않은 ${kind} URL scheme: ${target}`);
}

function rewriteTokenTarget(token, attribute, context, kind) {
  const target = token.attrGet(attribute);
  if (!target || target.startsWith("#") || target.startsWith("?")) return;
  if (allowedExternalTarget(target, kind, context.relativeSource)) return;
  const resolved = resolveRepositoryTarget(target, context.relativeSource);
  if (!resolved) return;
  if (kind === "link" && /\.md$/i.test(resolved.relative)) {
    token.attrSet(attribute, `${repositoryUrl(resolved.relative)}${resolved.suffix}`);
    context.rewrittenLinks += 1;
    return;
  }
  const outputRelative = path.posix.join("assets", resolved.relative);
  const publicTarget = `${encodedRelativePath(outputRelative)}${resolved.suffix}`;
  context.assets.set(resolved.relative, outputRelative);
  token.attrSet(attribute, publicTarget);
  if (token.meta?.marpitImage) token.meta.marpitImage.url = publicTarget;
}

function installUrlRewriter(marp) {
  marp.use((markdown) => {
    markdown.core.ruler.after("inline", "teaching_local_urls", (state) => {
      const context = state.env?.teaching;
      if (!context) return;
      const visit = (tokens) => {
        for (const token of tokens) {
          if (token.type === "link_open") rewriteTokenTarget(token, "href", context, "link");
          if (token.type === "image") rewriteTokenTarget(token, "src", context, "asset");
          if (token.children) visit(token.children);
        }
      };
      visit(state.tokens);
    });
  });
}

function prepareMarkdown(source, relativeSource) {
  const normalized = source.replace(/\r\n?/g, "\n");
  const themes = normalized.match(/^theme:\s*default\s*$/gm) ?? [];
  assert(themes.length === 1, `${relativeSource}: theme: default 지시문은 하나여야 합니다.`);
  const markdown = normalizeLegacyHtml(normalized, relativeSource).replace(
    /^theme:\s*default\s*$/m,
    "theme: teaching",
  );
  return markdown;
}

function slideCount(html) {
  return (html.match(/<svg\b(?=[^>]*\bdata-marpit-svg\b)[^>]*>/gi) ?? []).length;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function renderDocument({ course, chapter, sourceUrl, html, css }) {
  const title = `${chapter.label} · ${chapter.title}`;
  const description = `${course.title} ${chapter.label} 강의 슬라이드`;
  return `<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="${escapeHtml(description)}">
    <meta name="theme-color" content="#07111f">
    <title>${escapeHtml(title)} · ${escapeHtml(course.title)}</title>
    <link rel="icon" href="../../favicon.svg" type="image/svg+xml">
    <style>${css}</style>
    <link rel="stylesheet" href="../../assets/deck.css">
  </head>
  <body>
    <a class="library-return" data-library-return href="../../#chapters" aria-label="${escapeHtml(course.title)} 목차로 돌아가기">← 목차</a>
    <header class="deck-header">
      <p><span>${escapeHtml(course.title)}</span><strong>${escapeHtml(title)}</strong></p>
      <a href="${escapeHtml(sourceUrl)}" target="_blank" rel="noopener noreferrer">원고 보기 ↗</a>
    </header>
    <main class="deck-stage" aria-label="${escapeHtml(title)} 슬라이드">${html}</main>
    <nav class="deck-controls" aria-label="슬라이드 이동">
      <button type="button" data-action="previous" aria-label="이전 슬라이드">←</button>
      <div class="deck-progress" aria-hidden="true"><span data-progress></span></div>
      <output data-counter aria-live="polite">1 / 1</output>
      <button type="button" data-action="next" aria-label="다음 슬라이드">→</button>
      <button type="button" data-action="fullscreen" aria-label="전체 화면 전환">⛶</button>
    </nav>
    <p class="deck-help">← → 이동 · Home/End 처음/끝 · F 전체 화면</p>
    <script src="../../assets/deck.js"></script>
  </body>
</html>
`;
}

async function readCatalog() {
  const catalog = JSON.parse(await readFile(catalogFile, "utf8"));
  assert(catalog?.site && Array.isArray(catalog.courses), "site/catalog.json 형식이 올바르지 않습니다.");
  const courseIds = new Set();
  const courseSlugs = new Set(["assets", "decks"]);
  const entries = [];

  for (const course of catalog.courses) {
    assertIdentifier(course.id, "course.id");
    assert(!courseIds.has(course.id), `중복 course.id: ${course.id}`);
    courseIds.add(course.id);
    assertIdentifier(course.slug, `${course.id}.slug`);
    assert(!courseSlugs.has(course.slug), `중복 또는 예약된 course.slug: ${course.slug}`);
    courseSlugs.add(course.slug);
    assert(["published", "planned"].includes(course.status), `잘못된 course.status: ${course.id}`);
    assert(Array.isArray(course.chapters), `${course.id}.chapters가 배열이 아닙니다.`);
    if (course.status === "planned") {
      assert(course.chapters.length === 0, `준비 중 교재에는 단원을 둘 수 없습니다: ${course.id}`);
      continue;
    }

    const chapterIds = new Set();
    for (const chapter of course.chapters) {
      assertIdentifier(chapter.id, `${course.id}.chapter.id`);
      assert(!chapterIds.has(chapter.id), `중복 chapter.id: ${course.id}/${chapter.id}`);
      chapterIds.add(chapter.id);
      assert(["week", "special"].includes(chapter.type), `잘못된 chapter.type: ${course.id}/${chapter.id}`);
      entries.push({ course, chapter });
    }
  }
  assert(entries.length === EXPECTED_DECKS, `공개 덱은 ${EXPECTED_DECKS}개여야 합니다: ${entries.length}`);
  return { catalog, entries };
}

async function copyPublishedFiles() {
  for (const [source, destination] of publishedFiles) {
    assert(await isFile(source), `사이트 입력 파일이 없습니다: ${path.relative(root, source)}`);
    assertInside(dist, destination, "배포 파일");
    await mkdir(path.dirname(destination), { recursive: true });
    await copyFile(source, destination);
  }
}

async function writeCoursePages(catalog) {
  const template = await readFile(courseTemplateFile, "utf8");
  for (const course of catalog.courses) {
    const directory = path.join(dist, course.slug);
    assertInside(dist, directory, "과목 페이지");
    const courseCatalog = {
      ...course,
      updated: catalog.site.updated,
      chapters: course.chapters.map((chapter) => ({
        ...chapter,
        href: path.posix.relative(course.slug, chapter.href),
      })),
    };
    const fields = {
      title: course.title,
      eyebrow: course.eyebrow,
      description: course.description,
      chapterCount: course.chapters.length,
      slideCount: course.chapters.reduce((total, chapter) => total + chapter.slides, 0),
      sourceUrl: course.sourceUrl,
      updated: catalog.site.updated,
    };
    const html = template.replace(/\{\{(\w+)\}\}/g, (_match, key) => {
      assert(Object.hasOwn(fields, key), `알 수 없는 과목 템플릿 필드: ${key}`);
      return escapeHtml(fields[key]);
    });
    await mkdir(directory, { recursive: true });
    await writeFile(path.join(directory, "index.html"), html, "utf8");
    await writeFile(path.join(directory, "catalog.json"), `${JSON.stringify(courseCatalog, null, 2)}\n`, "utf8");
    for (const asset of courseAssets) {
      const destination = path.join(directory, ...asset.split("/"));
      await mkdir(path.dirname(destination), { recursive: true });
      await copyFile(path.join(site, ...asset.split("/")), destination);
    }
    await copyFile(path.join(root, "LICENSE"), path.join(directory, "LICENSE"));
  }
}

async function writeLegacyRedirect(course, chapter) {
  const directory = path.join(legacyDecksRoot, course.id, chapter.id);
  assertInside(legacyDecksRoot, directory, "기존 슬라이드 주소");
  const href = `../../../${course.slug}/decks/${chapter.id}/index.html`;
  const html = `<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>${escapeHtml(chapter.title)} · ${escapeHtml(course.title)}</title>
    <noscript><meta http-equiv="refresh" content="0; url=${escapeHtml(href)}"></noscript>
  </head>
  <body>
    <p><a id="redirect-link" href="${escapeHtml(href)}">${escapeHtml(course.title)} · ${escapeHtml(chapter.title)} 열기</a></p>
    <script>
      const target = new URL(document.querySelector("#redirect-link").href);
      target.search = window.location.search;
      target.hash = window.location.hash;
      window.location.replace(target.href);
    </script>
  </body>
</html>
`;
  await mkdir(directory, { recursive: true });
  await writeFile(path.join(directory, "index.html"), html, "utf8");
}

async function copyDeckAssets(context, deckDirectory, canonicalRoot) {
  const assets = [...context.assets].sort(([left], [right]) => left.localeCompare(right));
  for (const [relative, outputRelative] of assets) {
    const source = path.resolve(root, ...relative.split("/"));
    assertInside(root, source, "교재 자산");
    assert(await isFile(source), `교재 자산이 없습니다: ${relative}`);
    const canonicalSource = await realpath(source);
    assertInside(canonicalRoot, canonicalSource, "교재 자산 실제 경로");
    const destination = path.join(deckDirectory, ...outputRelative.split("/"));
    assertInside(deckDirectory, destination, "생성된 교재 자산");
    await mkdir(path.dirname(destination), { recursive: true });
    await copyFile(canonicalSource, destination);
  }
}

async function main() {
  const nodeMajor = Number(process.versions.node.split(".")[0]);
  assert(nodeMajor >= EXPECTED_NODE_MAJOR, `Node.js ${EXPECTED_NODE_MAJOR}+가 필요합니다: ${process.versions.node}`);
  assertInside(root, dist, "dist");

  const [{ catalog, entries }, theme] = await Promise.all([
    readCatalog(),
    readFile(themeFile, "utf8"),
  ]);
  for (const [source] of publishedFiles) {
    assert(await isFile(source), `사이트 입력 파일이 없습니다: ${path.relative(root, source)}`);
  }
  for (const source of [courseTemplateFile, ...courseAssets.map((asset) => path.join(site, ...asset.split("/")))]) {
    assert(await isFile(source), `과목 사이트 입력 파일이 없습니다: ${path.relative(root, source)}`);
  }

  const marp = new Marp({ html: false });
  installUrlRewriter(marp);
  marp.themeSet.add(theme);
  const canonicalRoot = await realpath(root);
  const records = new Map();
  let initialized = false;
  let totalSlides = 0;
  let rewrittenLinks = 0;
  let copiedAssets = 0;

  try {
    await rm(dist, { recursive: true, force: true });
    await mkdir(legacyDecksRoot, { recursive: true });
    initialized = true;
    await copyPublishedFiles();

    for (const { course, chapter } of entries) {
      const relativeSource = sourcePath(course, chapter);
      const sourceFile = path.resolve(root, ...relativeSource.split("/"));
      assertInside(root, sourceFile, "슬라이드 원고");
      assert(await isFile(sourceFile), `슬라이드 원고가 없습니다: ${relativeSource}`);

      const prepared = prepareMarkdown(await readFile(sourceFile, "utf8"), relativeSource);
      const context = { assets: new Map(), relativeSource, rewrittenLinks: 0 };
      const rendered = marp.render(prepared, { teaching: context });
      rewrittenLinks += context.rewrittenLinks;
      copiedAssets += context.assets.size;
      const slides = slideCount(rendered.html);
      assert(slides > 0, `렌더된 슬라이드가 없습니다: ${course.id}/${chapter.id}`);
      totalSlides += slides;

      const href = path.posix.join(course.slug, "decks", chapter.id, "index.html");
      const output = path.join(dist, ...href.split("/"));
      assertInside(path.join(dist, course.slug, "decks"), output, "생성된 덱");
      await mkdir(path.dirname(output), { recursive: true });
      const record = { href, slides, sourceUrl: repositoryUrl(relativeSource) };
      await writeFile(
        output,
        renderDocument({ course, chapter, sourceUrl: record.sourceUrl, html: rendered.html, css: rendered.css }),
        "utf8",
      );
      await copyDeckAssets(context, path.dirname(output), canonicalRoot);
      await writeLegacyRedirect(course, chapter);
      records.set(`${course.id}/${chapter.id}`, record);
    }

    assert(totalSlides === EXPECTED_SLIDES, `전체 슬라이드는 ${EXPECTED_SLIDES}장이어야 합니다: ${totalSlides}`);
    const outputCatalog = {
      site: {
        ...catalog.site,
        stats: {
          courses: catalog.courses.length,
          publishedCourses: catalog.courses.filter((course) => course.status === "published").length,
          decks: entries.length,
          slides: totalSlides,
        },
      },
      courses: catalog.courses.map((course) => ({
        ...course,
        chapters: course.chapters.map((chapter) => {
          const record = records.get(`${course.id}/${chapter.id}`);
          assert(record, `빌드 결과가 없습니다: ${course.id}/${chapter.id}`);
          return { ...chapter, ...record };
        }),
      })),
    };
    await writeFile(path.join(dist, "catalog.json"), `${JSON.stringify(outputCatalog, null, 2)}\n`, "utf8");
    await writeCoursePages(outputCatalog);
    console.log(
      `교재 도서관 빌드 완료: ${entries.length}개 덱, ${totalSlides}장, 상대 Markdown 링크 ${rewrittenLinks}개 변환, 자산 ${copiedAssets}개 복사`,
    );
  } catch (error) {
    if (initialized) await rm(dist, { recursive: true, force: true });
    throw error;
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack : error);
  process.exitCode = 1;
});

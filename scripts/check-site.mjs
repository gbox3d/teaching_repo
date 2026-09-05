import { readFile, readdir, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runInNewContext } from "node:vm";
import { isDeepStrictEqual } from "node:util";

const EXPECTED_DECKS = 46;
const EXPECTED_SLIDES = 923;
const EXPECTED = {
  android: { slug: "android", decks: 15, slides: 228, status: "published" },
  web: { slug: "webprg", decks: 16, slides: 288, status: "published" },
  "open-source-ai": { slug: "open_source_ai", decks: 15, slides: 407, status: "published" },
};
const BLOB = "https://github.com/gbox3d/teaching_repo/blob/main";
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const dist = path.join(root, "dist");
const courseSlugs = new Set(Object.values(EXPECTED).map((course) => course.slug));
const failures = [];

const check = (value, message) => {
  if (!value) failures.push(message);
};

const inside = (base, candidate) => {
  const relative = path.relative(base, candidate);
  return (
    relative === "" ||
    (!relative.startsWith(`..${path.sep}`) && relative !== ".." && !path.isAbsolute(relative))
  );
};

async function fileInfo(filename) {
  try {
    return await stat(filename);
  } catch (error) {
    if (error?.code === "ENOENT") return null;
    throw error;
  }
}

async function exists(filename) {
  return Boolean(await fileInfo(filename));
}

async function walk(directory) {
  const files = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const filename = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...(await walk(filename)));
    else if (entry.isFile()) files.push(filename);
  }
  return files;
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
  return null;
}

const sourceUrl = (relative) =>
  `${BLOB}/${relative.split("/").map(encodeURIComponent).join("/")}`;

const slideCount = (html) =>
  (html.match(/<svg\b(?=[^>]*\bdata-marpit-svg\b)[^>]*>/gi) ?? []).length;

function splitTarget(target) {
  const positions = [target.indexOf("?"), target.indexOf("#")].filter((index) => index >= 0);
  const splitAt = positions.length ? Math.min(...positions) : target.length;
  return { pathname: target.slice(0, splitAt), suffix: target.slice(splitAt) };
}

function decodeHtml(value) {
  return value
    .replace(/&#(\d+);/g, (_whole, number) => String.fromCodePoint(Number(number)))
    .replace(/&#x([\da-f]+);/gi, (_whole, number) =>
      String.fromCodePoint(Number.parseInt(number, 16)),
    )
    .replaceAll("&quot;", '"')
    .replaceAll("&#39;", "'")
    .replaceAll("&lt;", "<")
    .replaceAll("&gt;", ">")
    .replaceAll("&amp;", "&");
}

const identifierCache = new Map();

async function identifiers(filename) {
  if (identifierCache.has(filename)) return identifierCache.get(filename);
  const values = new Set();
  const contents = await readFile(filename, "utf8");
  for (const match of contents.matchAll(/\s(?:id|name)\s*=\s*(?:"([^"]*)"|'([^']*)')/gi)) {
    values.add(decodeHtml(match[1] ?? match[2] ?? ""));
  }
  identifierCache.set(filename, values);
  return values;
}

function allowedProtocol(kind, protocol, target) {
  if (kind === "href") return ["http", "https", "mailto", "tel"].includes(protocol);
  if (kind === "action") return ["http", "https"].includes(protocol);
  if (protocol === "data") return /^data:image\//i.test(target);
  return ["http", "https"].includes(protocol);
}

async function localTarget(filename, rawTarget, kind) {
  const target = decodeHtml(rawTarget).trim();
  if (!target) return;
  const protocol = target.match(/^([a-z][a-z\d+.-]*):/i)?.[1].toLowerCase();
  if (protocol) {
    check(
      allowedProtocol(kind, protocol, target),
      `${path.relative(dist, filename)}: unsafe ${kind} protocol: ${target}`,
    );
    return;
  }
  check(
    !target.startsWith("//"),
    `${path.relative(dist, filename)}: protocol-relative ${kind}: ${target}`,
  );
  if (target.startsWith("//")) return;
  check(!target.includes("\\"), `${path.relative(dist, filename)}: backslash in ${kind}: ${target}`);
  if (target.includes("\\")) return;

  const { pathname: encodedPath } = splitTarget(target);
  let decodedPath;
  try {
    decodedPath = decodeURIComponent(encodedPath);
  } catch {
    failures.push(`${path.relative(dist, filename)}: malformed ${kind}: ${target}`);
    return;
  }
  check(
    !decodedPath.includes("\\") && !/[\u0000-\u001f\u007f]/.test(decodedPath),
    `${path.relative(dist, filename)}: unsafe decoded ${kind}: ${target}`,
  );
  if (decodedPath.includes("\\") || /[\u0000-\u001f\u007f]/.test(decodedPath)) return;
  check(!decodedPath.startsWith("/"), `${path.relative(dist, filename)}: root-relative ${kind}: ${target}`);
  if (decodedPath.startsWith("/")) return;
  let resolved = decodedPath
    ? path.resolve(path.dirname(filename), ...decodedPath.split("/"))
    : filename;
  check(inside(dist, resolved), `${path.relative(dist, filename)}: ${kind} escapes dist: ${target}`);
  if (!inside(dist, resolved)) return;
  const slug = path.relative(dist, filename).split(path.sep)[0];
  if (courseSlugs.has(slug)) {
    check(
      inside(path.join(dist, slug), resolved),
      `${path.relative(dist, filename)}: ${kind} leaves the standalone course: ${target}`,
    );
  }

  let info = await fileInfo(resolved);
  if (info?.isDirectory() && kind === "href") {
    resolved = path.join(resolved, "index.html");
    info = await fileInfo(resolved);
  }
  check(Boolean(info), `${path.relative(dist, filename)}: missing ${kind}: ${target}`);
  if (!info) return;
  check(kind === "href" || info.isFile(), `${path.relative(dist, filename)}: ${kind} is not a file: ${target}`);

  const hashAt = target.indexOf("#");
  if (hashAt < 0 || hashAt === target.length - 1) return;
  const rawFragment = target.slice(hashAt + 1);
  let decodedFragment;
  try {
    decodedFragment = decodeURIComponent(rawFragment);
  } catch {
    failures.push(`${path.relative(dist, filename)}: malformed fragment: ${target}`);
    return;
  }
  if (![".html", ".svg"].includes(path.extname(resolved).toLowerCase())) return;
  const ids = await identifiers(resolved);
  check(
    ids.has(rawFragment) || ids.has(decodedFragment),
    `${path.relative(dist, filename)}: missing fragment: ${target}`,
  );
}

function rootRelative(filename, contents) {
  const patterns = [
    /\b(?:href|src|action|poster)\s*=\s*["']\/(?!\/)/i,
    /\burl\(\s*["']?\/(?!\/)/i,
    /\b(?:fetch|import)\(\s*["']\/(?!\/)/i,
    /\bnew\s+URL\(\s*["']\/(?!\/)/i,
  ];
  check(
    !patterns.some((pattern) => pattern.test(contents)),
    `${path.relative(dist, filename)}: root-relative URL`,
  );
}

async function localAttributes(filename, html) {
  const pattern = /\s(href|src|poster|action)\s*=\s*(?:"([^"]*)"|'([^']*)')/gi;
  for (const match of html.matchAll(pattern)) {
    await localTarget(filename, match[2] ?? match[3] ?? "", match[1].toLowerCase());
  }
}

async function cssUrls(filename, contents, extension) {
  const blocks = [];
  if (extension === ".css") blocks.push(contents);
  if (extension === ".html" || extension === ".svg") {
    for (const match of contents.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/gi)) {
      blocks.push(match[1]);
    }
    for (const match of contents.matchAll(/\sstyle\s*=\s*(?:"([^"]*)"|'([^']*)')/gi)) {
      blocks.push(decodeHtml(match[1] ?? match[2] ?? ""));
    }
  }
  const pattern = /\burl\(\s*(?:(["'])(.*?)\1|([^'"\)]*))\s*\)/gi;
  for (const block of blocks) {
    for (const match of block.matchAll(pattern)) {
      await localTarget(filename, match[2] ?? match[3] ?? "", "css");
    }
  }
}

async function checkLibraryPage(relative, course) {
  const filename = path.join(dist, ...relative.split("/"));
  check(await exists(filename), `${relative} missing`);
  if (!(await exists(filename))) return;
  const html = await readFile(filename, "utf8");
  const assets = course
    ? ["favicon.svg", "assets/library.css", "assets/course.css", "assets/course.js"]
    : ["favicon.svg", "assets/library.css", "assets/library.js"];
  for (const asset of assets) {
    check(html.includes(`="./${asset}"`), `${relative}: wrong local asset URL: ${asset}`);
  }
  check(!/<base\b/i.test(html), `${relative}: base element would change local section links`);
  check(html.includes('class="brand" href="./"'), `${relative}: wrong home link`);
  if (course) {
    const title = decodeHtml(html.match(/<title>([\s\S]*?)<\/title>/)?.[1] ?? "");
    const description = decodeHtml(html.match(/<meta\s+name="description"\s+content="([^"]*)"/)?.[1] ?? "");
    const heading = decodeHtml(html.match(/<h1\b[^>]*>([\s\S]*?)<\/h1>/)?.[1] ?? "").replace(/<[^>]*>/g, "");
    check(title.includes(course.title), `${relative}: course title missing`);
    check(description.includes(course.title), `${relative}: course description missing`);
    check(heading.includes(course.title), `${relative}: course heading missing`);
    check(html.includes('id="chapters"'), `${relative}: chapter table of contents missing`);
    check(!html.includes('id="course-filters"'), `${relative}: global course filters remain`);
  }
}

async function checkCourseCatalog(course, updated) {
  const relative = `${course.slug}/catalog.json`;
  const filename = path.join(dist, ...relative.split("/"));
  check(await exists(filename), `${relative} missing`);
  if (!(await exists(filename))) return;
  const catalog = JSON.parse(await readFile(filename, "utf8"));
  const expected = {
    ...course,
    updated,
    chapters: course.chapters.map((chapter) => ({
      ...chapter,
      href: path.posix.join("decks", chapter.id, "index.html"),
    })),
  };
  check(
    isDeepStrictEqual(catalog, expected),
    `${relative}: standalone catalog must contain only this course with local chapter links`,
  );
  for (const chapter of catalog.chapters ?? []) {
    await localTarget(filename, chapter.href, "href");
  }
  for (const asset of [
    "index.html", "LICENSE", "favicon.svg", "assets/library.css", "assets/course.css",
    "assets/course.js", "assets/deck.css", "assets/deck.js",
  ]) {
    check(await exists(path.join(dist, course.slug, ...asset.split("/"))), `${course.slug}/${asset} missing`);
  }
}

async function checkLegacyRedirect(course, chapter) {
  const relative = path.posix.join("decks", course.id, chapter.id, "index.html");
  const filename = path.join(dist, ...relative.split("/"));
  check(await exists(filename), `${relative} legacy redirect missing`);
  if (!(await exists(filename))) return relative;
  const html = await readFile(filename, "utf8");
  check(slideCount(html) === 0, `${relative}: old shared deck still contains slides`);
  const target = `../../../${course.slug}/decks/${chapter.id}/index.html`;
  check(html.includes(`href="${target}"`), `${relative}: legacy fallback link missing`);
  const scripts = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)].map((match) => match[1]);
  let redirected;
  const location = {
    href: `https://example.test/teaching_repo/${relative}?view=presenter#slide-7`,
    search: "?view=presenter",
    hash: "#slide-7",
    replace(value) { redirected = value; },
  };
  const document = {
    querySelector(selector) {
      if (selector !== "#redirect-link") throw new Error(`Unexpected redirect selector: ${selector}`);
      const href = html.match(/<a\b(?=[^>]*\bid="redirect-link")[^>]*\bhref="([^"]*)"/)?.[1];
      if (!href) throw new Error("Redirect destination missing");
      return { href: new URL(decodeHtml(href), location.href).href };
    },
  };
  try {
    for (const script of scripts) {
      runInNewContext(script, { location, window: { location }, document, URL }, { timeout: 1000 });
    }
    check(
      redirected && new URL(redirected, location.href).href === new URL(`${target}${location.search}${location.hash}`, location.href).href,
      `${relative}: redirect must preserve query and slide fragment`,
    );
  } catch (error) {
    failures.push(`${relative}: redirect failed: ${error.message}`);
  }
  return relative;
}

async function main() {
  check(
    Number(process.versions.node.split(".")[0]) >= 24,
    `Node 24+ required; got ${process.versions.node}`,
  );
  for (const name of ["index.html", "catalog.json", "LICENSE", "favicon.svg"]) {
    check(await exists(path.join(dist, name)), `dist/${name} missing`);
  }
  if (!(await exists(path.join(dist, "catalog.json")))) throw new Error(failures.join("\n"));

  const catalog = JSON.parse(await readFile(path.join(dist, "catalog.json"), "utf8"));
  check(Array.isArray(catalog.courses), "catalog.courses must be an array");
  const courses = Array.isArray(catalog.courses) ? catalog.courses : [];
  const ids = new Set(courses.map((course) => course.id));
  for (const id of Object.keys(EXPECTED)) check(ids.has(id), `course missing: ${id}`);
  await checkLibraryPage("index.html");

  let decks = 0;
  let slides = 0;
  const expectedHtml = new Set();
  const expectedLegacy = new Set();
  for (const course of courses) {
    const expected = EXPECTED[course.id];
    check(Boolean(expected), `unexpected course: ${course.id}`);
    check(Array.isArray(course.chapters), `${course.id}.chapters must be an array`);
    if (!expected || !Array.isArray(course.chapters)) continue;
    check(course.slug === expected.slug, `${course.id}: wrong course slug`);
    await checkLibraryPage(`${expected.slug}/index.html`, course);
    await checkCourseCatalog(course, catalog.site.updated);
    check(course.status === expected.status, `${course.id}: wrong status`);
    check(
      course.chapters.length === expected.decks,
      `${course.id}: expected ${expected.decks} decks, got ${course.chapters.length}`,
    );

    let courseSlides = 0;
    const chapterIds = new Set();
    for (const chapter of course.chapters) {
      check(!chapterIds.has(chapter.id), `duplicate chapter: ${course.id}/${chapter.id}`);
      chapterIds.add(chapter.id);
      decks += 1;
      const count = Number.isInteger(chapter.slides) ? chapter.slides : 0;
      slides += count;
      courseSlides += count;
      const href = path.posix.join(expected.slug, "decks", chapter.id, "index.html");
      check(chapter.href === href, `${course.id}/${chapter.id}: wrong href`);
      expectedHtml.add(href);

      const source = sourcePath(course, chapter);
      check(Boolean(source), `${course.id}/${chapter.id}: unknown source`);
      if (source) {
        check(chapter.sourceUrl === sourceUrl(source), `${course.id}/${chapter.id}: wrong sourceUrl`);
        check(
          await exists(path.join(root, ...source.split("/"))),
          `${course.id}/${chapter.id}: source missing`,
        );
      }

      const deckFile = path.join(dist, ...href.split("/"));
      check(await exists(deckFile), `${href} missing`);
      if (await exists(deckFile)) {
        const html = await readFile(deckFile, "utf8");
        check(slideCount(html) === chapter.slides, `${href}: catalog/HTML slide mismatch`);
        check(
          html.includes('data-library-return href="../../#chapters"'),
          `${href}: return link missing`,
        );
        for (const asset of ["favicon.svg", "assets/deck.css", "assets/deck.js"]) {
          check(html.includes(`="../../${asset}"`), `${href}: wrong course asset URL: ${asset}`);
        }
      }
      expectedLegacy.add(await checkLegacyRedirect(course, chapter));
    }
    check(
      courseSlides === expected.slides,
      `${course.id}: expected ${expected.slides} slides, got ${courseSlides}`,
    );
  }

  check(decks === EXPECTED_DECKS, `expected ${EXPECTED_DECKS} decks, got ${decks}`);
  check(slides === EXPECTED_SLIDES, `expected ${EXPECTED_SLIDES} slides, got ${slides}`);
  check(catalog.site?.stats?.decks === EXPECTED_DECKS, "site.stats.decks must be 46");
  check(catalog.site?.stats?.slides === EXPECTED_SLIDES, "site.stats.slides must be 923");

  const files = await walk(dist);
  const actualHtml = new Set(
    files
      .map((file) => path.relative(dist, file).split(path.sep).join("/"))
      .filter((file) => /^[^/]+\/decks\/[^/]+\/index\.html$/.test(file)),
  );
  check(
    actualHtml.size === EXPECTED_DECKS,
    `expected ${EXPECTED_DECKS} deck files, got ${actualHtml.size}`,
  );
  for (const file of expectedHtml) check(actualHtml.has(file), `catalog deck missing: ${file}`);
  for (const file of actualHtml) check(expectedHtml.has(file), `uncatalogued deck: ${file}`);
  const actualLegacy = new Set(
    files
      .map((file) => path.relative(dist, file).split(path.sep).join("/"))
      .filter((file) => /^decks\/[^/]+\/[^/]+\/index\.html$/.test(file)),
  );
  check(actualLegacy.size === EXPECTED_DECKS, `expected ${EXPECTED_DECKS} legacy redirects, got ${actualLegacy.size}`);
  for (const file of expectedLegacy) check(actualLegacy.has(file), `legacy redirect missing: ${file}`);
  for (const file of actualLegacy) check(expectedLegacy.has(file), `unexpected legacy redirect: ${file}`);

  const allowedTop = new Set([
    "LICENSE",
    "assets",
    "catalog.json",
    "decks",
    "favicon.svg",
    "index.html",
    ...Object.values(EXPECTED).map((course) => course.slug),
  ]);
  for (const entry of await readdir(dist)) {
    check(allowedTop.has(entry), `unexpected dist entry: ${entry}`);
  }

  for (const filename of files) {
    const extension = path.extname(filename).toLowerCase();
    check(extension !== ".md", `source Markdown leaked: ${path.relative(dist, filename)}`);
    if ([".html", ".css", ".js", ".json", ".svg"].includes(extension)) {
      const contents = await readFile(filename, "utf8");
      rootRelative(filename, contents);
      if (extension === ".html" || extension === ".svg") {
        await localAttributes(filename, contents);
      }
      if ([".html", ".css", ".svg"].includes(extension)) {
        await cssUrls(filename, contents, extension);
      }
    }
  }

  if (failures.length) {
    throw new Error(`Site check failed (${failures.length})\n- ${failures.join("\n- ")}`);
  }
  console.log(`사이트 검증 완료: 독립 교재 ${courses.length}개, ${EXPECTED_DECKS}개 덱, ${EXPECTED_SLIDES}장, 기존 주소 리다이렉트 및 교재 내부 링크 정상`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack : error);
  process.exitCode = 1;
});

(function () {
  "use strict";

  const libraryRoot = new URL("../", document.currentScript.src);
  const catalogUrl = new URL("catalog.json", libraryRoot);
  const LANGUAGE_KEY = "teaching-language";
  const LANGUAGES = ["ko", "en"];

  // 정적 문구의 한국어는 HTML에 있는 그대로 쓰고, 영어만 여기 둔다.
  const STATIC_EN = {
    skip: "Skip to the course list",
    brandHome: "Teaching Library home",
    siteTitle: "Teaching Library",
    menu: "Main menu",
    find: "Find a course",
    language: "Language",
    repository: "Source",
    heroLine1: "A record of learning,",
    heroLine2: "open the next page",
    heroDescription:
      "Choose the course for your class. Each course has its own address and table of contents, so you can open that class's materials right away.",
    browse: "Browse courses",
    viewGithub: "View on GitHub",
    terminalNote: "Learning goes on.",
    stats: "Library overview",
    statCourses: "Courses",
    courseUnit: "",
    statChapters: "Chapters",
    chapterUnit: "",
    statSlides: "Slides",
    slideUnit: "",
    statNote: "Tip",
    statNoteText: "Share each course's address with your students.",
    libraryTitle: "Course shelf",
    libraryNote: "Search by title or topic. Opening a course takes you to its table of contents.",
    search: "Course search",
    searchLabel: "Search course titles and topics",
    searchPlaceholder: "e.g. Android, Supabase, local LLM",
    clearSearch: "Clear search",
    loading: "Loading the course list.",
    reset: "Reset search",
    license: "For class and personal study only. Redistribution and commercial use are prohibited.",
    updated: "Last updated",
    footerLinks: "Related links",
    githubRepository: "GitHub repository",
    licenseLink: "License",
  };

  const TEXT = {
    ko: {
      siteTitle: "교재 도서관",
      unknown: "정보 없음",
      untitled: "이름 없는 교재",
      defaultDescription: "주차별 강의 교재입니다.",
      metadata: (chapters, slides) => `${chapters}개 단원 · ${slides}장 슬라이드`,
      open: "교재 열기 →",
      openLabel: (title) => `${title} 교재 열기`,
      planned: "교재 준비 중",
      noMatch: "일치하는 교재가 없습니다",
      noMatchHint: "검색어를 줄이거나 다른 제목과 주제로 검색해 보세요.",
      searchPrefix: "검색 결과 ",
      courseCount: (count) => `${count}개 교재`,
      resultSuffix: " · 수업에 맞는 교재를 열어 주세요.",
      loadError: "교재 목록을 불러오지 못했습니다",
      loadErrorHint: "네트워크 상태를 확인한 뒤 다시 시도해 주세요. 로컬 파일이라면 웹 서버를 통해 열어야 합니다.",
      retry: "다시 불러오기",
      errorStatus: "교재 목록을 표시할 수 없습니다.",
      loading: "교재 목록을 불러오는 중입니다.",
    },
    en: {
      siteTitle: "Teaching Library",
      unknown: "Unknown",
      untitled: "Untitled course",
      defaultDescription: "Weekly lecture materials.",
      metadata: (chapters, slides) => `${chapters} chapters · ${slides} slides`,
      open: "Open course →",
      openLabel: (title) => `Open ${title}`,
      planned: "Coming soon",
      noMatch: "No matching courses",
      noMatchHint: "Try fewer words or another title or topic.",
      searchPrefix: "Search results: ",
      courseCount: (count) => `${count} courses`,
      resultSuffix: " · Open the course for your class.",
      loadError: "Could not load the course list",
      loadErrorHint: "Check your network and try again. A local file must be opened through a web server.",
      retry: "Reload",
      errorStatus: "The course list cannot be shown.",
      loading: "Loading the course list.",
    },
  };

  const originalText = new Map();
  const originalAttributes = new Map();

  const elements = {
    searchForm: document.querySelector("#search-form"),
    searchInput: document.querySelector("#catalog-search"),
    clearSearch: document.querySelector("#clear-search"),
    resetFilters: document.querySelector("#reset-filters"),
    resultStatus: document.querySelector("#result-status"),
    shelfList: document.querySelector("#shelf-list"),
    repositoryLink: document.querySelector("#repository-link"),
    heroSourceLink: document.querySelector("#hero-source-link"),
    footerRepositoryLink: document.querySelector("#footer-repository-link"),
    licenseLink: document.querySelector("#license-link"),
    updatedDate: document.querySelector("#updated-date"),
    statCourses: document.querySelector("#stat-courses"),
    statChapters: document.querySelector("#stat-chapters"),
    statSlides: document.querySelector("#stat-slides"),
    languageSelect: document.querySelector("#language-select"),
  };

  const state = {
    catalog: null,
    query: "",
    language: initialLanguage(),
  };

  function initialLanguage() {
    const requested = new URL(window.location.href).searchParams.get("lang");
    if (LANGUAGES.includes(requested)) return requested;
    try {
      const saved = window.localStorage.getItem(LANGUAGE_KEY);
      if (LANGUAGES.includes(saved)) return saved;
    } catch (_error) {}
    return "ko";
  }

  function text(key, ...args) {
    const value = TEXT[state.language][key];
    return typeof value === "function" ? value(...args) : value;
  }

  // 영문 필드가 있으면 그것을, 없으면 한국어 원문을 쓴다.
  function localized(entry, key) {
    if (state.language === "en" && entry && entry.en && typeof entry.en[key] === "string") return entry.en[key];
    return entry ? entry[key] : undefined;
  }

  function locale() {
    return state.language === "en" ? "en-US" : "ko-KR";
  }

  function createElement(tagName, className, text) {
    const node = document.createElement(tagName);
    if (className) node.className = className;
    if (typeof text === "string") node.textContent = text;
    return node;
  }

  function normaliseText(value) {
    return String(value || "")
      .normalize("NFKC")
      .toLocaleLowerCase("ko-KR")
      .replace(/\s+/g, " ")
      .trim();
  }

  function textValue(value, fallback) {
    if (typeof value !== "string") return fallback;
    const trimmed = value.trim();
    return trimmed || fallback;
  }

  function numericValue(value) {
    const number = Number(value);
    return Number.isFinite(number) && number > 0 ? Math.round(number) : 0;
  }

  function safeInternalHref(value) {
    const href = textValue(value, "");
    if (!href) return "";

    try {
      const parsed = new URL(href, libraryRoot);
      if (
        ["http:", "https:"].includes(parsed.protocol) &&
        parsed.origin === libraryRoot.origin &&
        parsed.pathname.startsWith(libraryRoot.pathname)
      ) {
        return parsed.href;
      }
    } catch (_error) {
      return "";
    }

    return "";
  }

  function safeExternalHref(value) {
    const href = textValue(value, "");
    if (!href) return "";

    try {
      const parsed = new URL(href);
      if (["http:", "https:"].includes(parsed.protocol)) return parsed.href;
    } catch (_error) {
      return "";
    }

    return "";
  }

  function configureLink(link, rawHref, options) {
    const config = options || {};
    const href = config.external ? safeExternalHref(rawHref) : safeInternalHref(rawHref);
    if (!href) {
      if (config.hideWhenMissing) link.hidden = true;
      return false;
    }

    link.href = href;
    link.hidden = false;

    if (config.external || config.newTab) {
      link.target = "_blank";
      link.rel = "noopener noreferrer";
    }

    return true;
  }

  function formatNumber(value) {
    return new Intl.NumberFormat(locale()).format(numericValue(value));
  }

  function getCourses() {
    return Array.isArray(state.catalog && state.catalog.courses) ? state.catalog.courses : [];
  }

  function validateCatalog(payload) {
    if (!payload || typeof payload !== "object" || !Array.isArray(payload.courses)) {
      throw new Error("catalog.json 형식이 올바르지 않습니다.");
    }

    return payload;
  }

  function setSiteInformation(site) {
    const siteInfo = site && typeof site === "object" ? site : {};
    const title = textValue(localized(siteInfo, "title"), text("siteTitle"));
    document.title = `${title} · Teaching Archive`;

    [elements.repositoryLink, elements.heroSourceLink, elements.footerRepositoryLink].forEach((link) => {
      configureLink(link, siteInfo.repositoryUrl, { external: true, hideWhenMissing: true });
    });
    configureLink(elements.licenseLink, siteInfo.licenseUrl, {
      external: true,
      hideWhenMissing: true,
    });

    const updated = textValue(siteInfo.updated, "");
    if (!updated) {
      elements.updatedDate.textContent = text("unknown");
      elements.updatedDate.removeAttribute("datetime");
      return;
    }

    const date = new Date(updated);
    elements.updatedDate.dateTime = updated;
    const dateFormatter = new Intl.DateTimeFormat(locale(), { year: "numeric", month: "long", day: "numeric" });
    elements.updatedDate.textContent = Number.isNaN(date.getTime()) ? updated : dateFormatter.format(date);
  }

  function setStatistics(courses) {
    const publishedCourses = courses.filter((course) => course.status === "published");
    const chapters = publishedCourses.flatMap((course) =>
      Array.isArray(course.chapters) ? course.chapters : [],
    );
    const slides = chapters.reduce((total, chapter) => total + numericValue(chapter.slides), 0);

    elements.statCourses.textContent = formatNumber(publishedCourses.length);
    elements.statChapters.textContent = formatNumber(chapters.length);
    elements.statSlides.textContent = formatNumber(slides);
  }

  function filteredCourses() {
    const query = normaliseText(state.query);
    const weekQuery = query.match(/^0*(\d+)\s*주차$/) || query.match(/^week\s*0*(\d+)$/);

    return getCourses().filter((course) => {
      if (!query) return true;
      const chapters = Array.isArray(course.chapters) ? course.chapters : [];
      if (weekQuery) {
        return chapters.some((chapter) =>
          [chapter.label, chapter.en && chapter.en.label]
            .map(normaliseText)
            .some((label) => label === `${Number(weekQuery[1])}주차` || label === `week ${Number(weekQuery[1])}`),
        );
      }
      const english = (entry) => entry.en || {};
      const searchText = [
        course.id, course.slug, course.title, course.eyebrow, course.description,
        english(course).title, english(course).description,
        ...chapters.flatMap((chapter) => [
          chapter.id, chapter.label, chapter.title, chapter.description,
          english(chapter).label, english(chapter).title, english(chapter).description,
        ]),
      ].filter(Boolean).join(" ");
      return normaliseText(searchText).includes(query);
    });
  }

  function createBookCover(course, courseNumber) {
    const cover = createElement("div", "book-cover");
    cover.setAttribute("aria-hidden", "true");

    const code = createElement("div", "book-code");
    code.append(
      createElement("span", "", `COURSE ${String(courseNumber).padStart(2, "0")}`),
      createElement("span", "", "LECTURE NOTE"),
    );

    const title = createElement("div", "book-title", textValue(localized(course, "title"), text("untitled")));

    const footer = createElement("div", "book-footer");
    footer.append(
      createElement("span", "", "COURSE ARCHIVE"),
      createElement("span", "book-edition", course.status === "planned" ? "SOON" : "READ"),
    );

    cover.append(code, title, footer);
    return cover;
  }

  function createCourseCard(course) {
    const courseNumber = getCourses().indexOf(course) + 1;
    const title = textValue(localized(course, "title"), text("untitled"));
    const headingId = `course-heading-${course.slug}`;
    const card = createElement("article", "portal-card");
    card.dataset.course = course.slug;
    card.setAttribute("aria-labelledby", headingId);
    const cover = createElement("div", "portal-cover");
    cover.append(createBookCover(course, courseNumber));

    const content = createElement("div", "portal-content");
    const eyebrow = createElement("p", "course-eyebrow", textValue(course.eyebrow, "Course textbook"));
    const heading = createElement("h3", "portal-title", title);
    heading.id = headingId;
    const description = createElement(
      "p", "portal-description", textValue(localized(course, "description"), text("defaultDescription")),
    );

    const chapters = Array.isArray(course.chapters) ? course.chapters : [];
    const slides = chapters.reduce((total, chapter) => total + numericValue(chapter.slides), 0);
    const metadata = createElement(
      "p", "portal-metadata", text("metadata", formatNumber(chapters.length), formatNumber(slides)),
    );
    const address = createElement("p", "portal-address", `/${course.slug}/`);
    content.append(eyebrow, heading, description, metadata, address);

    if (course.status === "published") {
      const link = createElement("a", "button button--primary course-open-link", text("open"));
      configureLink(link, `${course.slug}/${state.language === "en" ? "?lang=en" : ""}`);
      link.setAttribute("aria-label", text("openLabel", title));
      content.append(link);
    } else {
      content.append(createElement("span", "course-status course-status--planned", text("planned")));
    }

    card.append(cover, content);
    return card;
  }

  function createEmptyState() {
    const empty = createElement("div", "empty-state");
    empty.append(
      createElement("div", "empty-state-mark", "⌕"),
      createElement("h3", "", text("noMatch")),
      createElement("p", "", text("noMatchHint")),
    );
    return empty;
  }

  function setResultSummary(courses) {
    elements.resultStatus.replaceChildren(
      document.createTextNode(state.query ? text("searchPrefix") : ""),
      createElement("strong", "", text("courseCount", formatNumber(courses.length))),
      document.createTextNode(text("resultSuffix")),
    );
    elements.resetFilters.hidden = !state.query;
  }

  function renderCatalog() {
    if (!state.catalog) return;

    const entries = filteredCourses();
    const fragment = document.createDocumentFragment();
    entries.forEach((course) => fragment.append(createCourseCard(course)));

    elements.shelfList.replaceChildren(fragment.childNodes.length ? fragment : createEmptyState());
    elements.shelfList.setAttribute("aria-busy", "false");
    elements.clearSearch.hidden = !state.query;
    setResultSummary(entries);
  }

  function resetCatalogView(options) {
    const config = options || {};
    state.query = "";
    elements.searchInput.value = "";
    renderCatalog();
    if (config.focusSearch) elements.searchInput.focus();
  }

  function showError(error) {
    const errorState = createElement("div", "error-state");
    errorState.append(
      createElement("div", "error-state-mark", "!"),
      createElement("h3", "", text("loadError")),
      createElement("p", "", text("loadErrorHint")),
    );
    const retry = createElement("button", "", text("retry"));
    retry.type = "button";
    retry.addEventListener("click", loadCatalog, { once: true });
    errorState.append(retry);

    elements.shelfList.replaceChildren(errorState);
    elements.shelfList.setAttribute("aria-busy", "false");
    elements.resultStatus.textContent = text("errorStatus");
    elements.resetFilters.hidden = true;

    if (window.console && typeof window.console.error === "function") {
      console.error("교재 카탈로그 로드 실패:", error);
    }
  }

  async function loadCatalog() {
    elements.shelfList.setAttribute("aria-busy", "true");
    elements.resultStatus.textContent = text("loading");

    try {
      const response = await fetch(catalogUrl, {
        cache: "no-cache",
        headers: { Accept: "application/json" },
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      state.catalog = validateCatalog(await response.json());
      const courses = getCourses();
      state.query = elements.searchInput.value;
      setStatistics(courses);
      applyLanguage();
    } catch (error) {
      showError(error);
    }
  }

  elements.searchForm.addEventListener("submit", function (event) {
    event.preventDefault();
  });

  elements.searchInput.addEventListener("input", function (event) {
    state.query = event.currentTarget.value;
    renderCatalog();
  });

  elements.clearSearch.addEventListener("click", function () {
    state.query = "";
    elements.searchInput.value = "";
    elements.searchInput.focus();
    renderCatalog();
  });

  elements.resetFilters.addEventListener("click", function () {
    resetCatalogView({ focusSearch: true });
  });

  function applyStaticText() {
    document.querySelectorAll("[data-i18n]").forEach((node) => {
      if (!originalText.has(node)) originalText.set(node, node.innerHTML);
      if (state.language === "en") node.textContent = STATIC_EN[node.dataset.i18n];
      else node.innerHTML = originalText.get(node);
    });
    document.querySelectorAll("[data-i18n-attr]").forEach((node) => {
      node.dataset.i18nAttr.split(";").forEach((pair) => {
        const [attribute, key] = pair.split(":");
        const id = `${attribute}\u0000${key}`;
        if (!originalAttributes.has(node)) originalAttributes.set(node, new Map());
        const saved = originalAttributes.get(node);
        if (!saved.has(id)) saved.set(id, node.getAttribute(attribute));
        node.setAttribute(attribute, state.language === "en" ? STATIC_EN[key] : saved.get(id));
      });
    });
  }

  function applyLanguage() {
    document.documentElement.lang = state.language;
    if (elements.languageSelect) elements.languageSelect.value = state.language;
    applyStaticText();
    if (!state.catalog) return;
    setSiteInformation(state.catalog.site);
    renderCatalog();
  }

  function setLanguage(language) {
    if (!LANGUAGES.includes(language)) return;
    state.language = language;
    try {
      window.localStorage.setItem(LANGUAGE_KEY, language);
    } catch (_error) {}
    const url = new URL(window.location.href);
    if (language === "ko") url.searchParams.delete("lang");
    else url.searchParams.set("lang", language);
    window.history.replaceState(null, "", url.href);
    applyLanguage();
  }

  if (elements.languageSelect) {
    elements.languageSelect.addEventListener("change", function () {
      setLanguage(elements.languageSelect.value);
    });
  }

  applyLanguage();
  loadCatalog();
})();

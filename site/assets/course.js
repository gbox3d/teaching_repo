(function () {
  "use strict";

  const courseRoot = new URL("../", document.currentScript.src);
  const catalogUrl = new URL("catalog.json", courseRoot);
  const LANGUAGE_KEY = "teaching-language";
  const LANGUAGES = ["ko", "en"];
  const elements = {
    searchForm: document.querySelector("#search-form"),
    searchInput: document.querySelector("#chapter-search"),
    clearSearch: document.querySelector("#clear-search"),
    resetSearch: document.querySelector("#reset-search"),
    resultStatus: document.querySelector("#result-status"),
    chapterList: document.querySelector("#chapter-list"),
    languageSelect: document.querySelector("#language-select"),
  };
  const state = { course: null, query: "", language: initialLanguage() };

  // 정적 문구의 한국어는 HTML에 있는 그대로 쓰고, 영어만 여기 둔다.
  const STATIC_EN = {
    skip: "Skip to contents",
    brandHome: "Course home",
    menu: "Course menu",
    contents: "Contents",
    language: "Language",
    source: "Source",
    newTab: " (new tab)",
    openContents: "Open contents",
    facts: "About this course",
    chapters: "Chapters",
    chapterUnit: "",
    slides: "Slides",
    slideUnit: "",
    readingNote: "Pick today's chapter from the contents.",
    chaptersTitle: "Contents",
    chaptersNote: "Each chapter opens its lecture slides in a new tab.",
    searchLabel: "Search this course's chapters",
    searchPlaceholder: "Search by title, topic, or week",
    clearSearch: "Clear search",
    loading: "Loading contents.",
    showAll: "Show all chapters",
    license: "For class and personal study only. Redistribution and commercial use are prohibited.",
    updated: "Last updated",
    footerLinks: "Course links",
    licenseLink: "License",
  };

  const TEXT = {
    ko: {
      pageTitle: (title) => `${title} · 강의 교재`,
      chapter: "단원",
      untitled: "제목 없는 단원",
      special: "특별 자료",
      defaultDescription: "해당 단원의 강의 슬라이드입니다.",
      slideCount: (count) => `${count}장`,
      slidesFallback: "슬라이드",
      planned: "준비 중",
      source: "원고 ↗",
      open: "열기",
      soon: "예정",
      newTab: (label) => `${label} (새 탭)`,
      openSlides: (label, title) => `${label} ${title} 슬라이드 열기`,
      viewSource: (label) => `${label} 원본 원고 보기`,
      noMatch: "일치하는 단원이 없습니다",
      noMatchHint: "검색어를 줄이거나 다른 단원 제목으로 검색해 보세요.",
      preparing: "단원을 준비하고 있습니다",
      preparingHint: "이 교재의 강의 자료가 준비되면 목차에서 읽을 수 있습니다.",
      searchResult: (found, total) => `검색 결과 ${found}개 단원 · 이 교재의 전체 ${total}개 단원`,
      allResult: (count) => `이 교재의 ${count}개 단원`,
      loadError: "이 교재의 목차를 불러오지 못했습니다",
      loadErrorHint: "연결 상태를 확인한 뒤 다시 시도해 주세요.",
      retry: "목차 다시 불러오기",
      errorStatus: "이 교재의 목차를 표시할 수 없습니다.",
      loading: "단원 목차를 불러오는 중입니다.",
      koreanOnly: "",
    },
    en: {
      pageTitle: (title) => `${title} · Lecture Notes`,
      chapter: "Chapter",
      untitled: "Untitled chapter",
      special: "Special",
      defaultDescription: "Lecture slides for this chapter.",
      slideCount: (count) => `${count} slides`,
      slidesFallback: "Slides",
      planned: "Coming soon",
      source: "Source ↗",
      open: "Open",
      soon: "Soon",
      newTab: (label) => `${label} (new tab)`,
      openSlides: (label, title) => `Open ${label} ${title} slides`,
      viewSource: (label) => `View ${label} source`,
      noMatch: "No matching chapters",
      noMatchHint: "Try fewer words or another chapter title.",
      preparing: "Chapters are being prepared",
      preparingHint: "Lecture materials will appear here when they are ready.",
      searchResult: (found, total) => `${found} matching chapters · ${total} in this course`,
      allResult: (count) => `${count} chapters in this course`,
      loadError: "Could not load this course's contents",
      loadErrorHint: "Check your connection and try again.",
      retry: "Reload contents",
      errorStatus: "The contents cannot be shown.",
      loading: "Loading contents.",
      koreanOnly: "Korean only",
    },
  };

  const originalText = new Map();
  const originalAttributes = new Map();

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

  function formatNumber(value) {
    return new Intl.NumberFormat(state.language === "en" ? "en-US" : "ko-KR").format(value);
  }

  function createElement(tagName, className, content) {
    const node = document.createElement(tagName);
    if (className) node.className = className;
    if (typeof content === "string") node.textContent = content;
    return node;
  }

  function textValue(value, fallback) {
    return typeof value === "string" && value.trim() ? value.trim() : fallback;
  }

  // 영문 필드가 있으면 그것을, 없으면 한국어 원문을 쓴다.
  function localized(entry, key) {
    if (state.language === "en" && entry && entry.en && typeof entry.en[key] === "string") return entry.en[key];
    return entry ? entry[key] : undefined;
  }

  function normaliseText(value) {
    return String(value || "").normalize("NFKC").toLocaleLowerCase("ko-KR").replace(/\s+/g, " ").trim();
  }

  function safeHref(value, external) {
    if (typeof value !== "string" || !value.trim()) return "";
    try {
      const url = external ? new URL(value) : new URL(value, courseRoot);
      if (!["http:", "https:"].includes(url.protocol)) return "";
      if (external || (url.origin === courseRoot.origin && url.pathname.startsWith(courseRoot.pathname))) {
        return url.href;
      }
    } catch (_error) {
      return "";
    }
    return "";
  }

  function newTabLink(className, title, href, label) {
    const link = createElement("a", className, title);
    link.href = href;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.setAttribute("aria-label", text("newTab", label));
    return link;
  }

  function chapterVersion(chapter) {
    const english = state.language === "en" && chapter.hrefEn;
    return {
      href: english ? chapter.hrefEn : chapter.href,
      slides: english ? chapter.slidesEn : chapter.slides,
      sourceUrl: english ? chapter.sourceUrlEn : chapter.sourceUrl,
      koreanOnly: state.language === "en" && !chapter.hrefEn,
    };
  }

  function createChapterCard(chapter) {
    const version = chapterVersion(chapter);
    const href = state.course.status === "published" ? safeHref(version.href, false) : "";
    const label = textValue(localized(chapter, "label"), text("chapter"));
    const title = textValue(localized(chapter, "title"), text("untitled"));
    const card = createElement("article", `chapter-card${href ? "" : " chapter-card--planned"}`);
    const topLine = createElement("div", "chapter-topline");
    topLine.append(createElement("span", "chapter-label", label));
    if (chapter.type === "special") topLine.append(createElement("span", "chapter-type", text("special")));
    if (version.koreanOnly && href) topLine.append(createElement("span", "chapter-type", text("koreanOnly")));

    const heading = createElement("h3");
    heading.append(href ? newTabLink("chapter-link", title, href, text("openSlides", label, title)) : createElement("span", "", title));
    const description = createElement("p", "", textValue(localized(chapter, "description"), text("defaultDescription")));
    const footer = createElement("div", "chapter-footer");
    const slides = Number(version.slides);
    const slideCount = Number.isFinite(slides) && slides > 0 ? text("slideCount", formatNumber(Math.round(slides))) : href ? text("slidesFallback") : text("planned");
    footer.append(createElement("span", "chapter-slide-count", slideCount));

    const footerLinks = createElement("span", "chapter-footer-links");
    const sourceHref = safeHref(version.sourceUrl, true);
    if (sourceHref) footerLinks.append(newTabLink("chapter-source", text("source"), sourceHref, text("viewSource", label)));
    footerLinks.append(createElement("span", "chapter-open", href ? text("open") : text("soon")));
    footer.append(footerLinks);
    card.append(topLine, heading, description, footer);
    return card;
  }

  function createEmptyState() {
    const panel = createElement("div", "empty-state");
    const searching = Boolean(normaliseText(state.query));
    panel.append(
      createElement("div", "empty-state-mark", searching ? "⌕" : ">_"),
      createElement("h3", "", searching ? text("noMatch") : text("preparing")),
      createElement("p", "", searching ? text("noMatchHint") : textValue(localized(state.course, "summary"), text("preparingHint"))),
    );
    return panel;
  }

  function requestedWeek(query) {
    const match = query.match(/^0*(\d+)\s*주차$/) || query.match(/^week\s*0*(\d+)$/);
    return match ? Number(match[1]) : null;
  }

  function renderChapters() {
    if (!state.course) return;
    const query = normaliseText(state.query);
    const terms = query.split(" ").filter(Boolean);
    const week = requestedWeek(query);
    const chapters = state.course.chapters.filter((chapter) => {
      if (week !== null) {
        const labels = [chapter.label, chapter.en && chapter.en.label].map(normaliseText);
        return labels.some((label) => requestedWeek(label) === week);
      }
      const english = chapter.en || {};
      const searchable = [chapter.id, chapter.label, chapter.title, chapter.description, chapter.type, english.label, english.title, english.description];
      const haystack = normaliseText(searchable.filter(Boolean).join(" "));
      return terms.every((term) => haystack.includes(term));
    });
    const grid = createElement("div", "chapter-grid");
    chapters.forEach((chapter) => grid.append(createChapterCard(chapter)));
    elements.chapterList.replaceChildren(chapters.length ? grid : createEmptyState());
    elements.chapterList.setAttribute("aria-busy", "false");
    elements.clearSearch.hidden = !state.query;
    elements.resetSearch.hidden = !state.query;
    elements.resultStatus.textContent = query
      ? text("searchResult", formatNumber(chapters.length), formatNumber(state.course.chapters.length))
      : text("allResult", formatNumber(chapters.length));
  }

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

  function applyCourseText() {
    if (!state.course) return;
    document.querySelectorAll("[data-course-field]").forEach((node) => {
      node.textContent = textValue(localized(state.course, node.dataset.courseField), node.textContent);
    });
    document.title = text("pageTitle", textValue(localized(state.course, "title"), state.course.title));
  }

  function applyLanguage() {
    document.documentElement.lang = state.language;
    if (elements.languageSelect) elements.languageSelect.value = state.language;
    applyStaticText();
    applyCourseText();
    renderChapters();
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

  function resetSearch() {
    state.query = "";
    elements.searchInput.value = "";
    renderChapters();
    elements.searchInput.focus();
  }

  function showError(error) {
    const panel = createElement("div", "error-state");
    panel.append(
      createElement("div", "error-state-mark", "!"),
      createElement("h3", "", text("loadError")),
      createElement("p", "", text("loadErrorHint")),
    );
    const retry = createElement("button", "", text("retry"));
    retry.type = "button";
    retry.addEventListener("click", loadCatalog, { once: true });
    panel.append(retry);
    elements.chapterList.replaceChildren(panel);
    elements.chapterList.setAttribute("aria-busy", "false");
    elements.resultStatus.textContent = text("errorStatus");
    elements.resetSearch.hidden = true;
    console.error("교재 목차 로드 실패:", error);
  }

  async function loadCatalog() {
    elements.chapterList.setAttribute("aria-busy", "true");
    elements.resultStatus.textContent = text("loading");
    try {
      const response = await fetch(catalogUrl, { cache: "no-cache", headers: { Accept: "application/json" } });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const course = await response.json();
      if (!course || typeof course !== "object" || !Array.isArray(course.chapters) || typeof course.title !== "string") {
        throw new Error("교재 catalog.json 형식이 올바르지 않습니다.");
      }
      state.course = course;
      state.query = elements.searchInput.value;
      applyLanguage();
    } catch (error) {
      showError(error);
    }
  }

  elements.searchForm.addEventListener("submit", (event) => event.preventDefault());
  elements.searchInput.addEventListener("input", function () {
    state.query = elements.searchInput.value;
    renderChapters();
  });
  elements.clearSearch.addEventListener("click", resetSearch);
  elements.resetSearch.addEventListener("click", resetSearch);
  elements.searchInput.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      event.preventDefault();
      resetSearch();
    }
  });
  if (elements.languageSelect) {
    elements.languageSelect.addEventListener("change", () => setLanguage(elements.languageSelect.value));
  }

  document.documentElement.lang = state.language;
  if (elements.languageSelect) elements.languageSelect.value = state.language;
  applyStaticText();
  loadCatalog();
})();

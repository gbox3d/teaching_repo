(function () {
  "use strict";

  const catalogUrl = "./catalog.json";
  const defaultAccent = "#2d655e";
  const numberFormatter = new Intl.NumberFormat("ko-KR");
  const dateFormatter = new Intl.DateTimeFormat("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  const elements = {
    searchForm: document.querySelector("#search-form"),
    searchInput: document.querySelector("#catalog-search"),
    clearSearch: document.querySelector("#clear-search"),
    filters: document.querySelector("#course-filters"),
    resetFilters: document.querySelector("#reset-filters"),
    resultStatus: document.querySelector("#result-status"),
    shelfList: document.querySelector("#shelf-list"),
    heroDescription: document.querySelector("#hero-description"),
    repositoryLink: document.querySelector("#repository-link"),
    heroSourceLink: document.querySelector("#hero-source-link"),
    footerRepositoryLink: document.querySelector("#footer-repository-link"),
    licenseLink: document.querySelector("#license-link"),
    updatedDate: document.querySelector("#updated-date"),
    statCourses: document.querySelector("#stat-courses"),
    statChapters: document.querySelector("#stat-chapters"),
    statSlides: document.querySelector("#stat-slides"),
  };

  const state = {
    catalog: null,
    course: "all",
    query: "",
  };

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

  function safeAccent(value) {
    const color = textValue(value, "");
    if (/^#[0-9a-f]{3,8}$/i.test(color)) return color;
    return defaultAccent;
  }

  function safeInternalHref(value) {
    const href = textValue(value, "");
    if (!href) return "";

    try {
      const parsed = new URL(href, document.baseURI);
      const libraryRoot = new URL("./", document.baseURI);
      if (
        ["http:", "https:"].includes(parsed.protocol) &&
        parsed.origin === libraryRoot.origin &&
        parsed.pathname.startsWith(libraryRoot.pathname)
      ) {
        return href;
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

    const isExternal = /^https?:\/\//i.test(href);
    if (isExternal || config.newTab) {
      link.target = "_blank";
      link.rel = "noopener noreferrer";
    }

    return true;
  }

  function formatNumber(value) {
    return numberFormatter.format(numericValue(value));
  }

  function getChapterSearchText(chapter) {
    return normaliseText(
      [chapter.id, chapter.label, chapter.title, chapter.description, chapter.type].filter(Boolean).join(" "),
    );
  }

  function getCourseSearchText(course) {
    return normaliseText(
      [course.id, course.title, course.eyebrow].filter(Boolean).join(" "),
    );
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
    const title = textValue(siteInfo.title, "교재 도서관");
    const description = textValue(
      siteInfo.description,
      "강의별 교재와 주차별 슬라이드를 한곳에 모았습니다. 필요한 수업을 찾아 바로 열람해 보세요.",
    );

    document.title = `${title} · GBOX3 Teaching`;
    elements.heroDescription.textContent = description;

    [elements.repositoryLink, elements.heroSourceLink, elements.footerRepositoryLink].forEach((link) => {
      configureLink(link, siteInfo.repositoryUrl, { external: true, hideWhenMissing: true });
    });
    configureLink(elements.licenseLink, siteInfo.licenseUrl, {
      external: true,
      hideWhenMissing: true,
    });

    const updated = textValue(siteInfo.updated, "");
    if (!updated) {
      elements.updatedDate.textContent = "정보 없음";
      elements.updatedDate.removeAttribute("datetime");
      return;
    }

    const date = new Date(updated);
    elements.updatedDate.dateTime = updated;
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

  function createFilterButton(id, label) {
    const button = createElement("button", "filter-button", label);
    button.type = "button";
    button.dataset.course = id;
    button.setAttribute("aria-pressed", String(state.course === id));
    button.addEventListener("click", function () {
      state.course = id;
      updateFilterButtons();
      renderCatalog();
    });
    return button;
  }

  function buildFilters(courses) {
    const fragment = document.createDocumentFragment();
    fragment.append(createFilterButton("all", "전체 교재"));

    courses.forEach((course) => {
      const id = textValue(course.id, "");
      if (!id) return;
      fragment.append(createFilterButton(id, textValue(course.title, "이름 없는 교재")));
    });

    elements.filters.replaceChildren(fragment);
  }

  function updateFilterButtons() {
    elements.filters.querySelectorAll("[data-course]").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.course === state.course));
    });
  }

  function filteredCourses() {
    const query = normaliseText(state.query);
    const weekQuery = query.match(/^0*(\d+)\s*주차$/);

    return getCourses().flatMap((course) => {
      const id = textValue(course.id, "");
      if (state.course !== "all" && id !== state.course) return [];

      const chapters = Array.isArray(course.chapters) ? course.chapters : [];
      if (!query) return [{ course, chapters }];

      if (!weekQuery && getCourseSearchText(course).includes(query)) return [{ course, chapters }];

      const matchingChapters = chapters.filter((chapter) => {
        if (weekQuery) return normaliseText(chapter.label) === `${Number(weekQuery[1])}주차`;
        return getChapterSearchText(chapter).includes(query);
      });
      if (!matchingChapters.length) return [];
      return [{ course, chapters: matchingChapters }];
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

    const title = createElement("div", "book-title", textValue(course.title, "이름 없는 교재"));

    const footer = createElement("div", "book-footer");
    footer.append(
      createElement("span", "", "GBOX3 TEACHING"),
      createElement("span", "book-edition", course.status === "planned" ? "SOON" : "READ"),
    );

    cover.append(code, title, footer);
    return cover;
  }

  function createCourseOverview(course, chapters, courseNumber) {
    const overview = createElement("div", "course-overview");
    overview.append(createBookCover(course, courseNumber));

    const metadata = createElement("div", "course-meta");
    const metadataRow = createElement("div", "course-meta-row");
    const isPlanned = course.status === "planned";
    const status = createElement(
      "span",
      `course-status${isPlanned ? " course-status--planned" : ""}`,
      isPlanned ? "준비 중" : "열람 가능",
    );
    const chapterCount = createElement(
      "span",
      "course-count",
      chapters.length ? `· ${formatNumber(chapters.length)}개 단원` : "· 단원 준비 중",
    );
    metadataRow.append(status, chapterCount);

    const title = createElement("h3", "", textValue(course.title, "이름 없는 교재"));
    const summary = createElement(
      "p",
      "course-summary",
      textValue(course.summary, textValue(course.description, "강의 교재")),
    );

    metadata.append(metadataRow, title, summary);
    overview.append(metadata);
    return overview;
  }

  function createChapterCard(chapter, course) {
    const href = course.status === "published" ? safeInternalHref(chapter.href) : "";
    const card = createElement("article", `chapter-card${href ? "" : " chapter-card--planned"}`);

    const topLine = createElement("div", "chapter-topline");
    topLine.append(createElement("span", "chapter-label", textValue(chapter.label, "단원")));
    if (chapter.type === "special") {
      topLine.append(createElement("span", "chapter-type", "특별 자료"));
    }

    const heading = createElement("h3");
    const title = textValue(chapter.title, "제목 없는 단원");
    if (href) {
      const link = createElement("a", "chapter-link", title);
      link.setAttribute(
        "aria-label",
        `${textValue(chapter.label, "단원")} ${title} 슬라이드 열기 (새 탭)`,
      );
      configureLink(link, href, { newTab: true });
      heading.append(link);
    } else {
      heading.append(createElement("span", "", title));
    }

    const description = createElement(
      "p",
      "",
      textValue(chapter.description, "해당 단원의 강의 슬라이드입니다."),
    );

    const footer = createElement("div", "chapter-footer");
    const slides = numericValue(chapter.slides);
    footer.append(
      createElement(
        "span",
        "chapter-slide-count",
        slides ? `${formatNumber(slides)} slides` : href ? "슬라이드" : "준비 중",
      ),
    );

    const footerLinks = createElement("span", "chapter-footer-links");
    const sourceHref = safeExternalHref(chapter.sourceUrl);
    if (sourceHref) {
      const source = createElement("a", "chapter-source", "원고 ↗");
      source.setAttribute("aria-label", `${textValue(chapter.label, "단원")} 원본 원고 보기 (새 탭)`);
      configureLink(source, sourceHref, { external: true, newTab: true });
      footerLinks.append(source);
    }
    footerLinks.append(createElement("span", "chapter-open", href ? "열기" : "예정"));
    footer.append(footerLinks);

    card.append(topLine, heading, description, footer);
    return card;
  }

  function createPlannedPanel(course) {
    const panel = createElement("div", "planned-panel");
    const inner = createElement("div");
    inner.append(
      createElement("div", "planned-icon"),
      createElement("strong", "", "새 교재를 준비하고 있습니다"),
      createElement(
        "p",
        "",
        textValue(
          course.summary,
          "단원 구성과 슬라이드가 완성되는 대로 이 서가에서 바로 만나볼 수 있습니다.",
        ),
      ),
    );
    panel.append(inner);
    return panel;
  }

  function createCourseHeading(course, headingId) {
    const heading = createElement("div", "course-heading");
    const titleGroup = createElement("div");
    titleGroup.append(
      createElement("p", "course-eyebrow", textValue(course.eyebrow, "Course collection")),
    );
    const title = createElement("h2", "", textValue(course.title, "이름 없는 교재"));
    title.id = headingId;
    titleGroup.append(title);

    const detail = createElement("div", "course-heading-detail");
    detail.append(
      createElement(
        "p",
        "course-description",
        textValue(course.description, "주차별 강의 슬라이드를 확인하세요."),
      ),
    );

    const sourceHref = safeExternalHref(course.sourceUrl);
    if (sourceHref) {
      const source = createElement("a", "course-source-link", "교재 원본 보기 ↗");
      source.setAttribute("aria-label", `${textValue(course.title, "교재")} 원본 보기 (새 탭)`);
      configureLink(source, sourceHref, { external: true, newTab: true });
      detail.append(source);
    }

    heading.append(titleGroup, detail);
    return heading;
  }

  function createCourseShelf(entry, index) {
    const course = entry.course;
    const chapters = entry.chapters;
    const courseId = textValue(course.id, `course-${index + 1}`);
    const headingId = `course-heading-${courseId.replace(/[^a-z0-9_-]/gi, "-")}`;
    const shelf = createElement("section", "course-shelf");
    shelf.setAttribute("aria-labelledby", headingId);
    shelf.style.setProperty("--course-accent", safeAccent(course.accent));
    shelf.style.setProperty("--shelf-index", String(index));

    const allCourses = getCourses();
    const courseNumber = Math.max(1, allCourses.indexOf(course) + 1);
    shelf.append(createCourseOverview(course, chapters, courseNumber));

    const content = createElement("div", "course-content");
    content.append(createCourseHeading(course, headingId));

    if (chapters.length) {
      const chapterGrid = createElement("div", "chapter-grid");
      chapters.forEach((chapter) => chapterGrid.append(createChapterCard(chapter, course)));
      content.append(chapterGrid);
    } else {
      content.append(createPlannedPanel(course));
    }

    shelf.append(content);
    return shelf;
  }

  function createEmptyState() {
    const empty = createElement("div", "empty-state");
    empty.append(
      createElement("div", "empty-state-mark", "⌕"),
      createElement("h3", "", "일치하는 교재가 없습니다"),
      createElement("p", "", "검색어를 줄이거나 다른 과목을 선택해 보세요."),
    );
    return empty;
  }

  function setResultSummary(entries) {
    const chapterCount = entries.reduce((total, entry) => total + entry.chapters.length, 0);
    const hasFilters = Boolean(state.query) || state.course !== "all";

    if (hasFilters) {
      elements.resultStatus.replaceChildren(
        document.createTextNode("검색 결과 "),
        createElement("strong", "", `${formatNumber(entries.length)}개 교재`),
        document.createTextNode(` · ${formatNumber(chapterCount)}개 단원`),
      );
    } else {
      elements.resultStatus.replaceChildren(
        createElement("strong", "", `${formatNumber(entries.length)}개 교재`),
        document.createTextNode(`에서 ${formatNumber(chapterCount)}개 단원을 열람할 수 있습니다.`),
      );
    }

    elements.resetFilters.hidden = !hasFilters;
  }

  function renderCatalog() {
    if (!state.catalog) return;

    const entries = filteredCourses();
    const fragment = document.createDocumentFragment();
    entries.forEach((entry, index) => fragment.append(createCourseShelf(entry, index)));

    elements.shelfList.replaceChildren(fragment.childNodes.length ? fragment : createEmptyState());
    elements.shelfList.setAttribute("aria-busy", "false");
    elements.clearSearch.hidden = !state.query;
    setResultSummary(entries);
  }

  function resetCatalogView(options) {
    const config = options || {};
    state.query = "";
    state.course = "all";
    elements.searchInput.value = "";
    updateFilterButtons();
    renderCatalog();
    if (config.focusSearch) elements.searchInput.focus();
  }

  function showError(error) {
    const errorState = createElement("div", "error-state");
    errorState.append(
      createElement("div", "error-state-mark", "!"),
      createElement("h3", "", "교재 목록을 불러오지 못했습니다"),
      createElement(
        "p",
        "",
        "네트워크 상태를 확인한 뒤 다시 시도해 주세요. 로컬 파일이라면 웹 서버를 통해 열어야 합니다.",
      ),
    );
    const retry = createElement("button", "", "다시 불러오기");
    retry.type = "button";
    retry.addEventListener("click", loadCatalog, { once: true });
    errorState.append(retry);

    elements.shelfList.replaceChildren(errorState);
    elements.shelfList.setAttribute("aria-busy", "false");
    elements.filters.replaceChildren();
    elements.resultStatus.textContent = "교재 목록을 표시할 수 없습니다.";
    elements.resetFilters.hidden = true;

    if (window.console && typeof window.console.error === "function") {
      console.error("교재 카탈로그 로드 실패:", error);
    }
  }

  async function loadCatalog() {
    elements.shelfList.setAttribute("aria-busy", "true");
    elements.resultStatus.textContent = "교재 목록을 불러오는 중입니다.";

    try {
      const response = await fetch(catalogUrl, {
        cache: "no-cache",
        headers: { Accept: "application/json" },
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      state.catalog = validateCatalog(await response.json());
      const courses = getCourses();
      setSiteInformation(state.catalog.site);
      setStatistics(courses);
      buildFilters(courses);
      renderCatalog();
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

  loadCatalog();
})();

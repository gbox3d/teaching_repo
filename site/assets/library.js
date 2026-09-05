(function () {
  "use strict";

  const libraryRoot = new URL("../", document.currentScript.src);
  const catalogUrl = new URL("catalog.json", libraryRoot);
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
  };

  const state = {
    catalog: null,
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
    return numberFormatter.format(numericValue(value));
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

  function filteredCourses() {
    const query = normaliseText(state.query);
    const weekQuery = query.match(/^0*(\d+)\s*주차$/);

    return getCourses().filter((course) => {
      if (!query) return true;
      const chapters = Array.isArray(course.chapters) ? course.chapters : [];
      if (weekQuery) {
        return chapters.some((chapter) => normaliseText(chapter.label) === `${Number(weekQuery[1])}주차`);
      }
      const searchText = [
        course.id, course.slug, course.title, course.eyebrow, course.description,
        ...chapters.flatMap((chapter) => [chapter.id, chapter.label, chapter.title, chapter.description]),
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

    const title = createElement("div", "book-title", textValue(course.title, "이름 없는 교재"));

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
    const title = textValue(course.title, "이름 없는 교재");
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
      "p", "portal-description", textValue(course.description, "주차별 강의 교재입니다."),
    );

    const chapters = Array.isArray(course.chapters) ? course.chapters : [];
    const slides = chapters.reduce((total, chapter) => total + numericValue(chapter.slides), 0);
    const metadata = createElement(
      "p", "portal-metadata", `${formatNumber(chapters.length)}개 단원 · ${formatNumber(slides)}장 슬라이드`,
    );
    const address = createElement("p", "portal-address", `/${course.slug}/`);
    content.append(eyebrow, heading, description, metadata, address);

    if (course.status === "published") {
      const link = createElement("a", "button button--primary course-open-link", "교재 열기 →");
      configureLink(link, `${course.slug}/`);
      link.setAttribute("aria-label", `${title} 교재 열기`);
      content.append(link);
    } else {
      content.append(createElement("span", "course-status course-status--planned", "교재 준비 중"));
    }

    card.append(cover, content);
    return card;
  }

  function createEmptyState() {
    const empty = createElement("div", "empty-state");
    empty.append(
      createElement("div", "empty-state-mark", "⌕"),
      createElement("h3", "", "일치하는 교재가 없습니다"),
      createElement("p", "", "검색어를 줄이거나 다른 제목과 주제로 검색해 보세요."),
    );
    return empty;
  }

  function setResultSummary(courses) {
    elements.resultStatus.replaceChildren(
      document.createTextNode(state.query ? "검색 결과 " : ""),
      createElement("strong", "", `${formatNumber(courses.length)}개 교재`),
      document.createTextNode(" · 수업에 맞는 교재를 열어 주세요."),
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
      state.query = elements.searchInput.value;
      setSiteInformation(state.catalog.site);
      setStatistics(courses);
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

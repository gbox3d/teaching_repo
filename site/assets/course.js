(function () {
  "use strict";

  const courseRoot = new URL("../", document.currentScript.src);
  const catalogUrl = new URL("catalog.json", courseRoot);
  const numberFormatter = new Intl.NumberFormat("ko-KR");
  const elements = {
    searchForm: document.querySelector("#search-form"),
    searchInput: document.querySelector("#chapter-search"),
    clearSearch: document.querySelector("#clear-search"),
    resetSearch: document.querySelector("#reset-search"),
    resultStatus: document.querySelector("#result-status"),
    chapterList: document.querySelector("#chapter-list"),
  };
  const state = { course: null, query: "" };

  function createElement(tagName, className, text) {
    const node = document.createElement(tagName);
    if (className) node.className = className;
    if (typeof text === "string") node.textContent = text;
    return node;
  }

  function textValue(value, fallback) {
    return typeof value === "string" && value.trim() ? value.trim() : fallback;
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
    link.setAttribute("aria-label", `${label} (새 탭)`);
    return link;
  }

  function createChapterCard(chapter) {
    const href = state.course.status === "published" ? safeHref(chapter.href, false) : "";
    const label = textValue(chapter.label, "단원");
    const title = textValue(chapter.title, "제목 없는 단원");
    const card = createElement("article", `chapter-card${href ? "" : " chapter-card--planned"}`);
    const topLine = createElement("div", "chapter-topline");
    topLine.append(createElement("span", "chapter-label", label));
    if (chapter.type === "special") topLine.append(createElement("span", "chapter-type", "특별 자료"));

    const heading = createElement("h3");
    heading.append(href ? newTabLink("chapter-link", title, href, `${label} ${title} 슬라이드 열기`) : createElement("span", "", title));
    const description = createElement("p", "", textValue(chapter.description, "해당 단원의 강의 슬라이드입니다."));
    const footer = createElement("div", "chapter-footer");
    const slides = Number(chapter.slides);
    const slideCount = Number.isFinite(slides) && slides > 0 ? `${numberFormatter.format(Math.round(slides))}장` : href ? "슬라이드" : "준비 중";
    footer.append(createElement("span", "chapter-slide-count", slideCount));

    const footerLinks = createElement("span", "chapter-footer-links");
    const sourceHref = safeHref(chapter.sourceUrl, true);
    if (sourceHref) footerLinks.append(newTabLink("chapter-source", "원고 ↗", sourceHref, `${label} 원본 원고 보기`));
    footerLinks.append(createElement("span", "chapter-open", href ? "열기" : "예정"));
    footer.append(footerLinks);
    card.append(topLine, heading, description, footer);
    return card;
  }

  function createEmptyState() {
    const panel = createElement("div", "empty-state");
    const searching = Boolean(normaliseText(state.query));
    panel.append(
      createElement("div", "empty-state-mark", searching ? "⌕" : ">_"),
      createElement("h3", "", searching ? "일치하는 단원이 없습니다" : "단원을 준비하고 있습니다"),
      createElement("p", "", searching ? "검색어를 줄이거나 다른 단원 제목으로 검색해 보세요." : textValue(state.course.summary, "이 교재의 강의 자료가 준비되면 목차에서 읽을 수 있습니다.")),
    );
    return panel;
  }

  function renderChapters() {
    if (!state.course) return;
    const query = normaliseText(state.query);
    const terms = query.split(" ").filter(Boolean);
    const requestedWeek = query.match(/^0*(\d+)\s*주차$/);
    const chapters = state.course.chapters.filter((chapter) => {
      if (requestedWeek) {
        const chapterWeek = normaliseText(chapter.label).match(/^0*(\d+)\s*주차$/);
        return chapterWeek && Number(chapterWeek[1]) === Number(requestedWeek[1]);
      }
      const text = normaliseText([chapter.id, chapter.label, chapter.title, chapter.description, chapter.type].filter(Boolean).join(" "));
      return terms.every((term) => text.includes(term));
    });
    const grid = createElement("div", "chapter-grid");
    chapters.forEach((chapter) => grid.append(createChapterCard(chapter)));
    elements.chapterList.replaceChildren(chapters.length ? grid : createEmptyState());
    elements.chapterList.setAttribute("aria-busy", "false");
    elements.clearSearch.hidden = !state.query;
    elements.resetSearch.hidden = !state.query;
    elements.resultStatus.textContent = query
      ? `검색 결과 ${numberFormatter.format(chapters.length)}개 단원 · 이 교재의 전체 ${numberFormatter.format(state.course.chapters.length)}개 단원`
      : `이 교재의 ${numberFormatter.format(chapters.length)}개 단원`;
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
      createElement("h3", "", "이 교재의 목차를 불러오지 못했습니다"),
      createElement("p", "", "연결 상태를 확인한 뒤 다시 시도해 주세요."),
    );
    const retry = createElement("button", "", "목차 다시 불러오기");
    retry.type = "button";
    retry.addEventListener("click", loadCatalog, { once: true });
    panel.append(retry);
    elements.chapterList.replaceChildren(panel);
    elements.chapterList.setAttribute("aria-busy", "false");
    elements.resultStatus.textContent = "이 교재의 목차를 표시할 수 없습니다.";
    elements.resetSearch.hidden = true;
    console.error("교재 목차 로드 실패:", error);
  }

  async function loadCatalog() {
    elements.chapterList.setAttribute("aria-busy", "true");
    elements.resultStatus.textContent = "단원 목차를 불러오는 중입니다.";
    try {
      const response = await fetch(catalogUrl, { cache: "no-cache", headers: { Accept: "application/json" } });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const course = await response.json();
      if (!course || typeof course !== "object" || !Array.isArray(course.chapters) || typeof course.title !== "string") {
        throw new Error("교재 catalog.json 형식이 올바르지 않습니다.");
      }
      state.course = course;
      state.query = elements.searchInput.value;
      renderChapters();
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

  loadCatalog();
})();

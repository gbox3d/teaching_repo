(function () {
  "use strict";

  const slides = Array.from(document.querySelectorAll(".deck-stage .marpit > svg"));
  const previous = document.querySelector('[data-action="previous"]');
  const next = document.querySelector('[data-action="next"]');
  const fullscreen = document.querySelector('[data-action="fullscreen"]');
  const counter = document.querySelector("[data-counter]");
  const progress = document.querySelector("[data-progress]");
  let current = 0;
  let touchStartX = null;
  let touchStartY = null;

  function indexFromHash() {
    const match = window.location.hash.match(/^#slide-(\d+)$/);
    if (!match) return 0;
    return Math.min(Math.max(Number(match[1]) - 1, 0), Math.max(slides.length - 1, 0));
  }

  function updateHash(replace) {
    const hash = `#slide-${current + 1}`;
    if (window.location.hash === hash) return;
    const method = replace ? "replaceState" : "pushState";
    window.history[method](null, "", hash);
  }

  // 본문이 아래 여백을 넘는 슬라이드는 글자 크기를 줄여 한 화면에 맞춘다.
  // 테마가 em 단위를 쓰므로 section 글자 크기만 줄이면 제목·표·코드가 함께 줄어든다.
  const MIN_FIT_RATIO = 0.62;

  function contentBottom(section) {
    let bottom = 0;
    Array.from(section.children).forEach(function (child) {
      if (child.tagName === "HEADER" || child.tagName === "FOOTER") return;
      bottom = Math.max(bottom, child.offsetTop + child.offsetHeight);
    });
    return bottom;
  }

  function fitSlide(slide) {
    const section = slide.querySelector("foreignObject > section");
    if (!section) return;
    section.style.fontSize = "";
    const style = window.getComputedStyle(section);
    const base = parseFloat(style.fontSize);
    const limit = section.clientHeight - parseFloat(style.paddingBottom) + 1;
    let size = base;
    while (contentBottom(section) > limit && size > base * MIN_FIT_RATIO) {
      size -= 1;
      section.style.fontSize = `${size}px`;
    }
  }

  // 웹 글꼴처럼 늦게 들어오는 자원이 요소 크기를 바꾸면 현재 슬라이드를 다시 맞춘다.
  const resizeObserver = typeof ResizeObserver === "function"
    ? new ResizeObserver(function () { fitSlide(slides[current]); })
    : null;

  function watchSlide(slide) {
    const section = slide.querySelector("foreignObject > section");
    if (!resizeObserver || !section) return;
    resizeObserver.disconnect();
    Array.from(section.children).forEach(function (child) { resizeObserver.observe(child); });
  }

  function show(index, options) {
    if (!slides.length) return;
    const settings = options || {};
    current = Math.min(Math.max(index, 0), slides.length - 1);
    slides.forEach(function (slide, slideIndex) {
      const active = slideIndex === current;
      slide.classList.toggle("is-active", active);
      slide.setAttribute("aria-hidden", String(!active));
      if (active) slide.setAttribute("aria-current", "page");
      else slide.removeAttribute("aria-current");
    });
    fitSlide(slides[current]);
    watchSlide(slides[current]);
    previous.disabled = current === 0;
    next.disabled = current === slides.length - 1;
    counter.value = `${current + 1} / ${slides.length}`;
    counter.textContent = counter.value;
    progress.style.width = `${((current + 1) / slides.length) * 100}%`;
    document.body.classList.add("deck-ready");
    updateHash(settings.replaceHash);
  }

  function isInteractiveTarget(target) {
    return target instanceof Element && Boolean(target.closest("a, button, input, textarea, select"));
  }

  function requestFullscreen() {
    if (document.fullscreenElement) {
      if (typeof document.exitFullscreen === "function") document.exitFullscreen();
      return;
    }
    if (typeof document.documentElement.requestFullscreen !== "function") return;
    document.documentElement.requestFullscreen().catch(function () {});
  }

  previous.addEventListener("click", function () {
    show(current - 1);
  });
  next.addEventListener("click", function () {
    show(current + 1);
  });
  fullscreen.addEventListener("click", requestFullscreen);

  document.addEventListener("fullscreenchange", function () {
    const active = Boolean(document.fullscreenElement);
    fullscreen.setAttribute("aria-label", active ? "전체 화면 종료" : "전체 화면 전환");
    fullscreen.textContent = active ? "×" : "⛶";
  });

  document.addEventListener("keydown", function (event) {
    if (isInteractiveTarget(event.target) && event.key !== "Escape") return;
    if (event.ctrlKey || event.metaKey || event.altKey) return;
    const actions = {
      ArrowRight: function () { show(current + 1); },
      ArrowDown: function () { show(current + 1); },
      PageDown: function () { show(current + 1); },
      " ": function () { show(current + (event.shiftKey ? -1 : 1)); },
      ArrowLeft: function () { show(current - 1); },
      ArrowUp: function () { show(current - 1); },
      PageUp: function () { show(current - 1); },
      Home: function () { show(0); },
      End: function () { show(slides.length - 1); },
      f: requestFullscreen,
      F: requestFullscreen,
    };
    const action = actions[event.key];
    if (!action) return;
    event.preventDefault();
    action();
  });

  document.addEventListener(
    "touchstart",
    function (event) {
      if (event.touches.length !== 1) return;
      touchStartX = event.touches[0].clientX;
      touchStartY = event.touches[0].clientY;
    },
    { passive: true },
  );

  document.addEventListener(
    "touchend",
    function (event) {
      if (touchStartX === null || touchStartY === null || event.changedTouches.length !== 1) return;
      const deltaX = event.changedTouches[0].clientX - touchStartX;
      const deltaY = event.changedTouches[0].clientY - touchStartY;
      touchStartX = null;
      touchStartY = null;
      if (Math.abs(deltaX) < 50 || Math.abs(deltaX) <= Math.abs(deltaY)) return;
      show(current + (deltaX < 0 ? 1 : -1));
    },
    { passive: true },
  );

  const languageSelect = document.querySelector("[data-language-select]");
  if (languageSelect) {
    languageSelect.addEventListener("change", function () {
      const option = languageSelect.selectedOptions[0];
      try {
        window.localStorage.setItem("teaching-language", languageSelect.value);
      } catch (_error) {}
      const target = new URL(option.dataset.file, window.location.href);
      target.hash = `slide-${current + 1}`;
      window.location.href = target.href;
    });
  }

  window.addEventListener("hashchange", function () {
    const requested = indexFromHash();
    if (requested !== current) show(requested, { replaceHash: true });
  });

  show(indexFromHash(), { replaceHash: true });
})();

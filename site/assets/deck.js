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

  window.addEventListener("hashchange", function () {
    const requested = indexFromHash();
    if (requested !== current) show(requested, { replaceHash: true });
  });

  show(indexFromHash(), { replaceHash: true });
})();

(function () {
  function revealHero() {
    var hero = document.querySelector("[data-hero]");
    if (!hero) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      hero.classList.add("is-ready");
      return;
    }

    window.requestAnimationFrame(function () {
      hero.classList.add("is-ready");
    });
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(revealHero);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", revealHero, { once: true });
  } else {
    revealHero();
  }
})();

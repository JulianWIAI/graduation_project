/* layout.js — misst die tatsaechliche Hoehe von Kopf- und Fusszeile und legt
 * sie als CSS-Variablen (--topbar-h, --footer-h) auf :root ab.
 * So passen sich Bereiche mit fester Bildschirmhoehe (z. B. Generate-Seite)
 * automatisch an, wenn das Menue in eine zweite Zeile umbricht. */
(function () {
  const root = document.documentElement;
  const parts = { "--topbar-h": ".topbar", "--footer-h": ".footer" };

  function update() {
    for (const [cssVar, selector] of Object.entries(parts)) {
      const el = document.querySelector(selector);
      if (el) root.style.setProperty(cssVar, el.offsetHeight + "px");
    }
  }

  update();
  if ("ResizeObserver" in window) {
    const ro = new ResizeObserver(update);
    Object.values(parts).forEach(sel => {
      const el = document.querySelector(sel);
      if (el) ro.observe(el);
    });
  } else {
    window.addEventListener("resize", update);
  }
})();

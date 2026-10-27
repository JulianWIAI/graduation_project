/* nav.js — Verhalten der Kopfzeile:
 *  - Dropdowns (<details class="menu">) schliessen bei Klick ausserhalb,
 *    mit Escape und wenn ein anderes Dropdown geoeffnet wird.
 *  - Menue-Schalter (☰) klappt die Navigation auf schmalen Fenstern auf/zu. */
(function () {
  const menus = Array.from(document.querySelectorAll("details.menu"));

  function closeAll(except) {
    menus.forEach(m => { if (m !== except) m.removeAttribute("open"); });
  }

  menus.forEach(m => m.addEventListener("toggle", () => { if (m.open) closeAll(m); }));

  document.addEventListener("click", e => {
    if (!e.target.closest("details.menu")) closeAll(null);
  });

  document.addEventListener("keydown", e => {
    if (e.key === "Escape") closeAll(null);
  });

  const toggle = document.querySelector(".nav-toggle");
  const topbar = document.querySelector(".topbar");
  if (toggle && topbar) {
    toggle.addEventListener("click", () => {
      const open = topbar.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
})();

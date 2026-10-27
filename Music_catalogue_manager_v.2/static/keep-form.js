/* keep-form.js — behaelt Formulareingaben beim Sprachwechsel.
 *
 * Ein Klick auf DE/EN/FR laedt die Seite neu, dabei wuerden alle Felder
 * geleert. Felder mit dem Attribut data-keep werden vorher kurz im Browser
 * (sessionStorage, nur dieser Tab) gemerkt und nach dem Neuladen wieder
 * eingesetzt. Passwortfelder werden grundsaetzlich NIE gespeichert.
 *
 * Links mit dem Attribut data-keep-carry nehmen die Eingaben auf die
 * Zielseite mit (z. B. E-Mail von "Anmelden" zu "Passwort vergessen"). */
(function () {
  const keyFor = path => "keepForm:" + path;
  const KEY = keyFor(location.pathname);
  const fields = () =>
    Array.from(document.querySelectorAll("input[data-keep]"))
      .filter(el => el.type !== "password" && el.name);

  // Wiederherstellen (einmalig) und danach sofort wieder entfernen
  try {
    const saved = JSON.parse(sessionStorage.getItem(KEY) || "null");
    sessionStorage.removeItem(KEY);
    if (saved) fields().forEach(el => { if (saved[el.name] && !el.value) el.value = saved[el.name]; });
  } catch (e) { /* Speicher nicht verfuegbar: Seite funktioniert trotzdem */ }

  function remember(targetKey) {
    const data = {};
    fields().forEach(el => { if (el.value) data[el.name] = el.value; });
    try { sessionStorage.setItem(targetKey, JSON.stringify(data)); } catch (e) {}
  }

  // Sprachwechsel: dieselbe Seite wird neu geladen
  document.querySelectorAll(".lang-link").forEach(link =>
    link.addEventListener("click", () => remember(KEY)));

  // Weitergabe an eine andere Seite (Link mit data-keep-carry)
  document.querySelectorAll("a[data-keep-carry]").forEach(link =>
    link.addEventListener("click", () => remember(keyFor(new URL(link.href, location.href).pathname))));
})();

/* password-rules.js — Live-Checkliste fuer Passwortfelder.
 *
 * Ein Feld mit data-pw-rules="<id der Liste>" wird beim Tippen geprueft.
 * Die Liste (<ul>) enthaelt je Regel ein <li> mit data-min oder data-pattern;
 * erfuellte Regeln bekommen die Klasse "ok". Die Regeln kommen vom Server
 * (auth/password_policy.py) -- die endgueltige Pruefung macht ebenfalls der Server. */
(function () {
  document.querySelectorAll("input[data-pw-rules]").forEach(input => {
    const list = document.getElementById(input.dataset.pwRules);
    if (!list) return;
    const items = Array.from(list.querySelectorAll("li"));
    list.hidden = false;
    const hint = document.getElementById(input.dataset.pwRules + "-hint");
    if (hint) hint.hidden = true;               // Checkliste ersetzt den Hinweistext

    function check() {
      const v = input.value;
      items.forEach(li => {
        const ok = li.dataset.min ? v.length >= Number(li.dataset.min)
                                  : new RegExp(li.dataset.pattern).test(v);
        li.classList.toggle("ok", ok);
      });
    }
    input.addEventListener("input", check);
    check();
  });
})();

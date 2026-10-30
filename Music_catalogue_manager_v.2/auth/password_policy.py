"""
Passwort-Regeln fuer neu gesetzte Passwoerter (Registrierung, Passwort
vergessen, Passwort aendern). Beim Login wird nichts davon geprueft.

Alle Regeln sind hier als Konstanten einstellbar. Die Liste haeufiger
Passwoerter liegt in auth/common_passwords.txt (eine Zeile je Passwort,
Gross-/Kleinschreibung egal) und kann einfach erweitert werden.
"""

import pathlib
import re

from i18n import _

MIN_LENGTH = 10
REQUIRE_UPPER = True
REQUIRE_LOWER = True
REQUIRE_DIGIT = True
REQUIRE_SPECIAL = True

# Waehrend der Entwicklung: Admin-Konto von den Regeln ausnehmen, damit beim
# Testen kurze Passwoerter moeglich sind.
# TODO vor der Abgabe/Produktion auf False setzen!
ADMIN_EXEMPT = True

_COMMON_FILE = pathlib.Path(__file__).with_name("common_passwords.txt")


def _load_common():
    try:
        lines = _COMMON_FILE.read_text(encoding="utf-8").splitlines()
    except OSError:
        return frozenset()
    return frozenset(l.strip().lower() for l in lines if l.strip() and not l.startswith("#"))


COMMON_PASSWORDS = _load_common()


def applies_to(is_admin):
    """Gelten die Regeln fuer dieses Konto?"""
    return not (is_admin and ADMIN_EXEMPT)


# Zeichenarten-Regeln: (Schalter, Regex, Text). Dieselben Muster nutzt die
# Live-Checkliste im Browser (static/password-rules.js) -- nur hier pflegen.
def _char_rules():
    return [r for r in (
        (REQUIRE_UPPER, r"[A-ZÄÖÜ]", _("Großbuchstabe")),
        (REQUIRE_LOWER, r"[a-zäöüß]", _("Kleinbuchstabe")),
        (REQUIRE_DIGIT, r"[0-9]", _("Zahl")),
        (REQUIRE_SPECIAL, r"[^A-Za-z0-9ÄÖÜäöüß]", _("Sonderzeichen")),
    ) if r[0]]


def checklist():
    """Regeln fuer die Live-Checkliste: Liste von {label, pattern|min}."""
    rules = [{"label": _("Mindestens %(n)s Zeichen", n=MIN_LENGTH), "min": MIN_LENGTH}]
    rules += [{"label": label, "pattern": pattern} for _on, pattern, label in _char_rules()]
    return rules


def validate(password, email="", is_admin=False):
    """Liste der verletzten Regeln (leer = Passwort ist in Ordnung)."""
    if not applies_to(is_admin):
        return []
    errors = []
    if len(password) < MIN_LENGTH:
        errors.append(_("Mindestens %(n)s Zeichen", n=MIN_LENGTH))
    for _on, pattern, label in _char_rules():
        if not re.search(pattern, password):
            errors.append(label)
    if password.lower() in COMMON_PASSWORDS:
        errors.append(_("Dieses Passwort ist zu häufig und leicht zu erraten."))
    local = (email or "").split("@")[0].lower()
    if len(local) >= 3 and local in password.lower():
        errors.append(_("Das Passwort darf die E-Mail-Adresse nicht enthalten."))
    return errors


def message(errors):
    """Fehlermeldung fuer flash(): Ueberschrift und je Regel eine Zeile."""
    return _("Das Passwort erfüllt die Anforderungen nicht:") + "\n" + "\n".join("• " + e for e in errors)


def hint():
    """Kurzer Hinweistext (ohne JavaScript sichtbar)."""
    return _("Mindestens %(n)s Zeichen mit Groß- und Kleinbuchstaben, Zahl und Sonderzeichen.",
             n=MIN_LENGTH)

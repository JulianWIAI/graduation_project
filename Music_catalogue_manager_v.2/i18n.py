"""
Sprachumschaltung (Deutsch / Englisch / Franzoesisch) -- ohne Zusatzbibliothek.

Prinzip (wie gettext): Der DEUTSCHE Originaltext ist zugleich der Schluessel.
    _("Einstellungen gespeichert.")
schlaegt den Text in translations.py nach; fehlt dort ein Eintrag, erscheint
einfach der deutsche Text. Eine vergessene Uebersetzung kann die Anwendung
also nie zum Absturz bringen.

Die gewaehlte Sprache liegt in einem Cookie ("lang"). Dadurch funktioniert die
Auswahl schon VOR dem Login (Anmelde-/Registrierseite) und bleibt ueber
Logout und Browser-Neustart hinweg erhalten.

Verwendung:
    Python     from i18n import _            flash(_("Text %(n)s", n=3))
    Templates  {{ _('Text') }}               (wird in init_app registriert)
    JavaScript t('Text {n}', {n: 3})         (siehe templates/base.html)
"""

from flask import has_request_context, redirect, request, url_for
from markupsafe import Markup

from translations import JS, TRANSLATIONS

LANGUAGES = {"de": "Deutsch", "en": "English", "fr": "Français"}
DEFAULT_LANGUAGE = "de"
COOKIE_NAME = "lang"
COOKIE_MAX_AGE = 365 * 24 * 3600   # 1 Jahr


def get_lang():
    """Aktive Sprache des Requests; ausserhalb eines Requests (CLI) Deutsch."""
    if has_request_context():
        lang = request.cookies.get(COOKIE_NAME)
        if lang in LANGUAGES:
            return lang
    return DEFAULT_LANGUAGE


def _(text, **params):
    """Uebersetzt 'text' in die aktive Sprache. Platzhalter: %(name)s."""
    text = TRANSLATIONS.get(get_lang(), {}).get(text, text)
    return text % params if params else text


def _html(text, **params):
    """
    Variante fuer Templates: Der Text selbst darf HTML enthalten (<strong>,
    &amp; ...), weil er aus unserem Quellcode stammt. Eingesetzte Parameter
    werden dagegen von Markup automatisch escaped (Schutz vor XSS).
    """
    text = Markup(TRANSLATIONS.get(get_lang(), {}).get(text, text))
    return text % params if params else text


def init_app(app):
    """Registriert Template-Funktion, Template-Variablen und die Umschalt-Route."""
    app.jinja_env.globals["_"] = _html

    @app.context_processor
    def _inject():
        lang = get_lang()
        return {"lang": lang, "languages": LANGUAGES, "js_i18n": JS.get(lang, {})}

    @app.route("/lang/<code>")
    def set_language(code):
        resp = redirect(request.referrer or url_for("dashboard"))
        if code in LANGUAGES:
            resp.set_cookie(COOKIE_NAME, code, max_age=COOKIE_MAX_AGE, samesite="Lax")
        return resp

"""
Katalog- & Lizenzverwaltung -- Flask-Anwendung (Einstiegspunkt).

Ergaenzendes kaufmaennisches Modul zum Musikproduktions-Gesamtpaket
(Music Architect V7 + SBS-Synth Master). Koppelt read-only an deren
Ausgabeordner, verwaltet Katalog & Lizenzen, rechnet die Wirtschaftlichkeit
und fuehrt ein Audit-Protokoll.

Start:  python main.py     ->  http://127.0.0.1:5000
"""

import csv
import io
import math
import os
import pathlib
import secrets
from datetime import timedelta

from flask import (Flask, abort, flash, redirect, render_template, request,
                   Response, send_file, url_for)
from flask_login import LoginManager, login_required, current_user
from flask_session import Session

import config
import i18n
from i18n import _
from db import database as db
from commerce import billing
from commerce import economics
from commerce import gateway
from commerce import licensing
from commerce import quota
from commerce import tokens
from commerce.token_shop import tokens_bp
from catalog import scanner
from catalog import watermark_reader
from db.demo_data import generate as generate_demo
from auth.auth import auth_bp, User, lock_end, set_login_state
from beatgen.generate import generate_bp
from auth.rbac import require_admin
from catalog.sample_upload import sample_upload_bp
from catalog.stats import stats_bp



def _secret_key():
    """
    Schluessel zum Signieren der Sitzungs-Cookies. Er steht bewusst NICHT im
    Quelltext: Er kommt aus der Umgebungsvariable SBS_SECRET_KEY; fehlt sie, wird
    einmalig einer erzeugt und in instance/secret_key abgelegt (nicht in Git).
    """
    if os.environ.get("SBS_SECRET_KEY"):
        return os.environ["SBS_SECRET_KEY"]
    path = pathlib.Path(config.DB_PATH).parent / "secret_key"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(secrets.token_hex(32))
        path.chmod(0o600)
    return path.read_text().strip()


app = Flask(__name__)
app.secret_key = _secret_key()


@app.context_processor
def _inject_brand():
    """Stellt Name und Logo der Suite allen Templates als `brand` bereit."""
    return {"brand": {"name": config.BRAND_NAME, "logo_mark": config.BRAND_LOGO_MARK}}

# --- Serverseitige Session-Konfiguration ------------------------------------
# Cookie-basierte Sessions sind auf ~4 KB begrenzt — zu klein fuer Audio-Pfade.
# Flask-Session speichert Sitzungsdaten auf dem Dateisystem, kein Groessenlimit.
_session_dir = pathlib.Path(__file__).parent / "flask_session"
_session_dir.mkdir(exist_ok=True)
app.config["SESSION_TYPE"]             = "filesystem"
app.config["SESSION_FILE_DIR"]         = str(_session_dir)
# Permanent=True damit die Session einen Browser-Neustart ueberlebt (Mac-Kompatibilitaet).
app.config["SESSION_PERMANENT"]        = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)
app.config["SESSION_USE_SIGNER"]       = True   # Session-ID im Cookie signieren
app.config["SESSION_FILE_THRESHOLD"]   = 500    # max. Anzahl gespeicherter Session-Dateien
Session(app)

# --- Flask-Login setup ------------------------------------------------------

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"
login_manager.login_message = "Bitte melden Sie sich an, um auf diese Seite zuzugreifen."
login_manager.login_message_category = "error"
login_manager.localize_callback = _      # Login-Hinweis in der gewaehlten Sprache


@login_manager.user_loader
def load_user(user_id):
    return User.load(int(user_id))


# --- Blueprints -------------------------------------------------------------

app.register_blueprint(auth_bp)
app.register_blueprint(generate_bp)
app.register_blueprint(sample_upload_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(tokens_bp)
i18n.init_app(app)                       # Sprachumschaltung DE / EN / FR

# Datenbank beim Import initialisieren (idempotent).
db.init_db()
app.teardown_appcontext(db.close_request_conns)   # haengende Verbindungen schliessen


# --- Root redirect ----------------------------------------------------------

@app.route("/")
def dashboard():
    """Redirect to /generate when logged in, otherwise to login."""
    if current_user.is_authenticated:
        return redirect(url_for("generate.generate_page"))
    return redirect(url_for("auth.login"))


@app.route("/dashboard")
@login_required
@require_admin
def dashboard_view():
    metrics = economics.compute()
    return render_template("dashboard.html", m=metrics, tiers=config.DEFAULT_TIERS)


# --- Katalog ----------------------------------------------------------------

@app.route("/catalog")
@login_required
@require_admin
def catalog():
    genre = request.args.get("genre", "")
    status = request.args.get("status", "")
    query = "SELECT * FROM tracks WHERE 1=1"
    params = []
    if genre:
        query += " AND genre = ?"
        params.append(genre)
    if status:
        query += " AND status = ?"
        params.append(status)
    query += " ORDER BY genre, title"

    conn = db.get_conn()
    tracks = conn.execute(query, params).fetchall()
    genres = [r["genre"] for r in conn.execute(
        "SELECT DISTINCT genre FROM tracks ORDER BY genre").fetchall()]
    conn.close()
    # Wasserzeichen wirklich pruefen: Pruefsumme muss zum Dateinamen passen.
    verified = {t["id"] for t in tracks
                if watermark_reader.hash_matches(t["source_midi"], t["watermark_hash"])}
    return render_template("catalog.html", tracks=tracks, genres=genres, verified=verified,
                           sel_genre=genre, sel_status=status)


@app.route("/track/<int:track_id>")
@login_required
@require_admin
def track_detail(track_id):
    conn = db.get_conn()
    track = conn.execute("SELECT * FROM tracks WHERE id = ?", (track_id,)).fetchone()
    if not track:
        conn.close()
        flash(_("Track nicht gefunden."), "error")
        return redirect(url_for("catalog"))
    exports = conn.execute(
        "SELECT * FROM exports WHERE track_id = ? ORDER BY tier", (track_id,)
    ).fetchall()
    lics = conn.execute(
        "SELECT * FROM licenses WHERE track_id = ? ORDER BY id DESC", (track_id,)
    ).fetchall()
    # Beats aus dem Web-Generator (nur sie haben user_id) gehen beim ersten Export
    # an den Kunden -- ohne Lizenz. Wer, und ob Kontingent oder Token: Protokoll.
    customer = None
    if track["user_id"]:
        customer = conn.execute(
            "SELECT u.email, u.name, ("
            "  SELECT json_extract(e.details, '$.used_token') FROM audit_log s"
            "  JOIN audit_log e ON e.event = 'EXPORT'"
            "   AND e.entity_id = json_extract(s.details, '$.audio_uuid')"
            "  WHERE s.event = 'EXPORT_SAVE' AND s.entity = 'track' AND s.entity_id = ?"
            ") AS used_token FROM users u WHERE u.id = ?",
            (str(track_id), track["user_id"])).fetchone()
    conn.close()
    # Preise fuer die Verkaufsmaske.
    tiers = {k: {**v, "price": licensing.get_price(k)}
             for k, v in config.DEFAULT_TIERS.items()}
    users = quota.list_users()
    return render_template("track_detail.html", track=track, exports=exports,
                           licenses=lics, tiers=tiers, users=users, customer=customer)


# --- Lizenz verkaufen -------------------------------------------------------

@app.route("/license/sell", methods=["POST"])
@login_required
@require_admin
def sell():
    track_id = int(request.form["track_id"])
    tier = request.form["tier"]
    buyer = request.form.get("buyer_name", "").strip()
    email = request.form.get("buyer_email", "").strip()
    notes = request.form.get("notes", "").strip()
    buyer_user = request.form.get("buyer_user", "").strip()
    user_id = int(buyer_user) if buyer_user.isdigit() else None
    try:
        lid, warning = licensing.sell_license(
            track_id, tier, buyer_name=buyer, buyer_email=email, notes=notes,
            user_id=user_id)
        if warning:
            flash(warning, "warning")
        return redirect(url_for("checkout", license_id=lid))
    except licensing.LicenseError as exc:
        flash(str(exc), "error")
        return redirect(url_for("track_detail", track_id=track_id))


# --- Checkout & Zahlung (simuliert) -----------------------------------------

@app.route("/checkout/<int:license_id>")
@login_required
@require_admin
def checkout(license_id):
    lic = billing.get_license(license_id)
    if not lic:
        flash(_("Bestellung nicht gefunden."), "error")
        return redirect(url_for("catalog"))
    ctx = billing.invoice_context("license", lic)
    return render_template("checkout.html", lic=lic, ctx=ctx)


@app.route("/license/<int:license_id>/pay", methods=["POST"])
@login_required
@require_admin
def license_pay(license_id):
    ok, err = billing.pay_license(license_id)
    flash(_("Zahlung bestätigt — die Lizenz ist bezahlt.") if ok else err,
          "success" if ok else "error")
    return redirect(url_for("invoice", license_id=license_id))


@app.route("/license/<int:license_id>/cancel", methods=["POST"])
@login_required
@require_admin
def license_cancel(license_id):
    lic = billing.get_license(license_id)
    track_id = lic["track_id"] if lic else None
    ok, err = billing.cancel_license(license_id)
    flash(_("Bestellung storniert, Track wieder freigegeben.") if ok else err,
          "success" if ok else "error")
    return redirect(url_for("track_detail", track_id=track_id) if track_id
                    else url_for("licenses"))


@app.route("/invoice/<int:license_id>")
@login_required
@require_admin
def invoice(license_id):
    lic = billing.get_license(license_id)
    if not lic:
        flash(_("Rechnung nicht gefunden."), "error")
        return redirect(url_for("licenses"))
    ctx = billing.invoice_context("license", lic)
    return render_template("invoice.html", ctx=ctx)


@app.route("/licenses")
@login_required
@require_admin
def licenses():
    rows = licensing.list_licenses()
    return render_template("licenses.html", licenses=rows)


# --- Wirtschaftlichkeit -----------------------------------------------------

@app.route("/economics")
@login_required
@require_admin
def economics_view():
    metrics = economics.compute()
    settings = db.get_all_settings()
    return render_template("economics.html", m=metrics, s=settings,
                           tiers=config.DEFAULT_TIERS)


# --- Einstellungen ----------------------------------------------------------

@app.route("/settings", methods=["GET", "POST"])
@login_required
@require_admin
def settings_view():
    if request.method == "POST":
        # Pfade + Kostenannahmen + Preise speichern.
        keys = ["catalog_dir", "export_dir", "dev_hours", "hourly_rate",
                "tooling_cost", "cost_per_track", "music_architect_cmd",
                "limit_free", "limit_subscriber", "discount_pct",
                "seller_name", "vat_pct", "sub_price_month",
                "token_price_basic", "token_price_subscriber"]
        keys += [f"price_{k}" for k in config.DEFAULT_TIERS]
        # Zahlenfelder pruefen: ein leeres Limit legt sonst Generator und Tarifseite lahm.
        clean = {}
        numeric = ["dev_hours", "hourly_rate", "tooling_cost", "cost_per_track",
                   "sub_price_month"] + [f"price_{k}" for k in config.DEFAULT_TIERS]
        for key in numeric + ["limit_free", "limit_subscriber", "discount_pct", "vat_pct"]:
            if key not in request.form:
                continue
            try:
                value = float(request.form[key].replace(",", "."))
            except ValueError:
                value = -1
            if (not math.isfinite(value) or value < 0 or (key.startswith("limit_") and value != int(value))
                    or (key.endswith("_pct") and value > 100)):
                flash(_("Bitte alle Zahlenfelder ausfüllen: Werte ab 0, Prozente höchstens "
                        "100, Limits als ganze Zahl.") + " "
                      + _("Einstellungen wurden nicht gespeichert."), "error")
                return redirect(url_for("settings_view"))
            clean[key] = request.form[key].replace(",", ".")
        # Token-Preise vor dem Speichern pruefen: Abo muss guenstiger sein.
        if "token_price_basic" in request.form or "token_price_subscriber" in request.form:
            current = tokens.get_prices()
            err = tokens.validate_prices(
                request.form.get("token_price_basic", current["basic"]),
                request.form.get("token_price_subscriber", current["subscriber"]))
            if err:
                flash(err + " " + _("Einstellungen wurden nicht gespeichert."), "error")
                return redirect(url_for("settings_view"))
        changed = {}
        for key in keys:
            if key in request.form:
                value = clean.get(key, request.form[key])
                db.set_setting(key, value)
                changed[key] = value
        db.log_event("SETTINGS_CHANGED", "settings", None, changed)
        flash(_("Einstellungen gespeichert."), "success")
        return redirect(url_for("settings_view"))

    settings = db.get_all_settings()
    all_users = quota.list_users()
    return render_template("settings.html", s=settings, tiers=config.DEFAULT_TIERS,
                           all_users=all_users)


# --- Aktionen: Scan & Demo --------------------------------------------------

@app.route("/scan", methods=["POST"])
@login_required
@require_admin
def scan():
    result = scanner.scan_all()
    cat, exp = result["catalog"], result["exports"]
    if cat.get("error"):
        flash(cat["error"], "error")
    else:
        flash(_("Katalog gescannt: %(added)s neu, %(updated)s aktualisiert "
                "(%(scanned)s Dateien).", added=cat["added"], updated=cat["updated"],
                scanned=cat["scanned"]), "success")
    if exp.get("error"):
        flash(exp["error"], "error")
    else:
        flash(_("Exporte gescannt: %(linked)s verknuepft, %(unmatched)s ohne Zuordnung.",
                linked=exp["linked"], unmatched=exp["unmatched"]), "success")
    return redirect(request.referrer or url_for("dashboard_view"))


@app.route("/load-demo", methods=["POST"])
@login_required
@require_admin
def load_demo():
    result = generate_demo()
    if result.get("error"):
        flash(result["error"], "error")
    else:
        flash(_("Demo-Daten erzeugt: %(midi)s MIDI-Dateien, %(exports)s Exporte. "
                "Jetzt 'Scannen' klicken.", midi=result["midi_created"],
                exports=result["exports_created"]), "success")
        db.log_event("DEMO_LOADED", "catalog", None, result)
    return redirect(request.referrer or url_for("dashboard_view"))


# --- Nutzer & Abo -----------------------------------------------------------

@app.route("/users")
@login_required
@require_admin
def users_view():
    users = quota.list_users()
    # Kontingent-Status je Nutzer fuer die Anzeige.
    rows = []
    for u in users:
        st = quota.quota_status(u)
        rows.append({"u": u, "st": st, "locked_until": lock_end(u)})
    limits = {"free": db.get_setting("limit_free"),
              "sub": db.get_setting("limit_subscriber"),
              "discount": db.get_setting("discount_pct")}
    terms = [{"months": m, "price": billing.subscription_price(m)}
             for m in config.SUBSCRIPTION_TERMS]
    token_prices = tokens.get_prices()
    return render_template("users.html", rows=rows, limits=limits, terms=terms,
                           token_prices=token_prices,
                           token_purchases=tokens.list_purchases(limit=20))


@app.route("/users/<int:user_id>/tokens", methods=["POST"])
@login_required
@require_admin
def users_tokens(user_id):
    """Admin: Tokens manuell gutschreiben (positiv) oder abziehen (negativ)."""
    try:
        tokens.admin_adjust(user_id, int(request.form.get("amount", "0")),
                            admin_id=current_user.id)
        flash(_("Token-Guthaben angepasst."), "success")
    except (ValueError, tokens.TokenError) as exc:
        flash(str(exc) or _("Ungueltiger Betrag."), "error")
    return redirect(url_for("users_view"))


@app.route("/users/<int:user_id>/unlock", methods=["POST"])
@login_required
@require_admin
def users_unlock(user_id):
    """Admin: Login-Sperre nach falschen Passwoertern vorzeitig aufheben."""
    set_login_state(user_id, 0)
    db.log_event("LOGIN_UNLOCKED", "user", user_id, {"by": current_user.id})
    flash(_("Konto entsperrt."), "success")
    return redirect(url_for("users_view"))


# --- Tarifwahl & Abo-Checkout -----------------------------------------------
# Kunden buchen und bezahlen nur ihr EIGENES Abo; Admins duerfen es fuer jeden.

def _own_subscription_or_404(sub_id):
    sub = billing.get_subscription(sub_id)
    if not sub or (sub["user_id"] != current_user.id and not current_user.is_admin):
        abort(404)   # fremde Bestellungen nicht preisgeben
    return sub


@app.route("/plan")
@login_required
def plan():
    """Tarifwahl Basis/Abo -- erste Seite nach der Registrierung."""
    user = quota.get_user(current_user.id)
    terms = [{"months": m, "price": billing.subscription_price(m)}
             for m in config.SUBSCRIPTION_TERMS]
    limits = {"free": db.get_setting("limit_free"),
              "sub": db.get_setting("limit_subscriber"),
              "discount": db.get_setting("discount_pct")}
    return render_template("plan.html", user=user, terms=terms, limits=limits,
                           active=quota.is_active_subscriber(user),
                           notice=quota.subscription_notice(user),
                           status=quota.quota_status(user),
                           token_prices=tokens.get_prices())


@app.route("/subscription/start", methods=["POST"])
@login_required
def subscription_start():
    # Nur Admins duerfen fuer andere Nutzer buchen -- Kunden immer fuer sich selbst.
    for_other = current_user.is_admin and "user_id" in request.form
    user_id = request.form.get("user_id", type=int) if for_other else current_user.id
    back = url_for("users_view") if for_other else url_for("plan")
    term = request.form.get("term_months", 1, type=int)
    sub_id, err = billing.create_subscription(user_id, term)
    if err:
        flash(err, "error")
        return redirect(back)
    return redirect(url_for("subscription_checkout", sub_id=sub_id))


@app.route("/subscription/checkout/<int:sub_id>")
@login_required
def subscription_checkout(sub_id):
    sub = _own_subscription_or_404(sub_id)
    ctx = billing.invoice_context("subscription", sub)
    return render_template("checkout.html", sub=sub, ctx=ctx)


@app.route("/subscription/<int:sub_id>/pay", methods=["POST"])
@login_required
def subscription_pay(sub_id):
    _own_subscription_or_404(sub_id)
    ok, err = billing.pay_subscription(sub_id)
    flash(_("Abo bezahlt und aktiviert.") if ok else err, "success" if ok else "error")
    return redirect(url_for("subscription_invoice", sub_id=sub_id))


@app.route("/subscription/invoice/<int:sub_id>")
@login_required
def subscription_invoice(sub_id):
    sub = _own_subscription_or_404(sub_id)
    ctx = billing.invoice_context("subscription", sub)
    return render_template("invoice.html", ctx=ctx)


@app.route("/users/add", methods=["POST"])
@login_required
@require_admin
def users_add():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    is_sub = request.form.get("is_subscriber") == "on"
    if not name:
        flash(_("Bitte einen Namen angeben."), "error")
    else:
        quota.add_user(name, email, is_sub)
        flash(_("Nutzer '%(name)s' angelegt (Abo).", name=name) if is_sub
              else _("Nutzer '%(name)s' angelegt.", name=name), "success")
    return redirect(url_for("users_view"))


@app.route("/generate-legacy", methods=["POST"])
@login_required
@require_admin
def generate_track():
    user_id = int(request.form["user_id"])
    try:
        count = max(1, int(request.form.get("count", "1")))
    except ValueError:
        count = 1
    res = gateway.run_generation(user_id, count=count)
    if res["ok"]:
        st = res["status"]
        msg = _("[%(mode)s] %(count)s Track(s) fuer %(user)s erzeugt. "
                "Diesen Monat %(used)s/%(limit)s (noch %(remaining)s).",
                mode=res["mode"], count=res["count"], user=res["user"],
                used=st["used"], limit=st["limit"], remaining=st["remaining"])
        if res.get("tokens_used"):
            msg += " " + _("%(n)s Token(s) verbraucht.", n=res["tokens_used"])
        flash(msg + " " + _("Zum Uebernehmen: Scannen."), "success")
    else:
        flash(res["error"], "error")
    return redirect(request.referrer or url_for("users_view"))


# --- Audit-Protokoll --------------------------------------------------------

@app.route("/audit")
@login_required
@require_admin
def audit():
    q = request.args.get("q", "").strip()
    return render_template("audit.html", rows=db.get_audit_log(query=q), q=q)


@app.route("/audit.csv")
@login_required
@require_admin
def audit_csv():
    rows = db.get_audit_log(limit=100000, query=request.args.get("q", "").strip())
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=";")
    writer.writerow(["id", "zeitstempel", "ereignis", "objekt", "objekt_id", "details"])
    for r in rows:
        writer.writerow([r["id"], r["ts"], r["event"], r["entity"],
                         r["entity_id"], r["details"]])
    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=audit_protokoll.csv"},
    )


# --- DAW-Light Download -----------------------------------------------------

@app.route("/download")
@login_required
def download_page():
    dmg_available = pathlib.Path(config.DOWNLOADS_DIR, config.DAW_LIGHT_DMG).is_file()
    exe_available = pathlib.Path(config.DOWNLOADS_DIR, config.DAW_LIGHT_EXE).is_file()
    return render_template("download.html",
                           dmg_available=dmg_available,
                           exe_available=exe_available)


@app.route("/download/<platform>")
@login_required
def download_file(platform):
    if platform == "mac":
        filename = config.DAW_LIGHT_DMG
    elif platform == "windows":
        filename = config.DAW_LIGHT_EXE
    else:
        abort(404)
    filepath = pathlib.Path(config.DOWNLOADS_DIR, filename)
    if not filepath.is_file():
        flash(_("Datei nicht gefunden. Bitte wende dich an den Administrator."), "error")
        return redirect(url_for("download_page"))
    return send_file(filepath, as_attachment=True, download_name=filename)


# --- Jinja-Filter -----------------------------------------------------------

@app.template_filter("euro")
def euro(value):
    try:
        return f"{float(value):,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return "–"


@app.template_filter("datum")
def datum(value):
    """ISO-Zeitpunkt -> '16.10.2026, 12:25' (nur Datum, wenn keine Uhrzeit)."""
    text = str(value or "")
    if len(text) < 10:
        return text or "–"
    out = f"{text[8:10]}.{text[5:7]}.{text[:4]}"
    return f"{out}, {text[11:16]}" if len(text) >= 16 else out


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False, threaded=True)

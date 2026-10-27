"""
Authentifizierungs-Blueprint — Registrierung, Anmeldung, Abmeldung,
Passwort-Wiederherstellung (Sicherheitsfrage) und Admin-Passwort-Reset.

Verwendet Flask-Login fuer die Sitzungsverwaltung und Werkzeug fuer das
Passwort-Hashing. Die User-Klasse kapselt die SQLite-Zeile, damit die
Flask-Login-Mixins ohne ORM funktionieren.
"""

import secrets

from flask import (Blueprint, flash, redirect, render_template,
                   request, session, url_for)
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from auth import lockout
from auth.rbac import require_admin
from commerce import quota
from db import database as db
from i18n import _

auth_bp = Blueprint("auth", __name__)

# Sperr-Einstellungen (Fehlversuche, steigende Sperrdauer) stehen in auth/lockout.py.
MAX_FAILED_LOGINS = lockout.MAX_FAILED_ATTEMPTS


def _flash_locked(until):
    """Neutrale Sperrmeldung: nennt nur die Uhrzeit, ab der es wieder geht."""
    flash(_("Zu viele Fehlversuche. Bitte versuche es um %(time)s Uhr erneut.",
            time=until.strftime("%H:%M")), "error")

# --- User model -------------------------------------------------------------

class User(UserMixin):
    """Thin wrapper um eine users-Tabellenzeile fuer Flask-Login."""

    def __init__(self, row):
        self.id            = row["id"]
        self.email         = row["email"]
        self.password_hash = row["password_hash"]
        self.must_change_pw = bool(row["must_change_pw"]) if "must_change_pw" in row.keys() else False
        # Effektiver Tarif: 'pro' bei aktivem (nicht abgelaufenem) Abo, sonst 'free'.
        self.tier          = "pro" if quota.is_active_subscriber(row) else "free"
        # is_admin: 1 = voller Admin-Zugang, 0 = nur /generate und /stats.
        self.is_admin      = bool(row["is_admin"]) if "is_admin" in row.keys() else False

    def get_id(self):
        return str(self.id)

    @staticmethod
    def load(user_id: int):
        """Wird vom login_manager-user_loader-Callback in main.py aufgerufen."""
        conn = db.get_conn()
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        return User(row) if row else None


# --- Routen -----------------------------------------------------------------

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        security_question = request.form.get("security_question", "").strip()
        security_answer = request.form.get("security_answer", "").strip()

        if not email or not password:
            flash(_("E-Mail und Passwort sind erforderlich."), "error")
            return render_template("register.html")
        if password != confirm:
            flash(_("Passwörter stimmen nicht überein."), "error")
            return render_template("register.html")
        if not security_question or not security_answer:
            flash(_("Sicherheitsfrage und Antwort sind erforderlich."), "error")
            return render_template("register.html")
        if db.get_user_by_email(email):
            flash(_("Ein Konto mit dieser E-Mail-Adresse existiert bereits."), "error")
            return render_template("register.html")

        hashed = generate_password_hash(password)
        answer_hash = generate_password_hash(security_answer.lower())
        uid = db.create_user(email, hashed, security_question, answer_hash)
        db.log_event("USER_REGISTERED", "user", uid, {"email": email})

        row = db.get_user_by_email(email)
        login_user(User(row))
        # Neukunden waehlen direkt nach der Registrierung ihren Tarif (Basis/Abo).
        return redirect(url_for("plan"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        row = db.get_user_by_email(email)
        if not row or not row["password_hash"]:
            flash(_("Ungültige E-Mail oder falsches Passwort."), "error")
            return render_template("login.html")
        # Gesperrt (fuer diesen Nutzer an dieser IP): auch das richtige Passwort wird abgelehnt.
        until = lockout.active_lock(row["id"], lockout.KIND_LOGIN)
        if until:
            _flash_locked(until)
            return render_template("login.html")
        if not check_password_hash(row["password_hash"], password):
            until, _remaining = lockout.register_failure(row["id"], lockout.KIND_LOGIN)
            if until:
                db.log_event("LOGIN_LOCKED", "user", row["id"],
                             {"email": email, "ip": lockout.client_ip(), "until": until.isoformat()})
                _flash_locked(until)
            else:
                # Ohne Zaehler: sonst verraet die Meldung, dass das Konto existiert.
                flash(_("Ungültige E-Mail oder falsches Passwort."), "error")
            return render_template("login.html")

        lockout.reset(row["id"], lockout.KIND_LOGIN)
        login_user(User(row))

        # Muss das Passwort geaendert werden? (Admin-Reset)
        if row["must_change_pw"]:
            return redirect(url_for("auth.change_password"))

        next_page = request.args.get("next")
        # Nur Pfade dieser Seite zulassen -- "//x" und "/\x" fuehren Browser auf fremde Hosts.
        if next_page and (not next_page.startswith("/") or next_page[1:2] in ("/", "\\")):
            next_page = None
        # Laeuft das Abo bald aus oder ist es gerade abgelaufen, fuehrt der Login
        # zuerst auf die Tarifseite -- dort kann der Kunde verlaengern oder weitergehen.
        if not next_page and quota.subscription_notice(row):
            return redirect(url_for("plan"))
        return redirect(next_page or url_for("generate.generate_page"))

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


# --- Passwort vergessen (Sicherheitsfrage) ----------------------------------

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        row = db.get_user_by_email(email)
        if not row or not row["security_question"]:
            # Keine Information preisgeben, ob ein Konto existiert.
            flash(_("Falscher Benutzername"), "error")
            return render_template("forgot_password.html")
        # Token in der Session ablegen und weiterleiten.
        session["pw_reset_email"] = email
        return redirect(url_for("auth.forgot_password_question", email=email))
    return render_template("forgot_password.html")


@auth_bp.route("/forgot-password/<email>", methods=["GET", "POST"])
def forgot_password_question(email):
    row = db.get_user_by_email(email)
    if not row or not row["security_question"]:
        flash(_("Falscher Benutzername"), "error")
        return redirect(url_for("auth.forgot_password"))

    # Stellt sicher, dass nur der korrekte Ablauf hier ankommt.
    if session.get("pw_reset_email") != email:
        return redirect(url_for("auth.forgot_password"))

    # Sperr-Check in der Datenbank (nicht im Cookie -- Cookie-Loeschen hebt sie nicht auf).
    until = lockout.active_lock(row["id"], lockout.KIND_SECURITY_QUESTION)
    if until:
        _flash_locked(until)
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        answer = request.form.get("answer", "").strip()
        if check_password_hash(row["security_answer_hash"], answer.lower()):
            # Antwort korrekt: Reset-Token erzeugen.
            token = secrets.token_urlsafe(16)
            session["pw_reset_token"] = token
            lockout.reset(row["id"], lockout.KIND_SECURITY_QUESTION)
            return redirect(url_for("auth.reset_password", email=email, token=token))
        # Falsche Antwort.
        until, remaining = lockout.register_failure(row["id"], lockout.KIND_SECURITY_QUESTION)
        if until:
            db.log_event("SECURITY_QUESTION_LOCKED", "user", row["id"],
                         {"ip": lockout.client_ip(), "until": until.isoformat()})
            _flash_locked(until)
            return redirect(url_for("auth.forgot_password"))
        flash(_("Falsche Antwort") + " "
              + _("Noch %(n)s Versuch(e) bis zur Sperre.", n=remaining), "error")

    return render_template("forgot_password_question.html",
                           email=email,
                           question=row["security_question"])


@auth_bp.route("/reset-password/<email>/<token>", methods=["GET", "POST"])
def reset_password(email, token):
    # Token validieren.
    if (session.get("pw_reset_email") != email
            or session.get("pw_reset_token") != token):
        flash(_("Ungültige oder abgelaufene Sitzung."), "error")
        return redirect(url_for("auth.forgot_password"))

    row = db.get_user_by_email(email)
    if not row:
        flash(_("Falscher Benutzername"), "error")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        new_pw = request.form.get("new_password", "")
        confirm = request.form.get("confirm", "")
        if not new_pw:
            flash(_("Neues Passwort darf nicht leer sein."), "error")
            return render_template("reset_password.html", email=email, token=token)
        if new_pw != confirm:
            flash(_("Passwörter stimmen nicht überein."), "error")
            return render_template("reset_password.html", email=email, token=token)

        conn = db.get_conn()
        conn.execute("UPDATE users SET password_hash = ?, must_change_pw = 0 WHERE id = ?",
                     (generate_password_hash(new_pw), row["id"]))
        conn.commit()
        conn.close()
        db.log_event("PASSWORD_RESET", "user", row["id"], {"via": "security_question"})

        # Session-Tokens loeschen.
        session.pop("pw_reset_email", None)
        session.pop("pw_reset_token", None)
        # Identitaet per Sicherheitsfrage bestaetigt: alle Sperren des Kontos aufheben.
        lockout.unlock_user(row["id"])

        flash(_("Passwort erfolgreich geändert"), "success")
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", email=email, token=token)


# --- Erzwungene Passwortaenderung (nach Admin-Reset) ------------------------

@auth_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        new_pw = request.form.get("new_password", "")
        confirm = request.form.get("confirm", "")
        if not new_pw:
            flash(_("Neues Passwort darf nicht leer sein."), "error")
            return render_template("change_password.html")
        if new_pw != confirm:
            flash(_("Passwörter stimmen nicht überein."), "error")
            return render_template("change_password.html")

        conn = db.get_conn()
        conn.execute("UPDATE users SET password_hash = ?, must_change_pw = 0 WHERE id = ?",
                     (generate_password_hash(new_pw), current_user.id))
        conn.commit()
        conn.close()
        db.log_event("PASSWORD_CHANGED", "user", current_user.id, {"via": "forced_change"})

        flash(_("Passwort erfolgreich geändert"), "success")
        return redirect(url_for("generate.generate_page"))

    return render_template("change_password.html")


# --- Admin: Passwort-Reset --------------------------------------------------

@auth_bp.route("/admin/reset-password/<int:user_id>", methods=["POST"])
@login_required
@require_admin
def admin_reset_password(user_id):
    row = db.get_user_by_id(user_id)
    if not row:
        flash(_("Falscher Benutzername"), "error")
        return redirect(url_for("settings_view"))

    # 8-stelliges alphanumerisches Zufallspasswort (hex = 4 Byte = 8 Hex-Zeichen).
    temp_pw = secrets.token_hex(4)
    conn = db.get_conn()
    conn.execute(
        "UPDATE users SET password_hash = ?, must_change_pw = 1 WHERE id = ?",
        (generate_password_hash(temp_pw), user_id),
    )
    conn.commit()
    conn.close()
    db.log_event("ADMIN_PASSWORD_RESET", "user", user_id,
                 {"by_admin": current_user.id})

    flash(_("Das temporäre Passwort lautet:") + " " + temp_pw, "warning")
    return redirect(url_for("settings_view"))

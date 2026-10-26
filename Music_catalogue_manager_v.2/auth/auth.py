"""
Authentifizierungs-Blueprint — Registrierung, Anmeldung, Abmeldung.

Verwendet Flask-Login fuer die Sitzungsverwaltung und Werkzeug fuer das
Passwort-Hashing. Die User-Klasse kapselt die SQLite-Zeile, damit die
Flask-Login-Mixins ohne ORM funktionieren.
"""

from datetime import datetime, timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import UserMixin, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from commerce import quota
from db import database as db
from i18n import _

auth_bp = Blueprint("auth", __name__)

MAX_FAILED_LOGINS = 3                  # falsche Passwoerter in Folge bis zur Sperre
LOCK_DURATION = timedelta(hours=24)


def lock_end(row):
    """Ende einer laufenden Sperre als datetime, sonst None."""
    until = row["locked_until"]
    if until and datetime.fromisoformat(until) > datetime.now():
        return datetime.fromisoformat(until)
    return None


def set_login_state(user_id, failed, locked_until=None):
    conn = db.get_conn()
    conn.execute("UPDATE users SET failed_logins = ?, locked_until = ? WHERE id = ?",
                 (failed, locked_until.isoformat(timespec="seconds") if locked_until else None,
                  user_id))
    conn.commit()
    conn.close()


def _flash_locked(until):
    flash(_("Konto nach %(n)s falschen Passwoertern gesperrt bis %(until)s Uhr.",
            n=MAX_FAILED_LOGINS, until=until.strftime("%d.%m.%Y, %H:%M")), "error")

# --- User model -------------------------------------------------------------

class User(UserMixin):
    """Thin wrapper um eine users-Tabellenzeile fuer Flask-Login."""

    def __init__(self, row):
        self.id            = row["id"]
        self.email         = row["email"]
        self.password_hash = row["password_hash"]
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

        if not email or not password:
            flash(_("E-Mail und Passwort sind erforderlich."), "error")
            return render_template("register.html")
        if password != confirm:
            flash(_("Passwoerter stimmen nicht ueberein."), "error")
            return render_template("register.html")
        if db.get_user_by_email(email):
            flash(_("Ein Konto mit dieser E-Mail-Adresse existiert bereits."), "error")
            return render_template("register.html")

        hashed = generate_password_hash(password)
        uid = db.create_user(email, hashed)
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
            flash(_("Ungueltige E-Mail oder falsches Passwort."), "error")
            return render_template("login.html")
        # Gesperrt: auch das richtige Passwort wird abgelehnt.
        until = lock_end(row)
        if until:
            _flash_locked(until)
            return render_template("login.html")
        if not check_password_hash(row["password_hash"], password):
            failed = row["failed_logins"] + 1     # beim Sperren auf 0 gesetzt
            if failed >= MAX_FAILED_LOGINS:
                until = datetime.now() + LOCK_DURATION
                set_login_state(row["id"], 0, until)
                db.log_event("LOGIN_LOCKED", "user", row["id"], {"email": email})
                _flash_locked(until)
            else:
                set_login_state(row["id"], failed)
                flash(_("Ungueltige E-Mail oder falsches Passwort.") + " "
                      + _("Noch %(n)s Versuch(e) bis zur Sperre.", n=MAX_FAILED_LOGINS - failed),
                      "error")
            return render_template("login.html")

        if row["failed_logins"] or row["locked_until"]:
            set_login_state(row["id"], 0)
        login_user(User(row))
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

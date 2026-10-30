"""
Schutz vor Passwort-Raten (Login und Sicherheitsfrage).

Fehlversuche werden pro Kombination aus Nutzer, IP-Adresse und Vorgang
gezaehlt (Tabelle login_attempts). Dadurch sperrt sich ein Angreifer nur
selbst aus -- der echte Nutzer kann sich von seinem Geraet weiter anmelden.
Das schuetzt insbesondere das Admin-Konto vor gezieltem Aussperren, ohne
dass dort unbegrenzt geraten werden kann.

Die Sperrdauer steigt stufenweise (LOCK_STEPS). Nach LEVEL_RESET_AFTER ohne
neuen Fehlversuch beginnt die Zaehlung wieder bei der ersten Stufe.
"""

from datetime import datetime, timedelta

from flask import request

from db import database as db

# --- Einstellungen ----------------------------------------------------------
MAX_FAILED_ATTEMPTS = 3                       # Fehlversuche bis zur naechsten Sperrstufe
LOCK_STEPS = (timedelta(minutes=1),           # 1. Sperre
              timedelta(minutes=5),           # 2. Sperre
              timedelta(minutes=15),          # 3. Sperre
              timedelta(hours=1),             # 4. Sperre
              timedelta(hours=24))            # 5. und jede weitere Sperre
LEVEL_RESET_AFTER = timedelta(hours=24)       # Stufe verfaellt nach so langer Ruhe

KIND_LOGIN = "login"                          # Passwort bei der Anmeldung
KIND_SECURITY_QUESTION = "security_question"  # Antwort bei "Passwort vergessen"


def _now():
    return datetime.now()


def client_ip():
    """IP-Adresse der aktuellen Anfrage (hinter einem Proxy: ProxyFix verwenden)."""
    return request.remote_addr or "unknown"


def _row(conn, user_id, kind, ip):
    return conn.execute(
        "SELECT failed, level, locked_until, updated_at FROM login_attempts "
        "WHERE user_id = ? AND ip = ? AND kind = ?", (user_id, ip, kind)).fetchone()


def active_lock(user_id, kind):
    """Ende der laufenden Sperre fuer diesen Nutzer an dieser IP, sonst None."""
    conn = db.get_conn()
    row = _row(conn, user_id, kind, client_ip())
    conn.close()
    if row and row["locked_until"]:
        until = datetime.fromisoformat(row["locked_until"])
        if until > _now():
            return until
    return None


def register_failure(user_id, kind):
    """
    Zaehlt einen Fehlversuch. Rueckgabe: (gesperrt_bis, verbleibende_versuche).
    gesperrt_bis ist None, solange noch Versuche frei sind.
    """
    ip, now = client_ip(), _now()
    conn = db.get_conn()
    row = _row(conn, user_id, kind, ip)
    failed, level = (row["failed"], row["level"]) if row else (0, 0)
    if row and now - datetime.fromisoformat(row["updated_at"]) > LEVEL_RESET_AFTER:
        failed, level = 0, 0

    failed += 1
    locked_until = None
    if failed >= MAX_FAILED_ATTEMPTS:
        locked_until = now + LOCK_STEPS[min(level, len(LOCK_STEPS) - 1)]
        failed, level = 0, level + 1

    conn.execute(
        "INSERT INTO login_attempts (user_id, ip, kind, failed, level, locked_until, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(user_id, ip, kind) DO UPDATE SET failed = excluded.failed, "
        "level = excluded.level, locked_until = excluded.locked_until, "
        "updated_at = excluded.updated_at",
        (user_id, ip, kind, failed, level,
         locked_until.isoformat(timespec="seconds") if locked_until else None,
         now.isoformat(timespec="seconds")))
    conn.commit()
    conn.close()
    return locked_until, MAX_FAILED_ATTEMPTS - failed


def reset(user_id, kind):
    """Erfolg an dieser IP: Zaehler und Stufe zuruecksetzen."""
    conn = db.get_conn()
    conn.execute("DELETE FROM login_attempts WHERE user_id = ? AND ip = ? AND kind = ?",
                 (user_id, client_ip(), kind))
    conn.commit()
    conn.close()


def user_lock_end(user_id):
    """Spaeteste laufende Sperre des Nutzers ueber alle IPs (fuer die Nutzerverwaltung)."""
    conn = db.get_conn()
    row = conn.execute("SELECT MAX(locked_until) AS m FROM login_attempts "
                       "WHERE user_id = ? AND locked_until > ?",
                       (user_id, _now().isoformat(timespec="seconds"))).fetchone()
    conn.close()
    return datetime.fromisoformat(row["m"]) if row and row["m"] else None


def unlock_user(user_id):
    """Alle Sperren und Zaehler des Nutzers aufheben (Admin, Passwort-Reset)."""
    conn = db.get_conn()
    conn.execute("DELETE FROM login_attempts WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

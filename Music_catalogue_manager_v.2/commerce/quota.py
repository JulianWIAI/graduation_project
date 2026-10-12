"""
Abo-/Freemium-Logik: Nutzerverwaltung, Nutzungszaehlung und Monatslimit.

Das Kontingent gilt je Monats-Zeitraum (siehe quota_period): fuer Basis-Nutzer
der Kalendermonat, fuer Abonnenten der Abo-Monat ab dem Abschlussdatum. Es wird
nichts zurueckgesetzt -- gezaehlt wird nur, was im laufenden Zeitraum liegt.
Abonnenten haben ein hoeheres Limit als Basis-Nutzer; beide Limits sind in den
Einstellungen konfigurierbar (Standard 3 Basis / 10 Abo).
"""

from datetime import date, datetime, timedelta

import config
from commerce import billing
from db import database as db


# --- Nutzer -----------------------------------------------------------------

def list_users():
    conn = db.get_conn()
    rows = conn.execute("SELECT * FROM users ORDER BY name").fetchall()
    conn.close()
    return rows


def get_user(user_id):
    conn = db.get_conn()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return row


def get_user_by_name(name):
    conn = db.get_conn()
    row = conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone()
    conn.close()
    return row


def add_user(name, email=None, is_subscriber=False):
    conn = db.get_conn()
    cur = conn.execute(
        "INSERT INTO users (name, email, is_subscriber, created_at) VALUES (?, ?, ?, ?)",
        (name, email or None, 1 if is_subscriber else 0,
         datetime.now().isoformat(timespec="seconds")),
    )
    uid = cur.lastrowid
    conn.commit()
    conn.close()
    db.log_event("USER_ADDED", "user", uid,
                 {"name": name, "is_subscriber": bool(is_subscriber)})
    return uid


# --- Limits & Nutzung -------------------------------------------------------

def is_active_subscriber(user, on_day=None):
    """True, wenn der Nutzer ein Abo hat, dessen Laufzeit nicht abgelaufen ist."""
    if not user or not user["is_subscriber"]:
        return False
    end = user["sub_end"] if "sub_end" in user.keys() else None
    return (not end) or (end >= (on_day or date.today()).isoformat())


def monthly_limit(user, on_day=None):
    """Liefert das Monatslimit fuer einen Nutzer (aktives Abo vs. Basis)."""
    if is_active_subscriber(user, on_day):
        return int(db.get_setting("limit_subscriber", "10"))
    return int(db.get_setting("limit_free", "3"))


def quota_period(user, on_day=None):
    """
    Liefert (beginn, erneuerung) des laufenden Kontingent-Zeitraums als ISO-Daten.

    Jeder Zeitraum gehoert zu genau EINEM Tarif, damit Abo-Laufzeit und
    Kontingent im selben Takt laufen:
      * Abo:   Abo-Monate ab dem Abschlussdatum (z.B. 10.10. - 10.11.), nicht
               der Kalendermonat. Der letzte Abo-Monat reicht bis zum Enddatum.
      * Basis: Kalendermonat. Endete in diesem Monat ein Abo, beginnt der
               Basis-Zeitraum erst am Tag danach -- was noch im Abo bezogen
               wurde, belastet das Basis-Kontingent nicht.
    """
    day = on_day or date.today()
    today = day.isoformat()
    start = user["sub_start"] if "sub_start" in user.keys() else None
    end = user["sub_end"] if "sub_end" in user.keys() else None

    if is_active_subscriber(user, day) and start and end and start <= today:
        months = 0      # volle Abo-Monate seit Beginn (Monats-Jahrestage vor dem Enddatum)
        while billing.add_months(start, months + 1) <= min(today, _prev_day(end)):
            months += 1
        nxt = billing.add_months(start, months + 1)
        return billing.add_months(start, months), nxt if nxt < end else _next_day(end)

    begin = today[:8] + "01"
    if end and begin <= end < today:
        begin = _next_day(end)
    return begin, billing.add_months(today[:8] + "01", 1)


def _next_day(iso):
    return (date.fromisoformat(iso) + timedelta(days=1)).isoformat()


def _prev_day(iso):
    return (date.fromisoformat(iso) - timedelta(days=1)).isoformat()


def used_since(user_id, begin):
    """
    Zaehlt die seit 'begin' (ISO-Datum) BEZOGENEN Sounds eines Nutzers.
    Alle Bezugswege teilen sich denselben Topf:
      * gespeicherte/exportierte Beats aus dem Web-Generator (quota_ledger)
      * Gateway-Generierungen (generations)
      * gekaufte Lizenzen (licenses)
    Stornierte (geloeschte) Lizenzen fallen automatisch wieder heraus.
    """
    conn = db.get_conn()
    saves = conn.execute(
        "SELECT COALESCE(SUM(daily_saves), 0) c FROM quota_ledger "
        "WHERE user_id = ? AND date >= ?",
        (user_id, begin),
    ).fetchone()["c"]
    gens = conn.execute(
        "SELECT COUNT(*) c FROM generations "
        "WHERE user_id = ? AND substr(created_at, 1, 10) >= ?",
        (user_id, begin),
    ).fetchone()["c"]
    lics = conn.execute(
        "SELECT COUNT(*) c FROM licenses "
        "WHERE buyer_user_id = ? AND substr(sold_at, 1, 10) >= ?",
        (user_id, begin),
    ).fetchone()["c"]
    conn.close()
    return saves + gens + lics


def quota_status(user, on_day=None):
    """Gibt limit / used / remaining sowie den Zeitraum fuer die Anzeige zurueck."""
    from commerce import tokens  # lokaler Import vermeidet Zirkelbezug
    limit = monthly_limit(user, on_day)
    begin, resets_on = quota_period(user, on_day)
    used = used_since(user["id"], begin)
    return {"limit": limit, "used": used, "remaining": max(limit - used, 0),
            "tokens": tokens.balance(user["id"]),
            "period_start": begin, "resets_on": resets_on}


def subscription_notice(user, on_day=None):
    """
    Hinweis fuer die Tarifseite nach dem Login:
      "expiring" -- Abo laeuft in wenigen Tagen aus
      "expired"  -- Abo ist vor kurzem abgelaufen
      None       -- kein Hinweis noetig
    Die Fristen stehen in config.py.
    """
    end = user["sub_end"] if user and "sub_end" in user.keys() else None
    if not user or not user["is_subscriber"] or not end:
        return None
    days_left = (date.fromisoformat(end) - (on_day or date.today())).days
    if 0 <= days_left <= config.SUB_REMINDER_DAYS_BEFORE:
        return "expiring"
    if -config.SUB_REMINDER_DAYS_AFTER <= days_left < 0:
        return "expired"
    return None


def check_quota(user, count=1):
    """
    Prueft, ob 'count' weitere Bezuege in diesem Monat erlaubt sind.
    Gibt (allowed: bool, status: dict) zurueck.
    """
    status = quota_status(user)
    status["requested"] = count
    allowed = count <= status["remaining"]
    return allowed, status


def record_generation(user_id, source=None, count=1):
    """Traegt 'count' Generierungen fuer den Nutzer ein (Nutzungsprotokoll)."""
    conn = db.get_conn()
    now = datetime.now().isoformat(timespec="seconds")
    for _ in range(count):
        conn.execute(
            "INSERT INTO generations (user_id, source, created_at) VALUES (?, ?, ?)",
            (user_id, source, now),
        )
    conn.commit()
    conn.close()

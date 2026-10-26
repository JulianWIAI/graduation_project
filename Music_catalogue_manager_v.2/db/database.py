"""
Datenbankschicht (SQLite).

Enthaelt das Schema, den Verbindungsaufbau und kleine Hilfsfunktionen.
Bewusst ohne ORM gehalten, damit im Pruefungsgespraech jede Zeile SQL
nachvollziehbar und erklaerbar ist.
"""

import json
import os
import secrets
import sqlite3
from datetime import datetime

from flask import g, has_app_context
from werkzeug.security import generate_password_hash

import config


# --- Schema -----------------------------------------------------------------

SCHEMA = """
CREATE TABLE IF NOT EXISTS tracks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    title           TEXT    NOT NULL,
    genre           TEXT,
    source_midi     TEXT    UNIQUE,          -- Pfad der .mid aus Music Architect
    watermark_tag   TEXT,                    -- Layer-1 copyright-Tag
    watermark_hash  TEXT,                    -- Layer-1 SHA-256 (Dateiname)
    fitness_score   REAL,                    -- optional (falls im Namen kodiert)
    status          TEXT    NOT NULL DEFAULT 'available',  -- available|leased|exclusive_sold
    created_at      TEXT    NOT NULL,
    user_id         INTEGER REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS exports (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    track_id    INTEGER NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
    tier        TEXT    NOT NULL,            -- z.B. lease_wav, trackout ...
    file_path   TEXT    NOT NULL UNIQUE,     -- Pfad der gemasterten Audiodatei (DAW)
    file_format TEXT,
    found_at    TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS licenses (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    track_id      INTEGER NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
    tier          TEXT    NOT NULL,          -- Preis-Stufe (siehe config.DEFAULT_TIERS)
    license_type  TEXT    NOT NULL,          -- lease | exclusive
    buyer_name    TEXT,
    buyer_email   TEXT,
    buyer_user_id INTEGER REFERENCES users(id),  -- registrierter Kaeufer (NULL = Gast)
    price         REAL    NOT NULL,
    currency      TEXT    NOT NULL DEFAULT 'EUR',
    payment_status TEXT   NOT NULL DEFAULT 'open',  -- open | paid
    paid_at       TEXT,
    sold_at       TEXT    NOT NULL,
    notes         TEXT
);

CREATE TABLE IF NOT EXISTS users (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    name           TEXT NOT NULL,
    email          TEXT UNIQUE,
    is_subscriber  INTEGER NOT NULL DEFAULT 0,   -- 0 = Basis, 1 = Abo
    sub_start      TEXT,                          -- Abo-Beginn (ISO-Datum)
    sub_end        TEXT,                          -- Abo-Ende (ISO-Datum)
    created_at     TEXT NOT NULL
);

-- Abgeschlossene Abos (Freemium-Umsatzstrom, mit Laufzeit).
CREATE TABLE IF NOT EXISTS subscriptions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    term_months  INTEGER NOT NULL,
    price        REAL NOT NULL,
    status       TEXT NOT NULL DEFAULT 'open',    -- open | paid
    start_date   TEXT,
    end_date     TEXT,
    created_at   TEXT NOT NULL,
    paid_at      TEXT
);

-- Nutzungsprotokoll der Gateway-Generierung -> zaehlt ins Monatslimit (commerce/quota.py).
CREATE TABLE IF NOT EXISTS generations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    source      TEXT,                            -- z.B. erzeugte Datei / Lauf-Info
    created_at  TEXT NOT NULL                    -- ISO-Zeit (lokal)
);

-- Quota ledger: one row per user per calendar day, tracks saves (not generations).
-- Die Summe der daily_saves eines Kalendermonats zaehlt ins Monatslimit.
CREATE TABLE IF NOT EXISTS quota_ledger (
    user_id        INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    date           TEXT    NOT NULL,
    daily_saves    INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, date)
);

-- Token-Bestellungen (dritter Umsatzstrom). Preise werden zum Bestellzeitpunkt
-- eingefroren, damit spaetere Preisaenderungen alte Belege nicht verfaelschen.
CREATE TABLE IF NOT EXISTS token_purchases (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id          INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    quantity         INTEGER NOT NULL CHECK (quantity > 0),
    price_group      TEXT    NOT NULL CHECK (price_group IN ('basic', 'subscriber')),
    unit_price       REAL    NOT NULL CHECK (unit_price >= 0),   -- tatsaechlicher Stueckpreis
    list_unit_price  REAL    NOT NULL CHECK (list_unit_price >= 0), -- Basis-Stueckpreis (Vergleich)
    price            REAL    NOT NULL CHECK (price >= 0),        -- quantity * unit_price (netto)
    status           TEXT    NOT NULL DEFAULT 'open'
                     CHECK (status IN ('open', 'paid', 'cancelled')),
    created_at       TEXT    NOT NULL,
    paid_at          TEXT
);

-- Token-Konto als Buchungsjournal: jede Bewegung ist eine Zeile.
-- Kontostand = SUM(delta). Gutschrift (+) bei Kauf/Erstattung, Abbuchung (-)
-- bei Verbrauch. Dadurch ist jeder Token lueckenlos nachvollziehbar.
CREATE TABLE IF NOT EXISTS token_ledger (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    delta        INTEGER NOT NULL CHECK (delta <> 0),
    reason       TEXT    NOT NULL
                 CHECK (reason IN ('purchase', 'consume', 'refund', 'admin')),
    purchase_id  INTEGER REFERENCES token_purchases(id) ON DELETE SET NULL,
    reference    TEXT,                           -- z.B. audio_uuid oder Gateway-Lauf
    created_at   TEXT    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_token_ledger_user     ON token_ledger(user_id);
CREATE INDEX IF NOT EXISTS idx_token_purchases_user  ON token_purchases(user_id);

CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT
);

-- Audit-Protokoll: jede geschaeftsrelevante Aktion wird revisionssicher
-- mitgeschrieben (erfuellt die Anforderung "Protokoll fuehren").
CREATE TABLE IF NOT EXISTS audit_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    ts         TEXT NOT NULL,
    event      TEXT NOT NULL,                -- z.B. LICENSE_SOLD, SCAN, SETTING_CHANGED
    entity     TEXT,                         -- track | license | settings | catalog
    entity_id  TEXT,
    details    TEXT                          -- JSON mit Zusatzinfos
);
"""


def get_conn():
    """Liefert eine SQLite-Verbindung mit Fremdschluessel-Enforcement."""
    os.makedirs(os.path.dirname(config.DB_PATH), exist_ok=True)
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    # Innerhalb einer Anfrage merken: bricht der Aufrufer mit einem Fehler ab,
    # bevor er close() erreicht, schliesst close_request_conns() die Verbindung.
    # Sonst haelt die offene Schreib-Transaktion die Datenbank gesperrt.
    if has_app_context():
        g.setdefault("_db_conns", []).append(conn)
    return conn


def close_request_conns(_exc=None):
    """Teardown: alle Verbindungen der Anfrage schliessen (Offenes wird verworfen)."""
    for conn in g.pop("_db_conns", []):
        conn.close()


def init_db():
    """Legt Tabellen an und befuellt Standard-Einstellungen (idempotent)."""
    conn = get_conn()
    conn.executescript(SCHEMA)

    # Standardwerte fuer Einstellungen setzen, falls noch nicht vorhanden.
    defaults = {}
    defaults.update(config.DEFAULT_ECONOMICS)
    defaults.update(config.DEFAULT_SUBSCRIPTION)
    defaults.update(config.DEFAULT_BILLING)
    defaults.update(config.DEFAULT_TOKENS)
    defaults["catalog_dir"] = config.DEFAULT_CATALOG_DIR
    defaults["export_dir"] = config.DEFAULT_EXPORT_DIR
    defaults["music_architect_cmd"] = config.DEFAULT_MA_COMMAND
    for key, tier in config.DEFAULT_TIERS.items():
        defaults[f"price_{key}"] = str(tier["price"])

    for key, value in defaults.items():
        conn.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
            (key, value),
        )

    # --- Leichte Migration: neue Spalten ergaenzen (aeltere DBs) ------------
    lic_cols = {row["name"] for row in
                conn.execute("PRAGMA table_info(licenses)").fetchall()}
    if "list_price" not in lic_cols:
        conn.execute("ALTER TABLE licenses ADD COLUMN list_price REAL")
    if "discount_pct" not in lic_cols:
        conn.execute("ALTER TABLE licenses ADD COLUMN discount_pct REAL DEFAULT 0")
    if "payment_status" not in lic_cols:
        conn.execute("ALTER TABLE licenses ADD COLUMN payment_status TEXT DEFAULT 'open'")
    if "paid_at" not in lic_cols:
        conn.execute("ALTER TABLE licenses ADD COLUMN paid_at TEXT")
    if "buyer_user_id" not in lic_cols:
        conn.execute("ALTER TABLE licenses ADD COLUMN buyer_user_id INTEGER")

    user_cols = {row["name"] for row in
                 conn.execute("PRAGMA table_info(users)").fetchall()}
    if "sub_start" not in user_cols:
        conn.execute("ALTER TABLE users ADD COLUMN sub_start TEXT")
    if "sub_end" not in user_cols:
        conn.execute("ALTER TABLE users ADD COLUMN sub_end TEXT")
    # Auth-Spalten fuer Web-Login — nullable, damit Demo-Nutzer unveraendert bleiben.
    if "password_hash" not in user_cols:
        conn.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
    # is_admin: 1 = Zugang zu allen Admin-Routen, 0 = nur /generate und /stats.
    if "is_admin" not in user_cols:
        conn.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0")
    # Login-Sperre: Fehlversuche in Folge und Ende der Sperre (ISO-Zeitpunkt).
    if "failed_logins" not in user_cols:
        conn.execute("ALTER TABLE users ADD COLUMN failed_logins INTEGER NOT NULL DEFAULT 0")
    if "locked_until" not in user_cols:
        conn.execute("ALTER TABLE users ADD COLUMN locked_until TEXT")
    # Passwort-Wiederherstellung via Sicherheitsfrage.
    if "security_question" not in user_cols:
        conn.execute("ALTER TABLE users ADD COLUMN security_question TEXT")
    if "security_answer_hash" not in user_cols:
        conn.execute("ALTER TABLE users ADD COLUMN security_answer_hash TEXT")
    # Erzwungene Passwortaenderung (z. B. nach Admin-Reset).
    if "must_change_pw" not in user_cols:
        conn.execute("ALTER TABLE users ADD COLUMN must_change_pw INTEGER NOT NULL DEFAULT 0")

    track_cols = {row["name"] for row in
                  conn.execute("PRAGMA table_info(tracks)").fetchall()}
    if "user_id" not in track_cols:
        conn.execute("ALTER TABLE tracks ADD COLUMN user_id INTEGER REFERENCES users(id)")

    # --- Zwei Demo-Nutzer anlegen, damit Rabatt & Limit sofort erlebbar sind -
    user_count = conn.execute("SELECT COUNT(*) c FROM users").fetchone()["c"]
    if user_count == 0:
        now = datetime.now().isoformat(timespec="seconds")
        conn.execute("INSERT INTO users (name, email, is_subscriber, created_at) "
                     "VALUES (?, ?, 1, ?)", ("Abo-Kunde (Demo)", "abo@example.com", now))
        conn.execute("INSERT INTO users (name, email, is_subscriber, created_at) "
                     "VALUES (?, ?, 0, ?)", ("Basis-Kunde (Demo)", "basis@example.com", now))

    # --- Admin-Account (wird beim ersten Start angelegt) ---------------------
    # Das Passwort steht bewusst NICHT im Quelltext: Es kommt aus der Umgebungs-
    # variable SBS_ADMIN_PASSWORD. Fehlt sie, wird eines erzeugt und einmalig in
    # der Konsole angezeigt.
    admin = conn.execute("SELECT id FROM users WHERE email = 'admin@admin.com'").fetchone()
    if not admin:
        password = os.environ.get("SBS_ADMIN_PASSWORD") or secrets.token_urlsafe(9)
        now = datetime.now().isoformat(timespec="seconds")
        conn.execute(
            "INSERT INTO users (name, email, password_hash, is_subscriber, is_admin, created_at) "
            "VALUES (?, ?, ?, 0, 1, ?)",
            ("Admin", "admin@admin.com", generate_password_hash(password), now),
        )
        if not os.environ.get("SBS_ADMIN_PASSWORD"):
            print(f"\n*** Admin-Konto angelegt: admin@admin.com  Passwort: {password}\n"
                  "*** Bitte notieren -- es wird nicht noch einmal angezeigt.\n", flush=True)

    conn.commit()
    conn.close()


# --- Einstellungen ----------------------------------------------------------

def get_setting(key, default=None):
    conn = get_conn()
    row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default


def set_setting(key, value):
    conn = get_conn()
    conn.execute(
        "INSERT INTO settings (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (key, str(value)),
    )
    conn.commit()
    conn.close()


def get_all_settings():
    conn = get_conn()
    rows = conn.execute("SELECT key, value FROM settings").fetchall()
    conn.close()
    return {r["key"]: r["value"] for r in rows}


# --- Audit-Protokoll --------------------------------------------------------

def log_event(event, entity=None, entity_id=None, details=None):
    """Schreibt einen Eintrag ins Audit-Protokoll."""
    conn = get_conn()
    conn.execute(
        "INSERT INTO audit_log (ts, event, entity, entity_id, details) "
        "VALUES (?, ?, ?, ?, ?)",
        (
            datetime.now().isoformat(timespec="seconds"),
            event,
            entity,
            str(entity_id) if entity_id is not None else None,
            json.dumps(details, ensure_ascii=False) if details else None,
        ),
    )
    conn.commit()
    conn.close()


def get_audit_log(limit=500, query=""):
    """
    Neueste Protokoll-Eintraege. 'query' filtert nach Suchbegriffen: Jeder durch
    Leerzeichen getrennte Begriff muss in Zeitstempel, Ereignis, Objekt oder Details
    vorkommen (Gross-/Kleinschreibung egal), z.B. "token" oder "token 2026-10".
    """
    words = (query or "").split()
    text = ("ts || ' ' || event || ' ' || COALESCE(entity, '') || ' ' || "
            "COALESCE(entity_id, '') || ' ' || COALESCE(details, '')")
    where = " AND ".join([f"{text} LIKE ?"] * len(words))
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM audit_log " + (f"WHERE {where} " if where else "") +
        "ORDER BY id DESC LIMIT ?",
        [f"%{w}%" for w in words] + [limit],
    ).fetchall()
    conn.close()
    return rows


# --- Auth helpers ------------------------------------------------------------

def get_user_by_email(email: str):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return row


def get_user_by_id(user_id: int):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return row


def create_user(email: str, password_hash: str,
                security_question: str = None, security_answer_hash: str = None):
    """Legt einen neuen Web-Auth-Nutzer an; gibt die neue Nutzer-ID zurueck."""
    conn = get_conn()
    now = datetime.now().isoformat(timespec="seconds")
    cur = conn.execute(
        "INSERT INTO users (name, email, password_hash, is_subscriber, "
        "security_question, security_answer_hash, created_at) "
        "VALUES (?, ?, ?, 0, ?, ?, ?)",
        (email.split("@")[0], email, password_hash, security_question, security_answer_hash, now),
    )
    uid = cur.lastrowid
    conn.commit()
    conn.close()
    return uid


# --- Quota helpers -----------------------------------------------------------

def increment_quota(user_id: int, date: str):
    """Zaehlt einen bezogenen Sound fuer (user_id, date) -- eine Zeile je Nutzer und Tag."""
    conn = get_conn()
    conn.execute(
        "INSERT INTO quota_ledger (user_id, date, daily_saves) VALUES (?, ?, 1) "
        "ON CONFLICT(user_id, date) DO UPDATE SET daily_saves = daily_saves + 1",
        (user_id, date),
    )
    conn.commit()
    conn.close()

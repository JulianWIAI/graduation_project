"""
Zahlungsmethoden-Verwaltung (simuliert).

In einem echten System würden Kartendaten niemals im eigenen Server gespeichert —
sie werden an einen PCI-DSS-zertifizierten Zahlungsdienstleister (z. B. Stripe,
Braintree) übertragen, der im Gegenzug ein Token zurückgibt. Dieses Token ist
das Einzige, was lokal gespeichert wird.

Für die Demo gilt dasselbe Prinzip:
  * Kreditkarte: nur letzte 4 Stellen, Kartentyp, Ablaufdatum und Name werden
    gespeichert. Die vollständige Kartennummer wird sofort verworfen.
  * SEPA: IBAN wird maskiert (DE** **** … **49), BIC und Kontoinhaber im Klartext.

Beide Methoden simulieren damit professionelles Tokenisierungs-Verhalten, ohne
echte Zahlungsfunktionen zu benötigen.
"""

import re
from datetime import datetime

from db import database as db
from i18n import _


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def _mask_iban(iban: str) -> str:
    """Maskiert eine IBAN: Länderkürzel + Prüfziffer sichtbar, Rest mit *."""
    iban = iban.replace(" ", "").upper()
    if len(iban) < 6:
        return iban
    visible_start = iban[:4]   # z. B. DE49
    visible_end   = iban[-4:]
    masked_len    = len(iban) - 8
    return f"{visible_start} {'*' * masked_len} {visible_end}"


def _detect_card_type(number: str) -> str:
    """Erkennt den Kartentyp anhand der ersten Ziffern."""
    n = number.replace(" ", "")
    if n.startswith("4"):
        return "Visa"
    if re.match(r"^5[1-5]", n) or re.match(r"^2(2[2-9][1-9]|[3-6]\d{2}|7[01]\d|720)", n):
        return "Mastercard"
    if re.match(r"^3[47]", n):
        return "Amex"
    return "Other"


# ---------------------------------------------------------------------------
# Öffentliche API
# ---------------------------------------------------------------------------

def get_methods(user_id: int):
    """Gibt alle Zahlungsmethoden eines Nutzers zurück (neueste zuerst)."""
    conn = db.get_conn()
    rows = conn.execute(
        "SELECT * FROM payment_methods WHERE user_id = ? ORDER BY is_default DESC, id DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return rows


def get_all_methods_for_admin():
    """Gibt alle Zahlungsmethoden mit Nutzerdaten zurück (Admin-Ansicht)."""
    conn = db.get_conn()
    rows = conn.execute(
        "SELECT pm.*, u.email, u.name AS user_name "
        "FROM payment_methods pm "
        "JOIN users u ON u.id = pm.user_id "
        "ORDER BY pm.user_id, pm.is_default DESC, pm.id DESC"
    ).fetchall()
    conn.close()
    return rows


def add_card(user_id: int, card_number: str, expiry: str, holder: str) -> tuple:
    """
    Speichert eine Kreditkarte (nur maskierte Daten, nie die vollständige Nummer).

    Gibt (method_id, None) bei Erfolg zurück, (None, Fehlermeldung) bei Fehler.
    """
    number = card_number.replace(" ", "")
    if not re.fullmatch(r"\d{13,19}", number):
        return None, _("Ungültige Kartennummer.")
    if not re.fullmatch(r"(0[1-9]|1[0-2])/\d{2}", expiry):
        return None, _("Ungültiges Ablaufdatum (MM/JJ).")
    holder = holder.strip()
    if not holder:
        return None, _("Name des Karteninhabers ist erforderlich.")

    card_type = _detect_card_type(number)
    last4     = number[-4:]
    now       = datetime.now().isoformat(timespec="seconds")

    conn = db.get_conn()
    # Wenn erste Methode: automatisch als Standard setzen.
    count = conn.execute(
        "SELECT COUNT(*) c FROM payment_methods WHERE user_id = ?", (user_id,)
    ).fetchone()["c"]
    is_default = 1 if count == 0 else 0

    cur = conn.execute(
        "INSERT INTO payment_methods "
        "(user_id, method_type, card_type, card_last4, card_expiry, card_holder, is_default, created_at) "
        "VALUES (?, 'card', ?, ?, ?, ?, ?, ?)",
        (user_id, card_type, last4, expiry, holder, is_default, now)
    )
    conn.commit()
    conn.close()
    db.log_event("PAYMENT_METHOD_ADDED", "user", user_id,
                 {"type": "card", "card_type": card_type, "last4": last4})
    return cur.lastrowid, None


def add_sepa(user_id: int, iban: str, bic: str, holder: str) -> tuple:
    """
    Speichert eine SEPA-Lastschrift mit maskierter IBAN.

    Gibt (method_id, None) bei Erfolg zurück, (None, Fehlermeldung) bei Fehler.
    """
    iban_clean = iban.replace(" ", "").upper()
    if not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]{11,30}", iban_clean):
        return None, _("Ungültige IBAN.")
    bic = bic.strip().upper()
    holder = holder.strip()
    if not holder:
        return None, _("Name des Kontoinhabers ist erforderlich.")

    iban_masked = _mask_iban(iban_clean)
    now         = datetime.now().isoformat(timespec="seconds")

    conn = db.get_conn()
    count = conn.execute(
        "SELECT COUNT(*) c FROM payment_methods WHERE user_id = ?", (user_id,)
    ).fetchone()["c"]
    is_default = 1 if count == 0 else 0

    cur = conn.execute(
        "INSERT INTO payment_methods "
        "(user_id, method_type, iban_masked, bic, account_holder, is_default, created_at) "
        "VALUES (?, 'sepa', ?, ?, ?, ?, ?)",
        (user_id, iban_masked, bic, holder, is_default, now)
    )
    conn.commit()
    conn.close()
    db.log_event("PAYMENT_METHOD_ADDED", "user", user_id,
                 {"type": "sepa", "iban_masked": iban_masked})
    return cur.lastrowid, None


def set_default(method_id: int, user_id: int) -> bool:
    """Setzt eine Zahlungsmethode als Standard (entfernt anderen Standard)."""
    conn = db.get_conn()
    row = conn.execute(
        "SELECT id FROM payment_methods WHERE id = ? AND user_id = ?",
        (method_id, user_id)
    ).fetchone()
    if not row:
        conn.close()
        return False
    conn.execute("UPDATE payment_methods SET is_default = 0 WHERE user_id = ?", (user_id,))
    conn.execute("UPDATE payment_methods SET is_default = 1 WHERE id = ?", (method_id,))
    conn.commit()
    conn.close()
    return True


def delete_method(method_id: int, user_id: int) -> tuple:
    """
    Löscht eine Zahlungsmethode.
    Gibt (True, None) bei Erfolg zurück, (False, Fehlermeldung) wenn geblockt.
    Das Löschen der letzten Methode ist nicht erlaubt.
    """
    conn = db.get_conn()
    count = conn.execute(
        "SELECT COUNT(*) c FROM payment_methods WHERE user_id = ?", (user_id,)
    ).fetchone()["c"]
    if count <= 1:
        conn.close()
        return False, _("Die letzte Zahlungsmethode kann nicht gelöscht werden. Bitte hinterlege zuerst eine neue.")
    row = conn.execute(
        "SELECT id, is_default FROM payment_methods WHERE id = ? AND user_id = ?",
        (method_id, user_id)
    ).fetchone()
    if not row:
        conn.close()
        return False, None
    was_default = row["is_default"]
    conn.execute("DELETE FROM payment_methods WHERE id = ?", (method_id,))
    if was_default:
        next_row = conn.execute(
            "SELECT id FROM payment_methods WHERE user_id = ? ORDER BY id DESC LIMIT 1",
            (user_id,)
        ).fetchone()
        if next_row:
            conn.execute("UPDATE payment_methods SET is_default = 1 WHERE id = ?",
                         (next_row["id"],))
    conn.commit()
    conn.close()
    db.log_event("PAYMENT_METHOD_DELETED", "user", user_id, {"method_id": method_id})
    return True, None


def get_default(user_id: int):
    """Gibt die Standard-Zahlungsmethode eines Nutzers zurück (oder None)."""
    conn = db.get_conn()
    row = conn.execute(
        "SELECT * FROM payment_methods WHERE user_id = ? AND is_default = 1",
        (user_id,)
    ).fetchone()
    conn.close()
    return row


def label(method) -> str:
    """Gibt eine lesbare Kurzbezeichnung für eine Zahlungsmethode zurück."""
    if method is None:
        return "—"
    if method["method_type"] == "card":
        return f"{method['card_type']} •••• {method['card_last4']} ({method['card_expiry']})"
    return f"SEPA {method['iban_masked']}"

"""
Notfall-Zugang: setzt das Passwort eines Kontos (standardmaessig des Admins)
direkt in der Datenbank neu und hebt alle Login-Sperren auf.

Nur fuer den Fall, dass der Admin sein Passwort vergessen hat und niemand
sonst zuruecksetzen kann. Wer dieses Skript ausfuehren kann, hat ohnehin
Zugriff auf Rechner und Datenbank -- darum ist das unbedenklich.

Aufruf (im Ordner Music_catalogue_manager_v.2, Server darf laufen):
    .venv/bin/python reset_admin.py                    # Admin-Konto
    .venv/bin/python reset_admin.py name@example.com   # anderes Konto
"""

import getpass
import sys

from werkzeug.security import generate_password_hash

from auth import lockout, password_policy
from db import database as db

DEFAULT_EMAIL = "admin@admin.com"


def main(argv):
    email = (argv[1] if len(argv) > 1 else DEFAULT_EMAIL).strip().lower()
    db.init_db()                                   # stellt sicher, dass alle Tabellen existieren
    row = db.get_user_by_email(email)
    if not row:
        print(f"Kein Konto mit der E-Mail-Adresse {email} gefunden.")
        return 1

    print(f"Neues Passwort fuer {email} setzen (Eingabe bleibt unsichtbar).")
    if password_policy.applies_to(bool(row["is_admin"])):
        print(password_policy.hint())
    while True:
        pw = getpass.getpass("Neues Passwort: ")
        if pw != getpass.getpass("Wiederholen:   "):
            print("Die Passwoerter stimmen nicht ueberein.\n")
            continue
        problems = [] if pw else ["Passwort darf nicht leer sein."]
        problems += password_policy.validate(pw, email, bool(row["is_admin"]))
        if problems:
            print("\n".join("  - " + p for p in problems) + "\n")
            continue
        break

    conn = db.get_conn()
    conn.execute("UPDATE users SET password_hash = ?, must_change_pw = 0 WHERE id = ?",
                 (generate_password_hash(pw), row["id"]))
    conn.commit()
    conn.close()
    lockout.unlock_user(row["id"])
    db.log_event("PASSWORD_RESET", "user", row["id"], {"via": "reset_admin.py"})
    print(f"Passwort fuer {email} wurde geaendert, alle Sperren sind aufgehoben.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

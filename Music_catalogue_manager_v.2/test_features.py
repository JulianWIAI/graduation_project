"""
Selbsttest fuer: Sprachumschaltung, Tarifwahl nach Registrierung,
Monatskontingent (3 Basis / 10 Abo) und Token-Abbuchung.

Start:  python test_features.py      (laeuft auch unter pytest)

Arbeitet auf einer temporaeren Datenbank -- instance/catalog.db bleibt unberuehrt.
"""

import os
import re
import tempfile
import wave
from datetime import date, timedelta

import config

config.DB_PATH = os.path.join(tempfile.mkdtemp(), "test.db")   # VOR dem App-Import!
ADMIN_PASSWORD = "nur-fuer-den-test"
os.environ["SBS_ADMIN_PASSWORD"] = ADMIN_PASSWORD               # ebenfalls vor dem Import

import main                                   # noqa: E402
from commerce import billing, quota, tokens   # noqa: E402
from db import database as db                 # noqa: E402
from translations import _JS, _T              # noqa: E402

main.app.config["TESTING"] = True
_counter = iter(range(10_000))


def _register(client):
    """Registriert einen frischen Kunden; gibt (user_id, Antwort) zurueck."""
    email = f"kunde{next(_counter)}@example.com"
    resp = client.post("/register", data={"email": email, "password": "geheim", "confirm": "geheim"})
    return db.get_user_by_email(email)["id"], resp


def _use_quota(user_id, n):
    for _ in range(n):
        db.increment_quota(user_id, date.today().isoformat())


def test_registration_leads_to_plan_choice():
    client = main.app.test_client()
    _, resp = _register(client)
    assert resp.status_code == 302 and resp.headers["Location"].endswith("/plan")
    page = client.get("/plan").get_data(as_text=True)
    assert "Als Basis-Kunde starten" in page and "Abo abschließen" in page


def test_monthly_quota_basic_3_subscriber_10():
    client = main.app.test_client()
    uid, _ = _register(client)
    assert quota.quota_status(quota.get_user(uid))["limit"] == 3

    # Abo ueber die Kundenstrecke abschliessen und (simuliert) bezahlen.
    resp = client.post("/subscription/start", data={"term_months": "1"})
    sub_url = resp.headers["Location"]
    assert "/subscription/checkout/" in sub_url
    sub_id = sub_url.rsplit("/", 1)[1]
    client.post(f"/subscription/{sub_id}/pay")
    assert quota.quota_status(quota.get_user(uid))["limit"] == 10

    # Ein fremder Kunde darf diese Bestellung weder sehen noch bezahlen.
    other = main.app.test_client()
    _register(other)
    assert other.get(sub_url).status_code == 404
    assert other.post(f"/subscription/{sub_id}/pay").status_code == 404


def test_quota_counts_current_month_only():
    uid, _ = _register(main.app.test_client())
    db.increment_quota(uid, "2020-01-15")            # alter Monat zaehlt nicht
    _use_quota(uid, 2)
    status = quota.quota_status(quota.get_user(uid))
    assert (status["used"], status["remaining"]) == (2, 1)
    # Im Folgemonat ist das Kontingent wieder voll.
    assert quota.quota_status(quota.get_user(uid), on_day=date(2099, 1, 1))["remaining"] == 3


def _set_subscription(user_id, start, end):
    conn = db.get_conn()
    conn.execute("UPDATE users SET is_subscriber = 1, sub_start = ?, sub_end = ? WHERE id = ?",
                 (str(start), str(end), user_id))
    conn.commit()
    conn.close()


def test_quota_period_follows_subscription():
    uid, _ = _register(main.app.test_client())

    def status(iso):
        return quota.quota_status(quota.get_user(uid), on_day=date.fromisoformat(iso))

    def period(iso):
        s = status(iso)
        return s["period_start"], s["resets_on"]

    db.increment_quota(uid, "2030-10-05")                    # noch als Basis-Kunde bezogen
    _set_subscription(uid, "2030-10-10", "2030-11-10")       # 1 Monat Abo
    assert (status("2030-10-15")["limit"], status("2030-10-15")["used"]) == (10, 0)
    assert period("2030-10-15") == ("2030-10-10", "2030-11-11")

    db.increment_quota(uid, "2030-10-12")
    db.increment_quota(uid, "2030-11-05")                    # anderer Kalendermonat, selber Abo-Monat
    assert status("2030-11-10")["used"] == 2                 # letzter Abo-Tag: kein frisches Kontingent
    assert period("2030-11-10") == ("2030-10-10", "2030-11-11")

    # Nach Ablauf: Basis-Limit, und was im Abo bezogen wurde, zaehlt nicht mit.
    after = status("2030-11-11")
    assert (after["limit"], after["used"], after["remaining"]) == (3, 0, 3)
    assert period("2030-11-11") == ("2030-11-11", "2030-12-01")

    # Mehrmonatiges Abo: jeder Abo-Monat ist ein eigener Zeitraum.
    _set_subscription(uid, "2030-10-10", "2031-01-10")
    assert period("2030-11-20") == ("2030-11-10", "2030-12-10")
    assert period("2031-01-10") == ("2030-12-10", "2031-01-11")


def test_renewal_extends_from_current_end():
    client = main.app.test_client()
    uid, _ = _register(client)

    def subscribe(months):
        loc = client.post("/subscription/start", data={"term_months": str(months)}).headers["Location"]
        client.post(f"/subscription/{loc.rsplit('/', 1)[1]}/pay")
        return quota.get_user(uid)

    first = subscribe(1)
    renewed = subscribe(3)                                   # waehrend das Abo noch laeuft
    assert renewed["sub_start"] == first["sub_start"]        # Stichtag bleibt erhalten
    assert renewed["sub_end"] == billing.add_months(first["sub_end"], 3)


def test_login_reminds_about_expiring_subscription():
    client = main.app.test_client()
    uid, _ = _register(client)
    email = quota.get_user(uid)["email"]
    today = date.today()

    def login():
        client.get("/logout")
        return client.post("/login", data={"email": email, "password": "geheim"}).headers["Location"]

    _set_subscription(uid, today - timedelta(days=27), today + timedelta(days=3))
    assert login().endswith("/plan")
    assert "läuft am" in client.get("/plan").get_data(as_text=True)

    _set_subscription(uid, today - timedelta(days=32), today - timedelta(days=2))
    assert login().endswith("/plan")
    assert "abgelaufen" in client.get("/plan").get_data(as_text=True)

    _set_subscription(uid, today, today + timedelta(days=30))   # laeuft noch lange: kein Hinweis
    assert login().endswith("/generate")


def _fake_beat(client, name):
    """Legt in der Sitzung einen 'generierten' Beat ab, ohne den Motor zu starten."""
    tmp = os.path.join(tempfile.mkdtemp(), "beat.wav")
    with wave.open(tmp, "wb") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(8000), w.writeframes(b"\0\0")
    with client.session_transaction() as sess:
        sess[f"temp_{name}"] = tmp


def _remove_exports(user_id):
    """Raeumt die beim Export angelegten Audiodateien wieder weg."""
    conn = db.get_conn()
    rows = conn.execute("SELECT file_path FROM exports e JOIN tracks t ON t.id = e.track_id "
                        "WHERE t.user_id = ?", (user_id,)).fetchall()
    conn.close()
    for row in rows:
        path = os.path.join(config.BASE_DIR, row["file_path"])
        os.remove(path)
        if not os.listdir(os.path.dirname(path)):
            os.rmdir(os.path.dirname(path))


def test_token_is_consumed_when_quota_is_exhausted():
    client = main.app.test_client()
    uid, _ = _register(client)
    _use_quota(uid, 3)                               # Monatskontingent aufgebraucht

    def export(name):
        _fake_beat(client, name)
        return client.get(f"/export_audio/{name}?format=wav_cd")

    resp = export("a")
    assert resp.status_code == 429 and resp.get_json()["error"] == "quota_exceeded"

    tokens.admin_adjust(uid, 1)
    assert export("b").status_code == 200            # kostet den einen Token
    assert tokens.balance(uid) == 0
    assert export("b").status_code == 200            # derselbe Beat noch einmal: frei
    assert export("c").status_code == 429            # neuer Beat: Token ist wirklich weg
    _remove_exports(uid)


def test_exported_beat_keeps_its_seed_and_locks_it():
    client = main.app.test_client()
    uid, _ = _register(client)
    _fake_beat(client, "beat1")                          # Zustand wie nach /generate
    with client.session_transaction() as sess:
        sess["temp_seed_beat1"] = 424242

    assert client.get("/export_audio/beat1?format=wav_cd").status_code == 200
    conn = db.get_conn()
    row = conn.execute("SELECT watermark_tag FROM tracks WHERE user_id = ?", (uid,)).fetchone()
    conn.close()
    assert row["watermark_tag"] == "seed:424242"

    # Der exklusiv vergebene Seed laesst sich nicht noch einmal generieren.
    resp = client.post("/generate", json={"genre": "trap", "seed": "424242"})
    assert resp.status_code == 409 and resp.get_json()["error"] == "seed_locked"
    assert client.post("/generate", json={"seed": "abc"}).status_code == 400
    _remove_exports(uid)


def test_watermark_checksum_is_really_verified():
    import hashlib
    import mido
    from catalog import watermark_reader

    folder = tempfile.mkdtemp()

    def write(name, text):
        path = os.path.join(folder, name)
        track = mido.MidiTrack([mido.MetaMessage("copyright", text="(C) Test", time=0),
                                mido.MetaMessage("text", text=text, time=0)])
        midi = mido.MidiFile()
        midi.tracks.append(track)
        midi.save(path)
        return path

    full = hashlib.sha256(b"song.mid").hexdigest()
    engine = write("song.mid", f"TAG | SHA256_FNAME={full[:16].upper()}")     # Format des Motors
    demo = write("demo.mid", "WM_HASH:" + hashlib.sha256(b"demo.mid").hexdigest())
    for path in (engine, demo):
        assert watermark_reader.hash_matches(path, watermark_reader.read_watermark(path)["hash"])

    renamed = os.path.join(folder, "kopie.mid")                               # umbenannte Datei
    os.rename(engine, renamed)
    stored = watermark_reader.read_watermark(renamed)["hash"]
    assert stored and not watermark_reader.hash_matches(renamed, stored)


def test_language_switch():
    client = main.app.test_client()
    assert "Anmelden" in client.get("/login").get_data(as_text=True)          # Standard: Deutsch
    for code, text in (("en", "Sign in"), ("fr", "Se connecter"), ("de", "Anmelden")):
        client.get(f"/lang/{code}")
        page = client.get("/login").get_data(as_text=True)
        assert text in page and f'<html lang="{code}">' in page
    client.get("/lang/xx")                                                     # unbekannt -> unveraendert
    assert "Anmelden" in client.get("/login").get_data(as_text=True)

    # Auch Server-Meldungen folgen der Sprache.
    client.get("/lang/en")
    resp = client.post("/login", data={"email": "x@example.com", "password": "falsch"})
    assert "Invalid email or wrong password." in resp.get_data(as_text=True)


def test_all_pages_render_in_every_language():
    client = main.app.test_client()
    client.post("/login", data={"email": "admin@admin.com", "password": ADMIN_PASSWORD})
    pages = ["/generate", "/stats", "/tokens", "/plan", "/dashboard", "/catalog",
             "/licenses", "/users", "/economics", "/audit", "/settings"]
    for code in ("de", "en", "fr"):
        client.get(f"/lang/{code}")
        for page in pages:
            assert client.get(page).status_code == 200, (code, page)


def test_translations_keep_placeholders():
    def placeholders(text):
        return sorted(re.findall(r"%\(\w+\)s|\{\w+\}|&#10;", text))
    for table in (_T, _JS):
        for german, translated in table.items():
            assert len(translated) == 2, german
            for text in translated:
                assert placeholders(text) == placeholders(german), german


if __name__ == "__main__":
    for name, func in list(globals().items()):
        if name.startswith("test_"):
            func()
            print("ok ", name)

"""
Liest das Layer-1-Wasserzeichen aus den .mid-Dateien von Music Architect V7.

Music Architect schreibt in einen versteckten Track MetaMessages vom Typ
'copyright' (Katalog-Tag) und 'text' (u.a. der SHA-256-Hash des Dateinamens).
Wir lesen diese rein lesend mit mido aus -- exakt dasselbe Format, das die
Watermark-Engine des Partnerprojekts erzeugt. Der Leser ist bewusst tolerant
gehalten (findet den Hash heuristisch), damit kleine Format-Abweichungen nicht
zum Absturz fuehren.

Layer 2 (Velocity-LSB-Steganographie) wird hier NICHT dekodiert -- dafuer ist
die Original-Engine zustaendig (`python main.py watermark --extract ...`).
"""

import hashlib
import os
import re

try:
    import mido
except ImportError:  # pragma: no cover
    mido = None

# 64 Hex-Zeichen = SHA-256
# Zwei Schreibweisen der Dateinamen-Pruefsumme:
#   * Music Architect V7:  "... | SHA256_FNAME=<erste 16 Hex-Zeichen>"
#   * Demo-/Gateway-Daten: "WM_HASH:<volle 64 Hex-Zeichen>"
_SHA256_RE = re.compile(r"\b[0-9a-fA-F]{64}\b|(?<=SHA256_FNAME=)[0-9a-fA-F]{16}\b")


def read_watermark(midi_path):
    """
    Gibt ein dict zurueck:
        {"tag": <copyright-Text oder None>,
         "hash": <SHA-256 oder None>,
         "raw_meta": [<alle gelesenen Meta-Texte>]}
    Bei Lesefehlern werden None-Werte zurueckgegeben (nie eine Exception nach
    aussen), damit ein einzelner defekter File den Scan nicht abbricht.
    """
    result = {"tag": None, "hash": None, "raw_meta": []}
    if mido is None:
        return result

    try:
        midi = mido.MidiFile(midi_path)
    except Exception:
        return result

    texts = []
    for track in midi.tracks:
        for msg in track:
            if msg.is_meta and msg.type in ("copyright", "text", "track_name", "marker"):
                value = getattr(msg, "text", "") or ""
                texts.append(value)
                if msg.type == "copyright" and result["tag"] is None:
                    result["tag"] = value.strip()

    result["raw_meta"] = texts

    # Hash heuristisch ueber alle Meta-Texte suchen.
    for value in texts:
        match = _SHA256_RE.search(value)
        if match:
            result["hash"] = match.group(0).lower()
            break

    # Falls kein copyright-Feld existierte, aber Texte da sind: ersten
    # nicht-Hash-Text als Tag verwenden (Fallback).
    if result["tag"] is None:
        for value in texts:
            if value and not _SHA256_RE.search(value):
                result["tag"] = value.strip()
                break

    return result


def hash_matches(midi_path, stored_hash):
    """
    Echte Pruefung des Wasserzeichens: Die gespeicherte Pruefsumme muss zum
    SHA-256 des Dateinamens passen (voll oder als 16-Zeichen-Anfang). Wurde die
    Datei umbenannt oder die Pruefsumme veraendert, schlaegt der Vergleich fehl.
    """
    if not midi_path or not stored_hash or len(stored_hash) not in (16, 64):
        return False
    expected = hashlib.sha256(os.path.basename(midi_path).encode("utf-8")).hexdigest()
    return expected.startswith(stored_hash.lower())


def has_watermark(midi_path):
    wm = read_watermark(midi_path)
    return bool(wm["tag"] or wm["hash"])

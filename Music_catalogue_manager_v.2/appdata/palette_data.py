"""
palette_data.py — Laedt Instrumenten-Paletten, FX-Varianten und berechnet
den Theorie-Score direkt aus den MUSIC_ARCHITECT_V7 Production-Guide-JSONs.

Datenquellen (read-only):
  - instrument_palettes.json  → Paletten mit BDRA-Codes pro Genre
  - fx_variants.json          → FX-Ketten-Varianten (bright/neutral/dark)
  - <genre>.json              → valid_scales, bpm_range fuer Theorie-Pruefungen

Plattformunabhaengig — nur Python-Stdlib. Kein Tkinter, keine OS-APIs.
"""

from __future__ import annotations

import json
import pathlib
from typing import Dict, List, Optional
import config

# Pfad zum MA V7 Production-Guide-Verzeichnis
_GUIDE_DIR = (
    pathlib.Path(config.MA_ROOT)
    / "data"
    / "production_guide"
    / "json"
)

# Genre → Dateiname fuer Genre-JSONs (identisch mit production_advisor.py)
_GENRE_FILES: Dict[str, str] = {
    "trap":      "trap.json",
    "phonk":     "phonk.json",
    "hiphop":    "hiphop.json",
    "techno":    "techno.json",
    "house":     "house.json",
    "edm":       "house.json",
    "pop":       "pop.json",
    "cinematic": "cinematic.json",
    "classical": "cinematic.json",
    "jpop":      "jpop.json",
}

# Laufzeit-Caches (Dateien werden einmalig gelesen)
_palettes_cache: Optional[Dict]  = None
_fx_cache:       Optional[Dict]  = None
_genre_cache:    Dict[str, Dict] = {}


def _load_palettes() -> Dict:
    global _palettes_cache
    if _palettes_cache is None:
        path = _GUIDE_DIR / "instrument_palettes.json"
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        _palettes_cache = {k: v for k, v in data.items() if k != "_meta"}
    return _palettes_cache


def _load_fx() -> Dict:
    global _fx_cache
    if _fx_cache is None:
        path = _GUIDE_DIR / "fx_variants.json"
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        _fx_cache = data.get("variants", {})
    return _fx_cache


def _load_genre(genre: str) -> Dict:
    if genre not in _genre_cache:
        fname = _GENRE_FILES.get(genre, "pop.json")
        path  = _GUIDE_DIR / fname
        try:
            with open(path, encoding="utf-8") as fh:
                _genre_cache[genre] = json.load(fh)
        except FileNotFoundError:
            _genre_cache[genre] = {}
    return _genre_cache[genre]


# ---------------------------------------------------------------------------
# Oeffentliche API
# ---------------------------------------------------------------------------

def get_palettes(genre: str) -> List[Dict]:
    """
    Gibt alle vorvalidierten Instrumenten-Paletten fuer ein Genre zurueck.
    Jede Palette enthaelt id, name, branch, kick_code, kick_desc, instruments.
    """
    all_pal = _load_palettes()
    return all_pal.get(genre, all_pal.get("pop", []))


def get_fx_variants(genre: str) -> List[Dict]:
    """
    Gibt die FX-Ketten-Varianten (bright/neutral/dark) fuer ein Genre zurueck.
    Nur id, label und description werden zurueckgegeben (chain_overlay ausgelassen).
    """
    all_fx = _load_fx()
    variants = all_fx.get(genre, all_fx.get("pop", []))
    return [{"id": v["id"], "label": v["label"], "description": v.get("description", "")}
            for v in variants]


# ---------------------------------------------------------------------------
# Vollstaendige GM → BDRA-Zuordnung (genreuebergreifend)
# ---------------------------------------------------------------------------

def get_all_gm_bdra_codes() -> Dict[str, Dict[int, str]]:
    """
    Gibt eine vollstaendige Zuordnung von GM-Programmnummer zu BDRA-Code
    fuer alle Spur-Typen zurueck, aggregiert aus allen Genres und Paletten.

    Rueckgabe: { spur_key: { gm_nummer: bdra_code } }
    Beispiel:  { "bass": { 35: "B0 D2 A1 R0", 34: "B0 D2 A1 R0" }, ... }

    Wird einmalig beim ersten Aufruf berechnet und danach gecacht.
    """
    if _gm_bdra_cache:
        return _gm_bdra_cache

    alle_paletten = _load_palettes()
    # Ueber alle Genres und alle Paletten iterieren
    for genre_paletten in alle_paletten.values():
        for palette in genre_paletten:
            for spur_key, instr in palette.get("instruments", {}).items():
                gm   = instr.get("gm")
                code = instr.get("code", "")
                if gm is not None and code:
                    _gm_bdra_cache.setdefault(spur_key, {})[int(gm)] = code

    return _gm_bdra_cache


# Laufzeit-Cache fuer get_all_gm_bdra_codes (einmalig befuellt)
_gm_bdra_cache: Dict[str, Dict[int, str]] = {}


# ---------------------------------------------------------------------------
# BDRA-Hilfsfunktionen
# ---------------------------------------------------------------------------

def parse_bdra(code: str) -> Dict[str, int]:
    """
    Parst einen BDRA-Code-String in ein Dict.
    Beispiel: 'B1 D2 A0 R2' → {'B': 1, 'D': 2, 'A': 0, 'R': 2}
    """
    result: Dict[str, int] = {}
    for part in (code or "").split():
        if len(part) >= 2 and part[0] in "BDAR":
            try:
                result[part[0]] = int(part[1])
            except ValueError:
                pass
    return result


# ---------------------------------------------------------------------------
# Theorie-Score (P1–P5)
# ---------------------------------------------------------------------------

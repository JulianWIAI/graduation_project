"""
prompt_data.py — SemanticCipher-Wrapper fuer den Web-Generator.

Kapselt den Zugriff auf die SemanticCipher-Klasse aus dem MUSIC_ARCHITECT_V7-
Projekt und stellt eine einfache decode_prompt()-Funktion bereit.
Plattformunabhaengig (kein Tkinter, keine OS-spezifischen APIs).
"""

from __future__ import annotations

import pathlib
import sys
from typing import Dict, Any
import config

# ---------------------------------------------------------------------------
# MUSIC_ARCHITECT_V7-Pfad — relativ zu dieser Datei berechnet.
# ---------------------------------------------------------------------------
_MA_ROOT = pathlib.Path(config.MA_ROOT)
_MA_SRC  = _MA_ROOT / "src"


def _ensure_ma_path() -> None:
    """Fuegt MA-Pfade zu sys.path hinzu (idempotent)."""
    for p in (str(_MA_ROOT), str(_MA_SRC)):
        if p not in sys.path:
            sys.path.insert(0, p)


# Gecachte SemanticCipher-Instanz — wird beim ersten Aufruf erstellt.
_cipher = None


def _get_cipher():
    """Gibt die gecachte SemanticCipher-Instanz zurueck (lazy init)."""
    global _cipher
    if _cipher is None:
        _ensure_ma_path()
        from src.generation.prompt_decoder import SemanticCipher  # type: ignore
        _cipher = SemanticCipher()
    return _cipher


def decode_prompt(text: str) -> Dict[str, Any]:
    """
    Dekodiert einen natuerlichsprachigen Prompt in Kompositionsparameter.

    Parameter
    ---------
    text : z. B. "Bright POP Song" oder "fast dark trap beat"

    Rueckgabewert
    -------------
    Dict mit den erkannten Parametern:
      genre, bpm, scale_hint, tension_multiplier, complexity, matched_keywords
    Felder, die nicht erkannt wurden, enthalten None.
    Gibt ein leeres Dict zurueck, wenn die SemanticCipher nicht verfuegbar ist.
    """
    if not text or not text.strip():
        return {}

    try:
        cipher = _get_cipher()
        params = cipher.decode_prompt(text)
        return {
            "genre":              params.genre,
            "bpm":                params.bpm,
            "scale_hint":         params.scale_hint,
            "tension_multiplier": params.tension_multiplier,
            "complexity":         params.complexity,
            "matched_keywords":   params.matched_keywords,
            "summary":            params.summary(),
            "is_empty":           params.is_empty(),
        }
    except Exception:
        return {}

"""
timbre_presets.py — Named presets and parameter dataclasses for the built-in synthesiser.

Each percussion role (kick, snare, hihat) and the melodic role has:
  - A params dataclass whose fields map 1-to-1 to UI sliders.
  - A set of named presets.
  - PRESET_DEFAULTS: the "factory" slider values shown before any preset is chosen.

Public API
----------
  list_presets(role)            -> list[str]   — preset names for a role
  get_preset(role, name)        -> dataclass | None
  dict_to_params(role, d)       -> dataclass | None  — convert UI slider dict
  PRESET_DEFAULTS               -> dict[str, dict]   — default slider values per role
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Parameter dataclasses
# ---------------------------------------------------------------------------

@dataclass
class KickParams:
    pitch_start_hz: float = 150.0
    pitch_end_hz: float = 40.0
    duration: float = 0.30
    amp_decay_rate: float = 8.0
    click_level: float = 0.5
    volume: float = 0.80


@dataclass
class SnareParams:
    tone_hz: float = 180.0
    duration: float = 0.20
    tone_level: float = 0.40
    noise_level: float = 0.60
    tone_decay_rate: float = 20.0
    noise_decay_rate: float = 12.0
    volume: float = 0.70


@dataclass
class HihatParams:
    duration: float = 0.08
    is_open: bool = False
    decay_rate: float = 25.0
    volume: float = 0.40


@dataclass
class MelodicParams:
    harmonics: List[float] = field(default_factory=lambda: [1.0, 0.3, 0.1])
    adsr_attack: float = 0.01
    adsr_decay: float = 0.10
    adsr_sustain: float = 0.70
    adsr_release: float = 0.20
    wave_type: str = "sine"
    volume: float = 1.00


# ---------------------------------------------------------------------------
# Named presets
# ---------------------------------------------------------------------------

_KICK_PRESETS: Dict[str, KickParams] = {
    "Punchy":   KickParams(pitch_start_hz=180, pitch_end_hz=45,  duration=0.25, amp_decay_rate=10, click_level=0.6, volume=0.85),
    "Deep":     KickParams(pitch_start_hz=120, pitch_end_hz=30,  duration=0.40, amp_decay_rate=6,  click_level=0.3, volume=0.90),
    "Tight":    KickParams(pitch_start_hz=160, pitch_end_hz=50,  duration=0.18, amp_decay_rate=14, click_level=0.7, volume=0.80),
    "Sub":      KickParams(pitch_start_hz=100, pitch_end_hz=25,  duration=0.50, amp_decay_rate=5,  click_level=0.2, volume=0.95),
    "Acoustic": KickParams(pitch_start_hz=140, pitch_end_hz=38,  duration=0.35, amp_decay_rate=9,  click_level=0.5, volume=0.75),
}

_SNARE_PRESETS: Dict[str, SnareParams] = {
    "Snappy":   SnareParams(tone_hz=200, duration=0.15, tone_level=0.3, noise_level=0.7, tone_decay_rate=25, noise_decay_rate=15, volume=0.75),
    "Fat":      SnareParams(tone_hz=150, duration=0.30, tone_level=0.5, noise_level=0.5, tone_decay_rate=14, noise_decay_rate=8,  volume=0.80),
    "Rimshot":  SnareParams(tone_hz=250, duration=0.10, tone_level=0.6, noise_level=0.4, tone_decay_rate=30, noise_decay_rate=20, volume=0.70),
    "Brush":    SnareParams(tone_hz=160, duration=0.25, tone_level=0.2, noise_level=0.8, tone_decay_rate=18, noise_decay_rate=6,  volume=0.55),
    "Electronic": SnareParams(tone_hz=220, duration=0.18, tone_level=0.4, noise_level=0.6, tone_decay_rate=22, noise_decay_rate=10, volume=0.72),
}

_HIHAT_PRESETS: Dict[str, HihatParams] = {
    "Closed":     HihatParams(duration=0.06,  is_open=False, decay_rate=30, volume=0.35),
    "Open":       HihatParams(duration=0.30,  is_open=True,  decay_rate=5,  volume=0.40),
    "Half-open":  HihatParams(duration=0.15,  is_open=True,  decay_rate=10, volume=0.38),
    "Crisp":      HihatParams(duration=0.05,  is_open=False, decay_rate=40, volume=0.30),
    "Loose":      HihatParams(duration=0.10,  is_open=False, decay_rate=20, volume=0.42),
}

_MELODIC_PRESETS: Dict[str, MelodicParams] = {
    "Piano":    MelodicParams(harmonics=[1.0, 0.5, 0.25, 0.12, 0.06], adsr_attack=0.005, adsr_decay=0.3, adsr_sustain=0.3, adsr_release=0.4, wave_type="sine",   volume=1.0),
    "Bass":     MelodicParams(harmonics=[1.0, 0.7, 0.3],              adsr_attack=0.01,  adsr_decay=0.1, adsr_sustain=0.8, adsr_release=0.1, wave_type="sine",   volume=0.9),
    "Lead":     MelodicParams(harmonics=[1.0, 0.5, 0.3, 0.2, 0.1],   adsr_attack=0.01,  adsr_decay=0.05,adsr_sustain=0.8, adsr_release=0.1, wave_type="saw",    volume=0.85),
    "Pad":      MelodicParams(harmonics=[1.0, 0.3, 0.15, 0.08],      adsr_attack=0.4,   adsr_decay=0.2, adsr_sustain=0.7, adsr_release=0.5, wave_type="sine",   volume=0.8),
    "Strings":  MelodicParams(harmonics=[1.0, 0.4, 0.2, 0.1],        adsr_attack=0.15,  adsr_decay=0.1, adsr_sustain=0.8, adsr_release=0.3, wave_type="sine",   volume=0.85),
    "Pluck":    MelodicParams(harmonics=[1.0, 0.6, 0.4, 0.2, 0.1],   adsr_attack=0.005, adsr_decay=0.3, adsr_sustain=0.2, adsr_release=0.5, wave_type="sine",   volume=0.9),
}

_PRESETS: Dict[str, Dict[str, Any]] = {
    "kick":    _KICK_PRESETS,
    "snare":   _SNARE_PRESETS,
    "hihat":   _HIHAT_PRESETS,
    "melodic": _MELODIC_PRESETS,
}

# Default slider values shown in the UI before any preset is selected.
PRESET_DEFAULTS: Dict[str, Dict[str, Any]] = {
    role: asdict(cls())
    for role, cls in [
        ("kick",    KickParams),
        ("snare",   SnareParams),
        ("hihat",   HihatParams),
        ("melodic", MelodicParams),
    ]
}


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def list_presets(role: str) -> List[str]:
    """Return the names of all named presets for *role*."""
    return list(_PRESETS.get(role, {}).keys())


def get_preset(role: str, name: str) -> Optional[Any]:
    """Return the dataclass for *name* within *role*, or None if not found."""
    return _PRESETS.get(role, {}).get(name)


def dict_to_params(role: str, d: Dict[str, Any]) -> Optional[Any]:
    """
    Convert a flat slider dict from the UI into the appropriate params dataclass.
    Unknown keys are silently ignored; missing keys fall back to dataclass defaults.
    Returns None if *role* is unrecognised or *d* is empty.
    """
    _cls_map = {
        "kick":    KickParams,
        "snare":   SnareParams,
        "hihat":   HihatParams,
        "melodic": MelodicParams,
    }
    cls = _cls_map.get(role)
    if cls is None or not d:
        return None
    import dataclasses
    valid_fields = {f.name for f in dataclasses.fields(cls)}
    filtered = {k: v for k, v in d.items() if k in valid_fields}
    try:
        return cls(**filtered)
    except (TypeError, ValueError):
        return None
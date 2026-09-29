import json
from typing import Any, Dict

_CHROMATIC = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
_CIRCLE = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F']
_ENHARMONIC = {
    'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#',
    'Cb': 'B',  'E#': 'F',  'B#': 'C',  'Fb': 'E',
}

_GROOVE_SWING = {'swing', 'boom_bap', 'lo_fi'}
_GROOVE_TIGHT = {'tight', 'trap', 'modern'}

_WEIGHTS = {'tempo': 0.30, 'key': 0.25, 'genre': 0.20, 'timbral': 0.15, 'groove': 0.10}


def _norm(key: str) -> str:
    if key is None:
        return None
    return _ENHARMONIC.get(key, key)


def _cof_dist(k1: str, k2: str) -> int:
    k1, k2 = _norm(k1), _norm(k2)
    if k1 not in _CIRCLE or k2 not in _CIRCLE:
        return 6
    d = abs(_CIRCLE.index(k1) - _CIRCLE.index(k2))
    return min(d, 12 - d)


def _rel_minor(major: str) -> str:
    k = _norm(major)
    if k not in _CHROMATIC:
        return None
    return _CHROMATIC[(_CHROMATIC.index(k) + 9) % 12]


def _rel_major(minor: str) -> str:
    k = _norm(minor)
    if k not in _CHROMATIC:
        return None
    return _CHROMATIC[(_CHROMATIC.index(k) + 3) % 12]


class Scorer:
    def score(self, sample: Dict[str, Any], song_params: Dict[str, Any]) -> float:
        t  = self._tempo(sample, song_params)
        k  = self._key(sample, song_params)
        g  = self._genre(sample, song_params)
        ti = self._timbral(sample, song_params)
        gr = self._groove(sample, song_params)
        return float(
            t  * _WEIGHTS['tempo']
            + k  * _WEIGHTS['key']
            + g  * _WEIGHTS['genre']
            + ti * _WEIGHTS['timbral']
            + gr * _WEIGHTS['groove']
        )

    def _tempo(self, sample: Dict, song_params: Dict) -> float:
        if sample.get('tempo_free'):
            return 78.0
        sbpm = sample.get('bpm')
        obpm = song_params.get('bpm')
        if sbpm is None or obpm is None:
            return 78.0
        diff = abs(sbpm - obpm)
        if diff < 2:
            return 100.0
        if min(abs(sbpm / 2.0 - obpm), abs(sbpm * 2.0 - obpm)) < 2:
            return 90.0
        if diff < 5:
            return 70.0
        if diff < 10:
            return 50.0
        return 20.0

    def _key(self, sample: Dict, song_params: Dict) -> float:
        if sample.get('key_agnostic'):
            return 78.0
        sk = _norm(sample.get('key_root'))
        sm = sample.get('key_mode')
        ok = _norm(song_params.get('key'))
        om = song_params.get('key_mode')
        if sk is None or ok is None:
            return 78.0
        if sk == ok and sm == om:
            return 100.0
        if sm == 'major' and om == 'minor' and _rel_minor(sk) == ok:
            return 90.0
        if sm == 'minor' and om == 'major' and _rel_major(sk) == ok:
            return 90.0
        if sk == ok:
            return 80.0
        dist = _cof_dist(sk, ok)
        if dist == 1:
            return 70.0
        if dist == 2:
            return 55.0
        return 15.0

    def _genre(self, sample: Dict, song_params: Dict) -> float:
        genre = song_params.get('genre')
        raw = sample.get('genre_affinity') or '{}'
        try:
            affinity: Dict[str, float] = json.loads(raw) if isinstance(raw, str) else raw
        except (json.JSONDecodeError, TypeError):
            affinity = {}
        if not genre or genre not in affinity:
            return 70.0
        return float(min(100.0, max(0.0, affinity[genre])))

    def _timbral(self, sample: Dict, song_params: Dict) -> float:
        fx = (song_params.get('fx_variant') or 'NEUTRAL').upper()
        centroid = float(sample.get('spectral_centroid') or 0.0)
        norm = min(centroid / 8000.0, 1.0)
        if fx == 'BRIGHT':
            return norm * 100.0
        if fx == 'DARK':
            return (1.0 - norm) * 100.0
        return 78.0

    def _groove(self, sample: Dict, song_params: Dict) -> float:
        feel = (song_params.get('groove_feel') or 'default').lower()
        ts = float(sample.get('transient_strength') or 0.0)
        if feel in _GROOVE_SWING:
            return (1.0 - min(ts, 1.0)) * 100.0
        if feel in _GROOVE_TIGHT:
            return min(ts, 1.0) * 100.0
        return 78.0

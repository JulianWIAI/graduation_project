import logging
from typing import Any, Dict, List, Optional

from src.data.database import Database
from src.gui.styles import SETUP_ROLES, SLOT_TO_CLASSIFIER_ROLES
from src.matching.scorer import Scorer
from src.matching.cross_track import CrossTrack

logger = logging.getLogger(__name__)

_TOP_N = 20
_MIN_CANDIDATES = 5
_MAX_OVERLAP = 4


class SetupGenerator:
    def __init__(self, db: Database):
        self._db = db
        self._scorer = Scorer()
        self._cross = CrossTrack()

    def generate(
        self,
        song_params: Dict[str, Any],
        n_setups: int = 5,
        exclude_fps: Optional[set] = None,
    ) -> Dict[str, Any]:
        exclude_fps = exclude_fps or set()

        candidates: Dict[str, List[Dict]] = {}
        warnings: List[Dict] = []

        for role in SETUP_ROLES:
            classifier_tags = SLOT_TO_CLASSIFIER_ROLES.get(role, [role])
            pool = []
            for tag in classifier_tags:
                pool.extend(self._db.get_by_role(tag))
            pool = [s for s in pool if s['file_path'] not in exclude_fps]
            scored = []
            for s in pool:
                s['_score'] = self._scorer.score(s, song_params)
                scored.append(s)
            scored.sort(key=lambda x: x['_score'], reverse=True)
            top = scored[:_TOP_N]
            candidates[role] = top
            if len(top) < _MIN_CANDIDATES:
                warnings.append({'role': role, 'candidates': len(top)})

        setups = self._build_setups(candidates, n_setups)

        for setup in setups:
            track_pairs = [
                (role, setup['tracks'][role]['sample'])
                for role in SETUP_ROLES
                if role in setup['tracks']
            ]
            penalty = self._cross.score(track_pairs)
            raw_mean = (
                sum(t['score'] for t in setup['tracks'].values()) / len(setup['tracks'])
                if setup['tracks'] else 0.0
            )
            setup['score'] = round(raw_mean * (1.0 - penalty), 1)

        setups.sort(key=lambda s: s['score'], reverse=True)
        for i, s in enumerate(setups):
            s['rank'] = i + 1

        return {
            'setups': setups,
            'all_candidates': candidates,
            'warnings': warnings,
        }

    def _build_setups(
        self, candidates: Dict[str, List[Dict]], n_setups: int
    ) -> List[Dict]:
        setups: List[Dict] = []

        for setup_idx in range(n_setups):
            tracks: Dict[str, Dict] = {}

            for role in SETUP_ROLES:
                pool = candidates.get(role, [])
                if not pool:
                    continue

                used_fps = {s['tracks'].get(role, {}).get('file') for s in setups}
                chosen = None
                for cand in pool:
                    if cand['file_path'] not in used_fps:
                        chosen = cand
                        break
                if chosen is None:
                    chosen = pool[0]

                tracks[role] = {
                    'file':   chosen['file_path'],
                    'score':  round(float(chosen.get('_score', 0.0)), 1),
                    'bpm':    chosen.get('bpm'),
                    'key':    chosen.get('key_root'),
                    'sample': chosen,
                }

            overlaps = self._calc_overlap(tracks, setups)
            setups.append({
                'rank':         setup_idx + 1,
                'score':        0.0,
                'tracks':       tracks,
                'warnings':     [],
                'overlap_with': overlaps,
            })

        return setups

    def _calc_overlap(
        self, tracks: Dict[str, Dict], previous: List[Dict]
    ) -> List[int]:
        overlapping = []
        for prev in previous:
            shared = sum(
                1 for role in SETUP_ROLES
                if tracks.get(role, {}).get('file') == prev['tracks'].get(role, {}).get('file')
            )
            if shared > _MAX_OVERLAP:
                overlapping.append(prev['rank'])
        return overlapping

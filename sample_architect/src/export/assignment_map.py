import json
import pathlib
from datetime import datetime
from typing import Any, Dict

from src.data.database import Database


class AssignmentMap:
    def __init__(self, db: Database):
        self._db = db

    def export_setup(
        self,
        setup: Dict[str, Any],
        song_params: Dict[str, Any],
        output_path: pathlib.Path,
    ) -> pathlib.Path:
        assignments: Dict[str, str] = {}
        scores: Dict[str, float] = {}

        for role, track in setup.get('tracks', {}).items():
            fp = track.get('file')
            if fp:
                assignments[role] = fp
                scores[role] = track.get('score', 0.0)

        payload = {
            'song_params': song_params,
            'assignments': assignments,
            'scores': scores,
            'setup_score': setup.get('score', 0.0),
            'exported_at': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, indent=2), encoding='utf-8')

        genre = song_params.get('genre', '')
        for role, fp in assignments.items():
            self._db.update_genre_affinity(fp, genre, 5.0)
            self._db.mark_used(fp, genre)

        return output_path

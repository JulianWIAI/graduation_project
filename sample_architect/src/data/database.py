import sqlite3
import json
import pathlib
from datetime import datetime
from typing import Any, Dict, List, Optional


class Database:
    def __init__(self, db_path: pathlib.Path):
        self._path = db_path
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self._path), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _run(self, fn):
        """Execute fn(conn) with an auto-closing connection."""
        conn = self._connect()
        try:
            return fn(conn)
        finally:
            conn.close()

    def _init_schema(self):
        schema_path = pathlib.Path(__file__).parent / 'schema.sql'
        sql = schema_path.read_text()
        self._run(lambda c: c.executescript(sql))

    def get_by_role(self, role: str) -> List[Dict[str, Any]]:
        rows = self._run(lambda c: c.execute(
            "SELECT * FROM samples WHERE COALESCE(user_role, inferred_role) = ?",
            (role,),
        ).fetchall())
        return [dict(r) for r in rows]

    def upsert_sample(self, props: Dict[str, Any]):
        keys = list(props.keys())
        cols = ', '.join(keys)
        placeholders = ', '.join('?' for _ in keys)
        updates = ', '.join(
            f"{k} = excluded.{k}" for k in keys if k != 'file_path'
        )
        sql = (
            f"INSERT INTO samples ({cols}) VALUES ({placeholders}) "
            f"ON CONFLICT(file_path) DO UPDATE SET {updates}"
        )
        values = list(props.values())

        def _do(c):
            c.execute(sql, values)
            c.commit()

        self._run(_do)

    def update_role(self, file_path: str, role: str):
        def _do(c):
            c.execute("UPDATE samples SET user_role = ? WHERE file_path = ?",
                      (role, file_path))
            c.commit()
        self._run(_do)

    def update_genre_affinity(self, file_path: str, genre: str, delta: float):
        def _do(c):
            row = c.execute(
                "SELECT genre_affinity FROM samples WHERE file_path = ?",
                (file_path,),
            ).fetchone()
            if row is None:
                return
            affinity: Dict[str, float] = json.loads(row['genre_affinity'] or '{}')
            affinity[genre] = min(100.0, affinity.get(genre, 50.0) + delta)
            c.execute(
                "UPDATE samples SET genre_affinity = ? WHERE file_path = ?",
                (json.dumps(affinity), file_path),
            )
            c.commit()
        self._run(_do)

    def mark_used(self, file_path: str, genre: str):
        def _do(c):
            c.execute(
                """UPDATE samples
                   SET times_used = times_used + 1, last_used_at = ?
                   WHERE file_path = ?""",
                (datetime.utcnow().isoformat(), file_path),
            )
            c.commit()
        self._run(_do)

    def get_stats(self) -> Dict[str, int]:
        rows = self._run(lambda c: c.execute(
            """SELECT COALESCE(user_role, inferred_role) AS role, COUNT(*) AS cnt
               FROM samples GROUP BY role"""
        ).fetchall())
        return {r['role']: r['cnt'] for r in rows if r['role']}

    def get_all_samples(self) -> List[Dict[str, Any]]:
        rows = self._run(lambda c: c.execute(
            "SELECT * FROM samples ORDER BY file_name COLLATE NOCASE"
        ).fetchall())
        return [dict(r) for r in rows]

    def file_exists(self, file_path: str) -> bool:
        row = self._run(lambda c: c.execute(
            "SELECT 1 FROM samples WHERE file_path = ?", (file_path,)
        ).fetchone())
        return row is not None

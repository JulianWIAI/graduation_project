import logging
import threading
import pathlib
from datetime import datetime
from typing import Callable, Optional

from src.analysis.audio_analyser import AudioAnalyser, SUPPORTED_ALL
from src.analysis.role_classifier import RoleClassifier
from src.data.database import Database

logger = logging.getLogger(__name__)


class LibraryScanner:
    def __init__(self, db: Database):
        self._db = db
        self._analyser = AudioAnalyser()
        self._classifier = RoleClassifier()
        self._running = False

    def scan(
        self,
        folder: pathlib.Path,
        progress_cb: Optional[Callable[[int, int, str], None]] = None,
        done_cb: Optional[Callable[[int, int, int], None]] = None,
    ):
        thread = threading.Thread(
            target=self._scan_thread,
            args=(folder, progress_cb, done_cb),
            daemon=True,
        )
        thread.start()

    def _scan_thread(
        self,
        folder: pathlib.Path,
        progress_cb: Optional[Callable],
        done_cb: Optional[Callable],
    ):
        self._running = True
        audio_files = [
            p
            for p in folder.rglob('*')
            if p.is_file() and p.suffix.lower() in SUPPORTED_ALL
        ]
        total = len(audio_files)
        added = skipped = errors = 0

        for i, file_path in enumerate(audio_files):
            if not self._running:
                break
            if progress_cb:
                progress_cb(i + 1, total, file_path.name)
            if self._db.file_exists(str(file_path)):
                skipped += 1
                continue
            props = self._analyser.analyse(file_path)
            if props is None:
                errors += 1
                logger.warning("Skipping unanalysable file: %s", file_path.name)
                continue
            role = self._classifier.classify(props)
            props['inferred_role'] = role
            props['added_at'] = datetime.utcnow().isoformat()
            try:
                self._db.upsert_sample(props)
                added += 1
            except Exception as exc:
                logger.warning("DB write failed for %s: %s", file_path.name, exc)
                errors += 1

        self._running = False
        if done_cb:
            done_cb(added, skipped, errors)

    def stop(self):
        self._running = False

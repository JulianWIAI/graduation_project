import json
import logging
import pathlib
from typing import Any, Dict, Optional

import numpy as np

logger = logging.getLogger(__name__)

SUPPORTED_SOUNDFILE = {'.wav', '.aiff', '.aif', '.flac'}
SUPPORTED_PYDUB = {'.mp3', '.ogg'}
SUPPORTED_ALL = SUPPORTED_SOUNDFILE | SUPPORTED_PYDUB

_NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

_MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09,
                            2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
_MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53,
                            2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

ANALYSIS_VERSION = 1
_TARGET_SR = 22050
_HOP = 512


class AudioAnalyser:
    def analyse(self, file_path: pathlib.Path) -> Optional[Dict[str, Any]]:
        try:
            return self._analyse(file_path)
        except Exception as exc:
            logger.warning("Analysis failed for %s: %s", file_path.name, exc)
            return None

    def _analyse(self, file_path: pathlib.Path) -> Dict[str, Any]:
        import librosa

        y, sr = self._load_audio(file_path)
        duration_s = len(y) / sr
        duration_ms = duration_s * 1000.0

        bpm, bpm_confidence = self._detect_bpm(y, sr)
        key_root, key_mode, key_confidence = self._detect_key(y, sr)

        rms_frames = librosa.feature.rms(y=y, frame_length=2048, hop_length=_HOP)[0]
        frame_times = librosa.frames_to_time(np.arange(len(rms_frames)), sr=sr, hop_length=_HOP)
        attack_ms, decay_ms = self._attack_decay(rms_frames, frame_times)

        rms_mean = float(np.sqrt(np.mean(y ** 2)))

        centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=_HOP)
        spectral_centroid = float(np.mean(centroid))

        onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=_HOP)
        transient_strength = float(np.clip(np.max(onset_env) / 10.0, 0.0, 1.0))

        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=_HOP)
        mfcc_mean = np.mean(mfcc, axis=1).tolist()

        is_loop = bool(duration_s > 2.0 and bpm_confidence > 0.6)
        tempo_free = bool(bpm_confidence < 0.4)
        key_agnostic = bool(key_confidence < 0.35)

        return {
            'file_path': str(file_path),
            'file_name': file_path.name,
            'bpm': float(bpm) if bpm is not None else None,
            'bpm_confidence': float(bpm_confidence),
            'tempo_free': int(tempo_free),
            'key_root': key_root if not key_agnostic else None,
            'key_mode': key_mode if not key_agnostic else None,
            'key_agnostic': int(key_agnostic),
            'key_confidence': float(key_confidence),
            'spectral_centroid': spectral_centroid,
            'transient_strength': transient_strength,
            'attack_ms': attack_ms,
            'decay_ms': decay_ms,
            'is_loop': int(is_loop),
            'duration_ms': duration_ms,
            'rms': rms_mean,
            'mfcc': json.dumps(mfcc_mean),
            'analysis_version': ANALYSIS_VERSION,
        }

    def _load_audio(self, file_path: pathlib.Path):
        import librosa
        ext = file_path.suffix.lower()
        if ext in SUPPORTED_SOUNDFILE:
            y, sr = librosa.load(str(file_path), sr=_TARGET_SR, mono=True)
        elif ext in SUPPORTED_PYDUB:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(str(file_path))
            orig_sr = audio.frame_rate
            samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
            if audio.channels > 1:
                samples = samples.reshape(-1, audio.channels).mean(axis=1)
            max_val = float(np.max(np.abs(samples)))
            if max_val > 0:
                samples /= max_val
            if orig_sr != _TARGET_SR:
                samples = librosa.resample(samples, orig_sr=orig_sr, target_sr=_TARGET_SR)
            y = samples
            sr = _TARGET_SR
        else:
            raise ValueError(f"Unsupported format: {ext}")
        return y, sr

    def _detect_bpm(self, y, sr):
        import librosa
        result = librosa.beat.beat_track(y=y, sr=sr)
        tempo = result[0]
        beat_frames = result[1]
        if hasattr(tempo, '__len__'):
            tempo = float(tempo[0]) if len(tempo) > 0 else 120.0
        else:
            tempo = float(tempo)

        if len(beat_frames) > 2:
            beat_times = librosa.frames_to_time(beat_frames, sr=sr)
            ibis = np.diff(beat_times)
            mean_ibi = float(np.mean(ibis))
            if mean_ibi > 0:
                cv = float(np.std(ibis)) / mean_ibi
                confidence = float(np.clip(1.0 - cv * 2.0, 0.0, 1.0))
            else:
                confidence = 0.0
        else:
            confidence = 0.0

        return tempo, confidence

    def _detect_key(self, y, sr):
        import librosa
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)

        best_score = -np.inf
        best_key = 'C'
        best_mode = 'major'

        for i, note in enumerate(_NOTE_NAMES):
            rotated = np.roll(chroma_mean, -i)
            major_corr = float(np.corrcoef(rotated, _MAJOR_PROFILE)[0, 1])
            minor_corr = float(np.corrcoef(rotated, _MINOR_PROFILE)[0, 1])
            if major_corr > best_score:
                best_score = major_corr
                best_key = note
                best_mode = 'major'
            if minor_corr > best_score:
                best_score = minor_corr
                best_key = note
                best_mode = 'minor'

        key_confidence = float((best_score + 1.0) / 2.0)
        return best_key, best_mode, key_confidence

    def _attack_decay(self, rms_frames, frame_times):
        if len(rms_frames) == 0:
            return 0.0, 0.0

        peak_idx = int(np.argmax(rms_frames))
        attack_ms = float(frame_times[peak_idx] * 1000.0)

        peak_val = float(rms_frames[peak_idx])
        threshold = peak_val * (10 ** (-20.0 / 20.0))
        decay_end_idx = min(peak_idx + 1, len(rms_frames) - 1)
        for i in range(peak_idx + 1, len(rms_frames)):
            if rms_frames[i] <= threshold:
                decay_end_idx = i
                break

        decay_ms = max(0.0, float((frame_times[decay_end_idx] - frame_times[peak_idx]) * 1000.0))
        return attack_ms, decay_ms

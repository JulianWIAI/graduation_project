from typing import Any, Dict, List, Tuple


class CrossTrack:
    _MELODIC = {'bass', 'chords', 'lead', 'pad', 'arp', 'stabs', 'texture', 'fx'}

    def score(self, tracks: List[Tuple[str, Dict[str, Any]]]) -> float:
        penalty = 0.0

        melodic = [(r, s) for r, s in tracks if r in self._MELODIC]
        kicks   = [s for r, s in tracks if r == 'drums']
        basses  = [s for r, s in tracks if r == 'bass']

        # P1: sub-bass exclusivity — kick + bass both below 300 Hz
        for kick in kicks:
            for bass in basses:
                kc = float(kick.get('spectral_centroid') or 0.0)
                bc = float(bass.get('spectral_centroid') or 0.0)
                if kc < 300 and bc < 300:
                    penalty += 0.10
                    break

        # P2: register monotonicity — any pair of melodic tracks sharing key + centroid within 800 Hz
        found = False
        for i in range(len(melodic)):
            if found:
                break
            for j in range(i + 1, len(melodic)):
                _, s1 = melodic[i]
                _, s2 = melodic[j]
                k1 = s1.get('key_root')
                k2 = s2.get('key_root')
                c1 = float(s1.get('spectral_centroid') or 0.0)
                c2 = float(s2.get('spectral_centroid') or 0.0)
                if k1 and k2 and k1 == k2 and abs(c1 - c2) < 800:
                    penalty += 0.15
                    found = True
                    break

        # Density: more than 3 melodic tracks with attack_ms < 20
        stabs = sum(1 for _, s in melodic if float(s.get('attack_ms') or 0.0) < 20)
        if stabs > 3:
            penalty += 0.10

        # Adjacent centroid clash: +0.05 per adjacent melodic pair within 500 Hz
        centroids = [float(s.get('spectral_centroid') or 0.0) for _, s in melodic]
        for i in range(len(centroids) - 1):
            if abs(centroids[i] - centroids[i + 1]) < 500:
                penalty += 0.05

        return float(min(penalty, 0.4))

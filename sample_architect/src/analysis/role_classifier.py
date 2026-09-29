from typing import Any, Dict


class RoleClassifier:
    def classify(self, props: Dict[str, Any]) -> str:
        ts = float(props.get('transient_strength') or 0.0)
        centroid = float(props.get('spectral_centroid') or 0.0)
        dur = float(props.get('duration_ms') or 0.0)
        is_loop = bool(props.get('is_loop', 0))
        attack = float(props.get('attack_ms') or 0.0)

        if ts > 0.7 and centroid < 400 and dur < 800:
            return 'kick'
        elif ts > 0.6 and 400 <= centroid <= 2000 and dur < 600:
            return 'snare'
        elif ts > 0.5 and centroid > 5000 and dur < 400:
            return 'hihat'
        elif ts > 0.5 and 1000 <= centroid <= 6000 and dur < 1000:
            return 'percussion'
        elif is_loop and centroid < 500 and attack < 50:
            return 'bass'
        elif is_loop and 500 <= centroid <= 3000 and attack > 30:
            return 'chords'
        elif is_loop and attack > 200 and centroid < 4000:
            return 'pad'
        elif is_loop and centroid > 2000 and not (attack > 200 and centroid < 4000):
            return 'lead'
        elif is_loop and ts > 0.3 and dur < 4000:
            return 'arp'
        elif ts > 0.4 and dur < 1500:
            return 'stabs'
        elif is_loop and attack > 500:
            return 'texture'
        else:
            return 'fx'

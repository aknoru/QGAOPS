"""
LIVE HAND GA ENGINE — hand_detection/gesture.py
Static Hand Pose Recognition.

[IMPLEMENTED] Rule-based recognition using normalized landmark geometry.
[IMPLEMENTED] 14+ poses recognized via configurable feature thresholds.

Recognized poses:
    OPEN_PALM, FIST, THUMBS_UP, THUMBS_DOWN,
    INDEX_POINT, TWO_FINGER, THREE_FINGER, FOUR_FINGER,
    PINCH, OK_SIGN, ROCK_SIGN, PEACE_SIGN, CALL_ME, UNKNOWN
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np

from .landmarks import HandGeometry, FINGER_NAMES


@dataclass
class GestureResult:
    """Result of static hand pose recognition.

    Attributes:
        pose:       Recognized pose name.
        confidence: Confidence in [0, 1] from feature margin analysis.
        stability:  How consistent this is over recent frames (set externally).
        features:   Dict of computed feature values (for debugging).
    """
    pose:       str
    confidence: float
    stability:  float = 1.0
    features:   Dict[str, float] = None   # type: ignore

    def __post_init__(self) -> None:
        if self.features is None:
            self.features = {}


class StaticPoseRecognizer:
    """Rule-based static hand pose recognizer.

    [IMPLEMENTED]

    Uses normalized geometric features extracted from HandGeometry:
        - finger extension state (wrist-to-tip distance vs. finger length)
        - fingertip-to-palm distance
        - thumb-index pinch distance
        - inter-finger angles
        - palm orientation

    Thresholds are configurable.
    """

    def __init__(
        self,
        pinch_threshold:  float = 0.05,
        open_threshold:   float = 0.15,
        fist_threshold:   float = 0.08,
        curl_threshold:   float = 0.06,
        confidence_min:   float = 0.60,
    ) -> None:
        self.pinch_threshold  = pinch_threshold
        self.open_threshold   = open_threshold
        self.fist_threshold   = fist_threshold
        self.curl_threshold   = curl_threshold
        self.confidence_min   = confidence_min

    # ------------------------------------------------------------------
    # Feature extraction
    # ------------------------------------------------------------------

    def _finger_extended(self, geom: HandGeometry) -> Dict[str, bool]:
        """Classify each finger as extended (True) or curled (False).

        [IMPLEMENTED]
        Heuristic: wrist-to-tip distance > threshold * finger_length
        """
        result = {}
        for fname in FINGER_NAMES:
            w2t  = geom.wrist_to_tip_dists.get(fname, 0.0)
            flen = geom.finger_lengths.get(fname, 1.0)
            if flen < 1e-8:
                result[fname] = False
                continue
            ratio = w2t / (flen + 1e-8)
            result[fname] = ratio > 0.65
        return result

    def _finger_curl(self, geom: HandGeometry) -> Dict[str, float]:
        """Compute curl score per finger (0 = straight, 1 = fully curled)."""
        result = {}
        for fname in FINGER_NAMES:
            angles = geom.joint_angles.get(fname, [])
            if not angles:
                result[fname] = 0.0
                continue
            # Average joint angle; 0 = straight, pi/2 = curled
            avg = float(np.mean(angles))
            result[fname] = float(np.clip(avg / (np.pi / 2), 0.0, 1.0))
        return result

    def _thumb_index_distance(self, geom: HandGeometry) -> float:
        """Normalized thumb-index fingertip distance."""
        return geom.fingertip_distances.get(("thumb", "index"), 1.0)

    def _hand_openness(self, geom: HandGeometry) -> float:
        """Average wrist-to-tip distance (proxy for openness)."""
        dists = [geom.wrist_to_tip_dists.get(f, 0.0) for f in FINGER_NAMES]
        return float(np.mean(dists))

    # ------------------------------------------------------------------
    # Individual pose detectors
    # ------------------------------------------------------------------

    def _is_open_palm(
        self, ext: Dict[str, bool], geom: HandGeometry
    ) -> float:
        """All 5 fingers extended."""
        dist = self._thumb_index_distance(geom)
        if dist < self.pinch_threshold * 1.3:
            # Thumb and index are touching in circle -> OK_SIGN or PINCH, not OPEN_PALM
            return 0.3
        score = sum(1 for f in FINGER_NAMES if ext[f]) / 5.0
        return score

    def _is_fist(
        self, ext: Dict[str, bool], curl: Dict[str, float], geom: HandGeometry
    ) -> float:
        """All fingers curled, low wrist-to-tip."""
        not_ext = sum(1 for f in FINGER_NAMES if not ext[f]) / 5.0
        avg_curl = float(np.mean([curl[f] for f in FINGER_NAMES]))
        return 0.5 * not_ext + 0.5 * avg_curl

    def _is_thumbs_up(
        self, ext: Dict[str, bool], geom: HandGeometry
    ) -> float:
        """Thumb extended, all other fingers curled."""
        thumb_ok = ext["thumb"]
        others_curled = all(not ext[f] for f in FINGER_NAMES if f != "thumb")
        # Thumb should point roughly upward (negative y in image coords)
        thumb_v = geom.finger_vectors.get("thumb", np.zeros(3))
        up_score = float(np.clip(-thumb_v[1], 0.0, 1.0))  # -y = up in image
        if thumb_ok and others_curled:
            return 0.6 + 0.4 * up_score
        return 0.0

    def _is_thumbs_down(
        self, ext: Dict[str, bool], curl: Dict[str, float], geom: HandGeometry
    ) -> float:
        """Thumb extended downward, fingers curled."""
        others_curled = all(not ext[f] for f in ["index", "middle", "ring", "pinky"])
        thumb_v = geom.finger_vectors.get("thumb", np.zeros(3))
        is_down = thumb_v[1] > 0.35
        thumb_straight = curl.get("thumb", 1.0) < 0.65
        if is_down and others_curled and thumb_straight:
            return 0.70 + 0.30 * float(np.clip(thumb_v[1], 0.0, 1.0))
        return 0.0

    def _is_index_point(
        self, ext: Dict[str, bool], geom: HandGeometry
    ) -> float:
        """Index extended, others curled, thumb not touching index."""
        dist = self._thumb_index_distance(geom)
        if dist < self.pinch_threshold:
            return 0.0
        idx_ok = ext["index"]
        others = all(not ext[f] for f in ["middle", "ring", "pinky"])
        if idx_ok and others:
            return 0.92
        return 0.0

    def _is_two_finger(
        self, ext: Dict[str, bool], geom: HandGeometry
    ) -> float:
        """Index + middle extended together (<16 deg spread), others curled."""
        ok = ext["index"] and ext["middle"]
        others = not ext["ring"] and not ext["pinky"]
        if ok and others:
            angle = geom.inter_finger_angles.get(("index", "middle"), 0.0)
            if angle < np.radians(16):
                return 0.95
            return 0.2
        return 0.0

    def _is_three_finger(
        self, ext: Dict[str, bool], geom: HandGeometry
    ) -> float:
        """Index + middle + ring extended."""
        ok = ext["index"] and ext["middle"] and ext["ring"]
        if ok and not ext["pinky"]:
            return 0.88
        return 0.0

    def _is_four_finger(
        self, ext: Dict[str, bool], geom: HandGeometry
    ) -> float:
        """Index + middle + ring + pinky, thumb curled."""
        ok = ext["index"] and ext["middle"] and ext["ring"] and ext["pinky"]
        if ok and not ext["thumb"]:
            return 0.88
        return 0.0

    def _is_pinch(self, ext: Dict[str, bool], geom: HandGeometry) -> float:
        """Thumb and index tips close together (<5 cm), middle/ring curled."""
        dist = self._thumb_index_distance(geom)
        if dist < self.pinch_threshold:
            curled_others = not ext["middle"] and not ext["ring"]
            if curled_others:
                return 0.95 - 0.10 * (dist / self.pinch_threshold)
            return 0.4
        return 0.0

    def _is_ok_sign(
        self, ext: Dict[str, bool], geom: HandGeometry
    ) -> float:
        """Thumb + index circle pinch, middle + ring + pinky extended."""
        dist = self._thumb_index_distance(geom)
        others = ext["middle"] and ext["ring"] and ext["pinky"]
        if dist < self.pinch_threshold * 1.5 and others:
            return 0.98
        return 0.0

    def _is_rock_sign(
        self, ext: Dict[str, bool], geom: HandGeometry
    ) -> float:
        """Index + pinky extended, middle + ring curled."""
        ok = ext["index"] and ext["pinky"]
        curled = not ext["middle"] and not ext["ring"]
        if ok and curled:
            return 0.85
        return 0.0

    def _is_peace_sign(
        self, ext: Dict[str, bool], geom: HandGeometry
    ) -> float:
        """Index + middle extended with wide spread (>16 deg from wrist / victory)."""
        ok = ext["index"] and ext["middle"]
        others = not ext["ring"] and not ext["pinky"]
        if ok and others:
            angle = geom.inter_finger_angles.get(("index", "middle"), 0.0)
            if angle >= np.radians(16):
                spread = float(np.clip((angle - np.radians(16)) / np.radians(15), 0.0, 1.0))
                return 0.85 + 0.15 * spread
        return 0.0

    def _is_call_me(
        self, ext: Dict[str, bool], geom: HandGeometry
    ) -> float:
        """Thumb + pinky extended (phone gesture)."""
        ok = ext["thumb"] and ext["pinky"]
        curled = not ext["index"] and not ext["middle"] and not ext["ring"]
        if ok and curled:
            return 0.85
        return 0.0

    # ------------------------------------------------------------------
    # Main recognition
    # ------------------------------------------------------------------

    def recognize(self, geom: HandGeometry) -> GestureResult:
        """Recognize static pose from HandGeometry.

        [IMPLEMENTED]

        Returns:
            GestureResult with pose name and confidence.
        """
        ext  = self._finger_extended(geom)
        curl = self._finger_curl(geom)

        candidates: List[Tuple[str, float]] = [
            ("OPEN_PALM",   self._is_open_palm(ext, geom)),
            ("FIST",        self._is_fist(ext, curl, geom)),
            ("THUMBS_UP",   self._is_thumbs_up(ext, geom)),
            ("THUMBS_DOWN", self._is_thumbs_down(ext, curl, geom)),
            ("INDEX_POINT", self._is_index_point(ext, geom)),
            ("TWO_FINGER",  self._is_two_finger(ext, geom)),
            ("THREE_FINGER",self._is_three_finger(ext, geom)),
            ("FOUR_FINGER", self._is_four_finger(ext, geom)),
            ("PINCH",       self._is_pinch(ext, geom)),
            ("OK_SIGN",     self._is_ok_sign(ext, geom)),
            ("ROCK_SIGN",   self._is_rock_sign(ext, geom)),
            ("PEACE_SIGN",  self._is_peace_sign(ext, geom)),
            ("CALL_ME",     self._is_call_me(ext, geom)),
        ]

        best_pose, best_conf = max(candidates, key=lambda x: x[1])

        if best_conf < self.confidence_min:
            best_pose = "UNKNOWN"
            best_conf = 0.0

        features = {
            "open_palm": candidates[0][1],
            "fist": candidates[1][1],
            "pinch": candidates[8][1],
            "openness": self._hand_openness(geom),
            "thumb_idx_dist": self._thumb_index_distance(geom),
            "ext_thumb": float(ext["thumb"]),
            "ext_index": float(ext["index"]),
            "ext_middle": float(ext["middle"]),
            "ext_ring": float(ext["ring"]),
            "ext_pinky": float(ext["pinky"]),
        }

        return GestureResult(
            pose=best_pose,
            confidence=float(np.clip(best_conf, 0.0, 1.0)),
            features=features,
        )

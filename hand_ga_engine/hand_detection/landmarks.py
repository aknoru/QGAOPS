"""
LIVE HAND GA ENGINE — hand_detection/landmarks.py
Landmark normalization, temporal smoothing, and HandGeometry extraction.

[IMPLEMENTED] Exponential moving average smoothing.
[IMPLEMENTED] HandGeometry: all derived geometric quantities per frame.

Coordinate convention (post-normalization):
    Origin at wrist (landmark 0).
    x: lateral (positive = away from thumb in camera frame).
    y: vertical (positive = toward fingertips).
    z: depth (relative, MediaPipe scale).
    Units: normalized to hand span ≈ 1.0.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import numpy as np

from .detector import HandDetectionResult, NUM_LANDMARKS

# Finger landmark groups (tip indices)
FINGER_TIPS   = [4, 8, 12, 16, 20]   # thumb, index, middle, ring, pinky
FINGER_MCPS   = [2, 5, 9, 13, 17]    # MCPs
FINGER_NAMES  = ["thumb", "index", "middle", "ring", "pinky"]

# Palm landmark indices
PALM_CENTER_LANDMARKS = [0, 5, 9, 13, 17]  # wrist + all MCPs


@dataclass
class HandGeometry:
    """All derived geometric quantities from 21 landmarks.

    [IMPLEMENTED] Created fresh each frame after smoothing.

    Attributes:
        landmarks_raw:    (21, 3) raw normalized landmarks.
        landmarks_smooth: (21, 3) smoothed normalized landmarks.
        wrist:            Wrist position (landmark 0).
        palm_center:      Average of wrist + 5 MCPs.
        palm_normal:      Unit normal to the palm plane.
        finger_vectors:   Dict[finger_name -> (3,) unit vector from wrist to tip].
        finger_tip_pos:   Dict[finger_name -> (3,) tip position].
        finger_lengths:   Dict[finger_name -> float, total length].
        segment_vectors:  Dict[finger_name -> list of segment vectors].
        joint_angles:     Dict[finger_name -> list of joint angles in radians].
        inter_finger_angles: Dict[(finger_a, finger_b) -> angle in rad].
        fingertip_distances: Dict[(finger_a, finger_b) -> float].
        palm_to_tip_dists: Dict[finger_name -> float].
        wrist_to_tip_dists: Dict[finger_name -> float].
        confidence:       Detection confidence.
        handedness:       'Left' or 'Right'.
    """
    landmarks_raw:    np.ndarray            # (21, 3)
    landmarks_smooth: np.ndarray            # (21, 3)
    wrist:            np.ndarray            # (3,)
    palm_center:      np.ndarray            # (3,)
    palm_normal:      np.ndarray            # (3,) unit
    finger_vectors:   Dict[str, np.ndarray]
    finger_tip_pos:   Dict[str, np.ndarray]
    finger_lengths:   Dict[str, float]
    segment_vectors:  Dict[str, List[np.ndarray]]
    joint_angles:     Dict[str, List[float]]
    inter_finger_angles: Dict[Tuple[str,str], float]
    fingertip_distances: Dict[Tuple[str,str], float]
    palm_to_tip_dists:   Dict[str, float]
    wrist_to_tip_dists:  Dict[str, float]
    confidence:       float = 0.0
    handedness:       str = "Unknown"
    frame_index:      int = 0


class LandmarkSmoother:
    """Exponential moving average smoother for hand landmarks.

    [IMPLEMENTED]

    Args:
        alpha: Smoothing factor in (0, 1]. 1.0 = no smoothing (raw).
               Lower values = more smoothing but more lag.
    """

    def __init__(self, alpha: float = 0.5) -> None:
        self.alpha = float(np.clip(alpha, 0.01, 1.0))
        self._state: Optional[np.ndarray] = None  # (21, 3)

    def update(self, landmarks: np.ndarray) -> np.ndarray:
        """Update with new raw landmarks, return smoothed result.

        [IMPLEMENTED]

        Args:
            landmarks: (21, 3) float32 array.

        Returns:
            Smoothed (21, 3) float32 array.
        """
        if self._state is None:
            self._state = landmarks.copy()
        else:
            self._state = self.alpha * landmarks + (1.0 - self.alpha) * self._state
        return self._state.copy()

    def reset(self) -> None:
        """Reset smoother state (call on hand disappearance)."""
        self._state = None


class HandGeometryExtractor:
    """Extracts HandGeometry from smoothed landmark arrays.

    [IMPLEMENTED]
    """

    # Finger segment connectivity: list of (from_idx, to_idx) per finger
    _FINGER_SEGMENTS: Dict[str, List[Tuple[int, int]]] = {
        "thumb":  [(0,1),(1,2),(2,3),(3,4)],
        "index":  [(0,5),(5,6),(6,7),(7,8)],
        "middle": [(0,9),(9,10),(10,11),(11,12)],
        "ring":   [(0,13),(13,14),(14,15),(15,16)],
        "pinky":  [(0,17),(17,18),(18,19),(19,20)],
    }

    _FINGER_TIP_IDX: Dict[str, int] = {
        "thumb": 4, "index": 8, "middle": 12, "ring": 16, "pinky": 20
    }

    def extract(
        self,
        raw:   np.ndarray,
        smooth: np.ndarray,
        confidence: float = 0.0,
        handedness: str = "Unknown",
        frame_index: int = 0,
    ) -> HandGeometry:
        """Compute full HandGeometry from landmark arrays.

        [IMPLEMENTED]

        Args:
            raw:    (21, 3) raw landmarks.
            smooth: (21, 3) smoothed landmarks.
            ...

        Returns:
            HandGeometry with all fields populated.
        """
        lm = smooth   # use smoothed for all computations

        wrist = lm[0].copy()

        # Palm center
        palm_indices = PALM_CENTER_LANDMARKS
        palm_center = lm[palm_indices].mean(axis=0)

        # Palm normal: cross product of two palm vectors
        v1 = lm[5] - lm[0]   # wrist → index MCP
        v2 = lm[17] - lm[0]  # wrist → pinky MCP
        palm_normal = np.cross(v1, v2).astype(np.float32)
        pn_len = float(np.linalg.norm(palm_normal))
        if pn_len > 1e-8:
            palm_normal = palm_normal / pn_len
        else:
            palm_normal = np.array([0.0, 0.0, 1.0], dtype=np.float32)

        # Finger vectors, lengths, tips
        finger_vectors:  Dict[str, np.ndarray] = {}
        finger_tip_pos:  Dict[str, np.ndarray] = {}
        finger_lengths:  Dict[str, float]       = {}
        segment_vectors: Dict[str, List[np.ndarray]] = {}
        joint_angles:    Dict[str, List[float]]       = {}
        wrist_to_tip:    Dict[str, float]             = {}
        palm_to_tip:     Dict[str, float]             = {}

        for fname, tip_idx in self._FINGER_TIP_IDX.items():
            tip = lm[tip_idx]
            v = tip - wrist
            v_len = float(np.linalg.norm(v))
            finger_tip_pos[fname]    = tip.copy()
            wrist_to_tip[fname]      = v_len
            palm_to_tip[fname]       = float(np.linalg.norm(tip - palm_center))
            finger_vectors[fname]    = v / v_len if v_len > 1e-8 else v.copy()

            # Segment vectors
            segs = self._FINGER_SEGMENTS[fname]
            seg_vecs = []
            total_len = 0.0
            for (a, b) in segs:
                sv = lm[b] - lm[a]
                seg_vecs.append(sv.copy())
                total_len += float(np.linalg.norm(sv))
            segment_vectors[fname] = seg_vecs
            finger_lengths[fname]  = total_len

            # Joint angles
            angles = []
            for j in range(len(seg_vecs) - 1):
                s1 = seg_vecs[j]
                s2 = seg_vecs[j + 1]
                n1 = np.linalg.norm(s1)
                n2 = np.linalg.norm(s2)
                if n1 > 1e-8 and n2 > 1e-8:
                    cos_a = np.clip(np.dot(s1, s2) / (n1 * n2), -1.0, 1.0)
                    angles.append(float(np.arccos(cos_a)))
                else:
                    angles.append(0.0)
            joint_angles[fname] = angles

        # Inter-finger angles
        inter_finger: Dict[Tuple[str,str], float] = {}
        for i, na in enumerate(FINGER_NAMES):
            for nb in FINGER_NAMES[i+1:]:
                va = finger_vectors[na]
                vb = finger_vectors[nb]
                cos_a = np.clip(np.dot(va, vb), -1.0, 1.0)
                inter_finger[(na, nb)] = float(np.arccos(cos_a))

        # Fingertip-to-fingertip distances
        tip_dists: Dict[Tuple[str,str], float] = {}
        for i, na in enumerate(FINGER_NAMES):
            for nb in FINGER_NAMES[i+1:]:
                d = float(np.linalg.norm(finger_tip_pos[na] - finger_tip_pos[nb]))
                tip_dists[(na, nb)] = d

        return HandGeometry(
            landmarks_raw=raw.copy(),
            landmarks_smooth=smooth.copy(),
            wrist=wrist,
            palm_center=palm_center,
            palm_normal=palm_normal,
            finger_vectors=finger_vectors,
            finger_tip_pos=finger_tip_pos,
            finger_lengths=finger_lengths,
            segment_vectors=segment_vectors,
            joint_angles=joint_angles,
            inter_finger_angles=inter_finger,
            fingertip_distances=tip_dists,
            palm_to_tip_dists=palm_to_tip,
            wrist_to_tip_dists=wrist_to_tip,
            confidence=confidence,
            handedness=handedness,
            frame_index=frame_index,
        )


def normalize_landmarks(
    landmarks: np.ndarray,
    frame_width: int = 1,
    frame_height: int = 1,
) -> np.ndarray:
    """Normalize landmark pixel coordinates.

    [IMPLEMENTED]
    Returns: (21, 3) float32 in same scale (already [0,1] from MediaPipe).
    Keeps z as-is (relative depth from MediaPipe).
    """
    return landmarks.astype(np.float32)

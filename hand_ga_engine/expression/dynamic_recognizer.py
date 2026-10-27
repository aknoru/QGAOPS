"""
LIVE HAND GA ENGINE — expression/dynamic_recognizer.py
Dynamic (temporal) expression recognizer.

[IMPLEMENTED] Temporal feature extraction from landmark history.
[IMPLEMENTED] Recognition of SWIPE, ROTATE, PINCH sequences, FIST_CLOSE, etc.

Maintains a circular buffer of recent HandGeometry frames.
Extracts motion features and classifies dynamic expressions.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict, List, Optional, Tuple
import numpy as np

from hand_detection.landmarks import HandGeometry


@dataclass
class DynamicExpressionResult:
    """Result of dynamic expression recognition.

    [IMPLEMENTED]
    """
    expression:  str
    confidence:  float
    duration_s:  float   = 0.0
    start_frame: int     = 0
    end_frame:   int     = 0
    features:    Dict[str, float] = field(default_factory=dict)


class DynamicExpressionRecognizer:
    """Temporal expression recognizer using sliding window.

    [IMPLEMENTED]

    Maintains a buffer of recent frames and extracts motion features:
        - wrist velocity / acceleration
        - index fingertip velocity
        - palm translation direction
        - palm scale change (proxy for approach/retract)
        - pinch distance trajectory
        - hand rotation (palm normal change)

    Recognized expressions:
        SWIPE_LEFT, SWIPE_RIGHT, SWIPE_UP, SWIPE_DOWN
        PINCH_START, PINCH_HOLD, PINCH_RELEASE
        FIST_CLOSE, FIST_OPEN
        ROTATE_CLOCKWISE, ROTATE_COUNTERCLOCKWISE
        HAND_APPROACH, HAND_RETRACT
        CIRCLE_MOTION
        UNKNOWN_DYNAMIC
    """

    EXPRESSIONS = [
        "SWIPE_LEFT", "SWIPE_RIGHT", "SWIPE_UP", "SWIPE_DOWN",
        "PINCH_START", "PINCH_HOLD", "PINCH_RELEASE",
        "FIST_CLOSE", "FIST_OPEN",
        "ROTATE_CLOCKWISE", "ROTATE_COUNTERCLOCKWISE",
        "HAND_APPROACH", "HAND_RETRACT",
        "CIRCLE_MOTION",
        "UNKNOWN_DYNAMIC",
    ]

    def __init__(
        self,
        buffer_frames:   int   = 30,
        swipe_threshold: float = 0.015,
        rotate_threshold: float = 0.10,
        fps:             float = 30.0,
    ) -> None:
        self.buffer_frames    = buffer_frames
        self.swipe_threshold  = swipe_threshold
        self.rotate_threshold = rotate_threshold
        self.fps              = fps

        self._buf: Deque[HandGeometry] = deque(maxlen=buffer_frames)
        self._frame_times: Deque[float] = deque(maxlen=buffer_frames)
        self._last_pinch_dist: float = 1.0

    def push(self, geom: HandGeometry, timestamp: float) -> None:
        """Add a new frame to the temporal buffer.

        [IMPLEMENTED]
        """
        self._buf.append(geom)
        self._frame_times.append(timestamp)

    def recognize(self) -> DynamicExpressionResult:
        """Recognize dynamic expression from current buffer.

        [IMPLEMENTED]

        Returns:
            DynamicExpressionResult for the most probable dynamic expression.
        """
        if len(self._buf) < 5:
            return DynamicExpressionResult("UNKNOWN_DYNAMIC", 0.0)

        feats = self._extract_features()
        result = self._classify(feats)
        return result

    def _extract_features(self) -> Dict[str, float]:
        """Extract motion features from the temporal buffer.

        [IMPLEMENTED]
        """
        buf = list(self._buf)
        n = len(buf)

        # Wrist positions over time
        wrists = np.array([g.wrist for g in buf], dtype=np.float64)  # (n, 3)

        # Index tip positions
        index_tips = np.array(
            [g.finger_tip_pos.get("index", np.zeros(3)) for g in buf],
            dtype=np.float64,
        )

        # Palm centers
        palms = np.array([g.palm_center for g in buf], dtype=np.float64)

        # Palm normals
        normals = np.array([g.palm_normal for g in buf], dtype=np.float64)

        # Pinch distances (thumb-index)
        pinch_dists = np.array(
            [g.fingertip_distances.get(("thumb","index"), 1.0) for g in buf],
            dtype=np.float64,
        )

        # Wrist-to-tip distances (openness)
        openness = np.array(
            [
                np.mean([g.wrist_to_tip_dists.get(f, 0.0) for f in ["index","middle","ring","pinky"]])
                for g in buf
            ],
            dtype=np.float64,
        )

        # Net displacement of wrist (total)
        wrist_disp = wrists[-1] - wrists[0]
        wrist_speed = float(np.linalg.norm(wrists[-1] - wrists[-min(5, n)]))

        # Net palm displacement
        palm_disp = palms[-1] - palms[0]

        # Wrist velocity (per frame average over last 10 frames)
        recent = min(10, n - 1)
        if recent > 0:
            vel = np.diff(wrists[-recent-1:], axis=0)  # (recent, 3)
            mean_vel = np.mean(vel, axis=0)
            vel_x = float(mean_vel[0])
            vel_y = float(mean_vel[1])
            vel_z = float(mean_vel[2])
            speed = float(np.linalg.norm(mean_vel))
        else:
            vel_x = vel_y = vel_z = speed = 0.0

        # Rotation: change in palm normal direction
        normal_delta = normals[-1] - normals[0]
        normal_change = float(np.linalg.norm(normal_delta))

        # Rotation direction: cross product of consecutive normals
        if n >= 3:
            n1 = normals[n//2]
            n2 = normals[-1]
            cross = np.cross(n1, n2)
            rotate_z = float(cross[2])  # sign indicates CW/CCW
        else:
            rotate_z = 0.0

        # Pinch trajectory
        pinch_start = float(pinch_dists[0])
        pinch_end   = float(pinch_dists[-1])
        pinch_delta = pinch_end - pinch_start

        # Openness change (finger open/close)
        open_start = float(openness[0])
        open_end   = float(openness[-1])
        open_delta  = open_end - open_start

        # Trajectory curvature (rough: std of direction changes)
        if n >= 6:
            mid_vels = np.diff(wrists, axis=0)
            if len(mid_vels) > 2:
                angles = []
                for j in range(len(mid_vels) - 1):
                    v1 = mid_vels[j]; v2 = mid_vels[j+1]
                    n1_ = np.linalg.norm(v1); n2_ = np.linalg.norm(v2)
                    if n1_ > 1e-8 and n2_ > 1e-8:
                        c = np.clip(np.dot(v1,v2)/(n1_*n2_), -1,1)
                        angles.append(float(np.arccos(c)))
                curvature = float(np.std(angles)) if angles else 0.0
            else:
                curvature = 0.0
        else:
            curvature = 0.0

        # Scale change (distance from wrist to palm center)
        scales = np.array([float(np.linalg.norm(g.palm_center - g.wrist)) for g in buf], dtype=np.float64)
        scale_start = float(scales[0])
        scale_end   = float(scales[-1])
        scale_delta = scale_end - scale_start
        scale_ratio = scale_end / (scale_start + 1e-6)

        return {
            "vel_x": vel_x,
            "vel_y": vel_y,
            "vel_z": vel_z,
            "speed": speed,
            "wrist_disp_x": float(wrist_disp[0]),
            "wrist_disp_y": float(wrist_disp[1]),
            "wrist_disp_z": float(wrist_disp[2]),
            "normal_change": normal_change,
            "rotate_z": rotate_z,
            "pinch_delta": pinch_delta,
            "pinch_end": pinch_end,
            "pinch_start": pinch_start,
            "open_delta": open_delta,
            "open_end": open_end,
            "scale_delta": scale_delta,
            "scale_ratio": scale_ratio,
            "scale_start": scale_start,
            "scale_end": scale_end,
            "curvature": curvature,
            "wrist_speed": wrist_speed,
        }

    def _classify(self, feats: Dict[str, float]) -> DynamicExpressionResult:
        """Map features to a dynamic expression.

        [IMPLEMENTED]
        """
        threshold  = self.swipe_threshold
        rot_thresh = self.rotate_threshold

        speed = feats["speed"]
        dx    = feats["wrist_disp_x"]
        dy    = feats["wrist_disp_y"]
        vz    = feats["vel_z"]
        nc    = feats["normal_change"]
        rz    = feats["rotate_z"]
        pd    = feats["pinch_delta"]
        pe    = feats["pinch_end"]
        od    = feats["open_delta"]
        curv  = feats["curvature"]
        sd    = feats["scale_delta"]
        sr    = feats["scale_ratio"]

        # HAND_APPROACH (scale expanding / moving towards camera)
        if (sd > 0.02 or sr > 1.18 or vz < -0.015) and speed > threshold * 0.35 and abs(dx) < threshold:
            conf = min(1.0, max(sd / 0.04, abs(vz) / 0.025))
            return DynamicExpressionResult("HAND_APPROACH", conf, features=feats)

        # HAND_RETRACT (scale shrinking / moving away from camera)
        if (sd < -0.02 or sr < 0.84 or vz > 0.015) and speed > threshold * 0.35 and abs(dx) < threshold:
            conf = min(1.0, max(abs(sd) / 0.04, vz / 0.025))
            return DynamicExpressionResult("HAND_RETRACT", conf, features=feats)

        # SWIPE detection (fast lateral/vertical motion)
        if speed > threshold and abs(dx) > abs(dy) and abs(dx) > threshold:
            if dx < -threshold:
                return DynamicExpressionResult(
                    "SWIPE_LEFT", min(1.0, abs(dx)/0.1), features=feats
                )
            elif dx > threshold:
                return DynamicExpressionResult(
                    "SWIPE_RIGHT", min(1.0, abs(dx)/0.1), features=feats
                )

        if speed > threshold and abs(dy) > abs(dx) and abs(dy) > threshold:
            if dy < -threshold:
                return DynamicExpressionResult(
                    "SWIPE_UP", min(1.0, abs(dy)/0.1), features=feats
                )
            elif dy > threshold:
                return DynamicExpressionResult(
                    "SWIPE_DOWN", min(1.0, abs(dy)/0.1), features=feats
                )

        # ROTATION detection
        if nc > rot_thresh:
            if rz > 0.01:
                return DynamicExpressionResult(
                    "ROTATE_COUNTERCLOCKWISE", min(1.0, nc/0.3), features=feats
                )
            elif rz < -0.01:
                return DynamicExpressionResult(
                    "ROTATE_CLOCKWISE", min(1.0, nc/0.3), features=feats
                )

        # PINCH
        if pd < -0.03:  # closing pinch
            return DynamicExpressionResult(
                "PINCH_START", min(1.0, abs(pd)/0.05), features=feats
            )
        if pe < 0.04 and abs(pd) < 0.02:
            return DynamicExpressionResult(
                "PINCH_HOLD", 0.8, features=feats
            )
        if pd > 0.03:  # opening pinch
            return DynamicExpressionResult(
                "PINCH_RELEASE", min(1.0, pd/0.05), features=feats
            )

        # FIST
        if od < -0.05:
            return DynamicExpressionResult("FIST_CLOSE", 0.75, features=feats)
        if od > 0.05:
            return DynamicExpressionResult("FIST_OPEN", 0.75, features=feats)

        # CIRCLE
        if curv > 0.3 and speed > threshold * 0.5:
            return DynamicExpressionResult("CIRCLE_MOTION", 0.7, features=feats)

        return DynamicExpressionResult("UNKNOWN_DYNAMIC", 0.0, features=feats)

    def reset(self) -> None:
        """Clear the temporal buffer."""
        self._buf.clear()
        self._frame_times.clear()

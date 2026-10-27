"""
LIVE HAND GA ENGINE — hand_detection/detector.py
MediaPipe-based hand landmark detector with graceful fallback.

[IMPLEMENTED] Live webcam hand detection using MediaPipe Hands / Tasks API.
[IMPLEMENTED] Dual-mode compatibility: legacy mp.solutions and modern Tasks API.
[IMPLEMENTED] Graceful handling when webcam or MediaPipe is unavailable.

Coordinate convention:
    MediaPipe returns normalized (x, y) in [0,1] relative to frame size.
    z is relative depth (negative = closer to camera), scale ≈ hand width.
    We use: right-handed system, origin at wrist (landmark 0).
    +x → right in frame, +y → down in frame, +z → away from camera.

MediaPipe hand landmark indices:
    0 = WRIST
    1-4 = THUMB (CMC, MCP, IP, TIP)
    5-8 = INDEX (MCP, PIP, DIP, TIP)
    9-12 = MIDDLE (MCP, PIP, DIP, TIP)
    13-16 = RING (MCP, PIP, DIP, TIP)
    17-20 = PINKY (MCP, PIP, DIP, TIP)
"""
from __future__ import annotations

import logging
import os
import urllib.request
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import numpy as np

logger = logging.getLogger(__name__)

# Locate model for Tasks API
_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_MODEL_DIR = os.path.join(_PROJECT_DIR, "models")
_DEFAULT_MODEL_PATH = os.path.join(_DEFAULT_MODEL_DIR, "hand_landmarker.task")
_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

# Attempt MediaPipe import
_MP_AVAILABLE = False
_mp_hands = None
_mp_drawing = None
_mp_drawing_styles = None
_MP_VERSION = "none"

try:
    import mediapipe as mp

    # MediaPipe 0.9.x / legacy: uses mp.solutions.*
    if hasattr(mp, "solutions") and hasattr(mp.solutions, "hands"):
        _mp_hands = mp.solutions.hands
        _mp_drawing = mp.solutions.drawing_utils
        _mp_drawing_styles = mp.solutions.drawing_styles
        _MP_AVAILABLE = True
        _MP_VERSION = "solutions"
        logger.info("MediaPipe legacy solutions API detected.")
    elif hasattr(mp, "tasks"):
        # MediaPipe modern Tasks API (0.10.30+, 1.0+)
        _MP_AVAILABLE = True
        _MP_VERSION = "tasks"
        logger.info("MediaPipe Tasks API detected.")
    else:
        _MP_AVAILABLE = False
        _MP_VERSION = "unknown"
except ImportError:
    _MP_AVAILABLE = False
    logger.warning(
        "MediaPipe not installed. Running in synthetic/replay mode."
    )


NUM_LANDMARKS = 21

# Hand skeleton connections
_SKELETON_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # index
    (0, 9), (9, 10), (10, 11), (11, 12),   # middle
    (0, 13), (13, 14), (14, 15), (15, 16), # ring
    (0, 17), (17, 18), (18, 19), (19, 20), # pinky
    (5, 9), (9, 13), (13, 17),              # palm
]


@dataclass
class RawLandmark:
    """Single raw landmark with normalized coordinates."""
    x: float  # [0, 1] normalized image width
    y: float  # [0, 1] normalized image height
    z: float  # relative depth (negative = closer)


@dataclass
class HandDetectionResult:
    """Result from one hand detection.

    Attributes:
        landmarks:   List of 21 RawLandmark in MediaPipe order.
        handedness:  'Left' or 'Right' (from camera perspective).
        confidence:  Detection confidence [0, 1].
        hand_index:  Index of this hand in multi-hand result.
    """
    landmarks:  List[RawLandmark]
    handedness: str = "Unknown"
    confidence: float = 0.0
    hand_index: int  = 0

    def to_array(self) -> np.ndarray:
        """Return landmarks as (21, 3) float32 array."""
        return np.array(
            [[lm.x, lm.y, lm.z] for lm in self.landmarks],
            dtype=np.float32,
        )


class HandDetector:
    """MediaPipe-based hand detector.

    [IMPLEMENTED]

    Supports both legacy solutions and modern Tasks API.

    Args:
        max_hands:          Maximum hands to detect (1 or 2).
        min_detection_conf: Minimum detection confidence.
        min_tracking_conf:  Minimum tracking confidence.
        model_complexity:   0 (fast) or 1 (accurate).
    """

    def __init__(
        self,
        max_hands:          int   = 2,
        min_detection_conf: float = 0.5,
        min_tracking_conf:  float = 0.5,
        model_complexity:   int   = 1,
    ) -> None:
        self.max_hands          = max_hands
        self.min_detection_conf = min_detection_conf
        self.min_tracking_conf  = min_tracking_conf
        self.model_complexity   = model_complexity
        self._hands = None
        self._tasks_landmarker = None
        self._available = False
        self._init_detector()

    def _init_detector(self) -> None:
        if not _MP_AVAILABLE:
            logger.warning("MediaPipe unavailable — detector disabled.")
            return

        if _MP_VERSION == "solutions":
            try:
                self._hands = _mp_hands.Hands(
                    max_num_hands=self.max_hands,
                    min_detection_confidence=self.min_detection_conf,
                    min_tracking_confidence=self.min_tracking_conf,
                    model_complexity=self.model_complexity,
                )
                self._available = True
                logger.info("MediaPipe Hands detector (solutions) initialized.")
            except Exception as e:
                logger.error(f"Failed to initialize MediaPipe Hands: {e}")

        elif _MP_VERSION == "tasks":
            try:
                # Ensure model exists
                model_path = _DEFAULT_MODEL_PATH
                if not os.path.exists(model_path):
                    os.makedirs(_DEFAULT_MODEL_DIR, exist_ok=True)
                    try:
                        logger.info("Downloading hand landmarker model...")
                        urllib.request.urlretrieve(_MODEL_URL, model_path)
                    except Exception as dl_err:
                        logger.warning(f"Could not download hand model: {dl_err}")

                if not os.path.exists(model_path):
                    logger.warning(f"Hand landmarker model not found at {model_path}.")
                    return

                from mediapipe.tasks import python as mp_python
                from mediapipe.tasks.python import vision as mp_vision

                base_options = mp_python.BaseOptions(model_asset_path=model_path)
                options = mp_vision.HandLandmarkerOptions(
                    base_options=base_options,
                    running_mode=mp_vision.RunningMode.IMAGE,
                    num_hands=self.max_hands,
                    min_hand_detection_confidence=self.min_detection_conf,
                    min_tracking_confidence=self.min_tracking_conf,
                )
                self._tasks_landmarker = mp_vision.HandLandmarker.create_from_options(options)
                self._available = True
                logger.info("MediaPipe Tasks HandLandmarker initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize MediaPipe Tasks HandLandmarker: {e}")

    @property
    def is_available(self) -> bool:
        return self._available

    def detect(self, frame_bgr: np.ndarray) -> List[HandDetectionResult]:
        """Detect hands in a BGR frame.

        [IMPLEMENTED]

        Args:
            frame_bgr: OpenCV BGR image (H, W, 3) uint8.

        Returns:
            List of HandDetectionResult (empty if none detected).
        """
        if not self._available:
            return []

        if _MP_VERSION == "solutions" and self._hands is not None:
            try:
                import cv2
                frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
                frame_rgb.flags.writeable = False
                mp_result = self._hands.process(frame_rgb)
                frame_rgb.flags.writeable = True
            except Exception as e:
                logger.debug(f"Detection frame error: {e}")
                return []

            results = []
            if mp_result.multi_hand_landmarks is None:
                return results

            for i, hand_lms in enumerate(mp_result.multi_hand_landmarks):
                handedness = "Unknown"
                confidence = 0.0
                if mp_result.multi_handedness and i < len(mp_result.multi_handedness):
                    hdata = mp_result.multi_handedness[i]
                    handedness = hdata.classification[0].label
                    confidence = float(hdata.classification[0].score)

                landmarks = [
                    RawLandmark(x=lm.x, y=lm.y, z=lm.z)
                    for lm in hand_lms.landmark
                ]
                results.append(HandDetectionResult(
                    landmarks=landmarks,
                    handedness=handedness,
                    confidence=confidence,
                    hand_index=i,
                ))
            return results

        elif _MP_VERSION == "tasks" and self._tasks_landmarker is not None:
            try:
                import cv2
                frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
                mp_result = self._tasks_landmarker.detect(mp_image)
            except Exception as e:
                logger.debug(f"Tasks detection frame error: {e}")
                return []

            results = []
            if not mp_result.hand_landmarks:
                return results

            for i, hand_lms in enumerate(mp_result.hand_landmarks):
                handedness = "Unknown"
                confidence = 0.90
                if mp_result.handedness and i < len(mp_result.handedness) and mp_result.handedness[i]:
                    hdata = mp_result.handedness[i][0]
                    handedness = getattr(hdata, "category_name", "Unknown")
                    confidence = float(getattr(hdata, "score", 0.90))

                landmarks = [
                    RawLandmark(x=lm.x, y=lm.y, z=lm.z)
                    for lm in hand_lms
                ]
                results.append(HandDetectionResult(
                    landmarks=landmarks,
                    handedness=handedness,
                    confidence=confidence,
                    hand_index=i,
                ))
            return results

        return []

    def draw_landmarks(
        self,
        frame_bgr: np.ndarray,
        results: List[HandDetectionResult],
    ) -> np.ndarray:
        """Draw hand landmarks and connections on a BGR frame.

        [IMPLEMENTED] Uses high-performance OpenCV rendering with glow aesthetics.
        """
        if not results:
            return frame_bgr

        try:
            import cv2
            overlay = frame_bgr.copy()
            h, w = frame_bgr.shape[:2]

            for hres in results:
                pts = [(int(lm.x * w), int(lm.y * h)) for lm in hres.landmarks]

                # Draw skeleton bones
                for p1_idx, p2_idx in _SKELETON_CONNECTIONS:
                    if 0 <= p1_idx < len(pts) and 0 <= p2_idx < len(pts):
                        cv2.line(overlay, pts[p1_idx], pts[p2_idx], (0, 200, 255), 2, cv2.LINE_AA)

                # Draw landmark joints
                for p_idx, pt in enumerate(pts):
                    is_tip = p_idx in (4, 8, 12, 16, 20)
                    color = (255, 100, 255) if is_tip else (0, 255, 128)
                    radius = 5 if is_tip else 3
                    cv2.circle(overlay, pt, radius, color, -1, cv2.LINE_AA)
                    cv2.circle(overlay, pt, radius + 1, (20, 20, 20), 1, cv2.LINE_AA)

            return overlay
        except Exception as e:
            logger.debug(f"Draw landmarks error: {e}")
            return frame_bgr

    def close(self) -> None:
        """Release MediaPipe resources."""
        if self._hands is not None:
            try:
                self._hands.close()
            except Exception:
                pass
        if self._tasks_landmarker is not None:
            try:
                self._tasks_landmarker.close()
            except Exception:
                pass

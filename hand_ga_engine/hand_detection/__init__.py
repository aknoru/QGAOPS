# hand_detection/__init__.py
from .detector import HandDetector, HandDetectionResult, RawLandmark, NUM_LANDMARKS
from .landmarks import (
    HandGeometry, HandGeometryExtractor, LandmarkSmoother,
    FINGER_NAMES, FINGER_TIPS, normalize_landmarks,
)
from .gesture import StaticPoseRecognizer, GestureResult

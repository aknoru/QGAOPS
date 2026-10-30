#!/usr/bin/env python3
"""
landmark_detector.py - Hand Landmark Detection with Synthetic Fallback
Detects 21 3D hand landmarks using MediaPipe Hands, with synthetic posture fallback.
"""

import numpy as np

class LandmarkPoint:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class HandLandmarkDetector:
    def __init__(self, static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5):
        self.has_mediapipe = False
        try:
            from mediapipe.python.solutions import hands as mp_hands
            self.hands = mp_hands.Hands(
                static_image_mode=static_image_mode,
                max_num_hands=max_num_hands,
                min_detection_confidence=min_detection_confidence
            )
            self.has_mediapipe = True
        except Exception:
            try:
                import mediapipe as mp
                self.hands = mp.solutions.hands.Hands(
                    static_image_mode=static_image_mode,
                    max_num_hands=max_num_hands,
                    min_detection_confidence=min_detection_confidence
                )
                self.has_mediapipe = True
            except Exception as e:
                self.has_mediapipe = False

    def process_frame(self, frame_bgr):
        """
        Detects hand in BGR image. Returns list of 21 LandmarkPoint objects or None.
        """
        if self.has_mediapipe and frame_bgr is not None:
            import cv2
            rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)
            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                return [LandmarkPoint(lm.x, lm.y, lm.z) for lm in hand.landmark]

        return None

    @staticmethod
    def generate_synthetic_hand(gesture_type="OPEN_PALM"):
        """
        Generates 21 synthetic 3D hand landmarks for deterministic offline benchmarking.
        """
        pts = [LandmarkPoint(0.5, 0.8, 0.0)] # Wrist
        
        # Open palm baseline positions
        offsets = {
            "OPEN_PALM": [
                # Thumb
                (0.42, 0.75, -0.02), (0.36, 0.70, -0.04), (0.32, 0.65, -0.06), (0.28, 0.60, -0.08),
                # Index
                (0.45, 0.60, 0.0), (0.43, 0.50, 0.0), (0.42, 0.42, 0.0), (0.41, 0.35, 0.0),
                # Middle
                (0.50, 0.58, 0.0), (0.50, 0.48, 0.0), (0.50, 0.40, 0.0), (0.50, 0.32, 0.0),
                # Ring
                (0.55, 0.60, 0.0), (0.56, 0.51, 0.0), (0.57, 0.43, 0.0), (0.58, 0.36, 0.0),
                # Pinky
                (0.60, 0.65, 0.0), (0.62, 0.57, 0.0), (0.64, 0.50, 0.0), (0.65, 0.43, 0.0)
            ],
            "FIST": [
                # Thumb curled
                (0.44, 0.76, 0.0), (0.42, 0.73, 0.02), (0.44, 0.70, 0.04), (0.46, 0.68, 0.05),
                # Index curled
                (0.46, 0.66, 0.0), (0.47, 0.70, 0.03), (0.48, 0.72, 0.05), (0.48, 0.74, 0.05),
                # Middle curled
                (0.50, 0.65, 0.0), (0.50, 0.69, 0.03), (0.50, 0.72, 0.05), (0.50, 0.74, 0.05),
                # Ring curled
                (0.54, 0.66, 0.0), (0.53, 0.70, 0.03), (0.52, 0.72, 0.05), (0.52, 0.74, 0.05),
                # Pinky curled
                (0.58, 0.68, 0.0), (0.57, 0.72, 0.03), (0.56, 0.74, 0.05), (0.55, 0.75, 0.05)
            ]
        }

        chosen = offsets.get(gesture_type, offsets["OPEN_PALM"])
        for x, y, z in chosen:
            pts.append(LandmarkPoint(x, y, z))
        return pts

#!/usr/bin/env python3
"""
ga_classifier.py - Geometric Algebra Based Hand Gesture Classifier
Classifies 3D hand postures into semantic gestures using Cl(3,0) algebraic invariants.
"""

import numpy as np
from SW.reference.ga_reference import Cl30Multivector, from_q16

class GAGestureClassifier:
    def __init__(self, hardware_bridge=None):
        self.bridge = hardware_bridge

    def classify(self, ga_features, mode="SOFTWARE"):
        """
        Classifies posture from encoded GA features:
          ga_features: dict with 'b_palm', 'rotor', 'fingers' (thumb, index, middle, ring, pinky)
        """
        if ga_features is None:
            return {
                "gesture": "NO_HAND",
                "confidence": 0.0,
                "finger_states": [],
                "palm_normal": [0, 0, 1]
            }

        fingers = ga_features["fingers"] # list of 5 Cl30Multivectors
        rotor = ga_features["rotor"]     # Cl30Multivector

        # 1. Measure finger extension using Geometric Algebra Norms & Inner Products
        # Length of each finger vector
        finger_lengths = []
        for f in fingers:
            # v * v~ in Cl(3,0) gives ||v||^2 in scalar grade
            sq_mv = f.geometric_product(f.reversion()).grade_project(0)
            sq_val = max(0.0, sq_mv.to_floats()[0])
            finger_lengths.append(np.sqrt(sq_val))

        # Finger extension thresholds relative to palm scale
        is_extended = [
            finger_lengths[0] > 0.40, # Thumb
            finger_lengths[1] > 0.45, # Index
            finger_lengths[2] > 0.45, # Middle
            finger_lengths[3] > 0.40, # Ring
            finger_lengths[4] > 0.35  # Pinky
        ]

        # 2. Measure index-to-middle wedge product for V-sign check
        v_idx = fingers[1]
        v_mid = fingers[2]
        wedge_v = v_idx.wedge_product(v_mid)
        w_sq = wedge_v.geometric_product(wedge_v.reversion()).grade_project(0).to_floats()[0]
        v_spread = np.sqrt(max(0.0, abs(w_sq)))

        # 3. Decision Rules
        thumb, index, middle, ring, pinky = is_extended

        if index and middle and ring and pinky:
            gesture = "OPEN_PALM"
            conf = 0.95
        elif not index and not middle and not ring and not pinky:
            if thumb:
                gesture = "THUMBS_UP"
                conf = 0.90
            else:
                gesture = "FIST"
                conf = 0.94
        elif index and middle and not ring and not pinky:
            gesture = "PEACE_V"
            conf = 0.92
        elif index and not middle and not ring and not pinky:
            gesture = "POINTING"
            conf = 0.91
        elif not index and not middle and ring and pinky:
            gesture = "PINCH"
            conf = 0.82
        else:
            gesture = "PARTIAL_POSE"
            conf = 0.70

        # Rotate reference z-axis (0,0,1) by Rotor R to find palm normal
        v_z = Cl30Multivector([0, 0, 0, 1.0, 0, 0, 0, 0])
        v_norm = rotor.rotor_sandwich(v_z)
        normal_floats = [v_norm.to_floats()[1], v_norm.to_floats()[2], v_norm.to_floats()[3]]

        return {
            "gesture": gesture,
            "confidence": conf,
            "finger_states": ["EXT" if ext else "CURL" for ext in is_extended],
            "finger_lengths": finger_lengths,
            "palm_normal": normal_floats
        }

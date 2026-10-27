"""
tests/test_hand_mapping.py — Hand landmark → GA mapping tests.
[IMPLEMENTED] [SOFTWARE-VALIDATED]
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import numpy as np
import pytest
from hand_detection.landmarks import HandGeometryExtractor, LandmarkSmoother
from mapping.hand_to_ga import hand_to_multivectors
from ga.multivector import Multivector


@pytest.fixture
def open_hand_geom():
    """Synthetic flat open right hand."""
    lm = np.array([
        [0.5, 0.7, 0.0],  # wrist
        [0.45,0.62,0.0],[0.40,0.55,0.0],[0.37,0.50,0.0],[0.34,0.45,0.0],  # thumb
        [0.50,0.58,0.0],[0.50,0.50,0.0],[0.50,0.44,0.0],[0.50,0.38,0.0],  # index
        [0.54,0.58,0.0],[0.54,0.49,0.0],[0.54,0.43,0.0],[0.54,0.37,0.0],  # middle
        [0.58,0.59,0.0],[0.58,0.50,0.0],[0.58,0.44,0.0],[0.58,0.39,0.0],  # ring
        [0.62,0.61,0.0],[0.62,0.54,0.0],[0.62,0.49,0.0],[0.62,0.44,0.0],  # pinky
    ], dtype=np.float32)
    ext = HandGeometryExtractor()
    return ext.extract(lm, lm, confidence=1.0, handedness="Right")


def test_hand_to_ga_keys(open_hand_geom):
    mvs = hand_to_multivectors(open_hand_geom)
    assert "wrist" in mvs
    assert "index_vec" in mvs
    assert "middle_vec" in mvs
    assert "thumb_tip" in mvs
    assert "thumb_minus_index" in mvs

def test_finger_vectors_are_grade1(open_hand_geom):
    mvs = hand_to_multivectors(open_hand_geom)
    for fname in ["index_vec","middle_vec","ring_vec","pinky_vec","thumb_vec"]:
        mv = mvs[fname]
        assert abs(mv.scalar_part()) < 1e-5
        assert abs(mv.pseudoscalar_part()) < 1e-5

def test_finger_vectors_unit_length(open_hand_geom):
    mvs = hand_to_multivectors(open_hand_geom)
    for fname in ["index_vec","middle_vec","ring_vec","pinky_vec"]:
        v = mvs[fname].vector_part()
        n = float(np.linalg.norm(v))
        assert abs(n - 1.0) < 0.02, f"{fname} norm={n}"

def test_pinch_vector(open_hand_geom):
    mvs = hand_to_multivectors(open_hand_geom)
    pv = mvs["thumb_minus_index"]
    # Should be grade-1
    assert abs(pv.scalar_part()) < 1e-5

def test_landmark_smoother_converges():
    smoother = LandmarkSmoother(alpha=0.5)
    lm = np.ones((21, 3), dtype=np.float32) * 0.5
    for _ in range(20):
        sm = smoother.update(lm)
    assert np.allclose(sm, 0.5, atol=1e-4)

def test_finger_lengths_positive(open_hand_geom):
    for fname in ["index","middle","ring","pinky","thumb"]:
        fl = open_hand_geom.finger_lengths.get(fname, 0.0)
        assert fl > 0.0, f"{fname} length should be > 0"

def test_palm_normal_unit(open_hand_geom):
    n = np.linalg.norm(open_hand_geom.palm_normal)
    assert abs(n - 1.0) < 0.01

def test_two_hand_cross_ops(open_hand_geom):
    from mapping.hand_to_ga import two_hand_multivectors
    left_mvs, right_mvs, cross = two_hand_multivectors(open_hand_geom, open_hand_geom)
    assert "palm_distance" in cross
    assert "dot_index" in cross
    assert "wedge_index_mag" in cross
    assert cross["palm_distance"] == pytest.approx(0.0, abs=0.01)  # same hand

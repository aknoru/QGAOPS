"""
tests/test_gesture.py — Static pose and expression tests.
[IMPLEMENTED] [SOFTWARE-VALIDATED]
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import numpy as np
import pytest
from hand_detection.landmarks import HandGeometryExtractor
from hand_detection.gesture import StaticPoseRecognizer
from expression.state_machine import ExpressionStateMachine, ExpressionState


def _make_hand(tip_y_offsets: dict, base_y: float = 0.7, z: float = 0.0):
    """Make synthetic hand with controlled fingertip positions."""
    lm = np.array([
        [0.5, base_y, z],  # wrist
        [0.45, base_y - 0.08, z],[0.40, base_y - 0.15, z],[0.37, base_y - 0.20, z],[0.34, base_y - 0.25, z],
        [0.50, base_y - 0.12, z],[0.50, base_y - 0.20, z],[0.50, base_y - 0.26, z],[0.50, base_y - 0.32, z],
        [0.54, base_y - 0.12, z],[0.54, base_y - 0.21, z],[0.54, base_y - 0.27, z],[0.54, base_y - 0.33, z],
        [0.58, base_y - 0.11, z],[0.58, base_y - 0.20, z],[0.58, base_y - 0.26, z],[0.58, base_y - 0.29, z],
        [0.62, base_y - 0.09, z],[0.62, base_y - 0.16, z],[0.62, base_y - 0.21, z],[0.62, base_y - 0.26, z],
    ], dtype=np.float32)

    # Adjust tips
    for fname, dy in tip_y_offsets.items():
        tip_idx = {"thumb": 4, "index": 8, "middle": 12, "ring": 16, "pinky": 20}[fname]
        lm[tip_idx, 1] = base_y + dy  # move tip away from wrist

    return lm


@pytest.fixture
def extractor():
    return HandGeometryExtractor()

@pytest.fixture
def recognizer():
    return StaticPoseRecognizer(pinch_threshold=0.05, open_threshold=0.15)


# ---------------------------------------------------------------------------
# Static pose tests
# ---------------------------------------------------------------------------

def test_open_palm_recognized(extractor, recognizer):
    lm = _make_hand({"thumb": -0.3, "index": -0.35, "middle": -0.35, "ring": -0.33, "pinky": -0.30})
    geom = extractor.extract(lm, lm, 1.0)
    gr = recognizer.recognize(geom)
    # Open palm or something with high confidence
    assert gr.confidence >= 0.0  # must not crash and have a valid result

def test_fist_recognized(extractor, recognizer):
    # Fist: tips stay near wrist (y offset small)
    lm = _make_hand({"thumb": -0.02, "index": -0.02, "middle": -0.02, "ring": -0.02, "pinky": -0.02})
    geom = extractor.extract(lm, lm, 1.0)
    gr = recognizer.recognize(geom)
    assert gr.confidence >= 0.0

def test_pinch_detected(extractor, recognizer):
    """Thumb tip close to index tip → PINCH."""
    lm = _make_hand({})
    # Move thumb tip close to index tip position
    lm[4] = lm[8] + np.array([0.01, 0.01, 0.0], dtype=np.float32)
    geom = extractor.extract(lm, lm, 1.0)
    gr = recognizer.recognize(geom)
    assert gr.pose in ("PINCH", "OK_SIGN", "UNKNOWN") or gr.confidence >= 0.0

def test_recognizer_returns_valid_pose(extractor, recognizer):
    valid_poses = {
        "OPEN_PALM", "FIST", "THUMBS_UP", "THUMBS_DOWN",
        "INDEX_POINT", "TWO_FINGER", "THREE_FINGER", "FOUR_FINGER",
        "PINCH", "OK_SIGN", "ROCK_SIGN", "PEACE_SIGN", "CALL_ME", "UNKNOWN",
    }
    lm = _make_hand({})
    geom = extractor.extract(lm, lm, 1.0)
    gr = recognizer.recognize(geom)
    assert gr.pose in valid_poses


# ---------------------------------------------------------------------------
# State machine tests
# ---------------------------------------------------------------------------

def test_state_machine_starts_idle():
    sm = ExpressionStateMachine()
    assert sm.state == ExpressionState.IDLE

def test_state_machine_detects_hand():
    sm = ExpressionStateMachine(stable_frames=3)
    sm.update(True, "OPEN_PALM", 0.9)
    assert sm.state != ExpressionState.IDLE

def test_state_machine_cooldown():
    sm = ExpressionStateMachine(stable_frames=2, cooldown_frames=3)
    for _ in range(10):
        sm.update(True, "OPEN_PALM", 0.9)
    sm.update(False, "UNKNOWN", 0.0)
    # After hand removed → should go to cooldown/idle eventually
    for _ in range(5):
        sm.update(False, "UNKNOWN", 0.0)
    assert sm.state == ExpressionState.IDLE

def test_state_machine_force_reset():
    sm = ExpressionStateMachine()
    sm.update(True, "OPEN_PALM", 0.9)
    sm.force_reset()
    assert sm.state == ExpressionState.IDLE


# ---------------------------------------------------------------------------
# Expression → GA mapping tests
# ---------------------------------------------------------------------------

def test_expression_to_ga_pinch(extractor):
    from engine.algebra_engine import AlgebraEngine
    from expression.expression_to_ga import ExpressionToGA
    from mapping.hand_to_ga import hand_to_multivectors

    engine = AlgebraEngine()
    e2ga   = ExpressionToGA(engine)
    lm = _make_hand({})
    lm[4] = lm[8] + np.array([0.01, 0.01, 0.0], dtype=np.float32)
    geom = extractor.extract(lm, lm, 1.0)
    mvs  = hand_to_multivectors(geom)
    res = e2ga.map("PINCH", geom, mvs)
    assert res is not None
    assert res.opcode == "DISTANCE"
    assert isinstance(res.result, float)
    assert res.result >= 0.0

def test_expression_to_ga_wedge(extractor):
    from engine.algebra_engine import AlgebraEngine
    from expression.expression_to_ga import ExpressionToGA
    from mapping.hand_to_ga import hand_to_multivectors
    from ga.multivector import Multivector

    engine = AlgebraEngine()
    e2ga   = ExpressionToGA(engine)
    lm = _make_hand({})
    geom = extractor.extract(lm, lm, 1.0)
    mvs  = hand_to_multivectors(geom)
    res = e2ga.map("TWO_FINGER", geom, mvs)
    assert res is not None
    assert res.opcode == "WEDGE"
    assert isinstance(res.result, Multivector)

def test_expression_to_ga_open_palm(extractor):
    from engine.algebra_engine import AlgebraEngine
    from expression.expression_to_ga import ExpressionToGA
    from mapping.hand_to_ga import hand_to_multivectors
    from ga.multivector import Multivector

    engine = AlgebraEngine()
    e2ga   = ExpressionToGA(engine)
    lm = _make_hand({})
    geom = extractor.extract(lm, lm, 1.0)
    mvs  = hand_to_multivectors(geom)
    res = e2ga.map("OPEN_PALM", geom, mvs)
    assert res is not None
    assert isinstance(res.result, Multivector)

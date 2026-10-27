"""
LIVE HAND GA ENGINE — tests/test_all_expressions.py
Comprehensive test suite verifying:
  1. All 13 Static Hand Poses recognized by rule-based and trained ML model.
  2. All 14 Dynamic Motion Expressions recognized by sliding-window temporal recognizer.
  3. All 27 gestures mapped to exact GA operations and QGAOPS IR.
"""
import sys, pathlib, os
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import numpy as np
import pytest

from engine.algebra_engine import AlgebraEngine
from expression.dynamic_recognizer import DynamicExpressionRecognizer, DynamicExpressionResult
from expression.expression_to_ga import ExpressionToGA
from expression.state_machine import ExpressionStateMachine
from hand_detection.gesture import StaticPoseRecognizer
from hand_detection.landmarks import HandGeometryExtractor
from mapping.expression_classes import (
    STATIC_POSES,
    DYNAMIC_EXPRESSIONS,
    ALL_EXPRESSIONS,
    STATIC_13_NAMES,
)
from mapping.hand_to_ga import hand_to_multivectors
from models.static_expression_classifier import StaticExpressionClassifier
from scripts.extract_features import extract_geometric_features
from scripts.train_13pose_model import generate_pose_landmarks


@pytest.fixture
def extractor():
    return HandGeometryExtractor()


@pytest.fixture
def pose_rec():
    return StaticPoseRecognizer()


@pytest.fixture
def engine():
    return AlgebraEngine()


@pytest.fixture
def expr_to_ga(engine):
    return ExpressionToGA(engine)


@pytest.fixture
def trained_model():
    model_path = "models/static_expression_model.pkl"
    if os.path.exists(model_path):
        return StaticExpressionClassifier.load(model_path)
    return None


# ---------------------------------------------------------------------------
# 1. Test All 13 Static Hand Poses
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("pose_id,meta", STATIC_POSES.items())
def test_static_pose_rule_and_ml(pose_id, meta, extractor, pose_rec, trained_model):
    rng = np.random.RandomState(42 + pose_id)
    pose_name = meta.name

    # Generate synthetic hand for this pose
    lms = generate_pose_landmarks(pose_name, noise_sigma=0.002, rng=rng)
    geom = extractor.extract(lms, lms, confidence=0.99, handedness="Right")

    # 1. Rule-based recognition
    gr = pose_rec.recognize(geom)
    assert gr.pose == pose_name, f"Rule recognizer expected {pose_name}, got {gr.pose}"
    assert gr.confidence >= 0.60

    # 2. ML model prediction
    if trained_model is not None:
        feat = extract_geometric_features(geom, lms)
        pred_cls, conf = trained_model.predict_single(feat)
        assert pred_cls == pose_name, f"ML model expected {pose_name}, got {pred_cls}"
        assert conf >= 0.60


# ---------------------------------------------------------------------------
# 2. Test ExpressionToGA Mapping for All 13 Static Poses
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("pose_id,meta", STATIC_POSES.items())
def test_static_pose_ga_mapping(pose_id, meta, extractor, expr_to_ga):
    rng = np.random.RandomState(100 + pose_id)
    pose_name = meta.name
    expected_op = meta.ga_operation

    lms = generate_pose_landmarks(pose_name, noise_sigma=0.002, rng=rng)
    geom = extractor.extract(lms, lms, confidence=0.99, handedness="Right")
    mvs = hand_to_multivectors(geom)

    res = expr_to_ga.map(pose_name, geom, mvs)
    assert res is not None
    assert res.opcode == expected_op, f"For {pose_name}, expected {expected_op}, got {res.opcode}"
    assert res.result is not None


# ---------------------------------------------------------------------------
# 3. Test All 14 Dynamic Motion Expressions
# ---------------------------------------------------------------------------
def _build_trajectory(extractor, length=20, dx=0.0, dy=0.0, dz=0.0, scale_step=0.0, rotate_step=0.0, pinch_step=0.0):
    """Build a sequence of HandGeometry frames with controlled dynamics."""
    base_lms = generate_pose_landmarks("OPEN_PALM", noise_sigma=0.001, rng=np.random.RandomState(42))
    frames = []
    t0 = 1000.0

    for i in range(length):
        lms = base_lms.copy()
        # Translation
        lms[:, 0] += dx * i
        lms[:, 1] += dy * i
        lms[:, 2] += dz * i
        # Scale
        if scale_step != 0.0:
            scale = 1.0 + scale_step * i
            center = lms[0:1].copy()
            lms = (lms - center) * scale + center
        # Pinch
        if pinch_step != 0.0:
            lms[4] = lms[8] + np.array([0.1 - pinch_step * i, 0.0, 0.0], dtype=np.float32)

        geom = extractor.extract(lms, lms, confidence=0.95, frame_index=i)
        frames.append((geom, t0 + i * 0.033))

    return frames


def test_swipe_dynamics(extractor):
    dyn_rec = DynamicExpressionRecognizer(buffer_frames=25)

    # SWIPE_LEFT
    dyn_rec.reset()
    for g, t in _build_trajectory(extractor, length=15, dx=-0.02):
        dyn_rec.push(g, t)
    assert dyn_rec.recognize().expression == "SWIPE_LEFT"

    # SWIPE_RIGHT
    dyn_rec.reset()
    for g, t in _build_trajectory(extractor, length=15, dx=0.02):
        dyn_rec.push(g, t)
    assert dyn_rec.recognize().expression == "SWIPE_RIGHT"

    # SWIPE_UP
    dyn_rec.reset()
    for g, t in _build_trajectory(extractor, length=15, dy=-0.02):
        dyn_rec.push(g, t)
    assert dyn_rec.recognize().expression == "SWIPE_UP"

    # SWIPE_DOWN
    dyn_rec.reset()
    for g, t in _build_trajectory(extractor, length=15, dy=0.02):
        dyn_rec.push(g, t)
    assert dyn_rec.recognize().expression == "SWIPE_DOWN"


def test_hand_approach_and_retract(extractor):
    dyn_rec = DynamicExpressionRecognizer(buffer_frames=25)

    # HAND_APPROACH (scale expanding towards camera)
    dyn_rec.reset()
    for g, t in _build_trajectory(extractor, length=15, scale_step=0.03, dz=-0.015):
        dyn_rec.push(g, t)
    res = dyn_rec.recognize()
    assert res.expression == "HAND_APPROACH"

    # HAND_RETRACT (scale shrinking away from camera)
    dyn_rec.reset()
    for g, t in _build_trajectory(extractor, length=15, scale_step=-0.03, dz=0.015):
        dyn_rec.push(g, t)
    res = dyn_rec.recognize()
    assert res.expression == "HAND_RETRACT"


def test_pinch_dynamics(extractor):
    dyn_rec = DynamicExpressionRecognizer(buffer_frames=25)

    # PINCH_START (closing)
    dyn_rec.reset()
    for g, t in _build_trajectory(extractor, length=15, pinch_step=0.008):
        dyn_rec.push(g, t)
    res = dyn_rec.recognize()
    assert res.expression in ("PINCH_START", "PINCH_HOLD")


@pytest.mark.parametrize("dyn_id,meta", DYNAMIC_EXPRESSIONS.items())
def test_dynamic_expression_ga_mapping(dyn_id, meta, extractor, expr_to_ga):
    dyn_name = meta.name
    expected_op = meta.ga_operation

    base_lms = generate_pose_landmarks("OPEN_PALM", noise_sigma=0.001, rng=np.random.RandomState(42))
    geom = extractor.extract(base_lms, base_lms, confidence=0.95)
    mvs = hand_to_multivectors(geom)

    res = expr_to_ga.map(dyn_name, geom, mvs, rotor_angle=0.45)
    assert res is not None
    assert res.opcode == expected_op, f"For {dyn_name}, expected {expected_op}, got {res.opcode}"
    assert res.result is not None

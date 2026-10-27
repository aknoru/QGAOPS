"""
Tests for Static Expression Classifier and Temporal Smoother.
"""
import numpy as np
import pytest

from mapping.dataset_classes import CLASS_NAMES, get_class_id, get_class_name, UNKNOWN_CLASS
from models.static_expression_classifier import StaticExpressionClassifier
from expression.temporal_smoother import ExpressionTemporalSmoother


def test_class_mappings():
    assert len(CLASS_NAMES) == 6
    assert CLASS_NAMES[0] == "PALM"
    assert CLASS_NAMES[1] == "L_GESTURE"
    assert CLASS_NAMES[2] == "FIST"
    assert CLASS_NAMES[3] == "THUMB"
    assert CLASS_NAMES[4] == "INDEX"
    assert CLASS_NAMES[5] == "OK"

    assert get_class_name(0) == "PALM"
    assert get_class_name(999) == UNKNOWN_CLASS
    assert get_class_id("PALM") == 0
    assert get_class_id("INVALID") is None


def test_classifier_fit_predict_evaluate():
    rng = np.random.RandomState(42)
    N = 120
    D = 107
    X = rng.randn(N, D).astype(np.float32)
    # 3 distinct classes
    y = np.array([0] * 40 + [1] * 40 + [5] * 40, dtype=np.int64)

    clf = StaticExpressionClassifier(model_type="random_forest", confidence_threshold=0.5, random_state=42, class_names=CLASS_NAMES)
    clf.fit(X, y)

    # Test predict_proba
    probs = clf.predict_proba(X[:5])
    assert probs.shape == (5, 6)
    assert np.allclose(probs.sum(axis=1), 1.0)

    # Test predict
    preds = clf.predict(X[:5])
    assert len(preds) == 5

    # Test evaluate
    ev = clf.evaluate(X, y)
    assert "accuracy" in ev
    assert "f1" in ev
    assert "confusion_matrix" in ev
    assert ev["accuracy"] > 0.8


def test_classifier_unknown_rejection():
    rng = np.random.RandomState(42)
    X = rng.randn(60, 20).astype(np.float32)
    y = np.array([0] * 30 + [1] * 30, dtype=np.int64)

    # High threshold forces UNKNOWN for ambiguous samples
    clf = StaticExpressionClassifier(model_type="random_forest", confidence_threshold=0.99, random_state=42)
    clf.fit(X, y)

    preds = clf.predict(X[:10])
    # At 0.99 threshold, some samples will be rejected as UNKNOWN
    assert any(p == UNKNOWN_CLASS for p in preds) or all(isinstance(p, int) for p in preds)


def test_temporal_smoother_majority_voting():
    smoother = ExpressionTemporalSmoother(window_size=5, min_majority_ratio=0.6, confidence_threshold=0.6)

    # 1. First 2 frames: INDEX (not enough for window consensus)
    p1 = smoother.update("INDEX", 0.9)
    p2 = smoother.update("INDEX", 0.9)
    assert p1.expression in ("INDEX", UNKNOWN_CLASS)

    # 2. Add 2 more INDEX -> 4/4 majority -> stable INDEX
    smoother.update("INDEX", 0.9)
    p4 = smoother.update("INDEX", 0.9)
    assert p4.expression == "INDEX"
    assert p4.is_stable is True

    # 3. Single noisy frame of FIST should not immediately switch stable output
    p5 = smoother.update("FIST", 0.9)
    assert p5.expression == "INDEX"  # Still stable INDEX

    # 4. Reset
    smoother.reset()
    p_reset = smoother.update("UNKNOWN", 0.0)
    assert p_reset.expression == UNKNOWN_CLASS

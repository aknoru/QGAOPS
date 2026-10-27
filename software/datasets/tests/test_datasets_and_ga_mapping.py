import numpy as np
import pytest

from software.datasets.dimension_preserving_ga_map import (
    vector_to_multivectors,
    multivectors_to_vector,
    ga_l2_distance,
    ga_dot_product,
)
from software.datasets.vector_dataset_adapters import (
    validate_dataset_availability,
    run_vector_workload_benchmark,
)
from software.datasets.leap_gesture_evaluator import evaluate_leap_gesture_dataset


@pytest.mark.parametrize("dim", [1, 2, 3, 4, 8, 96, 128, 960])
def test_ga_mapping_roundtrip_and_dimension_preservation(dim):
    rng = np.random.default_rng(1234)
    original = rng.standard_normal(dim)
    
    mvs = vector_to_multivectors(original)
    expected_num_mvs = int(np.ceil(dim / 3))
    assert len(mvs) == expected_num_mvs
    
    reconstructed = multivectors_to_vector(mvs, dim)
    assert reconstructed.shape == (dim,)
    np.testing.assert_allclose(reconstructed, original, atol=1e-12)


@pytest.mark.parametrize("dim", [96, 128, 960])
def test_ga_l2_and_dot_exact_equivalence_with_numpy(dim):
    rng = np.random.default_rng(5678)
    a = rng.standard_normal(dim)
    b = rng.standard_normal(dim)
    
    ga_dist, metrics = ga_l2_distance(a, b)
    np_dist = float(np.linalg.norm(a - b))
    
    ga_dot, dot_metrics = ga_dot_product(a, b)
    np_dot = float(np.dot(a, b))
    
    assert abs(ga_dist - np_dist) < 1e-10
    assert abs(ga_dot - np_dot) < 1e-10
    assert metrics["multivectors_per_vector"] == int(np.ceil(dim / 3))


def test_vector_dataset_availability_and_audit():
    for dataset_id in ["deep1m", "sift1m", "gist1m"]:
        audit = validate_dataset_availability(dataset_id)
        assert audit["dataset_id"] == dataset_id
        assert audit["dimension"] in [96, 128, 960]
        assert audit["status"] in ["AVAILABLE", "BLOCKED_DATA_UNAVAILABLE"]


def test_vector_workload_benchmarking():
    for dataset_id in ["deep1m", "sift1m", "gist1m"]:
        res = run_vector_workload_benchmark(dataset_id, num_pairs=10, use_synthetic_if_missing=True)
        assert res["equivalent_to_numpy"] is True
        assert res["max_l2_error_vs_numpy"] < 1e-5
        assert res["max_dot_error_vs_numpy"] < 1e-4


def test_leap_hand_gesture_evaluation():
    res = evaluate_leap_gesture_dataset()
    assert res["status"] == "VALIDATED_REAL"
    assert res["landmark_classifier"]["test_accuracy"] > 0.90
    assert res["image_baseline_classifier"]["test_accuracy"] > 0.90

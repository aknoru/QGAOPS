import json
from pathlib import Path

from software.benchmarks.workloads import WorkloadConfig, generate_pairs, workload_record
from software.gesture_pipeline.pipeline import load_fixture, nearest_centroid
from software.hardware_interface.contract import OperationRequest, deserialize, serialize
from software.reference_model.qgaops_reference import FixedPointMultivector


def test_workloads_are_deterministic():
    config = WorkloadConfig(count=8, seed=7, distribution="sparse")
    assert workload_record(config) == workload_record(config)
    assert len(generate_pairs(config)) == 8


def test_fixture_pipeline_is_software_only_and_deterministic():
    root = Path(__file__).parents[1]
    samples = load_fixture(Path(__file__).parents[1].parent / "gesture_pipeline" / "fixtures.json")
    result = nearest_centroid(samples)
    assert result["sample_count"] == 4
    assert result["accuracy"] == 1.0


def test_hardware_contract_round_trip_and_fixed_result():
    values = FixedPointMultivector.from_reals([1.0] + [0.0] * 7)
    request = OperationRequest("geometric_product", values.coefficients, values.coefficients)
    assert deserialize(serialize(request)) == request

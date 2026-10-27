"""
tests/test_scheduler.py — Scheduler unit tests.
[IMPLEMENTED] [SOFTWARE-VALIDATED]
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import pytest
from ga.ir import make_ir, OperationIR
from engine.operation_scheduler import OperationScheduler, ExecutionSchedule


@pytest.fixture
def scheduler():
    return OperationScheduler(backend="python", precision="FLOAT32")


def test_empty_schedule(scheduler):
    s = scheduler.schedule([])
    assert s.total_ops == 0
    assert s.peak_live == 0


def test_single_op_schedule(scheduler):
    ops = [make_ir("GP", ["v1", "v2"], "r1")]
    s = scheduler.schedule(ops)
    assert s.total_ops == 1
    assert len(s.steps) == 1


def test_dependency_chain(scheduler):
    ops = [
        make_ir("GP",    ["v1", "v2"], "r1"),
        make_ir("WEDGE", ["r1", "v3"], "r2"),   # depends on r1
        make_ir("NORM",  ["r2"],       "r3"),   # depends on r2
    ]
    s = scheduler.schedule(ops)
    assert len(s.steps) == 3
    # Step 1 should depend on step 0
    assert 0 in s.steps[1].dependencies
    # Step 2 should depend on step 1
    assert 1 in s.steps[2].dependencies


def test_no_false_dependencies(scheduler):
    ops = [
        make_ir("GP",   ["v1", "v2"], "r1"),
        make_ir("GP",   ["v3", "v4"], "r2"),   # no dependency on r1
    ]
    s = scheduler.schedule(ops)
    assert s.steps[1].dependencies == []


def test_memory_b0_positive(scheduler):
    ops = [make_ir("GP", ["v1", "v2"], "r1") for _ in range(10)]
    s = scheduler.schedule(ops)
    assert s.b0_materialize > 0


def test_memory_b5_leq_b4(scheduler):
    ops = [
        make_ir("GP",      ["v1", "v2"], "r1"),
        make_ir("REVERSE", ["r1"],       "r1_rev"),
        make_ir("GP",      ["v1", "r1_rev"], "sandwich"),
    ]
    s = scheduler.schedule(ops)
    assert s.b5_fusion <= s.b4_lifetime_reuse


def test_fusion_detected_in_sandwich_chain(scheduler):
    # GP → REVERSE → GP = sandwich pattern
    ops = [
        make_ir("GP",      ["R", "v"],   "Rv"),
        make_ir("REVERSE", ["R"],        "R_rev"),
        make_ir("GP",      ["Rv", "R_rev"], "result"),
    ]
    s = scheduler.schedule(ops)
    assert s.fusion_opportunities >= 1


def test_schedule_peak_live_positive(scheduler):
    ops = [make_ir("GP", ["v1", "v2"], "r1")]
    s = scheduler.schedule(ops)
    assert s.peak_live >= 1


def test_schedule_summary_string(scheduler):
    ops = [make_ir("GP", ["a", "b"], "c")]
    s = scheduler.schedule(ops)
    summary = s.summary()
    assert "ExecutionSchedule" in summary
    assert "memory" in summary.lower()

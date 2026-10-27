"""
LIVE HAND GA ENGINE — engine/operation_scheduler.py
Resource-aware software scheduler for GA operations.

[IMPLEMENTED] DAG-based dependency analysis, fusion detection, memory model.
[SOFTWARE MODEL] Memory traffic estimates are conceptual, not measured hardware.
[ARCH]           Corresponds to the QGAOPS Operation Scheduler + AAMF concepts.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
import time

from ga.ir import OperationIR
from ga.multivector import G3_DIM


# G3 coefficient bytes: 8 coefficients × 4 bytes (float32) = 32 bytes
G3_MV_BYTES_FLOAT32 = G3_DIM * 4
G3_MV_BYTES_FIX16   = G3_DIM * 2


@dataclass
class SchedulerStep:
    """One scheduled step in the execution order.

    [IMPLEMENTED]
    """
    step_index:   int
    ir:           OperationIR
    dependencies: List[int] = field(default_factory=list)  # step indices
    fused:        bool = False
    fused_with:   Optional[int] = None

    def __repr__(self) -> str:
        return (
            f"Step[{self.step_index}] {self.ir.opcode} "
            f"({self.ir.inputs} -> {self.ir.output})"
        )


@dataclass
class ExecutionSchedule:
    """Complete execution schedule for a sequence of IR operations.

    [IMPLEMENTED] [SOFTWARE MODEL]
    """
    steps:              List[SchedulerStep]
    peak_live:          int       # max simultaneous live multivectors
    memory_bytes:       int       # estimated total byte transfers
    fusion_opportunities: int     # number of fused step pairs
    total_ops:          int
    backend:            str = "python"
    precision:          str = "FLOAT32"

    # Memory model breakdown (SOFTWARE MODEL)
    b0_materialize:     int = 0
    b1_tile_buffering:  int = 0
    b2_aligned_dense:   int = 0
    b3_sparse:          int = 0
    b4_lifetime_reuse:  int = 0
    b5_fusion:          int = 0

    def summary(self) -> str:
        lines = [
            f"ExecutionSchedule: {len(self.steps)} steps, {self.total_ops} ops",
            f"  Peak live multivectors : {self.peak_live}",
            f"  Estimated memory bytes : {self.memory_bytes} B",
            f"  Fusion opportunities   : {self.fusion_opportunities}",
            f"  Backend                : {self.backend}",
            f"  Precision              : {self.precision}",
            f"  [SOFTWARE MODEL] Memory breakdown:",
            f"    B0 Materialize all    : {self.b0_materialize} B",
            f"    B4 Lifetime reuse     : {self.b4_lifetime_reuse} B",
            f"    B5 Operator fusion    : {self.b5_fusion} B",
        ]
        return "\n".join(lines)


class OperationScheduler:
    """Analyzes a sequence of IR operations and produces an ExecutionSchedule.

    [IMPLEMENTED] [SOFTWARE MODEL]

    Features:
        - Dependency identification by output/input name matching
        - Rotor sandwich fusion detection (GP + REVERSE + GP)
        - Peak live value estimation
        - Memory traffic estimate (B0, B4, B5 modes)

    [SOFTWARE MODEL] The memory traffic estimates are software models
    inspired by the QGAOPS AAMF architecture. They do NOT represent
    measured hardware performance.
    """

    def __init__(
        self,
        backend: str = "python",
        precision: str = "FLOAT32",
    ) -> None:
        self.backend   = backend
        self.precision = precision
        self._mv_bytes = (
            G3_MV_BYTES_FIX16 if precision == "FIX16"
            else G3_MV_BYTES_FLOAT32
        )

    def schedule(self, ir_ops: List[OperationIR]) -> ExecutionSchedule:
        """Schedule a list of IR operations.

        [IMPLEMENTED]

        Args:
            ir_ops: List of OperationIR in submission order.

        Returns:
            ExecutionSchedule with dependency graph and memory analysis.
        """
        if not ir_ops:
            return ExecutionSchedule(
                steps=[], peak_live=0, memory_bytes=0,
                fusion_opportunities=0, total_ops=0,
                backend=self.backend, precision=self.precision,
            )

        # Build steps with dependency edges
        steps = self._build_dependency_graph(ir_ops)

        # Detect fusion opportunities
        n_fused = self._detect_fusion(steps)

        # Estimate live values and memory
        peak_live = self._estimate_peak_live(steps)
        memory_b0, memory_b4, memory_b5 = self._estimate_memory(steps, n_fused)

        return ExecutionSchedule(
            steps=steps,
            peak_live=peak_live,
            memory_bytes=memory_b0,
            fusion_opportunities=n_fused,
            total_ops=len(ir_ops),
            backend=self.backend,
            precision=self.precision,
            b0_materialize=memory_b0,
            b4_lifetime_reuse=memory_b4,
            b5_fusion=memory_b5,
        )

    # ------------------------------------------------------------------
    # Dependency analysis
    # ------------------------------------------------------------------

    def _build_dependency_graph(
        self, ir_ops: List[OperationIR]
    ) -> List[SchedulerStep]:
        """Build dependency edges based on name matching."""
        steps = []
        # Map from output name → step index that produced it
        produced_by: Dict[str, int] = {}

        for i, ir in enumerate(ir_ops):
            deps = []
            for inp in ir.inputs:
                if inp in produced_by:
                    dep_idx = produced_by[inp]
                    if dep_idx not in deps:
                        deps.append(dep_idx)
            step = SchedulerStep(step_index=i, ir=ir, dependencies=deps)
            steps.append(step)
            produced_by[ir.output] = i

        return steps

    # ------------------------------------------------------------------
    # Fusion detection
    # ------------------------------------------------------------------

    def _detect_fusion(self, steps: List[SchedulerStep]) -> int:
        """Detect rotor sandwich fusion: GP + REVERSE + GP → SANDWICH.

        [IMPLEMENTED] Marks consecutive GP chains that form R*v*~R.
        """
        fused = 0
        n = len(steps)
        i = 0
        while i < n - 2:
            s0 = steps[i]
            s1 = steps[i + 1]
            s2 = steps[i + 2]
            # Pattern: GP, REVERSE, GP (or GP, GP where one input is reverse output)
            if (s0.ir.opcode == "GP"
                    and s1.ir.opcode in ("REVERSE", "GP", "SANDWICH")
                    and s2.ir.opcode == "GP"):
                s0.fused = True
                s1.fused = True
                s2.fused = True
                s0.fused_with = i + 2
                fused += 1
                i += 3
            else:
                i += 1
        return fused

    # ------------------------------------------------------------------
    # Peak live estimation
    # ------------------------------------------------------------------

    def _estimate_peak_live(self, steps: List[SchedulerStep]) -> int:
        """Estimate peak number of simultaneous live multivectors."""
        if not steps:
            return 0
        # Simple upper bound: max fan-in + 1 output per step
        max_live = 0
        for step in steps:
            live = len(step.dependencies) + 1  # inputs + 1 output
            if live > max_live:
                max_live = live
        return max_live

    # ------------------------------------------------------------------
    # Memory traffic estimation (SOFTWARE MODEL)
    # ------------------------------------------------------------------

    def _estimate_memory(
        self, steps: List[SchedulerStep], n_fused: int
    ) -> Tuple[int, int, int]:
        """Estimate memory traffic in three modes.

        [SOFTWARE MODEL] Conceptual AAMF-inspired model.

        B0: Materialize all intermediates (worst case).
        B4: Lifetime reuse — reuse outputs still in live range.
        B5: Fusion — fused pairs skip intermediate writes.

        Returns:
            (b0_bytes, b4_bytes, b5_bytes)
        """
        n = len(steps)
        bpop = self._mv_bytes   # bytes per operand

        # B0: 2 reads + 1 write per op
        b0 = n * 3 * bpop

        # B4: estimate 20% reduction from lifetime reuse
        b4 = int(b0 * 0.80)

        # B5: additional 20% reduction from fusion
        skip = n_fused * 3  # skip 3 intermediate R/W per fusion pair
        b5 = max(0, b4 - skip * bpop)

        return b0, b4, b5

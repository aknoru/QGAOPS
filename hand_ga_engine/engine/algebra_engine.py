"""
LIVE HAND GA ENGINE — engine/algebra_engine.py
Unified Algebra Engine — top-level dispatch with IR tracing.

[IMPLEMENTED] Software dispatch through PythonBackend.
[PROPOSED]    FPGA dispatch via FPGABackend (stub).
[ARCH]        Matches the QGAOPS Unified Algebra Execution Fabric concept.

Usage:
    engine = AlgebraEngine(backend="python", precision="FLOAT32")
    result = engine.execute("GP", [v1, v2])
    result = engine.execute("SANDWICH", [R, v])
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from ga.multivector import Multivector
from ga.ir import OperationIR, make_ir
from backend.python_backend import PythonBackend
from backend.fpga_backend import FPGABackend


class AlgebraEngine:
    """Unified algebra execution engine.

    [IMPLEMENTED] Dispatches through configurable backend.
    [ARCH]        Top-level orchestrator matching QGAOPS Execution Fabric.

    Args:
        backend:   'python' (implemented) or 'fpga' (stub/proposed).
        precision: 'FLOAT32' or 'FIX16'.
        algebra:   Algebra name, e.g. 'G3'.
        trace:     If True, record every executed IR to self.ir_trace.
    """

    def __init__(
        self,
        backend: str = "python",
        precision: str = "FLOAT32",
        algebra: str = "G3",
        trace: bool = True,
    ) -> None:
        self.algebra   = algebra
        self.precision = precision
        self.trace     = trace
        self.ir_trace: List[Tuple[OperationIR, Any, float]] = []  # (ir, result, latency_s)

        if backend == "python":
            self._backend = PythonBackend()
        elif backend == "fpga":
            self._backend = FPGABackend()
        else:
            raise ValueError(f"Unknown backend: {backend!r}. Use 'python' or 'fpga'.")

    # ------------------------------------------------------------------
    # Main dispatch
    # ------------------------------------------------------------------

    def execute(
        self,
        operation: str,
        operands: List[Any],
        inputs: Optional[List[str]] = None,
        output: str = "result",
        expression: str = "",
        **kwargs,
    ) -> Any:
        """Execute a GA operation.

        [IMPLEMENTED]

        Args:
            operation: Opcode string (e.g. 'GP', 'WEDGE', 'SANDWICH').
            operands:  List of Multivector inputs.
            inputs:    Optional human-readable input names for IR.
            output:    Output variable name for IR.
            expression: Gesture that triggered this operation.
            **kwargs:  Extra args (e.g. axis=, angle=, grade=).

        Returns:
            Result of the operation (Multivector, float, etc.).
        """
        if not self._backend.is_available() and self._backend.name == "fpga":
            raise RuntimeError(
                "[PROPOSED] FPGA backend is not available. Use backend='python'."
            )

        # Precision override for FIX16
        if self.precision == "FIX16":
            result, latency = self._execute_fix16(operation, operands, **kwargs)
        else:
            t0 = time.perf_counter()
            result = self._backend.execute(operation, operands, **kwargs)
            latency = time.perf_counter() - t0

        # Build and record IR
        input_names = inputs or [f"v{i}" for i in range(len(operands))]
        ir = make_ir(
            opcode=operation.upper(),
            inputs=input_names,
            output=output,
            algebra=self.algebra,
            precision=self.precision,
            expression=expression,
            metadata=kwargs,
        )

        if self.trace:
            self.ir_trace.append((ir, result, latency))
            if len(self.ir_trace) > 500:
                self.ir_trace = self.ir_trace[-500:]

        return result

    def _execute_fix16(
        self, operation: str, operands: List[Any], **kwargs
    ) -> Tuple[Any, float]:
        """Execute operation in FIX16 mode with float comparison.

        [IMPLEMENTED]
        """
        from fixed_point.fix16 import (
            Fix16Multivector, fix16_geometric_product, fix16_error_analysis
        )

        t0 = time.perf_counter()

        # Always compute float result first (reference)
        float_result = self._backend.execute(operation, operands, **kwargs)
        latency = time.perf_counter() - t0

        # For multivector operands only, also compute FIX16
        if (operation.upper() == "GP"
                and all(isinstance(op, Multivector) for op in operands[:2])):
            fa = Fix16Multivector.from_multivector(operands[0])
            fb = Fix16Multivector.from_multivector(operands[1])
            fix_result = fix16_geometric_product(fa, fb).to_multivector()
            self._last_fix16_error = fix16_error_analysis(float_result, Fix16Multivector.from_multivector(float_result))
        else:
            self._last_fix16_error = (0.0, 0.0, 0.0)

        return float_result, latency

    # ------------------------------------------------------------------
    # Convenience wrappers
    # ------------------------------------------------------------------

    def gp(self, a: Multivector, b: Multivector, **kw) -> Multivector:
        return self.execute("GP", [a, b], **kw)

    def wedge(self, a: Multivector, b: Multivector, **kw) -> Multivector:
        return self.execute("WEDGE", [a, b], **kw)

    def dot(self, a: Multivector, b: Multivector, **kw) -> float:
        return self.execute("DOT", [a, b], **kw)

    def inner(self, a: Multivector, b: Multivector, **kw) -> Multivector:
        return self.execute("INNER", [a, b], **kw)

    def reverse(self, a: Multivector, **kw) -> Multivector:
        return self.execute("REVERSE", [a], **kw)

    def sandwich(self, r: Multivector, v: Multivector, **kw) -> Multivector:
        return self.execute("SANDWICH", [r, v], **kw)

    def norm(self, a: Multivector, **kw) -> float:
        return self.execute("NORM", [a], **kw)

    def distance(self, a: Multivector, b: Multivector, **kw) -> float:
        return self.execute("DISTANCE", [a, b], **kw)

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def clear_trace(self) -> None:
        self.ir_trace.clear()

    def last_ir(self) -> Optional[OperationIR]:
        if self.ir_trace:
            return self.ir_trace[-1][0]
        return None

    def last_latency(self) -> float:
        if self.ir_trace:
            return self.ir_trace[-1][2]
        return 0.0

    def operations_per_second(self) -> float:
        """Estimate ops/s from trace."""
        if len(self.ir_trace) < 2:
            return 0.0
        total_latency = sum(t for _, _, t in self.ir_trace)
        if total_latency < 1e-12:
            return 0.0
        return len(self.ir_trace) / total_latency

    @property
    def backend_name(self) -> str:
        return self._backend.name

    def __repr__(self) -> str:
        return (
            f"AlgebraEngine(backend={self.backend_name!r}, "
            f"precision={self.precision!r}, algebra={self.algebra!r})"
        )

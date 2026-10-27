"""
LIVE HAND GA ENGINE — backend/python_backend.py
Python/NumPy execution backend.

[IMPLEMENTED] All GA operations dispatch through this backend.
"""
from __future__ import annotations
from typing import Any, List, Optional
from ga.multivector import Multivector
from ga import (
    geometric_product, outer_product, inner_product, dot, wedge,
    reverse, dual, norm, normalize, commutator, anticommutator,
    sandwich_product, rotor_from_axis_angle, rotor_reverse,
    vector_angle, vector_length, bivector_magnitude,
)
import numpy as np


class PythonBackend:
    """Python/NumPy execution backend for GA operations.

    [IMPLEMENTED] Dispatches all operations through the ga module.
    [ARCH]        This is the software golden model for QGAOPS-QGPU.
                  All results produced here are the reference for RTL verification.
    """

    name = "python"

    def execute(self, operation: str, operands: List[Any], **kwargs) -> Any:
        """Dispatch an operation by name.

        [IMPLEMENTED]

        Args:
            operation: Opcode string (e.g., 'GP', 'WEDGE', 'DOT').
            operands:  List of Multivector or scalar inputs.
            **kwargs:  Extra parameters (e.g., axis, angle, grade).

        Returns:
            Result (Multivector, float, or other appropriate type).
        """
        op = operation.upper()

        if op == "GP":
            return geometric_product(operands[0], operands[1])
        elif op == "WEDGE":
            return outer_product(operands[0], operands[1])
        elif op == "INNER":
            return inner_product(operands[0], operands[1])
        elif op == "DOT":
            return dot(operands[0], operands[1])
        elif op == "REVERSE":
            return reverse(operands[0])
        elif op == "SANDWICH":
            return sandwich_product(operands[0], operands[1])
        elif op == "ROTOR":
            axis  = kwargs.get("axis", np.array([0.0, 0.0, 1.0]))
            angle = kwargs.get("angle", 0.0)
            return rotor_from_axis_angle(axis, angle)
        elif op == "NORM":
            return norm(operands[0])
        elif op == "NORMALIZE":
            return normalize(operands[0])
        elif op == "DUAL":
            return dual(operands[0])
        elif op == "COMMUTATOR":
            return commutator(operands[0], operands[1])
        elif op == "ANTI_COMM":
            return anticommutator(operands[0], operands[1])
        elif op == "DISTANCE":
            va = operands[0].vector_part()
            vb = operands[1].vector_part()
            return float(np.linalg.norm(va - vb))
        elif op == "VECTOR_ANGLE":
            return vector_angle(operands[0], operands[1])
        elif op == "ADD":
            return operands[0] + operands[1]
        elif op == "SUB":
            return operands[0] - operands[1]
        elif op == "SCALE":
            return operands[0] * float(operands[1])
        elif op == "CROSS":
            from ga.geometric_product import cross_product_mv
            return cross_product_mv(operands[0], operands[1])
        elif op == "GRADE":
            g = kwargs.get("grade", 1)
            return operands[0].grade_part(g)
        else:
            raise ValueError(f"Unknown operation: {operation!r}")

    def is_available(self) -> bool:
        """Python backend is always available."""
        return True

    def __repr__(self) -> str:
        return "PythonBackend()"

"""
LIVE HAND GA ENGINE — ga/__init__.py
Public API of the ga package.
"""
from .multivector import Multivector
from .basis import BasisElement, G3_BASIS, generate_basis, grade, sign_product
from .metric import Metric, G3_METRIC
from .geometric_product import (
    geometric_product, outer_product, inner_product, dot, wedge,
    cross_product_mv, cross_product_vec,
    verify_distributivity, verify_associativity, verify_gp_decomposition,
)
from .operations import (
    reverse, dual, grade_involution, commutator, anticommutator,
    norm, normalize, vector_angle, vector_length, bivector_magnitude,
)
from .rotor import (
    rotor_from_axis_angle, rotor_from_two_vectors, rotor_reverse,
    rotor_compose, sandwich_product, rotor_norm, verify_rotor_unit,
    extract_axis_angle,
)
from .ir import OperationIR, make_ir, save_ir_sequence, load_ir_sequence

__all__ = [
    "Multivector",
    "BasisElement", "G3_BASIS", "generate_basis", "grade", "sign_product",
    "Metric", "G3_METRIC",
    "geometric_product", "outer_product", "inner_product", "dot", "wedge",
    "cross_product_mv", "cross_product_vec",
    "verify_distributivity", "verify_associativity", "verify_gp_decomposition",
    "reverse", "dual", "grade_involution", "commutator", "anticommutator",
    "norm", "normalize", "vector_angle", "vector_length", "bivector_magnitude",
    "rotor_from_axis_angle", "rotor_from_two_vectors", "rotor_reverse",
    "rotor_compose", "sandwich_product", "rotor_norm", "verify_rotor_unit",
    "extract_axis_angle",
    "OperationIR", "make_ir", "save_ir_sequence", "load_ir_sequence",
]

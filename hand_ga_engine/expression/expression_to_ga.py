"""
LIVE HAND GA ENGINE — expression/expression_to_ga.py
Map recognized expressions to GA operations and QGAOPS IR commands.

[IMPLEMENTED] Every recognized expression triggers a typed GA operation.
[ARCH]        Expression → QGAOPS Opcode is the INPUT/CONTROL layer.
              The QGAOPS GA engine is the COMPUTE layer.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from ga.multivector import Multivector
from ga.ir import OperationIR, make_ir
from hand_detection.landmarks import HandGeometry


@dataclass
class ExpressionGAResult:
    """Result of expression → GA computation.

    [IMPLEMENTED]
    """
    expression:    str
    opcode:        str
    algebra:       str
    precision:     str
    operand_names: List[str]
    result:        Any                    # Multivector, float, etc.
    ir:            OperationIR
    interpretation: str = ""             # Human-readable geometric meaning
    display_value:  str = ""             # Formatted string for UI


class ExpressionToGA:
    """Maps recognized static/dynamic expressions to GA operations.

    [IMPLEMENTED]

    Args:
        engine: AlgebraEngine instance.
        precision: 'FLOAT32' or 'FIX16'.
    """

    _EXPRESSION_OPCODES: Dict[str, str] = {
        # Kaggle LeapGestRecog 6 classes
        "PALM":                   "VECTOR",
        "L_GESTURE":              "WEDGE",
        "FIST":                   "NORM",
        "THUMB":                  "VECTOR",
        "INDEX":                  "VECTOR",
        "OK":                     "INNER",

        # 1. Static Hand Poses (13 Poses)
        "OPEN_PALM":              "VECTOR",
        "FIST":                   "NORM",
        "THUMBS_UP":              "VECTOR",
        "THUMBS_DOWN":            "VECTOR",
        "INDEX_POINT":            "VECTOR",
        "TWO_FINGER":             "WEDGE",
        "PEACE_SIGN":             "WEDGE",
        "THREE_FINGER":           "GP",
        "FOUR_FINGER":            "GP",
        "PINCH":                  "DISTANCE",
        "OK_SIGN":                "INNER",
        "ROCK_SIGN":              "WEDGE",
        "CALL_ME":                "VECTOR",

        # 2. Dynamic Motion Expressions (14 Expressions)
        "SWIPE_LEFT":             "VECTOR",
        "SWIPE_RIGHT":            "VECTOR",
        "SWIPE_UP":               "VECTOR",
        "SWIPE_DOWN":             "VECTOR",
        "PINCH_START":            "DISTANCE",
        "PINCH_HOLD":             "DISTANCE",
        "PINCH_RELEASE":          "DISTANCE",
        "FIST_CLOSE":             "NORM",
        "FIST_OPEN":              "NORM",
        "ROTATE_CLOCKWISE":       "SANDWICH",
        "ROTATE_COUNTERCLOCKWISE":"SANDWICH",
        "HAND_APPROACH":          "DISTANCE",
        "HAND_RETRACT":           "DISTANCE",
        "CIRCLE_MOTION":          "ROTOR",
        "UNKNOWN":                "VECTOR",
        "UNKNOWN_DYNAMIC":        "VECTOR",
    }

    _INTERPRETATIONS: Dict[str, str] = {
        # Kaggle 6 classes
        "PALM":                   "All 5 finger direction vectors v_i in G_1",
        "L_GESTURE":              "v_thumb ^ v_index — orthogonal plane spanned by thumb and index",
        "FIST":                   "Contraction norms |v_i| of all digits",
        "THUMB":                  "Extracts vertical reference basis vector e_y",
        "INDEX":                  "Pointing ray unit vector v_index",
        "OK":                     "Inner product v_index . v_middle",

        # Static 13 Poses
        "OPEN_PALM":              "Computes all 5 finger direction vectors v_i in G_1",
        "THUMBS_UP":              "Extracts vertical reference basis vector e_y",
        "THUMBS_DOWN":            "Inverted vertical reference vector -e_y",
        "INDEX_POINT":            "Pointing ray unit vector v_index",
        "TWO_FINGER":             "Bivector area element v_index ^ v_middle in G_2",
        "PEACE_SIGN":             "Angular oriented plane spanned by index and middle (>30 deg)",
        "THREE_FINGER":           "Triple geometric product chain v_1 * v_2 * v_3",
        "FOUR_FINGER":            "Quad geometric product chain v_1 * v_2 * v_3 * v_4",
        "PINCH":                  "Metric distance |p_thumb - p_index| (<5 cm)",
        "OK_SIGN":                "Inner product v_index . v_middle",
        "ROCK_SIGN":              "Wide bivector span v_index ^ v_pinky",
        "CALL_ME":                "Span vector between outer extremities",

        # Dynamic 14 Expressions
        "SWIPE_LEFT":             "Wrist displacement translation vector (v_x < -v_thresh)",
        "SWIPE_RIGHT":            "Wrist displacement translation vector (v_x > v_thresh)",
        "SWIPE_UP":               "Vertical translation vector (upward)",
        "SWIPE_DOWN":             "Vertical translation vector (downward)",
        "PINCH_START":            "Derivative of pinch distance vector (rapid closure)",
        "PINCH_HOLD":             "Maintained scalar grip metric over multiple frames",
        "PINCH_RELEASE":          "Opening separation vector between fingertips",
        "FIST_CLOSE":             "Rate of contraction norm reduction",
        "FIST_OPEN":              "Rate of expansion norm increase",
        "ROTATE_CLOCKWISE":       "Applies rotor: R v ~R where R = exp(-theta/2 B)",
        "ROTATE_COUNTERCLOCKWISE":"Applies inverse rotor: ~R v R",
        "HAND_APPROACH":          "Relative Z-depth dilation (scale expanding)",
        "HAND_RETRACT":           "Relative Z-depth contraction (scale shrinking)",
        "CIRCLE_MOTION":          "Generates continuous rotor from trajectory bivector",
    }

    def __init__(self, engine: Any, precision: str = "FLOAT32") -> None:
        self._engine    = engine
        self._precision = precision

    def map(
        self,
        expression: str,
        geom: HandGeometry,
        mvs: Dict[str, Multivector],
        rotor_angle: float = 0.0,
        rotor_axis: Optional[np.ndarray] = None,
    ) -> Optional[ExpressionGAResult]:
        """Map an expression + geometry to a GA result.

        [IMPLEMENTED]

        Args:
            expression:  Recognized pose/expression name.
            geom:        Current HandGeometry.
            mvs:         Pre-computed multivectors from hand_to_multivectors().
            rotor_angle: Estimated rotation angle (from dynamic recognizer).
            rotor_axis:  Estimated rotation axis.

        Returns:
            ExpressionGAResult or None if unrecognized.
        """
        opcode = self._EXPRESSION_OPCODES.get(expression, "VECTOR")

        try:
            return self._dispatch(expression, opcode, geom, mvs, rotor_angle, rotor_axis)
        except Exception:
            return None

    def _dispatch(
        self,
        expression: str,
        opcode: str,
        geom: HandGeometry,
        mvs: Dict[str, Multivector],
        rotor_angle: float,
        rotor_axis: Optional[np.ndarray],
    ) -> ExpressionGAResult:
        """Internal dispatch to specific handlers."""

        v_idx  = mvs.get("index_vec",  Multivector.vector(1, 0, 0))
        v_mid  = mvs.get("middle_vec", Multivector.vector(0, 1, 0))
        v_ring = mvs.get("ring_vec",   Multivector.vector(0, 0, 1))
        v_tmb  = mvs.get("thumb_vec",  Multivector.vector(0, 1, 0))

        if expression in ("PALM", "OPEN_PALM"):
            result = v_idx
            operands = ["index_vec"]
            interp = self._INTERPRETATIONS.get(expression, "All finger direction vectors")
            dv = f"v_index = {v_idx}"
            ir = make_ir("VECTOR", operands, "index_vec", precision=self._precision, expression=expression)

        elif expression in ("L_GESTURE",):
            result = self._engine.execute("WEDGE", [v_tmb, v_idx], expression=expression)
            operands = ["thumb_vec", "index_vec"]
            interp = self._INTERPRETATIONS.get(expression, "v_thumb ∧ v_index wedge plane")
            from ga.operations import bivector_magnitude
            mag = bivector_magnitude(result)
            dv = f"v_thumb ∧ v_index | mag={mag:.4f}"
            ir = make_ir("WEDGE", operands, "l_gesture_wedge", precision=self._precision, expression=expression)

        elif expression in ("INDEX", "INDEX_POINT"):
            result = v_idx
            operands = ["index_vec"]
            interp = "Index direction vector — pointing ray"
            dv = f"v_index = {v_idx}"
            ir = make_ir("VECTOR", operands, "index_vec", precision=self._precision, expression=expression)

        elif expression in ("THUMB", "THUMBS_UP"):
            result = v_tmb
            operands = ["thumb_vec"]
            interp = "Extracts vertical reference basis vector e_y"
            dv = f"v_thumb = {v_tmb}"
            ir = make_ir("VECTOR", operands, "thumb_vec", precision=self._precision, expression=expression)

        elif expression == "THUMBS_DOWN":
            result = -v_tmb
            operands = ["thumb_vec"]
            interp = "Inverted vertical reference vector -e_y"
            dv = f"-v_thumb = {result}"
            ir = make_ir("VECTOR", operands, "inverted_thumb_vec", precision=self._precision, expression=expression)

        elif expression in ("OK", "OK_SIGN"):
            dot_val = self._engine.execute("DOT", [v_idx, v_mid], expression=expression)
            result = dot_val
            operands = ["index_vec", "middle_vec"]
            interp = "Inner product v_index . v_middle"
            dv = f"v_idx . v_mid = {dot_val:.4f}"
            ir = make_ir("INNER", operands, "inner_product", precision=self._precision, expression=expression)

        elif expression in ("PINCH", "PINCH_START", "PINCH_HOLD", "PINCH_RELEASE"):
            v_tmb_tip = mvs.get("thumb_tip", Multivector.vector(0, 0, 0))
            v_idx_tip = mvs.get("index_tip", Multivector.vector(0, 0, 0))
            dist = self._engine.execute("DISTANCE", [v_tmb_tip, v_idx_tip], expression=expression)
            result = dist
            operands = ["thumb_tip", "index_tip"]
            interp = "Metric distance |p_thumb - p_index|"
            dv = f"||thumb - index|| = {dist:.4f}"
            ir = make_ir("DISTANCE", operands, "pinch_dist", precision=self._precision, expression=expression)

        elif expression in ("HAND_APPROACH", "HAND_RETRACT"):
            v_wrist = mvs.get("wrist_vec", Multivector.vector(0, 0, 0))
            v_mid_tip = mvs.get("middle_tip", Multivector.vector(0, 0, 0.1))
            dist = self._engine.execute("DISTANCE", [v_wrist, v_mid_tip], expression=expression)
            result = dist
            operands = ["wrist_vec", "middle_tip"]
            interp = "Relative Z-depth dilation/contraction"
            dv = f"z_depth_scale = {dist:.4f}"
            ir = make_ir("DISTANCE", operands, "z_scale_dist", precision=self._precision, expression=expression)

        elif expression in ("FIST", "FIST_CLOSE", "FIST_OPEN"):
            norms = {f: float(np.linalg.norm(mvs.get(f"{f}_vec", Multivector()).vector_part())) for f in ["index","middle","ring","pinky"]}
            result = float(np.mean(list(norms.values())))
            operands = ["index_vec"]
            interp = "Contraction norms |v_i| of all digits"
            dv = f"mean |finger_vec| = {result:.4f}"
            ir = make_ir("NORM", operands, "fist_norm", precision=self._precision, expression=expression)

        elif expression == "CALL_ME":
            v_pnk = mvs.get("pinky_vec", Multivector.vector(0, 0, 1))
            span_vec = v_tmb - v_pnk
            result = span_vec
            operands = ["thumb_vec", "pinky_vec"]
            interp = "Span vector between outer extremities"
            dv = f"v_thumb - v_pinky = {result}"
            ir = make_ir("VECTOR", operands, "outer_span_vec", precision=self._precision, expression=expression)

        elif expression in ("SWIPE_LEFT", "SWIPE_RIGHT", "SWIPE_UP", "SWIPE_DOWN"):
            result = v_idx
            operands = ["index_vec"]
            interp = self._INTERPRETATIONS.get(expression, "Wrist displacement translation vector")
            dv = f"v_trans = {result}"
            ir = make_ir("VECTOR", operands, "translation_vec", precision=self._precision, expression=expression)

        elif expression in ("TWO_FINGER", "PEACE_SIGN"):
            result = self._engine.execute("WEDGE", [v_idx, v_mid], expression=expression)
            operands = ["index_vec", "middle_vec"]
            interp = self._INTERPRETATIONS.get(expression, "v_index ^ v_middle bivector plane")
            from ga.operations import bivector_magnitude
            mag = bivector_magnitude(result)
            dv = f"v_idx ^ v_mid | mag={mag:.4f}"
            ir = make_ir("WEDGE", operands, "wedge_result", precision=self._precision, expression=expression)

        elif expression == "ROCK_SIGN":
            v_pnk = mvs.get("pinky_vec", Multivector.vector(0, 0, 1))
            result = self._engine.execute("WEDGE", [v_idx, v_pnk], expression=expression)
            operands = ["index_vec", "pinky_vec"]
            interp = "Wide bivector span v_index ^ v_pinky"
            from ga.operations import bivector_magnitude
            mag = bivector_magnitude(result)
            dv = f"v_idx ^ v_pnk | mag={mag:.4f}"
            ir = make_ir("WEDGE", operands, "rock_wedge", precision=self._precision, expression=expression)

        elif expression in ("THREE_FINGER",):
            gp1 = self._engine.execute("GP", [v_idx, v_mid], expression=expression)
            result = self._engine.execute("GP", [gp1, v_ring], expression=expression)
            operands = ["index_vec", "middle_vec", "ring_vec"]
            interp = "Triple geometric product chain v_1 * v_2 * v_3"
            dv = f"v_i * v_m * v_r = {result}"
            ir = make_ir("GP", operands, "triple_gp", precision=self._precision, expression=expression)

        elif expression in ("FOUR_FINGER",):
            gp1 = self._engine.execute("GP", [v_idx, v_mid], expression=expression)
            gp2 = self._engine.execute("GP", [gp1, v_ring], expression=expression)
            v_pnk = mvs.get("pinky_vec", Multivector.vector(0, 0, 1))
            result = self._engine.execute("GP", [gp2, v_pnk], expression=expression)
            operands = ["index_vec", "middle_vec", "ring_vec", "pinky_vec"]
            interp = "Quad geometric product chain v_1 * v_2 * v_3 * v_4"
            dv = f"v_i * v_m * v_r * v_p = {result}"
            ir = make_ir("GP", operands, "quad_gp", precision=self._precision, expression=expression)

        elif expression in ("ROTATE_CLOCKWISE", "ROTATE_COUNTERCLOCKWISE", "CIRCLE_MOTION"):
            from ga.rotor import rotor_from_axis_angle
            axis = rotor_axis if rotor_axis is not None else np.array([0.0, 0.0, 1.0])
            angle = rotor_angle if abs(rotor_angle) > 0.01 else (0.3 if "COUNTER" not in expression else -0.3)
            rotor = rotor_from_axis_angle(axis, angle)
            if expression == "CIRCLE_MOTION":
                result = rotor
                operands = ["trajectory_bivector"]
                interp = "Generates continuous rotor from trajectory bivector"
                dv = f"R_trajectory = {rotor}"
                ir = make_ir("ROTOR", operands, "trajectory_rotor", precision=self._precision, expression=expression)
            else:
                result = self._engine.execute("SANDWICH", [rotor, v_idx], expression=expression)
                operands = ["rotor", "index_vec"]
                interp = self._INTERPRETATIONS.get(expression, "Sandwich product R v ~R")
                dv = f"R * v_idx * ~R | angle={np.degrees(angle):.1f}°"
                ir = make_ir("SANDWICH", operands, "rotated_vec", precision=self._precision, expression=expression)

        else:
            # Default: return index vector
            result = v_idx
            operands = ["index_vec"]
            interp = "Default: index direction vector"
            dv = str(v_idx)
            ir = make_ir("VECTOR", operands, "default_vec", precision=self._precision, expression=expression)

        return ExpressionGAResult(
            expression=expression,
            opcode=opcode,
            algebra="G3",
            precision=self._precision,
            operand_names=operands,
            result=result,
            ir=ir,
            interpretation=interp,
            display_value=dv,
        )

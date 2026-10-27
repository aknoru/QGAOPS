"""
LIVE HAND GA ENGINE — mapping/expression_classes.py
Centralized definitions and geometric metadata for all:
  1. Static Hand Poses (13 Poses)
  2. Dynamic Motion Expressions (14 Expressions)

[IMPLEMENTED] Complete 27-gesture dictionary with triggered GA operations and formulas.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ExpressionMeta:
    """Metadata describing visual cue, GA opcode, and geometric meaning."""
    id: int
    name: str
    category: str              # "STATIC" or "DYNAMIC"
    visual_cue: str            # Physical trigger description
    ga_operation: str          # VECTOR, NORM, WEDGE, GP, DISTANCE, INNER, SANDWICH, ROTOR
    geometric_meaning: str     # Mathematical GA interpretation


# ---------------------------------------------------------------------------
# 1. Static Hand Poses (13 Poses)
# ---------------------------------------------------------------------------
STATIC_POSES: Dict[int, ExpressionMeta] = {
    0: ExpressionMeta(
        id=0,
        name="OPEN_PALM",
        category="STATIC",
        visual_cue="All 5 fingers extended",
        ga_operation="VECTOR",
        geometric_meaning="Computes all 5 finger direction vectors v_i in G_1",
    ),
    1: ExpressionMeta(
        id=1,
        name="FIST",
        category="STATIC",
        visual_cue="All 5 fingers curled tight",
        ga_operation="NORM",
        geometric_meaning="Computes contraction norms |v_i| of all digits",
    ),
    2: ExpressionMeta(
        id=2,
        name="THUMBS_UP",
        category="STATIC",
        visual_cue="Thumb extended up, others curled",
        ga_operation="VECTOR",
        geometric_meaning="Extracts vertical reference basis vector e_y",
    ),
    3: ExpressionMeta(
        id=3,
        name="THUMBS_DOWN",
        category="STATIC",
        visual_cue="Thumb extended down, others curled",
        ga_operation="VECTOR",
        geometric_meaning="Inverted vertical reference vector -e_y",
    ),
    4: ExpressionMeta(
        id=4,
        name="INDEX_POINT",
        category="STATIC",
        visual_cue="Only index extended",
        ga_operation="VECTOR",
        geometric_meaning="Pointing ray unit vector v_index",
    ),
    5: ExpressionMeta(
        id=5,
        name="TWO_FINGER",
        category="STATIC",
        visual_cue="Index + middle extended together (<25 deg)",
        ga_operation="WEDGE",
        geometric_meaning="Bivector area element v_index ^ v_middle in G_2",
    ),
    6: ExpressionMeta(
        id=6,
        name="PEACE_SIGN",
        category="STATIC",
        visual_cue="Index + middle spread apart (>30 deg)",
        ga_operation="WEDGE",
        geometric_meaning="Angular oriented plane spanned by index and middle",
    ),
    7: ExpressionMeta(
        id=7,
        name="THREE_FINGER",
        category="STATIC",
        visual_cue="Index + middle + ring extended",
        ga_operation="GP",
        geometric_meaning="Triple geometric product chain v_1 * v_2 * v_3",
    ),
    8: ExpressionMeta(
        id=8,
        name="FOUR_FINGER",
        category="STATIC",
        visual_cue="All fingers extended except thumb",
        ga_operation="GP",
        geometric_meaning="Quad geometric product chain v_1 * v_2 * v_3 * v_4",
    ),
    9: ExpressionMeta(
        id=9,
        name="PINCH",
        category="STATIC",
        visual_cue="Thumb tip & index tip touching (<5 cm)",
        ga_operation="DISTANCE",
        geometric_meaning="Metric distance |p_thumb - p_index|",
    ),
    10: ExpressionMeta(
        id=10,
        name="OK_SIGN",
        category="STATIC",
        visual_cue="Thumb-index circle, other 3 extended",
        ga_operation="INNER",
        geometric_meaning="Inner product v_index . v_middle",
    ),
    11: ExpressionMeta(
        id=11,
        name="ROCK_SIGN",
        category="STATIC",
        visual_cue="Index + pinky extended (horns)",
        ga_operation="WEDGE",
        geometric_meaning="Wide bivector span v_index ^ v_pinky",
    ),
    12: ExpressionMeta(
        id=12,
        name="CALL_ME",
        category="STATIC",
        visual_cue="Thumb + pinky extended",
        ga_operation="VECTOR",
        geometric_meaning="Span vector between outer extremities",
    ),
}

STATIC_13_NAMES: Dict[int, str] = {k: v.name for k, v in STATIC_POSES.items()}
STATIC_NAME_TO_ID: Dict[str, int] = {v: k for k, v in STATIC_13_NAMES.items()}


# ---------------------------------------------------------------------------
# 2. Dynamic Motion Expressions (14 Expressions)
# ---------------------------------------------------------------------------
DYNAMIC_EXPRESSIONS: Dict[int, ExpressionMeta] = {
    13: ExpressionMeta(
        id=13,
        name="SWIPE_LEFT",
        category="DYNAMIC",
        visual_cue="Fast negative X translation (v_x < -v_thresh)",
        ga_operation="VECTOR",
        geometric_meaning="Wrist displacement translation vector",
    ),
    14: ExpressionMeta(
        id=14,
        name="SWIPE_RIGHT",
        category="DYNAMIC",
        visual_cue="Fast positive X translation (v_x > v_thresh)",
        ga_operation="VECTOR",
        geometric_meaning="Wrist displacement translation vector",
    ),
    15: ExpressionMeta(
        id=15,
        name="SWIPE_UP",
        category="DYNAMIC",
        visual_cue="Fast negative Y translation (upward)",
        ga_operation="VECTOR",
        geometric_meaning="Vertical translation vector",
    ),
    16: ExpressionMeta(
        id=16,
        name="SWIPE_DOWN",
        category="DYNAMIC",
        visual_cue="Fast positive Y translation (downward)",
        ga_operation="VECTOR",
        geometric_meaning="Vertical translation vector",
    ),
    17: ExpressionMeta(
        id=17,
        name="PINCH_START",
        category="DYNAMIC",
        visual_cue="Rapid distance closure between fingertips",
        ga_operation="DISTANCE",
        geometric_meaning="Derivative of pinch distance vector",
    ),
    18: ExpressionMeta(
        id=18,
        name="PINCH_HOLD",
        category="DYNAMIC",
        visual_cue="Sustained pinch over multiple frames",
        ga_operation="DISTANCE",
        geometric_meaning="Maintained scalar grip metric",
    ),
    19: ExpressionMeta(
        id=19,
        name="PINCH_RELEASE",
        category="DYNAMIC",
        visual_cue="Distance expansion between fingertips",
        ga_operation="DISTANCE",
        geometric_meaning="Opening separation vector",
    ),
    20: ExpressionMeta(
        id=20,
        name="FIST_CLOSE",
        category="DYNAMIC",
        visual_cue="Rapid transition from open palm to curled fist",
        ga_operation="NORM",
        geometric_meaning="Rate of contraction norm reduction",
    ),
    21: ExpressionMeta(
        id=21,
        name="FIST_OPEN",
        category="DYNAMIC",
        visual_cue="Rapid transition from curled fist to open palm",
        ga_operation="NORM",
        geometric_meaning="Rate of expansion norm increase",
    ),
    22: ExpressionMeta(
        id=22,
        name="ROTATE_CLOCKWISE",
        category="DYNAMIC",
        visual_cue="Palm normal rotating clockwise",
        ga_operation="SANDWICH",
        geometric_meaning="Applies rotor: R v ~R where R = exp(-theta/2 B)",
    ),
    23: ExpressionMeta(
        id=23,
        name="ROTATE_COUNTERCLOCKWISE",
        category="DYNAMIC",
        visual_cue="Palm normal rotating CCW",
        ga_operation="SANDWICH",
        geometric_meaning="Applies inverse rotor: ~R v R",
    ),
    24: ExpressionMeta(
        id=24,
        name="HAND_APPROACH",
        category="DYNAMIC",
        visual_cue="Hand moving towards camera (scale expanding)",
        ga_operation="DISTANCE",
        geometric_meaning="Relative Z-depth dilation",
    ),
    25: ExpressionMeta(
        id=25,
        name="HAND_RETRACT",
        category="DYNAMIC",
        visual_cue="Hand moving away from camera (scale shrinking)",
        ga_operation="DISTANCE",
        geometric_meaning="Relative Z-depth contraction",
    ),
    26: ExpressionMeta(
        id=26,
        name="CIRCLE_MOTION",
        category="DYNAMIC",
        visual_cue="Hand tip tracing a circular trajectory in space",
        ga_operation="ROTOR",
        geometric_meaning="Generates continuous rotor from trajectory bivector",
    ),
}

DYNAMIC_14_NAMES: Dict[int, str] = {k: v.name for k, v in DYNAMIC_EXPRESSIONS.items()}
DYNAMIC_NAME_TO_ID: Dict[str, int] = {v: k for k, v in DYNAMIC_14_NAMES.items()}

# Combined dictionary of all 27 gestures
ALL_EXPRESSIONS: Dict[int, ExpressionMeta] = {**STATIC_POSES, **DYNAMIC_EXPRESSIONS}
ALL_EXPRESSION_NAMES: Dict[int, str] = {k: v.name for k, v in ALL_EXPRESSIONS.items()}
NAME_TO_EXPRESSION_META: Dict[str, ExpressionMeta] = {v.name: v for v in ALL_EXPRESSIONS.values()}

UNKNOWN_CLASS: str = "UNKNOWN"
NUM_STATIC_CLASSES: int = len(STATIC_POSES)
NUM_DYNAMIC_CLASSES: int = len(DYNAMIC_EXPRESSIONS)
NUM_TOTAL_CLASSES: int = len(ALL_EXPRESSIONS)


def get_expression_meta(name_or_id: str | int) -> Optional[ExpressionMeta]:
    """Retrieve ExpressionMeta by integer ID or string name."""
    if isinstance(name_or_id, int):
        return ALL_EXPRESSIONS.get(name_or_id)
    return NAME_TO_EXPRESSION_META.get(str(name_or_id).upper())

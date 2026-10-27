"""
LIVE HAND GA ENGINE — mapping/hand_to_ga.py
Map HandGeometry to Multivectors for GA computation.

[IMPLEMENTED] Converts normalized hand landmark geometry into G3 multivectors.
[ARCH]        This is the "LANDMARK → GA ENCODING" stage of the QGAOPS pipeline.

All vectors are in the hand-local coordinate frame (normalized coordinates).
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple
import numpy as np

from ga.multivector import Multivector
from hand_detection.landmarks import HandGeometry, FINGER_NAMES


def hand_to_multivectors(geom: HandGeometry) -> Dict[str, Multivector]:
    """Convert HandGeometry to a dictionary of named Multivectors.

    [IMPLEMENTED]

    Returns a dict with keys:
        "wrist"           -> scalar zero multivector (origin)
        "palm_center"     -> position vector
        "palm_normal"     -> unit normal vector
        "thumb_vec"       -> thumb finger vector (unit)
        "index_vec"       -> index finger vector (unit)
        "middle_vec"      -> middle finger vector (unit)
        "ring_vec"        -> ring finger vector (unit)
        "pinky_vec"       -> pinky finger vector (unit)
        "thumb_tip"       -> thumb tip position
        "index_tip"       -> index tip position
        "middle_tip"      -> middle tip position
        "ring_tip"        -> ring tip position
        "pinky_tip"       -> pinky tip position
        "wrist_to_index"  -> wrist → index tip (not unit)
        "wrist_to_middle" -> wrist → middle tip (not unit)
        "index_minus_middle" -> index_tip - middle_tip (separation)
        "thumb_minus_index"  -> thumb_tip - index_tip (pinch vector)
    """
    mv: Dict[str, Multivector] = {}

    w = geom.wrist  # use as local origin (but don't subtract for position vecs)

    # Wrist (origin)
    mv["wrist"] = Multivector.vector(float(w[0]), float(w[1]), float(w[2]))

    # Palm center
    pc = geom.palm_center
    mv["palm_center"] = Multivector.vector(float(pc[0]), float(pc[1]), float(pc[2]))

    # Palm normal
    pn = geom.palm_normal
    mv["palm_normal"] = Multivector.vector(float(pn[0]), float(pn[1]), float(pn[2]))

    # Finger unit vectors (direction from wrist to tip)
    for fname in FINGER_NAMES:
        fv = geom.finger_vectors.get(fname, np.zeros(3))
        mv[f"{fname}_vec"] = Multivector.vector(float(fv[0]), float(fv[1]), float(fv[2]))

    # Fingertip positions
    for fname in FINGER_NAMES:
        tp = geom.finger_tip_pos.get(fname, np.zeros(3))
        mv[f"{fname}_tip"] = Multivector.vector(float(tp[0]), float(tp[1]), float(tp[2]))

    # Wrist-to-tip displacement vectors (not normalized — preserve magnitude)
    for fname in FINGER_NAMES:
        tp = geom.finger_tip_pos.get(fname, np.zeros(3))
        disp = tp - geom.wrist
        mv[f"wrist_to_{fname}"] = Multivector.vector(
            float(disp[0]), float(disp[1]), float(disp[2])
        )

    # Special cross-finger vectors
    thumb_tip  = geom.finger_tip_pos.get("thumb",  np.zeros(3))
    index_tip  = geom.finger_tip_pos.get("index",  np.zeros(3))
    middle_tip = geom.finger_tip_pos.get("middle", np.zeros(3))

    pinch = thumb_tip - index_tip
    mv["thumb_minus_index"] = Multivector.vector(
        float(pinch[0]), float(pinch[1]), float(pinch[2])
    )

    sep = index_tip - middle_tip
    mv["index_minus_middle"] = Multivector.vector(
        float(sep[0]), float(sep[1]), float(sep[2])
    )

    return mv


def two_hand_multivectors(
    geom_l: HandGeometry,
    geom_r: HandGeometry,
) -> Tuple[Dict[str, Multivector], Dict[str, Multivector], Dict[str, float]]:
    """Extract multivectors from both hands and compute cross-hand metrics.

    [IMPLEMENTED]

    Returns:
        (left_mvs, right_mvs, cross_metrics)
        cross_metrics keys: 'palm_distance', 'index_distance', 'dot_index', 'wedge_index_mag'
    """
    from ga.geometric_product import dot, outer_product
    from ga.operations import bivector_magnitude

    left_mvs  = hand_to_multivectors(geom_l)
    right_mvs = hand_to_multivectors(geom_r)

    # Palm-to-palm distance
    pl = geom_l.palm_center
    pr = geom_r.palm_center
    palm_dist = float(np.linalg.norm(pl - pr))

    # Index fingertip distance
    il = geom_l.finger_tip_pos.get("index", np.zeros(3))
    ir = geom_r.finger_tip_pos.get("index", np.zeros(3))
    idx_dist = float(np.linalg.norm(il - ir))

    # GA cross operations on index vectors
    v_l = left_mvs.get("index_vec", Multivector.vector(1,0,0))
    v_r = right_mvs.get("index_vec", Multivector.vector(1,0,0))
    dot_val = dot(v_l, v_r)
    wedge_mv = outer_product(v_l, v_r)
    wedge_mag = bivector_magnitude(wedge_mv)

    cross_metrics = {
        "palm_distance":   palm_dist,
        "index_distance":  idx_dist,
        "dot_index":       dot_val,
        "wedge_index_mag": wedge_mag,
    }

    return left_mvs, right_mvs, cross_metrics

"""
LIVE HAND GA ENGINE — visualization/dashboard.py
Composite dashboard: webcam | 3D vectors | algebra info panel.

[IMPLEMENTED] Assembles all panels into a single OpenCV window.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
import numpy as np

try:
    import cv2
    _CV2_OK = True
except ImportError:
    _CV2_OK = False

from hand_detection.landmarks import HandGeometry
from ga.multivector import Multivector
from ga.ir import OperationIR


# Shared font + colors
_FONT      = None
_C_ACCENT  = (0, 220, 140)
_C_TEXT    = (210, 210, 215)
_C_DIM     = (120, 120, 130)
_C_WARN    = (30, 100, 255)
_C_IR      = (255, 195, 0)
_C_BG      = (15, 15, 22)


def _get_font():
    global _FONT
    if _FONT is None and _CV2_OK:
        _FONT = cv2.FONT_HERSHEY_SIMPLEX
    return _FONT


def _text(img, text, pos, color=_C_TEXT, scale=0.5, thick=1):
    if _CV2_OK:
        cv2.putText(img, text, pos, _get_font(), scale, color, thick, cv2.LINE_AA)


def make_info_panel(
    width:  int,
    height: int,
    *,
    geom:         Optional[HandGeometry],
    mvs:          Optional[Dict[str, Multivector]],
    pose:         str = "UNKNOWN",
    expression:   str = "",
    confidence:   float = 0.0,
    ga_result:    Any = None,
    last_ir:      Optional[OperationIR] = None,
    ir_trace:     List[Tuple[OperationIR, Any, float]] = None,
    ops_per_s:    float = 0.0,
    fix16_error:  Tuple[float, float, float] = (0.0, 0.0, 0.0),
    use_fix16:    bool = False,
    backend:      str = "python",
    frame_ms:     float = 0.0,
    memory_bytes: int = 0,
    mode_name:    str = "HAND GEOMETRY",
) -> np.ndarray:
    """Build the right-side algebra information panel.

    [IMPLEMENTED]

    Returns:
        (height, width, 3) uint8 BGR image.
    """
    panel = np.full((height, width, 3), _C_BG, dtype=np.uint8)

    if not _CV2_OK:
        return panel

    # Title bar
    cv2.rectangle(panel, (0, 0), (width, 28), (25, 25, 38), -1)
    _text(panel, "QGAOPS-QGPU  GA ENGINE", (6, 20), _C_ACCENT, 0.55, 1)

    y = 46
    step = 18
    small = 0.42
    normal = 0.50

    def row(label, value, color=_C_TEXT, label_color=_C_DIM):
        nonlocal y
        _text(panel, label, (6, y), label_color, small, 1)
        _text(panel, str(value), (130, y), color, small, 1)
        y += step

    def section(title):
        nonlocal y
        cv2.line(panel, (4, y - 4), (width - 4, y - 4), (40, 40, 55), 1)
        _text(panel, title, (6, y + 8), (180, 180, 200), 0.44, 1)
        y += 18

    # --- Gesture & Expression ---
    section("RECOGNITION")
    row("POSE:", pose, _C_ACCENT)
    conf_color = _C_ACCENT if confidence >= 0.7 else _C_WARN
    row("CONFIDENCE:", f"{confidence*100:.0f}%", conf_color)
    if expression and expression not in ("UNKNOWN", "UNKNOWN_DYNAMIC"):
        row("EXPRESSION:", expression, (200, 140, 255))

    # --- Finger data ---
    if geom is not None:
        section("FINGER LENGTHS")
        for fname in ["thumb", "index", "middle", "ring", "pinky"]:
            fl = geom.finger_lengths.get(fname, 0.0)
            row(f"  {fname}:", f"{fl:.4f}", _C_TEXT, _C_DIM)

    # --- GA result ---
    if ga_result is not None:
        section("GA OPERATION")
        opcode = last_ir.opcode if last_ir else "?"
        algebra = last_ir.algebra if last_ir else "G3"
        prec = last_ir.precision if last_ir else "FLOAT32"
        row("OPCODE:", opcode, _C_IR)
        row("ALGEBRA:", algebra)
        row("PRECISION:", prec, (255, 195, 0) if use_fix16 else _C_TEXT)

        # Display result depending on type
        if isinstance(ga_result, Multivector):
            s = ga_result.scalar_part()
            vp = ga_result.vector_part()
            bp = ga_result.bivector_part()
            row("SCALAR:", f"{s:.5f}")
            row("VECTOR:", f"({vp[0]:.3f},{vp[1]:.3f},{vp[2]:.3f})")
            row("BIVEC:", f"({bp[0]:.3f},{bp[1]:.3f},{bp[2]:.3f})")
            row("|MV|:", f"{ga_result.norm():.5f}")
        elif isinstance(ga_result, float):
            row("RESULT:", f"{ga_result:.6f}")

    # --- FIX16 error ---
    if use_fix16 and any(e > 0 for e in fix16_error):
        section("FIX16 ERROR")
        row("max |err|:", f"{fix16_error[0]:.2e}", (255, 200, 50))
        row("mean |err|:", f"{fix16_error[1]:.2e}")
        row("RMS err:", f"{fix16_error[2]:.2e}")

    # --- QGAOPS IR trace ---
    if last_ir is not None:
        section("QGAOPS IR")
        row("OP_ID:", f"{last_ir.operation_id:04d}", _C_IR)
        row("OPCODE:", last_ir.opcode, _C_IR)
        row("ALGEBRA:", last_ir.algebra)
        row("PRECISION:", last_ir.precision)
        row("BACKEND:", backend.upper())
        row("STATUS:", "EXECUTED", _C_ACCENT)
        inputs_str = ", ".join(last_ir.inputs[:3])
        row("INPUTS:", inputs_str)

    # --- Performance ---
    section("PERFORMANCE")
    row("ops/s:", f"{ops_per_s:.0f}", _C_ACCENT)
    row("frame:", f"{frame_ms:.1f} ms")
    if memory_bytes > 0:
        row("mem est:", f"{memory_bytes} B [SW MODEL]", _C_DIM)

    # --- Keyboard help (bottom) ---
    help_y = height - 80
    cv2.line(panel, (4, help_y), (width - 4, help_y), (40, 40, 55), 1)
    helps = [
        "Q:Quit  M:Mode  F:FIX16  B:Bench",
        "G:GP  D:Dot  W:Wedge  R:Rotor",
        "V:3D View  H:Help  S:Sandwich",
    ]
    for i, h in enumerate(helps):
        _text(panel, h, (6, help_y + 16 + i * 15), _C_DIM, 0.38, 1)

    return panel


def assemble_dashboard(
    webcam_panel: np.ndarray,
    vector_panel: Optional[np.ndarray],
    info_panel:   np.ndarray,
    target_height: int = 720,
) -> np.ndarray:
    """Horizontally concatenate all panels into one dashboard frame.

    [IMPLEMENTED]

    Args:
        webcam_panel:  Annotated webcam frame.
        vector_panel:  3D vector plot (or None → grey placeholder).
        info_panel:    Algebra info panel.
        target_height: Height to resize all panels to.

    Returns:
        Combined dashboard image.
    """
    if not _CV2_OK:
        return webcam_panel

    def resize_h(img, h):
        if img is None:
            return np.full((h, 480, 3), (30, 30, 40), dtype=np.uint8)
        ratio = h / img.shape[0]
        return cv2.resize(img, (int(img.shape[1] * ratio), h))

    cam_r = resize_h(webcam_panel, target_height)
    vec_r = resize_h(vector_panel, target_height)
    inf_r = resize_h(info_panel, target_height)

    # Ensure same height
    panels = [cam_r, vec_r, inf_r]
    max_h = max(p.shape[0] for p in panels)
    final = []
    for p in panels:
        if p.shape[0] < max_h:
            pad = np.full((max_h - p.shape[0], p.shape[1], 3), _C_BG, dtype=np.uint8)
            p = np.vstack([p, pad])
        final.append(p)

    return np.hstack(final)

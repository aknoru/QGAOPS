"""
LIVE HAND GA ENGINE — visualization/webcam_view.py
Annotated webcam frame rendering.

[IMPLEMENTED] OpenCV-based overlay with landmarks, handedness, FPS, gesture.
"""
from __future__ import annotations

from typing import List, Optional
import numpy as np

try:
    import cv2
    _CV2_OK = True
except ImportError:
    _CV2_OK = False


def draw_webcam_overlay(
    frame: np.ndarray,
    gesture:    str = "UNKNOWN",
    expression: str = "",
    confidence: float = 0.0,
    handedness: str  = "Unknown",
    fps:        float = 0.0,
    tracking_conf: float = 0.0,
    mode_name:  str = "HAND GEOMETRY",
    use_fix16:  bool = False,
    backend:    str = "python",
) -> np.ndarray:
    """Draw information overlay on the webcam frame.

    [IMPLEMENTED]

    Args:
        frame:       BGR frame (H, W, 3).
        gesture:     Recognized static pose name.
        expression:  Dynamic expression name.
        confidence:  Recognition confidence.
        handedness:  'Left' or 'Right'.
        fps:         Current FPS.
        tracking_conf: MediaPipe tracking confidence.
        mode_name:   Active operation mode name.
        use_fix16:   Whether FIX16 mode is active.
        backend:     Backend name.

    Returns:
        Annotated BGR frame (copy).
    """
    if not _CV2_OK:
        return frame

    out = frame.copy()
    h, w = out.shape[:2]

    # ---- Color scheme ----
    C_ACCENT   = (0, 220, 140)    # green-teal accent
    C_TEXT     = (220, 220, 220)
    C_WARN     = (30, 100, 255)
    C_HEADER   = (20, 20, 28)
    C_FIX16    = (255, 180, 0)
    FONT       = cv2.FONT_HERSHEY_SIMPLEX

    # Semi-transparent header bar
    overlay = out.copy()
    cv2.rectangle(overlay, (0, 0), (w, 38), C_HEADER, -1)
    cv2.addWeighted(overlay, 0.75, out, 0.25, 0, out)

    # FPS
    cv2.putText(out, f"FPS: {fps:.1f}", (8, 26), FONT, 0.6, C_ACCENT, 2)

    # Mode
    cv2.putText(out, f"MODE: {mode_name}", (100, 26), FONT, 0.6, C_TEXT, 1)

    # Backend / Precision
    prec = "FIX16" if use_fix16 else "FLOAT32"
    cv2.putText(out, f"{backend.upper()} | {prec}", (w - 200, 26), FONT, 0.5, C_TEXT, 1)

    # Handedness + tracking confidence
    if handedness != "Unknown":
        cv2.putText(
            out, f"{handedness} ({tracking_conf:.2f})",
            (8, h - 80), FONT, 0.55, C_ACCENT, 2
        )

    # Gesture box
    cv2.rectangle(out, (6, h - 70), (340, h - 10), (20, 20, 30), -1)
    cv2.rectangle(out, (6, h - 70), (340, h - 10), C_ACCENT, 1)
    cv2.putText(out, f"POSE: {gesture}", (12, h - 50), FONT, 0.6, C_TEXT, 1)
    conf_color = C_ACCENT if confidence >= 0.7 else C_WARN
    cv2.putText(
        out, f"CONF: {confidence*100:.0f}%",
        (12, h - 28), FONT, 0.5, conf_color, 1
    )

    # Dynamic expression
    if expression and expression not in ("UNKNOWN_DYNAMIC", "UNKNOWN"):
        cv2.putText(out, f"EXPR: {expression}", (12, h - 8), FONT, 0.5, (180, 120, 255), 1)

    # FIX16 indicator
    if use_fix16:
        cv2.putText(out, "[FIX16]", (w - 100, h - 10), FONT, 0.5, C_FIX16, 2)

    return out


def draw_no_hand_message(frame: np.ndarray) -> np.ndarray:
    """Overlay a 'No hand detected' message."""
    if not _CV2_OK:
        return frame
    out = frame.copy()
    h, w = out.shape[:2]
    cv2.putText(
        out, "No hand detected — show your hand to the camera",
        (10, h // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (100, 100, 255), 2
    )
    return out

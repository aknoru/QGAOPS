"""
LIVE HAND GA ENGINE — visualization/control_overlay.py
Real-time transparent HUD overlay displaying computer vision control telemetry.

[IMPLEMENTED]
- Hand detection indicator
- Pose & Dynamic Expression status
- Active Computer Control Command
- Geometric Algebra operation & QGAOPS Opcode
- Emergency stop status / Control Active tag
"""
from __future__ import annotations

from typing import Optional
import cv2
import numpy as np

from control.controller import ControlExecutionReport


def render_control_hud(
    frame: np.ndarray,
    report: Optional[ControlExecutionReport],
    pose: str = "UNKNOWN",
    expression: str = "UNKNOWN",
    confidence: float = 0.0,
    hand_detected: bool = False,
    is_control_enabled: bool = False,
    active_profile: str = "mouse",
) -> np.ndarray:
    """Render high-contrast computer vision control overlay on camera frame."""
    h, w = frame.shape[:2]

    # Semi-transparent HUD header background
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (320, 210), (12, 14, 20), -1)
    cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)
    cv2.rectangle(frame, (10, 10), (320, 210), (0, 170, 255) if is_control_enabled else (80, 85, 100), 1)

    # Status indicator
    ctrl_status = "CONTROL: ACTIVE" if is_control_enabled else "CONTROL: OFF (Press F12)"
    ctrl_color = (0, 255, 130) if is_control_enabled else (120, 120, 140)

    cmd_text = report.command if (report and report.command) else "NONE"
    ga_op = report.ga_opcode if report else "VECTOR"

    lines = [
        ("HAND STATUS:", "DETECTED" if hand_detected else "SEARCHING...", (0, 255, 130) if hand_detected else (0, 120, 255)),
        ("POSE:", pose, (0, 229, 255)),
        ("EXPRESSION:", expression, (0, 229, 255)),
        ("CONFIDENCE:", f"{confidence * 100:.1f}%", (255, 255, 255)),
        ("COMMAND:", cmd_text, (0, 255, 255) if cmd_text != "NONE" else (160, 160, 160)),
        ("GA OPERATION:", ga_op, (255, 180, 0)),
        ("QGAOPS OPCODE:", f"OP_{ga_op}", (255, 180, 0)),
        ("PROFILE:", active_profile.upper(), (200, 200, 255)),
        ("SYSTEM:", ctrl_status, ctrl_color),
    ]

    for idx, (label, val, col) in enumerate(lines):
        y = 30 + idx * 19
        cv2.putText(frame, f"{label:<14} {val}", (18, y), cv2.FONT_HERSHEY_SIMPLEX, 0.42, col, 1, cv2.LINE_AA)

    # Emergency cut-off reminder tag in bottom right
    if is_control_enabled:
        cv2.putText(frame, "[F12] EMERGENCY STOP", (w - 210, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 60, 255), 2, cv2.LINE_AA)

    return frame

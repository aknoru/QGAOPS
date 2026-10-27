"""
LIVE HAND GA ENGINE — control/object3d.py
GA-Driven Virtual 3D Object Manipulation using Rotors & Sandwich Products.

[IMPLEMENTED]
- Virtual 3D Polyhedron / Cube represented as geometric algebra grade-1 multivectors.
- Rotation computed via GA rotor: R = exp(-theta/2 B) and sandwich product v' = R v ~R.
- Live inspection of: Original vector, Rotor, Reverse rotor, Transformed vector.
- Projection & wireframe rendering onto OpenCV image buffer.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np

from ga.multivector import Multivector
from ga.rotor import rotor_from_axis_angle, sandwich_product


@dataclass
class TransformationTrace:
    """Mathematical trace of the GA sandwich product transformation."""
    original_vector: Multivector
    rotor: Multivector
    reverse_rotor: Multivector
    transformed_vector: Multivector
    angle_deg: float
    axis: np.ndarray


class Virtual3DObject:
    """Virtual 3D object manipulated via Clifford Geometric Algebra operations.

    [IMPLEMENTED]
    """

    # Canonical 3D wireframe cube vertices
    BASE_CUBE_VERTICES = np.array([
        [-0.5, -0.5, -0.5],
        [ 0.5, -0.5, -0.5],
        [ 0.5,  0.5, -0.5],
        [-0.5,  0.5, -0.5],
        [-0.5, -0.5,  0.5],
        [ 0.5, -0.5,  0.5],
        [ 0.5,  0.5,  0.5],
        [-0.5,  0.5,  0.5],
    ], dtype=np.float64)

    CUBE_EDGES = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # back face
        (4, 5), (5, 6), (6, 7), (7, 4),  # front face
        (0, 4), (1, 5), (2, 6), (3, 7),  # connecting edges
    ]

    def __init__(self) -> None:
        self.vertices: List[Multivector] = []
        self.position = np.array([0.0, 0.0, 0.0], dtype=np.float64)
        self.scale_factor: float = 1.0
        self.last_trace: Optional[TransformationTrace] = None
        self.accumulated_rotor: Multivector = Multivector.scalar(1.0)
        self.reset()

    def reset(self) -> None:
        """Reset object to canonical geometry and orientation."""
        self.vertices = [
            Multivector.vector(float(v[0]), float(v[1]), float(v[2]))
            for v in self.BASE_CUBE_VERTICES
        ]
        self.position = np.array([0.0, 0.0, 0.0], dtype=np.float64)
        self.scale_factor = 1.0
        self.accumulated_rotor = Multivector.scalar(1.0)
        self.last_trace = None

    def rotate_via_rotor(self, axis: np.ndarray, angle_rad: float) -> TransformationTrace:
        """Rotate virtual object using GA rotor sandwich product: v' = R v ~R.

        [IMPLEMENTED]
        """
        unit_axis = axis / (np.linalg.norm(axis) + 1e-9)
        rotor = rotor_from_axis_angle(unit_axis, angle_rad)
        rev_rotor = rotor.reverse()

        # Update accumulated rotor: R_total = R_step * R_prev
        self.accumulated_rotor = rotor * self.accumulated_rotor

        sample_orig = self.vertices[1]
        sample_trans = sandwich_product(rotor, sample_orig)

        # Apply sandwich product to every vertex multivector: v' = R v ~R
        transformed_vertices = []
        for v in self.vertices:
            v_rot = sandwich_product(rotor, v)
            transformed_vertices.append(v_rot)

        self.vertices = transformed_vertices

        trace = TransformationTrace(
            original_vector=sample_orig,
            rotor=rotor,
            reverse_rotor=rev_rotor,
            transformed_vector=sample_trans,
            angle_deg=float(np.degrees(angle_rad)),
            axis=unit_axis,
        )
        self.last_trace = trace
        return trace

    @property
    def scale(self) -> float:
        return self.scale_factor

    @property
    def translation(self) -> np.ndarray:
        return self.position

    @property
    def transformation_trace(self) -> Dict[str, Any]:
        if self.last_trace is None:
            return {}
        return {
            "rotor": str(self.last_trace.rotor),
            "reverse_rotor": str(self.last_trace.reverse_rotor),
            "rotor_norm": float(self.last_trace.rotor.norm()),
            "original_vector": str(self.last_trace.original_vector),
            "transformed_vector": str(self.last_trace.transformed_vector),
            "angle_deg": self.last_trace.angle_deg,
            "axis": self.last_trace.axis.tolist(),
        }

    def translate(self, dx: float, dy: float, dz: float) -> None:
        """Translate object position in 3D coordinate space."""
        self.position += np.array([dx, dy, dz], dtype=np.float64)

    def zoom(self, factor: float) -> None:
        """Dilate or contract object scale."""
        self.scale_factor = float(np.clip(self.scale_factor * factor, 0.25, 4.0))

    def render(
        self,
        frame_or_width: Union[np.ndarray, int],
        height: Optional[int] = None,
        origin_xy: Optional[Tuple[int, int]] = None,
        pixel_scale: float = 140.0,
    ) -> np.ndarray:
        """Project and draw 3D wireframe cube onto an OpenCV image buffer."""
        if isinstance(frame_or_width, int):
            h = height or frame_or_width
            w = frame_or_width
            frame = np.zeros((h, w, 3), dtype=np.uint8)
            orig = origin_xy or (w // 2, h // 2)
        else:
            frame = frame_or_width
            h, w = frame.shape[:2]
            orig = origin_xy or (w // 2, h // 2)

        # Project 3D vertices to 2D screen coords with weak perspective
        pts_2d = []
        for v in self.vertices:
            vp = v.vector_part() * self.scale_factor + self.position
            # Perspective divide
            z_depth = max(vp[2] + 2.5, 0.5)
            px = int(orig[0] + (vp[0] / z_depth) * pixel_scale)
            py = int(orig[1] + (vp[1] / z_depth) * pixel_scale)
            pts_2d.append((px, py))

        # Draw wireframe edges
        for (i1, i2) in self.CUBE_EDGES:
            pt1 = pts_2d[i1]
            pt2 = pts_2d[i2]
            cv2.line(frame, pt1, pt2, (0, 229, 255), 2, cv2.LINE_AA)

        # Draw vertices
        for pt in pts_2d:
            cv2.circle(frame, pt, 4, (0, 130, 255), -1, cv2.LINE_AA)

        # Render GA Rotor Inspection Box
        if self.last_trace:
            tr = self.last_trace
            lines = [
                "=== GA ROTOR OBJECT TRANSFORMATION ===",
                f"Formula:  v' = R * v * ~R",
                f"Angle:    {tr.angle_deg:+.1f} deg around axis [{tr.axis[0]:.2f}, {tr.axis[1]:.2f}, {tr.axis[2]:.2f}]",
                f"v_orig:   {tr.original_vector}",
                f"Rotor R:  {tr.rotor}",
                f"Reverse:  {tr.reverse_rotor}",
                f"v_trans:  {tr.transformed_vector}",
                f"Scale:    {self.scale_factor:.2f}x | Pos: [{self.position[0]:.2f}, {self.position[1]:.2f}]",
            ]
            box_y = orig[1] + 100
            for j, line in enumerate(lines):
                cv2.putText(
                    frame, line, (orig[0] - 180, box_y + j * 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 200) if j == 0 else (220, 220, 220), 1, cv2.LINE_AA
                )

        return frame

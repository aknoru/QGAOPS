"""
LIVE HAND GA ENGINE — visualization/vector_view.py
Real-time 3D vector visualization using Matplotlib.

[IMPLEMENTED] Lightweight 3D plot: hand skeleton, vectors, bivector plane.
[IMPLEMENTED] Update every N frames to avoid FPS collapse.
"""
from __future__ import annotations

from typing import Dict, List, Optional
import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")  # non-interactive backend — render to buffer
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    _MPL_OK = True
except ImportError:
    _MPL_OK = False

from hand_detection.landmarks import HandGeometry, FINGER_NAMES
from ga.multivector import Multivector


# Skeleton connections (MediaPipe hand graph)
_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),       # thumb
    (0,5),(5,6),(6,7),(7,8),       # index
    (0,9),(9,10),(10,11),(11,12),  # middle
    (0,13),(13,14),(14,15),(15,16),# ring
    (0,17),(17,18),(18,19),(19,20),# pinky
    (5,9),(9,13),(13,17),           # palm
]


class VectorView3D:
    """3D vector visualization panel.

    [IMPLEMENTED]

    Renders to a RGBA buffer that can be converted to an OpenCV BGR image
    for embedding in the dashboard window.
    """

    def __init__(self, width: int = 480, height: int = 480) -> None:
        self.width  = width
        self.height = height
        self._fig   = None
        self._ax    = None
        self._init_figure()

    def _init_figure(self) -> None:
        if not _MPL_OK:
            return
        dpi = 80
        figw = self.width  / dpi
        figh = self.height / dpi
        self._fig = plt.figure(figsize=(figw, figh), dpi=dpi, facecolor="#12121A")
        self._ax  = self._fig.add_subplot(111, projection="3d")
        self._style_ax()

    def _style_ax(self) -> None:
        if self._ax is None:
            return
        ax = self._ax
        ax.set_facecolor("#12121A")
        ax.tick_params(colors="#555566", labelsize=6)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.grid(True, color="#2A2A35", linewidth=0.5)

    def render(
        self,
        geom:     Optional[HandGeometry],
        mvs:      Optional[Dict[str, Multivector]],
        highlight_vecs: Optional[List[str]] = None,
        wedge_pair: Optional[tuple] = None,
        show_axes: bool = True,
    ) -> Optional[np.ndarray]:
        """Render the 3D view and return an BGR image array.

        [IMPLEMENTED]

        Args:
            geom:           Current HandGeometry (or None if no hand).
            mvs:            Dict of Multivectors.
            highlight_vecs: Names of vectors to highlight.
            wedge_pair:     Pair of vector names for wedge plane visualization.
            show_axes:      Whether to draw coordinate axes.

        Returns:
            (H, W, 3) uint8 BGR image, or None if matplotlib unavailable.
        """
        if not _MPL_OK or self._fig is None or self._ax is None:
            return None

        ax = self._ax
        ax.cla()
        self._style_ax()

        # Set consistent axis limits
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.0, 1.0)
        ax.set_zlim(-0.2, 0.2)
        ax.set_xlabel("X", color="#888899", fontsize=7)
        ax.set_ylabel("Y", color="#888899", fontsize=7)
        ax.set_zlabel("Z", color="#888899", fontsize=7)
        ax.set_title("3D Hand — GA Vectors", color="#CCCCDD", fontsize=8, pad=2)

        if geom is not None:
            lm = geom.landmarks_smooth   # (21, 3)

            # Draw skeleton
            for (a, b) in _CONNECTIONS:
                ax.plot(
                    [lm[a, 0], lm[b, 0]],
                    [lm[a, 1], lm[b, 1]],
                    [lm[a, 2], lm[b, 2]],
                    color="#00DC78", linewidth=1.2, alpha=0.7,
                )

            # Draw landmark points
            ax.scatter(
                lm[:, 0], lm[:, 1], lm[:, 2],
                c="#00FFAA", s=12, zorder=5,
            )

            # Wrist origin marker
            w = geom.wrist
            ax.scatter([w[0]], [w[1]], [w[2]], c="#FF4080", s=30, zorder=6)

        if show_axes:
            # Reference coordinate axes at origin (0.5, 0.5, 0)
            origin = np.array([0.05, 0.95, 0.0])
            L = 0.07
            ax.quiver(*origin, L, 0, 0, color="#FF4444", linewidth=1.5, arrow_length_ratio=0.3)
            ax.quiver(*origin, 0, -L, 0, color="#44FF44", linewidth=1.5, arrow_length_ratio=0.3)
            ax.quiver(*origin, 0, 0, L, color="#4444FF", linewidth=1.5, arrow_length_ratio=0.3)
            ax.text(origin[0]+L+0.01, origin[1], origin[2], "X", color="#FF4444", fontsize=6)
            ax.text(origin[0], origin[1]-L-0.01, origin[2], "Y", color="#44FF44", fontsize=6)

        # Highlighted vectors
        highlight_vecs = highlight_vecs or []
        if geom is not None and mvs is not None:
            w = geom.wrist
            for vname in highlight_vecs:
                mv = mvs.get(vname)
                if mv is None:
                    continue
                v = mv.vector_part()
                scale = 0.12
                ax.quiver(
                    w[0], w[1], w[2],
                    v[0]*scale, v[1]*scale, v[2]*scale,
                    color="#00C8FF", linewidth=2.0, arrow_length_ratio=0.25, zorder=10,
                )
                ax.text(
                    w[0]+v[0]*scale*1.1, w[1]+v[1]*scale*1.1, w[2]+v[2]*scale*1.1,
                    vname.replace("_vec", ""), color="#00C8FF", fontsize=7,
                )

        # Wedge plane
        if geom is not None and mvs is not None and wedge_pair is not None:
            name_a, name_b = wedge_pair
            va = mvs.get(name_a)
            vb = mvs.get(name_b)
            if va is not None and vb is not None:
                self._draw_wedge_plane(ax, geom.wrist, va.vector_part(), vb.vector_part())

        # Render to numpy array
        self._fig.canvas.draw()
        w, h = self._fig.canvas.get_width_height()
        if hasattr(self._fig.canvas, "buffer_rgba"):
            rgba = np.frombuffer(self._fig.canvas.buffer_rgba(), dtype=np.uint8).reshape((h, w, 4))
            rgb = rgba[:, :, :3]
        elif hasattr(self._fig.canvas, "tostring_rgb"):
            rgb = np.frombuffer(self._fig.canvas.tostring_rgb(), dtype=np.uint8).reshape((h, w, 3))
        elif hasattr(self._fig.canvas, "tostring_argb"):
            argb = np.frombuffer(self._fig.canvas.tostring_argb(), dtype=np.uint8).reshape((h, w, 4))
            rgb = argb[:, :, 1:4]
        else:
            rgb = np.asarray(self._fig.canvas.renderer.buffer_rgba())[:, :, :3]

        try:
            import cv2
            return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        except ImportError:
            return rgb

    def _draw_wedge_plane(
        self,
        ax,
        origin: np.ndarray,
        va: np.ndarray,
        vb: np.ndarray,
    ) -> None:
        """Draw the parallelogram (wedge plane) spanned by va, vb."""
        scale = 0.10
        p0 = origin
        p1 = origin + va * scale
        p2 = origin + va * scale + vb * scale
        p3 = origin + vb * scale
        vertices = [[p0, p1, p2, p3]]
        poly = Poly3DCollection(
            vertices,
            alpha=0.25, facecolor="#BB44FF", edgecolor="#BB44FF", linewidth=1,
        )
        ax.add_collection3d(poly)

    def close(self) -> None:
        if _MPL_OK and self._fig is not None:
            plt.close(self._fig)

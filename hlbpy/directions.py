import numpy as np


CENTER: np.ndarray = np.array((0.0, 0.0, 0.0))
"""The center of the coordinate system."""

UP: np.ndarray = np.array((0.0, 1.0, 0.0))
"""One unit step in the positive Y direction."""

DOWN: np.ndarray = np.array((0.0, -1.0, 0.0))
"""One unit step in the negative Y direction."""

RIGHT: np.ndarray = np.array((1.0, 0.0, 0.0))
"""One unit step in the positive X direction."""

LEFT: np.ndarray = np.array((-1.0, 0.0, 0.0))
"""One unit step in the negative X direction."""

IN: np.ndarray = np.array((0.0, 0.0, 1.0))
"""One unit step in the negative Z direction."""

OUT: np.ndarray = np.array((0.0, 0.0, -1.0))
"""One unit step in the positive Z direction."""

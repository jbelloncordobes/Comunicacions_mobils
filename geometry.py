"""
geometry.py
-----------
Hexagonal cell geometry and user-position generation for the simulation.
"""

import numpy as np
from config import CELL_RADIUS, SECTOR_ANGLE, SECTOR_ORIENTATION


# -----------------------------------------------------
# 1. GET COORDINATES OF THE 19 CELL CENTERS
# -----------------------------------------------------
def generate_hex_grid():
    """
    Generates the 19 hexagonal cell centers (central + 2 rings).
    Returns:
        centers : ndarray of shape (19, 2)
    """
    centers = [(0, 0)]  # Central cell at origin

    # Hex grid directions (distance between adjacent BS sites = sqrt(3) * R)
    d = np.sqrt(3) * CELL_RADIUS

    directions = [
        (1, 0),
        (0.5, np.sqrt(3)/2),
        (-0.5, np.sqrt(3)/2),
        (-1, 0),
        (-0.5, -np.sqrt(3)/2),
        (0.5, -np.sqrt(3)/2)
    ]

    # First ring (6 points)
    for dx, dy in directions:
        centers.append((d * dx, d * dy))

    # Second ring (12 points)
    for i in range(6):
        dx1, dy1 = directions[i]
        dx2, dy2 = directions[(i + 1) % 6]

        # Two points between each pair
        centers.append((d * (dx1 + dx2), d * (dy1 + dy2)))
        centers.append((2 * d * dx1, 2 * d * dy1))

    return np.array(centers)


def random_user_position():
    """
    Generates a random (x, y) uniformly inside the central sector shaped
    as a rhombus (two triangles covering 0°–120°).

    Returns:
        (x, y) : tuple of floats
    """
    h = CELL_RADIUS * np.sqrt(3)/2  # altura de un hexágono

    # Triángulo base para 0°–60°
    u = np.random.uniform(0, 1)
    v = np.random.uniform(0, 1)
    if u + v > 1:
        u = 1 - u
        v = 1 - v

    # Coordenadas dentro del triángulo 0°–60°
    x = u * CELL_RADIUS + v * (CELL_RADIUS/2)
    y = v * h

    # Elegir aleatoriamente uno de los dos triángulos
    if np.random.rand() < 0.5:
        # Rotar 60° para el triángulo 60°–120°
        angle = np.radians(60)
        x_rot = x * np.cos(angle) - y * np.sin(angle)
        y_rot = x * np.sin(angle) + y * np.cos(angle)
        x, y = x_rot, y_rot

    return x, y




# -----------------------------------------------------
# 3. DISTANCES BETWEEN USER AND ALL BS SITES
# -----------------------------------------------------
def compute_distances(user_pos, centers):
    """
    Computes distance between the user and each BS site.

    Args:
        user_pos : tuple (x, y)
        centers : ndarray of shape (19, 2)

    Returns:
        distances : ndarray of shape (19,)
    """
    ux, uy = user_pos
    dx = centers[:, 0] - ux
    dy = centers[:, 1] - uy
    return np.sqrt(dx**2 + dy**2)

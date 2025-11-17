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


# -----------------------------------------------------
# 2. RANDOM USER POSITION IN THE CENTRAL SECTOR
# -----------------------------------------------------
def random_user_position():
    """
    Generates a random (x, y) uniformly inside the 120° main sector of the
    central cell.

    Returns:
        (x, y) : tuple of floats
    """
    # Convert degrees to radians
    angle_start = np.deg2rad(SECTOR_ORIENTATION - SECTOR_ANGLE / 2)
    angle_end = np.deg2rad(SECTOR_ORIENTATION + SECTOR_ANGLE / 2)

    # Uniform angle within the sector
    theta = np.random.uniform(angle_start, angle_end)

    # For uniform distribution in 2D area: r = R * sqrt(U)
    r = CELL_RADIUS * np.sqrt(np.random.uniform(0, 1))

    x = r * np.cos(theta)
    y = r * np.sin(theta)

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

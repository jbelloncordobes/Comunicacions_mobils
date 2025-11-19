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
    ADJUSTMENT: Rotated 30 degrees to match 'Flat-Topped' orientation
    typically used in plots, ensuring no gaps between cells.
    
    Returns:
        centers : ndarray of shape (19, 2)
    """
    centers = [(0, 0)]  # Central cell at origin

    # Hex grid directions (distance between adjacent BS sites = sqrt(3) * R)
    d = np.sqrt(3) * CELL_RADIUS

    # CORRECCIÓN: Las direcciones ahora están rotadas 30 grados.
    # Ángulos: 30, 90, 150, 210, 270, 330.
    # Esto corresponde a:
    # 30:  (sqrt(3)/2, 0.5)
    # 90:  (0, 1)
    # 150: (-sqrt(3)/2, 0.5)
    # ...
    
    s3_2 = np.sqrt(3) / 2  # Valor de cos(30) o sin(60) -> aprox 0.866
    
    directions = [
        (s3_2, 0.5),   # 30 grados
        (0, 1),        # 90 grados
        (-s3_2, 0.5),  # 150 grados
        (-s3_2, -0.5), # 210 grados
        (0, -1),       # 270 grados
        (s3_2, -0.5)   # 330 grados
    ]

    # First ring (6 points)
    for dx, dy in directions:
        centers.append((d * dx, d * dy))

    # Second ring (12 points)
    for i in range(6):
        dx1, dy1 = directions[i]
        dx2, dy2 = directions[(i + 1) % 6]

        # Two points between each pair
        # Punto intermedio (la suma vectorial apunta al hueco correcto)
        centers.append((d * (dx1 + dx2), d * (dy1 + dy2)))
        # Punto extremo (2 veces la dirección principal)
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
    # Si el punto cae fuera del triángulo (en el cuadrado unitario), lo reflejamos
    if u + v > 1:
        u = 1 - u
        v = 1 - v

    # Transformación de coordenadas oblicuas a cartesianas
    # Base vectores: (R, 0) y (R/2, h) -> Ángulo 0 y 60
    x = u * CELL_RADIUS + v * (CELL_RADIUS/2)
    y = v * h

    # Elegir aleatoriamente uno de los dos triángulos para cubrir 120 grados
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
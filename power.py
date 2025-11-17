"""
power.py
---------
Functions to compute received powers and Signal-to-Interference Ratio (SIR).
"""

import numpy as np
from channel import total_channel_gain
from config import NUM_INTERFERING_CELLS


# -----------------------------------------------------
# 1. RECEIVED POWER FROM ALL CELLS
# -----------------------------------------------------
def received_powers(distances):
    """
    Computes received powers from the serving cell (index 0)
    and all interfering cells (indices 1..18).

    Args:
        distances : ndarray shape (19,)
            Distance from user to each BS site.

    Returns:
        desired : float
        interferers : ndarray shape (18,)
    """
    gains = total_channel_gain(distances)

    desired = gains[0]          # Central cell
    interferers = gains[1:]     # 18 surrounding cells

    return desired, interferers


# -----------------------------------------------------
# 2. COMPUTE SIR
# -----------------------------------------------------
def compute_sir(distances):
    """
    Computes SIR for one Monte-Carlo snapshot.

    Args:
        distances : ndarray shape (19,)

    Returns:
        sir : float
            Signal-to-Interference Ratio (linear scale)
    """
    desired, interferers = received_powers(distances)

    interference_power = np.sum(interferers)
    sir = desired / interference_power

    return sir

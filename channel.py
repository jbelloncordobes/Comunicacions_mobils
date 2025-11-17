"""
channel.py
-----------
Wireless channel models:
- Path loss
- Shadow fading (log-normal)
- Total channel gain
"""

import numpy as np
from config import PATHLOSS_EXPONENT, SHADOW_FADING_STD


# -----------------------------------------------------
# 1. PATH LOSS MODEL
# -----------------------------------------------------
def path_loss(distances):
    """
    Computes path-loss gain for each distance.

    PL ∝ d^{-ν}
    (The absolute constant cancels out in SIR, so we use proportional form.)

    Args:
        distances : ndarray of shape (19,)

    Returns:
        pl : ndarray of shape (19,)   (path-loss gain)
    """
    return distances ** (-PATHLOSS_EXPONENT)


# -----------------------------------------------------
# 2. SHADOW FADING (LOG-NORMAL)
# -----------------------------------------------------
def shadow_fading(num_samples):
    """
    Generates log-normal shadow fading values.

        X ~ N(0, σ^2) in dB
        SF_linear = 10^(X/10)

    Args:
        num_samples : int

    Returns:
        sf : ndarray of shape (num_samples,)
    """
    X = np.random.normal(0, SHADOW_FADING_STD, num_samples)
    return 10 ** (X / 10)


# -----------------------------------------------------
# 3. TOTAL CHANNEL GAIN
# -----------------------------------------------------
def total_channel_gain(distances):
    """
    Computes total channel gain for each distance, including:
        - Path loss
        - Shadow fading (log-normal)

    Args:
        distances : ndarray (19,)

    Returns:
        gains : ndarray (19,)
    """
    pl = path_loss(distances)
    sf = shadow_fading(len(distances))
    return pl * sf

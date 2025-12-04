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
    Computa la pérdida de path-loss para cada distancia

    PL ∝ d^{-ν}
    Alfa se cancela en SIR, usamos la forma proporcional
 
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
    Genera valores de shadow fading usando distribución log-normal

        X ~ N(0, σ^2) in dB
        SF_linear = 10^(X/10)

    Args:
        num_samples : int

    Returns:
        sf : ndarray of shape (num_samples,)
    """
    X = np.random.normal(loc = 0, scale = SHADOW_FADING_STD, size = num_samples)
    return 10 ** (X / 10)


# -----------------------------------------------------
# 3. TOTAL CHANNEL GAIN
# -----------------------------------------------------
def get_channel_gain(distance, pathloss_exp):
    # Evitar log(0)
    dist = np.maximum(distance, 1.0) # No puede ser superior a 1
    pl = dist ** (-pathloss_exp)
    
    # Shadowing independiente
    num_samples = 1 if np.isscalar(dist) else len(dist)
    X_dB = np.random.normal(0, SHADOW_FADING_STD, num_samples)
    sf = 10 ** (X_dB / 10.0)
    
    return pl * sf
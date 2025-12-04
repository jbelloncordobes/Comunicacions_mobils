"""
channel.py
-----------
Wireless channel models:
- Path loss
- Shadow fading (log-normal)
- Total channel gain
"""

import numpy as np
from config import SHADOW_FADING_STD

# -----------------------------------------------------
# TOTAL CHANNEL GAIN
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
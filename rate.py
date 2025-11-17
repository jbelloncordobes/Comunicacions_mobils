"""
rate.py
--------
Bit-rate computation based on SIR.
"""

import numpy as np

# ----------------------------
# Bit-rate calculation
# ----------------------------
def shannon_rate(sir, bandwidth=1e6):
    """
    Computes the Shannon capacity (bps) given SIR.

    R = B * log2(1 + SIR)

    Args:
        sir : float or ndarray
            Signal-to-Interference Ratio (linear scale)
        bandwidth : float
            Channel bandwidth in Hz (default 1 MHz)

    Returns:
        rate : float or ndarray
            Bit rate in bps
    """
    return bandwidth * np.log2(1 + sir)

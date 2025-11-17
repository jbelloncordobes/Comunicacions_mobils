"""
config.py
---------
Configuration constants for the wireless communication Monte-Carlo simulation.
These values are imported by all modules.
"""

import numpy as np

# ---------------------------
# Simulation parameters
# ---------------------------
NUM_SNAPSHOTS = 150      # Number of Monte-Carlo runs
CELL_RADIUS = 1000         # meters (typical macrocell)
NUM_INTERFERING_CELLS = 18 # Surrounding cells around the center
NUM_SECTORS = 3            # 3-sector antennas

# ---------------------------
# Channel parameters
# ---------------------------
PATHLOSS_EXPONENT = 3.8    # ν
SHADOW_FADING_STD = 8      # sigma in dB

# ---------------------------
# Antenna / geometry parameters
# ---------------------------
SECTOR_ANGLE = 120         # degrees
SECTOR_ORIENTATION = 0     # central sector pointing = 0 degrees

# ---------------------------
# Utility
# ---------------------------
# For reproducibility (optional)
#np.random.seed(1)

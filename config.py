import numpy as np

# ---------------------------
# Simulation parameters
# ---------------------------
NUM_SNAPSHOTS = 1500       # Cantidad de iteraciones Monte-Carlo
CELL_RADIUS = 1000         # Metros
NUM_SECTORS = 3            # Sectores por celda

# ---------------------------
# Channel parameters
# ---------------------------
SHADOW_FADING_STD = 8      # dB

# ---------------------------
# Physical parameters
# ---------------------------
TOTAL_BANDWIDTH = 100e6    # 100 MHz
SNR_GAP_DB = 4.0
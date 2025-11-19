import numpy as np

# ---------------------------
# Simulation parameters
# ---------------------------
NUM_SNAPSHOTS = 1500       # Cantidad de iteraciones Monte-Carlo
CELL_RADIUS = 1000         # Metros
NUM_CELLS = 19
NUM_SECTORS = 3            # Sectores por celda

# ---------------------------
# Channel parameters
# ---------------------------
PATHLOSS_EXPONENT = 3.8
SHADOW_FADING_STD = 8      # dB

# ---------------------------
# Physical parameters
# ---------------------------
TOTAL_BANDWIDTH = 100e6    # 100 MHz
SNR_GAP_DB = 4.0

# ---------------------------
# Antenna Geometry
# ---------------------------
# Asumimos orientación Flat-Top.
# Sector 0 apunta a 30° (Noreste)
# Sector 1 apunta a 150° (Noroeste)
# Sector 2 apunta a 270° (Sur)
SECTOR_BORESIGHTS = [30, 150, 270] 
SECTOR_WIDTH = 120         # Ancho de haz perfecto
"""
main.py
--------
Monte-Carlo simulation for uplink cellular network.
"""

import numpy as np
import matplotlib.pyplot as plt

from config import NUM_SNAPSHOTS
from geometry import generate_hex_grid, random_user_position, compute_distances
from power import compute_sir
from rate import shannon_rate


# ----------------------------
# 1. Generate BS positions
# ----------------------------
bs_centers = generate_hex_grid()


# ----------------------------
# 2. Run Monte-Carlo simulation
# ----------------------------
sir_values = np.zeros(NUM_SNAPSHOTS)

for i in range(NUM_SNAPSHOTS):
    # Random user position in central sector
    user_pos = random_user_position()

    # Compute distances to all BSs
    distances = compute_distances(user_pos, bs_centers)

    # Compute SIR for this snapshot
    sir = compute_sir(distances)
    sir_values[i] = sir

    if (i+1) % 1000 == 0:
        print(f"Snapshot {i+1}/{NUM_SNAPSHOTS} done")


# ----------------------------
# 3. Compute bit rates
# ----------------------------
bit_rates = shannon_rate(sir_values, bandwidth=1e6)  # 1 MHz channel


# ----------------------------
# 4. Plot results
# ----------------------------
plt.figure(figsize=(8,6))
plt.hist(10*np.log10(sir_values), bins=50, density=True, alpha=0.7)
plt.xlabel("SIR [dB]")
plt.ylabel("Probability Density")
plt.title("Histogram of SIR")
plt.grid(True)
plt.show()


plt.figure(figsize=(8,6))
plt.hist(bit_rates/1e6, bins=50, density=True, alpha=0.7)
plt.xlabel("Bit rate [Mbps]")
plt.ylabel("Probability Density")
plt.title("Histogram of Bit Rate")
plt.grid(True)
plt.show()


# ----------------------------
# 5. Summary statistics
# ----------------------------
print(f"Mean SIR: {np.mean(sir_values):.3f} (linear), {10*np.log10(np.mean(sir_values)):.2f} dB")
print(f"Mean bit rate: {np.mean(bit_rates)/1e6:.3f} Mbps")

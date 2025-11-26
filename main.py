"""
main.py
--------
Monte-Carlo simulation for uplink cellular network.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

from config import NUM_SNAPSHOTS, CELL_RADIUS
from geometry import generate_hex_grid, random_user_position, compute_distances
from power import compute_sir
from rate import shannon_rate

# ----------------------------
# 1. Generate BS positions
# ----------------------------
bs_centers = generate_hex_grid()

<<<<<<< Updated upstream
# ----------------------------
# 2. Run Monte-Carlo simulation
# ----------------------------
sir_values = np.zeros(NUM_SNAPSHOTS)
user_positions = np.zeros((NUM_SNAPSHOTS, 2))  # store user positions for plotting
=======
def run_simulation(reuse, alpha, v_exp):
    sirs = []
    
    centers = generate_hex_grid()
    users = generate_all_users(centers)
    
    print("Mostrando geometría... Cierra la ventana para continuar.")
    #plot_snapshot_geometry(centers, users)
    for _ in range(NUM_SNAPSHOTS): # tqdm para barra de progreso si quieres
        # 1. Generar 57 usuarios (3 por celda)
        users = generate_all_users(bs_centers)
        
        # 2. Calcular SIR para el link central
        val = calculate_uplink_sir(users, bs_centers, reuse, alpha, v_exp)
        sirs.append(val)
    return np.array(sirs)
>>>>>>> Stashed changes

for i in range(NUM_SNAPSHOTS):
    # Random user position in central sector
    user_pos = random_user_position()
    user_positions[i] = user_pos  # save position

    # Compute distances to all BSs
    distances = compute_distances(user_pos, bs_centers)

    # Compute SIR for this snapshot
    sir = compute_sir(distances)
    sir_values[i] = sir

    if (i+1) % 1000 == 0:
        print(f"Snapshot {i+1}/{NUM_SNAPSHOTS} done")

<<<<<<< Updated upstream
# ----------------------------
# 2b. Plot user positions and hexagonal cells
# ----------------------------
fig, ax = plt.subplots(figsize=(10,10))
=======
    plt.figure(figsize=(8, 6))
    plot_cdf(sir_n1, "N=1")
    plot_cdf(sir_n3, "N=3")
    plot_cdf(sir_n9, "N=9")
    # N=9 es probable que no se vea si es infinito, agregamos nota
    plt.axhline(0.03, label="N=9 (Ideal)", linestyle="--", color="green")
    plt.axvline(-5, color='r', linestyle=':', label="Target -5 dB")
    plt.title("CDF of Uplink SIR (One user per sector)")
    plt.xlabel("SIR (dB)")
    plt.ylabel("CDF")
    plt.legend()
    plt.grid(True)
    plt.show()
>>>>>>> Stashed changes

# Plot each BS cell as a hexagon
for (x, y) in bs_centers:
    hexagon = RegularPolygon(
        (x, y),
        numVertices=6,
        radius=CELL_RADIUS,
        orientation=np.radians(30),
        facecolor='none',
        edgecolor='black'
    )
    ax.add_patch(hexagon)

# Plot all user positions
ax.scatter(user_positions[:,0], user_positions[:,1], s=5, c='red', alpha=0.5, label='Users')

ax.set_aspect('equal')
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_title('User positions in the 19-cell hexagonal layout')
ax.legend()
plt.grid(True)
plt.show()

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

<<<<<<< Updated upstream
# ----------------------------
# 5. Summary statistics
# ----------------------------
print(f"Mean SIR: {np.mean(sir_values):.3f} (linear), {10*np.log10(np.mean(sir_values)):.2f} dB")
print(f"Mean bit rate: {np.mean(bit_rates)/1e6:.3f} Mbps")
=======
    plt.figure()
    plot_cdf(sir_n3, "Alpha=0")
    plot_cdf(best_sirs, f"Alpha={best_alpha:.1f}")
    plt.title(f"Impact of Fractional Power Control (N=3)")
    plt.legend()
    plt.grid()
    plt.show()


# ==========================================
# 4. EJERCICIO 4: THROUGHPUT
# ==========================================
def ex4(sir_n1, sir_n3, sir_n9):
    print("Simulating Question 4...")
    # Throughput = (W/N) * log2(1 + SIR/Gamma)
    # Reuse implica dividir ancho de banda W entre los sectores/celdas.
    # N=1: BW total en cada sector? Ojo: "Universal BW reuse" -> W en cada sector.
    # N=3: "Different BW in each sector" -> W/3 por sector.

    gamma = 10**(SNR_GAP_DB/10)

    # Tasas
    rate_n1 = (TOTAL_BANDWIDTH / 1) * np.log2(1 + sir_n1 / gamma)
    rate_n3 = (TOTAL_BANDWIDTH / 3) * np.log2(1 + sir_n3 / gamma)

    plt.figure()
    # Función auxiliar para rate
    def plot_rate(data, lbl):
        d = np.sort(data)/1e6
        y = np.arange(len(d))/len(d)
        plt.plot(d, y, label=lbl)

    plot_rate(rate_n1, "N=1 (BW=100M)")
    plot_rate(rate_n3, "N=3 (BW=33M)")
    plt.title("User Throughput CDF")
    plt.xlabel("Mbps")
    plt.ylabel("CDF")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    sir_n1, sir_n3, sir_n9 = ex1()
    #ex2()
    # ex4(sir_n1, sir_n3, sir_n9)
>>>>>>> Stashed changes

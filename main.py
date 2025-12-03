import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from tqdm import tqdm

from config import NUM_SNAPSHOTS, TOTAL_BANDWIDTH, SNR_GAP_DB, CELL_RADIUS
from geometry import generate_hex_grid, generate_all_users
from power import calculate_uplink_sir

def plot_snapshot_geometry(bs_centers, users_tensor):
    """
    Pinta el grid hexagonal y la posición de los 57 usuarios.
    users_tensor: shape (19, 3, 2)
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 1. Dibujar Celdas (Hexágonos)
    for i, (x, y) in enumerate(bs_centers):
        # Nota: orientation=np.radians(30) es para que quede "Flat Top" 
        # y encaje con las coordenadas que calculamos en geometry.py
        hex_patch = RegularPolygon(
            (x, y),
            numVertices=6,
            radius=CELL_RADIUS,
            orientation=np.radians(30), 
            facecolor='none',
            edgecolor='gray'
            # linestyle='--'
        )
        ax.add_patch(hex_patch)


        # Generar sectores
        angles = np.arange(6) * np.radians(60)
        vx = x + CELL_RADIUS * np.cos(angles)
        vy = y + CELL_RADIUS * np.sin(angles)

        for i in [0, 2, 4]:
            ax.plot([x, vx[i]], [y, vy[i]], linestyle='dotted', color='gray')
        
        # Poner número de celda
        ax.text(x, y, str(i), ha='center', va='center', fontsize=8, color='black')

    # 2. Dibujar Usuarios (Coloreados por sector)
    # Sector 0 (~0°)   -> Rojo
    # Sector 1 (~120°) -> Verde
    # Sector 2 (~240°) -> Azul

    colors = ['red', 'green', 'blue']
    labels = ['Sector 0', 'Sector 1', 'Sector 2']
    
    
    for s in range(3):
        # Extraer todos los usuarios del sector 's' de todas las celdas
        # users_tensor[:, s, 0] son las X, users_tensor[:, s, 1] son las Y
        xs = users_tensor[:, s, 0]
        ys = users_tensor[:, s, 1]
        
        ax.scatter(xs, ys, c=colors[s], s=20, label=labels[s], alpha=0.7)

    # Ajustes finales
    ax.set_aspect('equal')
    plt.xlabel('X [meters]')
    plt.ylabel('Y [meters]')
    plt.title('Snapshot: 19 Cells, 3 Users per Cell (1 per sector)')
    plt.legend(loc='upper right')
    plt.grid(True, which='both', linestyle=':', alpha=0.4)
    
    # Asegurar que se vea todo el grid
    margin = 500
    all_x = bs_centers[:,0]
    all_y = bs_centers[:,1]
    plt.xlim(min(all_x) - CELL_RADIUS - margin, max(all_x) + CELL_RADIUS + margin)
    plt.ylim(min(all_y) - CELL_RADIUS - margin, max(all_y) + CELL_RADIUS + margin)
    
    plt.show()


# Setup inicial
bs_centers = generate_hex_grid()

def run_simulation(reuse, powcont, v_exp):
    sirs = []
    
    # centers = generate_hex_grid()
    # users = generate_all_users(centers)
    
    # print("Mostrando geometría... Cierra la ventana para continuar.")
    # plot_snapshot_geometry(centers, users)
    for _ in range(NUM_SNAPSHOTS):
        # 1. Generar 57 usuarios (3 por celda)
        users = generate_all_users(bs_centers)
        
        # 2. Calcular SIR para el link central
        val = calculate_uplink_sir(users, bs_centers, reuse, powcont, v_exp)
        sirs.append(val)
    return np.array(sirs)

def plot_cdf(data, label, color=None):
    data = data[np.isfinite(data)]
    if len(data) == 0: return
    sorted_data = np.sort(data)
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
    if color:
        plt.plot(10 * np.log10(sorted_data), yvals, label=label, color=color)
    else:
        plt.plot(10 * np.log10(sorted_data), yvals, label=label)


# ==========================================
# 1. EJERCICIO 1: REUSE FACTORS
# ==========================================

def ex1():

    print("Simulating Question 1...")
    sir_n1 = run_simulation(reuse=1, powcont=0, v_exp=3.8)
    sir_n3 = run_simulation(reuse=3, powcont=0, v_exp=3.8)
    # sir_n9 dará infinito en grid pequeño, lo simulamos igual
    sir_n9 = run_simulation(reuse=9, powcont=0, v_exp=3.8)

    plt.figure(figsize=(8, 6))
    plot_cdf(sir_n1, "N=1")
    plot_cdf(sir_n3, "N=3")
    plot_cdf(sir_n9, "N=9")
    plt.axvline(-5, color='r', linestyle=':', label="Target -5 dB")
    plt.title("CDF of Uplink SIR (One user per sector)")
    plt.xlabel("SIR (dB)")
    plt.ylabel("CDF")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Probabilidades > -5dB
    p1 = np.mean(10*np.log10(sir_n1) >= -5)
    p3 = np.mean(10*np.log10(sir_n3) >= -5)
    p9 = np.mean(10*np.log10(sir_n9) >= -5)
    print(f"Prob SIR >= -5 dB: N=1 -> {p1:.2%}, N=3 -> {p3:.2%}, N=9 -> {p9:.2%}")

    return sir_n1, sir_n3, sir_n9


# ==========================================
# 2. EJERCICIO 2: POWER CONTROL (N=3)
# ==========================================
def ex2():
    print("Simulating Question 2...")
    powconts = np.arange(0.1, 1.1, 0.1)
    best_powcont = 0
    best_prob = 0
    best_sirs = None

    simulation_0 = run_simulation(reuse=3, powcont=0, v_exp=3.8)

    for a in powconts:
        s = run_simulation(reuse=3, powcont=a, v_exp=3.8)
        prob = np.mean(10*np.log10(s) >= -5)
        if prob > best_prob:
            best_prob = prob
            best_powcont = a
            best_sirs = s

    print(f"Mejor Power Control: {best_powcont:.1f} con cobertura {best_prob:.2%}")

    plt.figure()
    plot_cdf(simulation_0, "Power Control = 0")
    plot_cdf(best_sirs, f"Power Control = {best_powcont:.1f}")
    plt.title(f"Impact of Fractional Power Control (N=3)")
    plt.legend()
    plt.grid()
    plt.show()

# ==========================================
# 3. EJERCICIO 3: POWER CONTROL (N=3, 3.8, 4.5)
# ==========================================
def ex3():
    print("Simulating Question 3...")
    powconts = np.arange(0.1, 1.1, 0.1)
    best_powcont = 0
    best_prob = 0
    best_sirs = None

    
    for a in powconts:
        s = run_simulation(reuse=3, powcont=a, v_exp=3)
        prob = np.mean(10*np.log10(s) >= -5)
        if prob > best_prob:
            best_prob = prob
            best_powcont = a
            best_sirs = s

    print(f"Mejor Power Control (v = 3): {best_powcont:.1f} con cobertura {best_prob:.2%}")

    plt.figure()
    simulation_0_v3 = run_simulation(reuse=3, powcont=0, v_exp=3)
    plot_cdf(simulation_0_v3, "Power Control = 0 (v = 3)", "green")
    plot_cdf(best_sirs, f"Power Control = {best_powcont:.1f} (v = 3)", "yellow")

    for a in powconts:
        s = run_simulation(reuse=3, powcont=a, v_exp=3.8)
        prob = np.mean(10*np.log10(s) >= -5)
        if prob > best_prob:
            best_prob = prob
            best_powcont = a
            best_sirs = s

    print(f"Mejor Power Control (v = 3.8): {best_powcont:.1f} con cobertura {best_prob:.2%}")

    simulation_0_v38 = run_simulation(reuse=3, powcont=0, v_exp=3.8)
    plot_cdf(simulation_0_v38, "Power Control = 0 (v = 3.8)", "red")
    plot_cdf(best_sirs, f"Power Control = {best_powcont:.1f} (v = 3.8)", "orange")

    for a in powconts:
        s = run_simulation(reuse=3, powcont=a, v_exp=4.5)
        prob = np.mean(10*np.log10(s) >= -5)
        if prob > best_prob:
            best_prob = prob
            best_powcont = a
            best_sirs = s

    print(f"Mejor Power Control (v = 4.5): {best_powcont:.1f} con cobertura {best_prob:.2%}")

    simulation_0_v45 = run_simulation(reuse=3, powcont=0, v_exp=4.5)
    plot_cdf(simulation_0_v45, "Power Control = 0 (v = 4.5)", "magenta")
    plot_cdf(best_sirs, f"Power Control = {best_powcont:.1f} (v = 4.5)", "purple")

    plt.title(f"Impact of Fractional Power Control (N=3, 3.8, 4.5)")
    plt.xlabel("SIR (dB)")
    plt.ylabel("CDF")
    plt.legend()
    plt.grid()
    plt.show()

# ==========================================
# 4. EJERCICIO 4: THROUGHPUT
# ==========================================
def ex4(sir_n1, sir_n3, sir_n9):
    print("Simulating Question 4...")
    # Throughput = (W/N) * log2(1 + SIR/Gamma)
    gamma = 10**(SNR_GAP_DB/10)

    # Rates in bps
    rate_n1 = (TOTAL_BANDWIDTH / 1) * np.log2(1 + sir_n1 / gamma)
    rate_n3 = (TOTAL_BANDWIDTH / 3) * np.log2(1 + sir_n3 / gamma)
    rate_n9 = (TOTAL_BANDWIDTH / 9) * np.log2(1 + sir_n9 / gamma)

    # Helper to prepare sorted, finite, non-negative Mbps arrays
    def prepare_rate(r):
        r = np.array(r, dtype=float)
        r = r[np.isfinite(r)]       # drop inf/nan
        r = r[r > 0]                # drop non-positive rates (if any)
        r_mbps = r / 1e6            # convert to Mbps
        r_sorted = np.sort(r_mbps)
        return r_sorted

    r1 = prepare_rate(rate_n1)
    r3 = prepare_rate(rate_n3)
    r9 = prepare_rate(rate_n9)

    plt.figure(figsize=(8,6))

    def plot_rate_cdf(sorted_mbps, lbl):
        if len(sorted_mbps) == 0:
            return
        y = np.linspace(0, 1, len(sorted_mbps))        # proper CDF axis from 0 to 1
        plt.plot(sorted_mbps, y, label=lbl)

    # Statistics (in Mbps)
    avg1 = np.mean(r1) if len(r1)>0 else np.nan
    avg3 = np.mean(r3) if len(r3)>0 else np.nan
    avg9 = np.mean(r9) if len(r9)>0 else np.nan

    # the value r such that 97% of users have rate >= r -> that's the 3rd percentile.
    r97_1 = np.percentile(r1, 3) if len(r1)>0 else np.nan
    r97_3 = np.percentile(r3, 3) if len(r3)>0 else np.nan
    r97_9 = np.percentile(r9, 3) if len(r9)>0 else np.nan

    print(f"Average bit rate (Mbps): N=1 -> {avg1:.2f} Mbps, N=3 -> {avg3:.2f} Mbps, N=9 -> {avg9:.2f} Mbps")
    print(f"Rate that 97% of users achieve or exceed (3rd percentile) [Mbps]: N=1 -> {r97_1:.2f}, N=3 -> {r97_3:.2f}, N=9 -> {r97_9:.2f}")

    plot_rate_cdf(r1, "N=1 (BW=100 MHz)")
    plot_rate_cdf(r3, "N=3 (BW=33.33 MHz)")
    plot_rate_cdf(r9, "N=9 (BW=11.11 MHz)")

    plt.title("User Throughput CDF")
    plt.xlabel("Throughput (Mbps)")
    plt.ylabel("CDF")
    plt.grid(True, linestyle=':', alpha=0.4)
    plt.xlim(-20, 1250.0)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    sir_n1, sir_n3, sir_n9 = ex1() # Tenemos que tener en cuenta solo los sectores en la dirección del sector 0. Dos sectores se cortan por la mitad así que tenemos en cuenta solo 1 sector por esos dos.
    # ex2()
    ex3()
    # We can reuse the simulations from ex1 to save time
    ex4(sir_n1, sir_n3, sir_n9)
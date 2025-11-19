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
            edgecolor='gray',
            linestyle='--'
        )
        ax.add_patch(hex_patch)
        angles = np.arange(6) * np.radians(60)
        vx = x + CELL_RADIUS * np.cos(angles)
        vy = y + CELL_RADIUS * np.sin(angles)
    
        # Draw 3 internal lines (every other vertex = 0, 2, 4)
        for i in [0, 2, 4]:
            ax.plot([x, vx[i]], [y, vy[i]], linestyle='dotted', color='black')
        
        # Poner número de celda
        ax.text(x, y, str(i), ha='center', va='center', fontsize=8, color='black')

    # 2. Dibujar Usuarios (Coloreados por sector)
    # Sector 0 (30°) -> Rojo
    # Sector 1 (150°) -> Verde
    # Sector 2 (270°) -> Azul
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

def run_simulation(reuse, alpha, v_exp):
    sirs = []
    
    centers = generate_hex_grid()
    users = generate_all_users(centers)
    
    print("Mostrando geometría... Cierra la ventana para continuar.")
    plot_snapshot_geometry(centers, users)
    for _ in range(NUM_SNAPSHOTS): # tqdm para barra de progreso si quieres
        # 1. Generar 57 usuarios (3 por celda)
        users = generate_all_users(bs_centers)
        
        # 2. Calcular SIR para el link central
        val = calculate_uplink_sir(users, bs_centers, reuse, alpha, v_exp)
        sirs.append(val)
    return np.array(sirs)

def plot_cdf(data, label):
    data = data[np.isfinite(data)]
    if len(data) == 0: return
    sorted_data = np.sort(data)
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
    plt.plot(10 * np.log10(sorted_data), yvals, label=label)

# ==========================================
# 1. EJERCICIO 1: REUSE FACTORS
# ==========================================
print("Simulating Question 1...")
sir_n1 = run_simulation(reuse=1, alpha=0, v_exp=3.8)
sir_n3 = run_simulation(reuse=3, alpha=0, v_exp=3.8)
# sir_n9 dará infinito en grid pequeño, lo simulamos igual
sir_n9 = run_simulation(reuse=9, alpha=0, v_exp=3.8)

plt.figure(figsize=(8, 6))
plot_cdf(sir_n1, "N=1")
plot_cdf(sir_n3, "N=3")
plot_cdf(sir_n9, "N=9")
# N=9 es probable que no se vea si es infinito, agregamos nota
plt.axvline(x=100, label="N=9 (Ideal)", linestyle="--", color="green")
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
print(f"Prob SIR >= -5 dB: N=1 -> {p1:.2%}, N=3 -> {p3:.2%}")


# ==========================================
# 2. EJERCICIO 2: POWER CONTROL (N=3)
# ==========================================
print("Simulating Question 2...")
alphas = np.arange(0, 1.1, 0.1)
best_alpha = 0
best_prob = 0
best_sirs = None

for a in alphas:
    s = run_simulation(reuse=3, alpha=a, v_exp=3.8)
    prob = np.mean(10*np.log10(s) >= -5)
    if prob > best_prob:
        best_prob = prob
        best_alpha = a
        best_sirs = s

print(f"Mejor Alpha: {best_alpha:.1f} con cobertura {best_prob:.2%}")

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
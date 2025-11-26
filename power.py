"""
power.py
---------
Functions to compute received powers and Signal-to-Interference Ratio (SIR).
<<<<<<< Updated upstream
"""

import numpy as np
from channel import total_channel_gain
from config import NUM_INTERFERING_CELLS
=======
CORREGIDO: Incluye lógica de antena direccional (Triángulo) y filtrado de frecuencia.
"""

import numpy as np
from channel import get_channel_gain
from config import SECTOR_BORESIGHTS, SECTOR_WIDTH
>>>>>>> Stashed changes


# -----------------------------------------------------
# 1. RECEIVED POWER FROM ALL CELLS
# -----------------------------------------------------
def received_powers(distances):
    """
<<<<<<< Updated upstream
    Computes received powers from the serving cell (index 0)
    and all interfering cells (indices 1..18).

    Args:
        distances : ndarray shape (19,)
            Distance from user to each BS site.

    Returns:
        desired : float
        interferers : ndarray shape (18,)
    """
    gains = total_channel_gain(distances)

    desired = gains[0]          # Central cell
    interferers = gains[1:]     # 18 surrounding cells

    return desired, interferers


# -----------------------------------------------------
# 2. COMPUTE SIR
# -----------------------------------------------------
def compute_sir(distances):
    """
    Computes SIR for one Monte-Carlo snapshot.

    Args:
        distances : ndarray shape (19,)

    Returns:
        sir : float
            Signal-to-Interference Ratio (linear scale)
    """
    desired, interferers = received_powers(distances)

    interference_power = np.sum(interferers)
    sir = desired / interference_power

    return sir
=======
    Calcula SIR para el usuario víctima en Celda 0, Sector 0 (Uplink).
    
    Aplica:
    1. Power Control Fraccional (Tx basada en su propia celda).
    2. Filtrado por Reúso de Frecuencia (Solo sectores co-canal).
    3. Filtrado por Antena Direccional (Solo usuarios en el 'triángulo' de visión).

    Args:
        users_tensor: (19, 3, 2) -> Posiciones de todos los usuarios [celda, sector, xy]
        bs_centers: (19, 2) -> Posiciones de las estaciones base
        reuse_factor: (int) 1, 3, o 9.
        alpha: (float) Exponente de control de potencia (0.0 a 1.0).
        pathloss_exp: (float) Exponente de pérdidas.
    """
    
    # ------------------------------------------------
    # 1. USUARIO VÍCTIMA (Celda 0, Sector 0)
    # ------------------------------------------------
    # Antena receptora: BS 0, Sector 0 (Apunta a 30 grados según config)
    victim_bs = bs_centers[0]
    victim_user = users_tensor[0, 0] 
    
    # Boresight: Hacia dónde apunta la antena víctima
    boresight_angle = SECTOR_BORESIGHTS[0] # 30 grados
    beam_width = SECTOR_WIDTH              # 120 grados
    
    # Potencia de la señal deseada
    # Distancia a su propia BS (que es la 0)
    dist_signal = np.linalg.norm(victim_user - victim_bs)
    gain_signal = get_channel_gain(dist_signal, pathloss_exp)
    
    # Potencia de Transmisión (Power Control)
    # P_tx = (Gain)^(-alpha)
    p_tx_victim = gain_signal ** (-alpha)
    
    # Potencia Recibida (Señal)
    p_rx_signal = p_tx_victim * gain_signal
    
    # ------------------------------------------------
    # 2. CÁLCULO DE INTERFERENCIA
    # ------------------------------------------------
    interference_sum = 0.0
    
    # Iteramos sobre las celdas interferentes (1 a 18)
    # Saltamos la 0 porque es la propia celda (asumimos ortogonalidad intra-celda)
    for c in range(1, 19):
        
        # --- FILTRO A: REÚSO DE FRECUENCIA (Nivel Celda) ---
        # Si Reuse=1: Todas las celdas interfieren.
        # Si Reuse=3: Solo 1 de cada 3 celdas interfiere (aprox).
        # Usamos modulo como aproximación de cluster sin mapa explícito.
        if reuse_factor > 1 and (c % reuse_factor != 0):
            continue

        # Iteramos sobre los sectores de la celda 'c'
        for s in range(3):
            
            # --- FILTRO B: REÚSO DE FRECUENCIA (Nivel Sector) ---
            # "Solo sectores en la misma dirección con la misma frecuencia"
            # Asumimos patrón estándar: 
            # El Sector 0 de la Celda 'c' usa la Frecuencia A.
            # El Sector 1 usa Frecuencia B, Sector 2 usa Frecuencia C.
            # Como nuestra víctima está en Sector 0 (Frec A), SOLO nos interfiere
            # el Sector 0 de las celdas vecinas.
            if s != 0:
                continue
            
            # Posición del interferente y su BS
            interferer_pos = users_tensor[c, s]
            interferer_bs = bs_centers[c]
            
            # --- C. POWER CONTROL (¿Cuánto grita el interferente?) ---
            # El interferente ajusta su potencia según SU propia BS
            dist_own = np.linalg.norm(interferer_pos - interferer_bs)
            gain_own = get_channel_gain(dist_own, pathloss_exp)
            p_tx_interferer = gain_own ** (-alpha)
            
            # --- D. CANAL HACIA LA VÍCTIMA ---
            # Pérdidas desde el interferente hasta la BS 0
            dist_to_victim = np.linalg.norm(interferer_pos - victim_bs)
            gain_to_victim = get_channel_gain(dist_to_victim, pathloss_exp)
            
            # --- E. ANTENA DIRECCIONAL (EL TRIÁNGULO) ---
            # ¿Ve la BS 0 al interferente?
            # Calculamos vector desde BS 0 hacia el interferente
            delta = interferer_pos - victim_bs
            angle_rad = np.arctan2(delta[1], delta[0])
            angle_deg = np.degrees(angle_rad)
            
            # Normalizamos diferencia angular respecto al Boresight (30º)
            diff = angle_deg - boresight_angle
            # Truco matemático para normalizar entre -180 y 180
            diff = (diff + 180) % 360 - 180
            
            antenna_gain = 0.0
            # Si está dentro del ancho de haz (mitad izq, mitad der)
            if abs(diff) <= (beam_width / 2.0):
                antenna_gain = 1.0 # Ganancia unitaria (0 dB)
            else:
                antenna_gain = 0.0 # Fuera del haz -> No interfiere
            
            # Sumamos potencia
            p_rx_interferer = p_tx_interferer * gain_to_victim * antenna_gain
            interference_sum += p_rx_interferer

    # Evitar división por cero si no hay interferencia
    if interference_sum == 0:
        return 1e9 # Valor muy alto de SIR (ideal)
        
    return p_rx_signal / interference_sum
>>>>>>> Stashed changes

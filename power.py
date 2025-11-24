import numpy as np
from config import SECTOR_BORESIGHTS, SECTOR_WIDTH
from channel import get_channel_gain

def calculate_uplink_sir(users_tensor, bs_centers, reuse_factor, powcont, pathloss_exp):
    """
    Calcula SIR para el usuario en Celda 0, Sector 0.
    
    users_tensor: (19, 3, 2) -> Todos los usuarios del sistema
    """
    
    # --- 1. Definir Víctima y su Potencia ---
    # Usuario víctima: Celda 0, Sector 0
    victim_pos = users_tensor[0, 0]
    bs_victim_pos = bs_centers[0] # (0,0)
    
    # Calcula la distancia de la victima a su centro y el pathloss de dicha distancia (R)
    dist_own = np.linalg.norm(victim_pos - bs_victim_pos)
    gain_own = get_channel_gain(dist_own, pathloss_exp)
    
    # Potencia Transmisión Víctima (Power Control)
    p_tx_victim = gain_own ** (-powcont)
    p_rx_signal = p_tx_victim * gain_own #Falta por checkear
    
    # --- 2. Calcular Interferencia ---
    interference_sum = 0.0
    
    # Iteramos sobre TODAS las celdas y TODOS los sectores
    for c in range(19):
        for s in range(3):
            # Saltamos al usuario víctima (no se interfiere a sí mismo)
            if c == 0 and s == 0:
                continue
            
            # --- FILTRO 1: REUSO DE FRECUENCIA ---
            # Determina si este usuario (c, s) transmite en la freq de la víctima
            is_co_channel = False
            
            if reuse_factor == 1:
                # Todos los sectores de todas las celdas usan la freq
                is_co_channel = True
                
            elif reuse_factor == 3:
                # Reuso por sector: Solo el sector con misma orientación usa la freq
                # Es decir, solo Sector 0 de cualquier celda
                if s == 0:
                    is_co_channel = True
                    
            elif reuse_factor == 9:
                # Reuso 3 espacial y 3 sectorial
                # Solo Sector 0 de un cluster de celdas
                # Patrón aproximado para grid pequeño: 
                # Celdas 0 (centro), y anillos exteriores específicos. 
                # Para simulación simple N=9 en 19 celdas:
                # Solo interfieren las celdas que estarían en el tier co-canal.
                # En un grid de 19, con N=3 (cluster celdas), las vecinas directas NO interfieren.
                # Las del segundo anillo SÍ (parcialmente). 
                # Con N=9, la distancia de reuso es muy grande. 
                # Asumiremos que en este universo de 19 celdas, N=9 implica 
                # interferencia casi nula (solo ruido de fondo si hubiera).
                is_co_channel = False 
            
            if not is_co_channel:
                continue

            # --- SI ES CO-CANAL, CALCULAMOS POTENCIA ---
            interferer_pos = users_tensor[c, s]
            
            # Distancia a SU propia BS (para Power Control)
            dist_to_own_bs = np.linalg.norm(interferer_pos - bs_centers[c])
            gain_to_own = get_channel_gain(dist_to_own_bs, pathloss_exp)
            p_tx_interferer = gain_to_own ** (-powcont)
            
            # Distancia a BS Víctima (BS 0)
            dist_to_victim_bs = np.linalg.norm(interferer_pos - bs_centers[0])
            gain_to_victim = get_channel_gain(dist_to_victim_bs, pathloss_exp)
            
            # --- FILTRO 2: ANTENA SECTORIAL DE BS VÍCTIMA ---
            # La BS 0 Sector 0 mira a 30 grados. 
            # Chequear si el interferente cae en su lóbulo principal.
            # Ángulo de llegada del interferente:
            angle_rad = np.arctan2(interferer_pos[1], interferer_pos[0])
            angle_deg = np.degrees(angle_rad)
            
            boresight = SECTOR_BORESIGHTS[0] # 30 grados
            diff = np.abs(angle_deg - boresight)
            diff = diff % 360
            if diff > 180: diff = 360 - diff
            
            # Ganancia de antena: 1 (0dB) si está dentro, 0 (linear) si fuera
            antenna_gain = 1.0 if diff <= (SECTOR_WIDTH / 2) else 0.0
            
            if antenna_gain > 0:
                p_rx_interf = p_tx_interferer * gain_to_victim * antenna_gain
                interference_sum += p_rx_interf

    if interference_sum == 0:
        return np.inf # Caso ideal
        
    return p_rx_signal / interference_sum
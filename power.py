import numpy as np
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
    # Mapeos de los sectores que influyen en cada reuse factor
    mp1 = dict()
    mp1[0] = []
    mp1[1] = [0, 1, 2]
    mp1[2] = [0, 1, 2]
    mp1[3] = []
    mp1[4] = []
    mp1[5] = []
    mp1[6] = []
    mp1[7] = [0, 1, 2]
    mp1[8] = [0, 1, 2]
    mp1[9] = [0, 2]
    mp1[10] = [0, 1, 2]
    mp1[11] = []
    mp1[12] = []
    mp1[13] = []
    mp1[14] = []
    mp1[15] = []
    mp1[16] = []
    mp1[17] = [0]
    mp1[18] = []

    mp3 = dict()
    mp3[0] = []
    mp3[1] = [0]
    mp3[2] = [0]
    mp3[3] = []
    mp3[4] = []
    mp3[5] = []
    mp3[6] = []
    mp3[7] = [0]
    mp3[8] = [0]
    mp3[9] = [0]
    mp3[10] = [0]
    mp3[11] = []
    mp3[12] = []
    mp3[13] = []
    mp3[14] = []
    mp3[15] = []
    mp3[16] = []
    mp3[17] = [0]
    mp3[18] = []

    mp9 = dict()
    mp9[0] = []
    mp9[1] = []
    mp9[2] = []
    mp9[3] = []
    mp9[4] = []
    mp9[5] = []
    mp9[6] = []
    mp9[7] = [0]
    mp9[8] = []
    mp9[9] = [0]
    mp9[10] = []
    mp9[11] = []
    mp9[12] = []
    mp9[13] = []
    mp9[14] = []
    mp9[15] = []
    mp9[16] = []
    mp9[17] = [0]
    mp9[18] = []
    # Calcula la distancia de la victima a su centro y el pathloss de dicha distancia (R)
    R = np.linalg.norm(victim_pos - bs_victim_pos)
    Victim_gain = get_channel_gain(R, pathloss_exp)
    
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
                if (s in mp1[c]):
                    is_co_channel = True
                
            elif reuse_factor == 3:
                # Reuso por sector: Solo el sector con misma orientación usa la freq
                # Es decir, solo Sector 0 de cualquier celda
                if (s in mp3[c]):
                    is_co_channel = True
                    
            elif reuse_factor == 9:
                if (s in mp9[c]):
                    is_co_channel = True
            
            if not is_co_channel:
                continue

            # --- SI ES CO-CANAL, CALCULAMOS POTENCIA ---
            interferer_pos = users_tensor[c, s]
            d = np.linalg.norm(bs_victim_pos - interferer_pos)
            d_inter_center = np.linalg.norm(bs_centers[c] - interferer_pos)
            interferer_gain = get_channel_gain(d, pathloss_exp)
            interferer_center_gain = get_channel_gain(d_inter_center, pathloss_exp)
            interference_sum += (interferer_gain/(interferer_center_gain)**powcont)

    if interference_sum == 0:
        return np.inf # Caso ideal
    
    sir = (Victim_gain/(Victim_gain ** powcont)) / interference_sum
    
    return sir
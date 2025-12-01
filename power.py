import numpy as np
from config import SECTOR_BORESIGHTS, SECTOR_WIDTH
from channel import get_channel_gain

def calculate_uplink_sir1(users_tensor, bs_centers, reuse_factor, powcont, pathloss_exp):
    """
    Calcula SIR para el usuario en Celda 0, Sector 0.
    
    users_tensor: (19, 3, 2) -> Todos los usuarios del sistema
    """
    
    # --- 1. Definir Víctima y su Potencia ---
    # Usuario víctima: Celda 0, Sector 0
    victim_pos = users_tensor[0, 0]
    bs_victim_pos = bs_centers[0] # (0,0)
    mp = dict()
    mp[0] = []
    mp[1] = [1]
    mp[2] = [2]
    mp[3] = [2]
    mp[4] = [0]
    mp[5] = [0]
    mp[6] = [1]
    mp[7] = [1, 2]
    mp[8] = [1]
    mp[9] = [2]
    mp[10] = [2]
    mp[11] = [0]
    mp[12] = [2]
    mp[13] = [0]
    mp[14] = [0]
    mp[15] = [0]
    mp[16] = [0]
    mp[17] = [1]
    mp[18] = [1]
    # Calcula la distancia de la victima a su centro y el pathloss de dicha distancia (R)
    R = np.linalg.norm(victim_pos - bs_victim_pos)
    # signal = (R ** (powcont * pathloss_exp)) * (R ** (-pathloss_exp))
    # victim_pathloss = 1/(R ** pathloss_exp)
    # signal = victim_pathloss * (10 ** (SHADOW_FADING_STD/10))
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
                if (s in mp[c]):
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
            d = np.linalg.norm(victim_pos - interferer_pos)
            interference_sum += 1/ (d ** pathloss_exp)

    if interference_sum == 0:
        return np.inf # Caso ideal
    
    sir = (1/ (R ** pathloss_exp)) * (1/(interference_sum))
    
    return 10*np.log10(sir)
    #return sir


def calculate_uplink_sir2(users_tensor, bs_centers, reuse_factor, powcont, pathloss_exp):
    """
    Calcula SIR para el usuario en Celda 0, Sector 0.
    
    users_tensor: (19, 3, 2) -> Todos los usuarios del sistema
    """
    
    # --- 1. Definir Víctima y su Potencia ---
    # Usuario víctima: Celda 0, Sector 0
    victim_pos = users_tensor[0, 0]
    bs_victim_pos = bs_centers[0] # (0,0)
    mp = dict()
    mp[0] = []
    mp[1] = [0, 1, 2]
    mp[2] = [0, 1, 2]
    mp[3] = []
    mp[4] = []
    mp[5] = []
    mp[6] = []
    mp[7] = [0, 1, 2]
    mp[8] = [0, 1, 2]
    mp[9] = [0, 2]
    mp[10] = [0, 1, 2]
    mp[11] = []
    mp[12] = []
    mp[13] = []
    mp[14] = []
    mp[15] = []
    mp[16] = []
    mp[17] = [0]
    mp[18] = []
    # Calcula la distancia de la victima a su centro y el pathloss de dicha distancia (R)
    R = np.linalg.norm(victim_pos - bs_victim_pos)
    # signal = (R ** (powcont * pathloss_exp)) * (R ** (-pathloss_exp))
    # victim_pathloss = 1/(R ** pathloss_exp)
    # signal = victim_pathloss * (10 ** (SHADOW_FADING_STD/10))
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
                if (s in mp[c]):
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
            d = np.linalg.norm(victim_pos - interferer_pos)
            interference_sum += get_channel_gain(d, pathloss_exp)

    if interference_sum == 0:
        return np.inf # Caso ideal
    
    sir = get_channel_gain(R, pathloss_exp) / interference_sum
    
    return sir
    #return sir

def calculate_uplink_sir(users_tensor, bs_centers, reuse_factor, powcont, pathloss_exp):
    """
    Calcula SIR para el usuario en Celda 0, Sector 0.
    """
    
    # Usuario víctima
    victim_pos = users_tensor[0, 0]
    bs_victim_pos = bs_centers[0]
    mp = dict()
    mp[0] = []
    mp[1] = [0, 1, 2]
    mp[2] = [0, 1, 2]
    mp[3] = []
    mp[4] = []
    mp[5] = []
    mp[6] = []
    mp[7] = [0, 1, 2]
    mp[8] = [0, 1, 2]
    mp[9] = [0, 2]
    mp[10] = [0, 1, 2]
    mp[11] = []
    mp[12] = []
    mp[13] = []
    mp[14] = []
    mp[15] = []
    mp[16] = []
    mp[17] = [0]
    mp[18] = []
    
    # Distancia usuario → BS
    R = np.linalg.norm(victim_pos - bs_victim_pos)
    
    # Control de potencia UL
    # Ganancia de transmisión proporcional a R^(powcont * alpha)
    tx_gain_victim = R**(powcont * pathloss_exp)
    signal = tx_gain_victim * get_channel_gain(R, pathloss_exp)
    
    interference_sum = 0.0
    
    for c in range(19):
        for s in range(3):
            if c == 0 and s == 0:
                continue
            
            # Reuse (NO TOCADO)
            is_co_channel = False
            
            if reuse_factor == 1:
                if (s in mp[c]):
                    is_co_channel = True
                    
            elif reuse_factor == 3:
                if s == 0:
                    is_co_channel = True
                    
            elif reuse_factor == 9:
                is_co_channel = False
            
            if not is_co_channel:
                continue
            
            interferer_pos = users_tensor[c, s]
            
            d = np.linalg.norm(victim_pos - interferer_pos)
            
            # Control de potencia para el interferente
            tx_gain_int = d**(powcont * pathloss_exp)
            interference_sum += tx_gain_int * get_channel_gain(d, pathloss_exp)
    
    if interference_sum == 0:
        return np.inf
    
    sir = signal / interference_sum
    return sir

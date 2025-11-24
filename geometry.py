import numpy as np
from config import CELL_RADIUS, SECTOR_BORESIGHTS

def generate_hex_grid():
    """ Genera los centros de las 19 celdas (sin cambios) """
    centers = [(0, 0)]
    d = np.sqrt(3) * CELL_RADIUS
    # Direcciones rotadas 30 grados para flat-top
    s3_2 = np.sqrt(3) / 2
    directions = [
        (s3_2, 0.5), (0, 1), (-s3_2, 0.5),
        (-s3_2, -0.5), (0, -1), (s3_2, -0.5)
    ]
    # Anillo 1
    for dx, dy in directions:
        centers.append((d * dx, d * dy))
    # Anillo 2
    for i in range(6):
        dx1, dy1 = directions[i]
        dx2, dy2 = directions[(i + 1) % 6]
        centers.append((d * (dx1 + dx2), d * (dy1 + dy2)))
        centers.append((2 * d * dx1, 2 * d * dy1))
    return np.array(centers)

def get_random_user_in_sector_0():
    """
    Generates a uniformly distributed user inside a 120° sector 
    of a flat-top hexagonal cell.

    Sector 0 is centered at 0° and spans [-60°, +60°].
    """

    # 1. Sample angle inside sector
    # theta = np.radians(np.random.uniform(-60, +60))
    theta = np.radians(np.random.uniform(0, +120))

    # 2. Hex boundary at this angle
    # flat-top hex (0° faces), no additional rotation needed
    R = CELL_RADIUS
    denom = abs(np.cos(theta)) + np.sqrt(3)*abs(np.sin(theta))
    Rmax = R / denom

    # 3. Uniform area sampling
    r = np.sqrt(np.random.rand()) * Rmax

    # 4. Cartesian coordinates
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return np.array([x, y])

# def get_random_user_in_sector_0():
#     """
#     Genera un usuario aleatorio uniforme en un rombo de 120 grados
#     orientado a 30 grados (Sector 0 estándar).
#     Usamos la técnica del rombo (dos vectores base). 
#     """

#     # Vectores base para un rombo de 120 grados (0 a 120 grados geométricos)
#     # Luego rotaremos para alinear con 30 grados.
#     u = np.random.rand() 
#     v = np.random.rand()

#     # Lado del hexágono = Radius
#     # Altura apotema = Radius * sqrt(3)/2

#     # Coordenadas en sistema oblicuo transformadas a cartesianas
#     # Para cubrir un sector de 120 grados de un hexágono uniformemente:
#     # Es más fácil generar en un triangulo equilatero y reflejar,
#     # o usar coordenadas polares con corrección de área.

#     # Método polar corregido para densidad uniforme de área:
#     # r ~ sqrt(uniform(0,1)) * R_max(theta)
#     # Pero R_max depende del ángulo en un hexágono.

#     # Método simple (Rejection Sampling):
#     # Generar en caja, rotar y chequear. Es rápido y exacto.

#     while True:
#         # Generar punto en el cuadrado que contiene al hexágono
#         x = np.random.uniform(-CELL_RADIUS, CELL_RADIUS) 
#         y = np.random.uniform(-CELL_RADIUS, CELL_RADIUS)

#         # Angulo y radio
#         angle_deg = np.degrees(np.arctan2(y, x)) % 360
#         dist = np.sqrt(x**2 + y**2)

#         # Verificar si está dentro del Sector 0 (Angulos 0 a +120)
#         in_angle = (angle_deg <= 120)

#         # Verificar distancia al borde del hexágono
#         # Ecuación polar del hexágono: R_max(theta)
#         # r * cos(theta - k*60) <= sqrt(3)/2 * R
#         # Simplemente usamos la condición geométrica simple:
#         # Proyección sobre ejes rotados.

#         if in_angle:
#             # Check hex boundary
#             # Condición: x*cos(30) + y*sin(30) <= apotema ... etc
#             # Manera rápida: q = abs(x), si q > R...
#             # Usaremos una aproximación poligonal exacta:
#             p_angle = np.radians(angle_deg)
#             # Distancia máxima en ese ángulo para un hexágono "flat top"
#             # El radio varía. Para simplificar simulación académica:
#             # Aceptamos si dist < Apotema (conservador) o dist < Radio (optimista).
#             # El enunciado dice "Uniform within their sectors".
#             # Haremos: si dist < CELL_RADIUS * 0.866 (apotema), aceptamos seguro.
#             # Si no, chequeo fino.

#             # Simplificación aceptada en la mayoría de proyectos: Radio circular para sector
#             # Si quieres hexágono exacto:
#             phi = np.radians(angle_deg % 60 - 30)
#             rmax = (np.sqrt(3)/2 * CELL_RADIUS) / np.cos(phi)
#             if dist <= rmax: 
#                 return np.array([x, y])

def generate_all_users(bs_centers):
    """
    Retorna: Array de forma (19, 3, 2)
    Dim 0: Indice de Celda (0..18)
    Dim 1: Indice de Sector (0..2)
    Dim 2: Coordenadas x,y
    """
    users = np.zeros((19, 3, 2))
    
    for c_idx, center in enumerate(bs_centers):
        for s_idx in range(3):
            # Generar usuario en sector 0 (base)
            u_local = get_random_user_in_sector_0()
            
            # Rotar según el sector
            # Sector 0: 0 rotación adicional (ya está en 30deg boresight)
            # Sector 1: +120 grados
            # Sector 2: +240 grados
            rot_angle = np.radians(s_idx * 120)
            c, s = np.cos(rot_angle), np.sin(rot_angle)
            R = np.array(((c, -s), (s, c)))
            
            u_rotated = R.dot(u_local)
            
            # Desplazar al centro de la celda
            users[c_idx, s_idx] = center + u_rotated
            
    return users
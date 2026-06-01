import itertools
import numpy as np
from skimage.color import rgb2lab, deltaE_ciede2000

def rgb_to_cmyk(rgb):
    """Convierte color RGB (0-255) a CMYK (0.0 - 1.0)"""
    r = rgb[0] / 255.0
    g = rgb[1] / 255.0
    b = rgb[2] / 255.0
    
    k = 1.0 - max(r, g, b)
    if k == 1.0:
        return np.array([0.0, 0.0, 0.0, 1.0])
    
    c = (1.0 - r - k) / (1.0 - k)
    m = (1.0 - g - k) / (1.0 - k)
    y = (1.0 - b - k) / (1.0 - k)
    
    return np.array([c, m, y, k])

def cmyk_to_rgb(cmyk):
    """Convierte color CMYK (0.0 - 1.0) a RGB (0-255)"""
    c, m, y, k = cmyk
    r = int(255 * (1.0 - c) * (1.0 - k))
    g = int(255 * (1.0 - m) * (1.0 - k))
    b = int(255 * (1.0 - y) * (1.0 - k))
    return np.array([r, g, b])

def mezclar_cmyk(pinturas_cmyk, gotas_por_pintura):
    """
    Simula la mezcla sustractiva promediando las proporciones de CMYK 
    según la cantidad de gotas de cada una.
    """
    total_gotas = sum(gotas_por_pintura)
    if total_gotas == 0:
        return np.array([0.0, 0.0, 0.0, 0.0]) # Sin pintura
    
    mezcla = np.zeros(4)
    for cmyk, gotas in zip(pinturas_cmyk, gotas_por_pintura):
        mezcla += cmyk * gotas
        
    mezcla /= total_gotas
    return mezcla

def rgb_a_lab_unidad(rgb):
    """Convierte un único color RGB [0-255] a CIELAB para cálculo de Delta E"""
    # rgb2lab espera un array de dimensiones (H, W, 3) y valores entre 0 y 1
    rgb_normalizado = np.array([[rgb]], dtype=np.float64) / 255.0
    return rgb2lab(rgb_normalizado)[0][0]

def optimizar_mezcla(rgb_objetivo, lista_rgb_pinturas, max_gotas_total=15):
    """
    Encuentra la combinación óptima de gotas para acercarse al color objetivo.
    """
    # 1. Convertir todo a CMYK para la simulación de mezcla
    cmyk_objetivo = rgb_to_cmyk(rgb_objetivo)
    cmyk_pinturas = [rgb_to_cmyk(rgb) for rgb in lista_rgb_pinturas]
    
    # Convertir el objetivo a LAB para medir distancia perceptual real
    lab_objetivo = rgb_a_lab_unidad(rgb_objetivo)
    
    num_pinturas = len(lista_rgb_pinturas)
    
    mejor_distancia = float('inf')
    mejores_gotas = None
    mejor_rgb_resultante = None
    
    # 2. Generar todas las combinaciones posibles de gotas
    # Evaluamos desde 1 gota en total hasta max_gotas_total
    for total_g in range(1, max_gotas_total + 1):
        # itertools.combinations_with_replacement ayuda a repartir las gotas
        for comb in itertools.combinations_with_replacement(range(num_pinturas), total_g):
            # Contar cuántas gotas de cada pintura hay en esta combinación
            gotas = [comb.count(i) for i in range(num_pinturas)]
            
            # Simular mezcla en CMYK y revertir a RGB
            mezcla_cmyk = mezclar_cmyk(cmyk_pinturas, gotas)
            rgb_mezcla = cmyk_to_rgb(mezcla_cmyk)
            
            # Convertir a LAB para calcular la diferencia perceptual (Delta E CIE2000)
            lab_mezcla = rgb_a_lab_unidad(rgb_mezcla)
            distancia = deltaE_ciede2000(lab_objetivo, lab_mezcla)
            
            # Si es la mejor distancia encontrada, guardamos el resultado
            if distancia < mejor_distancia:
                mejor_distancia = distancia
                mejores_gotas = gotas
                mejor_rgb_resultante = rgb_mezcla
                
    return mejores_gotas, mejor_rgb_resultante, mejor_distancia

# --- EJEMPLO DE USO ---
if __name__ == "__main__":
    # Color que queremos lograr (ej. un verde oliva oscuro)
    color_objetivo = [145, 186, 115]
    
    # Pinturas de las que disponemos en nuestra paleta (RGB)
    # Ejemplo: Azul, Amarillo, Blanco, Negro
    mis_pinturas = [
        [44, 113, 91], 
        [194, 240, 45], 
        [161, 221, 94],
        [255, 255, 255], # Blanco
        [15, 15, 15]     # Negro
    ]
    
    print("Calculando la mezcla óptima...")
    gotas_optimas, rgb_resultado, d_e = optimizar_mezcla(
        color_objetivo, 
        mis_pinturas, 
        max_gotas_total=12 # Límite de gotas totales para la mezcla
    )
    
    print("\n--- RESULTADOS ---")
    print(f"Color Objetivo (RGB): {color_objetivo}")
    print("Pinturas disponibles:")
    for i, p in enumerate(mis_pinturas):
        print(f"  Pintura {i+1}: {p} -> Gotas necesarias: {gotas_optimas[i]}")
        
    print(f"\nColor Resultante de la mezcla (RGB): {rgb_resultado.astype(int).tolist()}")
    print(f"Distancia Perceptual (Delta E CIE2000): {d_e:.2f}")
    
    if d_e < 1.0:
        print("Resultado: La diferencia es imperceptible para el ojo humano.")
    elif d_e < 3.0:
        print("Resultado: Excelente aproximación (difícil de notar la diferencia).")
    else:
        print("Resultado: Aproximación cercana, pero no tan buena con las pinturas actuales.")

# 🎨 Optimizador de Mezclas de Pintura (RGB a CMYK)

Este script en Python ayuda a recrear un color objetivo a partir de una paleta de pinturas reales utilizando un enfoque discreto (por gotas). 

Dado que los códigos RGB representan **síntesis aditiva** (luz) y las pinturas físicas se comportan bajo la **síntesis sustractiva** (pigmentos), el script convierte los colores de entrada al espacio **CMYK** para simular mezclas físicas reales del mundo real. Posteriormente, utiliza la métrica industrial **Delta E (CIEDE2000)** en el espacio de color **CIELAB** para encontrar de forma exacta la combinación de gotas que ofrece la menor diferencia perceptual para el ojo humano.

---

## 🚀 Características

- **Simulación Sustractiva Real:** Conversión de RGB a CMYK para emular cómo se mezclan las pinturas físicas en lugar de los colores en una pantalla.
- **Enfoque Discreto (Gotas):** Ideal para la vida real; calcula combinaciones exactas usando "unidades" o gotas enteras de pintura.
- **Optimización Perceptual:** No utiliza una simple distancia euclidiana. Implementa el estándar **CIEDE2000** que se adapta a la forma real en la que el ojo humano percibe las diferencias de color.
- **Limpio y Legible:** Formatea las salidas de NumPy para que los resultados RGB sean listas nativas de Python fáciles de leer.

---

## 📋 Requisitos Previos

El proyecto requiere Python 3.x y las siguientes librerías científicas para el manejo de matrices y análisis de color:

```bash
pip install numpy scikit-image
```

---

## 💻 Código Fuente (`mezclador.py`)

Crea un archivo llamado `mezclador.py` y pega el siguiente código:

```python
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
    """Simula la mezcla sustractiva promediando las proporciones CMYK"""
    total_gotas = sum(gotas_por_pintura)
    if total_gotas == 0:
        return np.array([0.0, 0.0, 0.0, 0.0])
    
    mezcla = np.zeros(4)
    for cmyk, gotas in zip(pinturas_cmyk, gotas_por_pintura):
        mezcla += cmyk * gotas
        
    mezcla /= total_gotas
    return mezcla

def rgb_a_lab_unidad(rgb):
    """Convierte un único color RGB [0-255] a CIELAB para Delta E"""
    rgb_normalizado = np.array([[rgb]], dtype=np.float64) / 255.0
    return rgb2lab(rgb_normalizado)[0][0]

def optimizar_mezcla(rgb_objetivo, lista_rgb_pinturas, max_gotas_total=15):
    """Encuentra la combinación óptima de gotas mediante fuerza bruta acotada"""
    cmyk_pinturas = [rgb_to_cmyk(rgb) for rgb in lista_rgb_pinturas]
    lab_objetivo = rgb_a_lab_unidad(rgb_objetivo)
    num_pinturas = len(lista_rgb_pinturas)
    
    mejor_distancia = float('inf')
    mejores_gotas = None
    mejor_rgb_resultante = None
    
    for total_g in range(1, max_gotas_total + 1):
        for comb in itertools.combinations_with_replacement(range(num_pinturas), total_g):
            gotas = [comb.count(i) for i in range(num_pinturas)]
            
            mezcla_cmyk = mezclar_cmyk(cmyk_pinturas, gotas)
            rgb_mezcla = cmyk_to_rgb(mezcla_cmyk)
            
            lab_mezcla = rgb_a_lab_unidad(rgb_mezcla)
            distancia = deltaE_ciede2000(lab_objetivo, lab_mezcla)
            
            if distancia < mejor_distancia:
                mejor_distancia = distancia
                mejores_gotas = gotas
                mejor_rgb_resultante = rgb_mezcla
                
    return mejores_gotas, mejor_rgb_resultante, mejor_distancia

# --- CONFIGURACIÓN DE PRUEBA ---
if __name__ == "__main__":
    # Color que queremos conseguir (ej: un verde oliva)
    color_objetivo = [100, 130, 60] 
    
    # Paleta de pinturas reales de las que disponemos (RGB)
    mis_pinturas = [
        [10, 50, 180],   # Pintura 1: Azul
        [240, 210, 20],  # Pintura 2: Amarillo
        [255, 255, 255], # Pintura 3: Blanco
        [15, 15, 15]     # Pintura 4: Negro
    ]
    
    print("Calculando la mezcla óptima...")
    gotas_optimas, rgb_resultado, d_e = optimizar_mezcla(
        color_objetivo, 
        mis_pinturas, 
        max_gotas_total=12
    )
    
    print("\n--- RESULTADOS ---")
    print(f"Color Objetivo (RGB): {color_objetivo}")
    print("Pinturas disponibles y dosis requerida:")
    for i, p in enumerate(mis_pinturas):
        print(f"  🟢 Pintura {i+1} {p} -> Gotas necesarias: {gotas_optimas[i]}")
        
    print(f"\nColor Resultante (RGB): {rgb_resultado.astype(int).tolist()}")
    print(f"Distancia Perceptual (Delta E CIE2000): {d_e:.2f}")
    
    if d_e < 1.0:
        print("Resultado: La diferencia es imperceptible para el ojo humano.")
    elif d_e < 3.0:
        print("Resultado: Excelente aproximación (difícil de notar la diferencia).")
    else:
        print("Resultado: Aproximación más cercana posible con las pinturas actuales.")
```

---

## 📊 Entendiendo el Resultado (Delta E)

La distancia de color se mide mediante el estándar **CIEDE2000 ($\Delta E_{00}$)**:
* **$\Delta E < 1.0$**: Imperceptible para el ojo humano.
* **$1.0 \le \Delta E < 2.0$**: Perceptible solo por observadores experimentados o pantallas muy juntas.
* **$2.0 \le \Delta E < 3.5$**: Perceptible por cualquier persona, pero se considera una aproximación aceptable en aplicaciones prácticas.
* **$\Delta E \ge 3.5$**: Diferencia clara. Si obtienes este valor, significa que necesitas añadir un color diferente a tus pinturas base para poder aproximar mejor el objetivo.

---

## 🛠️ Personalización

Puedes editar las variables dentro del bloque `if __name__ == "__main__":` para adaptarlo a tus necesidades:
1. Cambia `color_objetivo` por el color RGB que quieres clonar.
2. Añade o quita arreglos RGB dentro de `mis_pinturas` (soporta perfectamente de 3 a 5 pinturas base).
3. Modifica `max_gotas_total` para permitir combinaciones más grandes (un número entre 10 y 15 suele ser ideal para mantener el cálculo instantáneo).

---

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT. ¡Siente libre de clonarlo y adaptarlo para tus proyectos de arte o diseño!

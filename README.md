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

## 📊 Entendiendo el Resultado (Delta E)

La distancia de color se mide mediante el estándar **CIEDE2000 ($\Delta E_{00}$)**:
* **$\Delta E < 1.0$**: Imperceptible para el ojo humano.
* **$1.0 \le \Delta E < 2.0$**: Perceptible solo por observadores experimentados o pantallas muy juntas.
* **$2.0 \le \Delta E < 3.5$**: Perceptible por cualquier persona, pero se considera una aproximación aceptable en aplicaciones prácticas.
* **$\Delta E \ge 3.5$**: Diferencia clara. Si obtienes este valor, significa que necesitas añadir un color diferente a tus pinturas base para poder aproximar mejor el objetivo.

---

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT. ¡Siente libre de clonarlo y adaptarlo para tus proyectos de arte o diseño!

# 🔢 Dualidad Binaria y Evolución de Patrones en la Conjetura de Collatz

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20458849.svg)](https://doi.org/10.5281/zenodo.20458849)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LaTeX](https://img.shields.io/badge/LaTeX-pdfLaTeX-green.svg)](https://www.latex-project.org/)

> **Autor:** Cristian F. F. (Investigador Independiente)  
> **Asistente técnico:** Grok (xAI)  
> **Fecha:** Mayo 2026  
> **DOI:** [10.5281/zenodo.20458849](https://doi.org/10.5281/zenodo.20458849)

---

## 📋 Resumen

Este repositorio contiene un **marco conceptual exploratorio** que combina dos perspectivas complementarias para analizar la Conjetura de Collatz:

1. **Dualidad Binaria**: Asociación de una trayectoria de Collatz con su "secuencia espejo" mediante inversión de bits de longitud fija.
2. **Evolución de Patrones Binarios**: Análisis de cómo los patrones binarios evolucionan bajo la operación de Collatz, con énfasis en la reducción de entropía.

### 🎯 Resultados Principales

- **Teorema de Dualidad Final**: Si una trayectoria alcanza $N_K = 1$, entonces su espejo satisface $M_K = 2^L - 2$ (demostrado formalmente).
- **Identidad de Conservación**: $N_k + M_k = 2^L - 1$ (sin truncamiento).
- **Patrones Alternantes**: Los números de la forma $(2^{2m} - 1)/3$ alcanzan una potencia de 2 en un único paso de $3n+1$.
- **Sincronía de Extremos**: En 100% de las trayectorias analizadas, el máximo de $N_k$ coincide temporalmente con el mínimo de $M_k$.
- **Estructura Modular**: El tiempo de parada depende fuertemente de la clase residual módulo potencias de 2, pero no de la módulo 3.

> ⚠️ **Nota importante**: Este trabajo **no demuestra la Conjetura de Collatz**. Es un estudio exploratorio que proporciona nueva perspectiva algebraica y evidencia computacional.

---

## 📁 Estructura del Repositorio

```
Dualidad-Binaria/
│
├── paper/                    # Documentación académica
│   ├── main.tex              # Código fuente LaTeX
│   └── main.pdf              # Versión PDF compilada
│
├── scripts/                  # Scripts Python para reproducibilidad
│   ├── appendix_generator.py # Genera datos para L=20
│   ├── advanced_analysis.py  # Análisis para L=32 y ML
│   └── modular_analysis.py   # Test de Kruskal-Wallis
│
├── data/                     # Datos generados (CSV)
│   ├── l20/                  # Datos para longitud L=20
│   ├── l32/                  # Datos para longitud L=32
│   └── modular/              # Datos de análisis modular
│
├── figures/                  # Figuras generadas (PNG)
│   ├── l20/                  # Gráficos de anti-correlación
│   ├── l32/                  # Gráficos de ML y estadísticos
│   └── modular/              # Gráficos de Kruskal-Wallis
│
├── README.md                 # Este archivo
├── LICENSE                   # Licencia CC BY 4.0
├── requirements.txt          # Dependencias Python
└── .gitignore                # Archivos ignorados por Git
```

---

## 🚀 Inicio Rápido

### 1. Requisitos Previos

- **Python 3.8+** con pip
- **LaTeX** (TeX Live, MiKTeX o MacTeX) para compilar el PDF
- **Git** para clonar el repositorio

### 2. Clonar el Repositorio

```bash
git clone https://github.com/MrVenomSnake/Dualidad-Binaria.git
cd Dualidad-Binaria
```

### 3. Instalar Dependencias Python

```bash
pip install -r requirements.txt
```

O manualmente:

```bash
pip install numpy pandas matplotlib scipy scikit-learn tqdm
```

### 4. Generar Datos y Figuras

Ejecuta los scripts en orden:

```bash
# Genera datos para el Apéndice A (L=20)
python scripts/appendix_generator.py

# Genera datos para el Apéndice B (L=32)
python scripts/advanced_analysis.py

# Genera datos para el Apéndice C (análisis modular)
python scripts/modular_analysis.py
```

Los resultados se guardarán automáticamente en `data/` y `figures/`.

### 5. Compilar el PDF

```bash
cd paper
pdflatex main.tex
pdflatex main.tex  # Ejecutar dos veces para resolver referencias
```

O usando `latexmk`:

```bash
cd paper
latexmk -pdf main.tex
```

El PDF compilado estará disponible en `paper/main.pdf`.

---

## 🔬 Metodología

### Dualidad Binaria

Para cada trayectoria de Collatz $(N_k)$ y longitud fija de bits $L$, definimos la **secuencia espejo**:

$$M_k = \neg_L(N_k) = (2^L - 1) - N_k$$

donde $\neg_L$ invierte los bits de la representación binaria de longitud $L$.

### Evolución de Patrones

Analizamos cómo cambian los patrones binarios a lo largo de la trayectoria, midiendo:

- **Entropía binaria** $H(n)$
- **Peso de Hamming** (número de bits 1)
- **Distancia Hamming** entre $N_k$ y $M_k$

### Análisis Modular

Aplicamos el test de **Kruskal-Wallis** para evaluar si el tiempo de parada depende de la clase residual $n_0 \bmod m$ para $m \in \{2, 3, 4, 6, 8, 12\}$.

---

## 📊 Resultados Computacionales Destacados

| Métrica | Valor |
|---------|-------|
| Trayectorias analizadas | $10^5$ |
| Longitud máxima estudiada | $L = 32$ |
| Correlación $\max(N_k)$ vs $\min(M_k)$ | $-1.000$ (exacto) |
| Sincronía de extremos | 100% |
| $R^2$ del modelo Random Forest | $\approx 0.48$ |
| Proporción media de pasos pares | 0.6845 (vs 0.6131 teórico) |

---

## 🛠️ Herramientas Utilizadas

- **Python 3.10+**: Lenguaje principal para análisis
- **NumPy**: Computación numérica
- **Pandas**: Manipulación de datos
- **Matplotlib**: Visualización
- **SciPy**: Tests estadísticos
- **scikit-learn**: Modelos de Machine Learning
- **LaTeX (pdfLaTeX)**: Composición del documento

---

## 📚 Cómo Citar este Trabajo

Si utilizas este trabajo en tu investigación, por favor cita:

```bibtex
@misc{DualidadBinaria2026,
  author = {Cristian F. F. and Grok (xAI Assistant)},
  title = {Dualidad Binaria y Evolución de Patrones en la Conjetura de Collatz: Un Marco Exploratorio},
  year = {2026},
  month = {May},
  doi = {10.5281/zenodo.20458849},
  url = {https://github.com/MrVenomSnake/Dualidad-Binaria},
  note = {Preprint exploratorio}
}
```

---

## 🤝 Contribuciones y Feedback

Este es un trabajo **exploratorio** y toda retroalimentación es bienvenida:

- 🐛 **¿Encontraste un error?** Abre un [Issue](https://github.com/MrVenomSnake/Dualidad-Binaria/issues)
- 💡 **¿Tienes sugerencias?** Inicia una [Discusión](https://github.com/MrVenomSnake/Dualidad-Binaria/discussions)
- 🔀 **¿Quieres contribuir?** Haz un Pull Request

---

## 📜 Licencia

Este trabajo está bajo la **Licencia Creative Commons Attribution 4.0 International (CC BY 4.0)**.

Eres libre de:
- ✅ Compartir — copiar y redistribuir el material
- ✅ Adaptar — remezclar, transformar y construir sobre el material
- ✅ Uso comercial permitido

Bajo la condición de:
- 📝 **Atribución** — Dar crédito apropiado y enlazar a la licencia

Ver [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

A la comunidad matemática por mantener viva la curiosidad sobre problemas abiertos elementales. Al equipo de xAI por el soporte técnico a través de Grok.

---

## 📧 Contacto

Para preguntas o colaboraciones:
- **GitHub Issues**: [MrVenomSnake/Dualidad-Binaria/issues](https://github.com/MrVenomSnake/Dualidad-Binaria/issues)
- **Zenodo**: [10.5281/zenodo.20458849](https://doi.org/10.5281/zenodo.20458849)

---

<p align="center">
  <sub>Hecho con ❤️ y mucho café ☕ | Última actualización: Mayo 2026</sub>
</p>

# Dualidad Binaria y Evolución de Patrones en la Conjetura de Collatz

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20458849.svg)](https://doi.org/10.5281/zenodo.20458849)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

---

## Resumen

Este repositorio contiene el código fuente, datos y artículo del estudio
**"Dualidad Binaria y Evolución de Patrones en la Conjetura de Collatz: Un Marco Exploratorio"**.

El trabajo introduce un **marco algebraico novedoso** para analizar la Conjetura de Collatz
mediante **dualidad binaria**: cada trayectoria de Collatz $N_k$ tiene una "secuencia espejo"
$M_k$ generada por inversión de bits con longitud fija $L$.

### Hallazgos clave

- **Teorema Principal**: Cuando $N_K = 1$, entonces $M_K = 2^L - 2$ (demostrado formalmente).
- **Patrones Alternantes**: Los números $(2^{2m}-1)/3$ alcanzan una potencia de 2 en un único paso.
- **Identidad de Conservación**: $N_k + M_k = 2^L - 1$ (mientras no haya truncamiento).
- **Estructura Modular**: El tiempo de parada depende de $n_0 \bmod 2^k$ ($p < 10^{-200}$),
  pero **no** de $n_0 \bmod 3$ ($p = 0.552$).
- **ML Exploratorio**: Random Forest alcanza $R^2 \approx 0.48$ prediciendo el tiempo de parada.

> **Nota importante:** Este es un trabajo exploratorio. No constituye una demostración
> de la Conjetura de Collatz.

---

## Estructura del Repositorio

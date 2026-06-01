#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
collatz_advanced_analysis.py
============================
Análisis avanzado para el Apéndice B de la Dualidad Binaria Collatz.

Incluye:
1. Generación de datos para L=32, n=1..10^5.
2. Verificación de sanidad (Pearson, regresión) -> DEBE dar tautología perfecta.
3. Análisis NO trivial: ¿pico de N y valle de M en mismo paso?
4. ML exploratorio (Random Forest) para predecir pasos_hasta_1.

Requisitos: numpy, pandas, matplotlib, scikit-learn, tqdm (opcional).
Uso: python collatz_advanced_analysis.py
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(x, **k): return x

try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import r2_score, mean_absolute_error
    from scipy.stats import pearsonr, linregress
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("[Aviso] Instala scikit-learn y scipy para ML/estadística: pip install scikit-learn scipy")

# ============================================================
# CORE
# ============================================================
def collatz_step(n): return n // 2 if n % 2 == 0 else 3 * n + 1

def analyze(n0, L, max_steps=100000):
    """Retorna dict con extremos Y los pasos donde ocurren."""
    mask = (1 << L) - 1
    N = n0
    max_N, max_N_step = N, 0
    min_M, min_M_step = mask ^ (N & mask), 0
    truncated = False
    k = 0
    while N != 1 and k < max_steps:
        N = collatz_step(N)
        k += 1
        if N > mask:
            truncated = True
        M = mask ^ (N & mask)
        if N > max_N:
            max_N, max_N_step = N, k
        if M < min_M:
            min_M, min_M_step = M, k
    return {
        'n0': n0, 'L': L, 'steps_to_1': k if N == 1 else -1,
        'max_N': max_N, 'max_N_step': max_N_step,
        'min_M': min_M, 'min_M_step': min_M_step,
        'peaks_aligned': (max_N_step == min_M_step),  # ¿mismo paso?
        'truncated': truncated, 'converged': (N == 1)
    }

# ============================================================
# GENERACIÓN
# ============================================================
def generate(n_start, n_end, L, csv_path):
    if csv_path.exists():
        print(f"[Info] Cargando datos existentes: {csv_path}")
        return pd.read_csv(csv_path)
    print(f"[Gen] n=[{n_start},{n_end}), L={L} ...")
    rows = [analyze(n, L) for n in tqdm(range(n_start, n_end))]
    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)
    print(f"[Gen] Guardado: {csv_path} ({len(df)} filas)")
    return df

# ============================================================
# ANÁLISIS 1: SANIDAD (TAUTOLOGÍA ESPERADA)
# ============================================================
def sanity_check(df, L):
    print("\n" + "="*60)
    print("ANÁLISIS 1: VERIFICACIÓN DE SANIDAD (TAUTOLOGÍA)")
    print("="*60)
    d = df[df['converged'] & ~df['truncated']]  # sin truncamiento
    if len(d) < 2:
        print("  No hay suficientes casos sin truncamiento.")
        return
    r, p = pearsonr(d['max_N'], d['min_M'])
    slope, intercept, rval, _, _ = linregress(d['max_N'], d['min_M'])
    print(f"  Casos sin truncamiento: {len(d):,}")
    print(f"  Pearson(max_N, min_M)  = {r:.10f}   (esperado: -1.0 EXACTO)")
    print(f"  Regresión: min_M = {slope:.6f}*max_N + {intercept:.2f}")
    print(f"             pendiente esperada = -1, intercepto esperado = {2**L-1}")
    print(f"  R^2 = {rval**2:.10f}   (esperado: 1.0 EXACTO)")
    print("\n  >>> INTERPRETACIÓN: Esto es una IDENTIDAD, no un hallazgo.")
    print("  >>> min(M) = (2^L-1) - max(N) por definición. NO citar como descubrimiento.")
    # Verificación bit a bit
    d2 = d.copy()
    d2['suma'] = d2['max_N'] + d2['min_M']
    ok = (d2['suma'] == (2**L - 1)).all()
    print(f"  Verificación max_N + min_M == 2^L-1 en TODOS los casos: {ok}")

# ============================================================
# ANÁLISIS 2: NO TRIVIAL - ALINEAMIENTO TEMPORAL
# ============================================================
def alignment_analysis(df):
    print("\n" + "="*60)
    print("ANÁLISIS 2: ¿PICO DE N Y VALLE DE M EN EL MISMO PASO? (NO trivial)")
    print("="*60)
    d = df[df['converged']]
    aligned = d['peaks_aligned'].sum()
    total = len(d)
    print(f"  Trayectorias donde max_N_step == min_M_step: {aligned:,}/{total:,} "
          f"({100*aligned/total:.2f}%)")
    print("\n  >>> INTERPRETACIÓN: Sin truncamiento, M_k=(2^L-1)-N_k es MONÓTONA")
    print("  >>> decreciente en N_k, por lo que el valle de M SIEMPRE coincide con")
    print("  >>> el pico de N. Si <100%, indica casos con TRUNCAMIENTO (N_k>=2^L).")
    truncated = d['truncated'].sum()
    print(f"  Trayectorias con truncamiento (N_k >= 2^L): {truncated:,} "
          f"({100*truncated/total:.2f}%)")

# ============================================================
# ANÁLISIS 3: ML EXPLORATORIO (HONESTO)
# ============================================================
def ml_explore(df, save_path):
    if not HAS_SKLEARN:
        print("\n[ML] Omitido (falta scikit-learn).")
        return
    print("\n" + "="*60)
    print("ANÁLISIS 3: ML EXPLORATORIO - Predecir pasos_hasta_1")
    print("="*60)
    d = df[df['converged']].copy()
    # NOTA: min_M es redundante con max_N. Usamos features genuinas.
    d['log_max_N'] = np.log2(d['max_N'].clip(lower=1))
    d['log_n0'] = np.log2(d['n0'].clip(lower=1))
    d['n0_mod3'] = d['n0'] % 3
    d['n0_mod4'] = d['n0'] % 4
    features = ['n0', 'log_n0', 'max_N', 'log_max_N', 'n0_mod3', 'n0_mod4']
    X = d[features].values
    y = d['steps_to_1'].values
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42)
    rf = RandomForestRegressor(n_estimators=100, max_depth=15,
                                n_jobs=-1, random_state=42)
    rf.fit(Xtr, ytr)
    pred = rf.predict(Xte)
    r2 = r2_score(yte, pred)
    mae = mean_absolute_error(yte, pred)
    print(f"  Features: {features}")
    print(f"  R^2 (test)  = {r2:.4f}")
    print(f"  MAE (test)  = {mae:.2f} pasos")
    print("\n  Importancia de variables:")
    for f, imp in sorted(zip(features, rf.feature_importances_),
                          key=lambda t: -t[1]):
        print(f"    {f:12s}: {imp:.4f}")
    print("\n  >>> INTERPRETACIÓN HONESTA:")
    print("  >>> Un R^2 alto NO 'resuelve' Collatz. log2(max_N) es el predictor")
    print("  >>> dominante porque pasos ~ correlaciona con altura alcanzada (obvio).")
    print("  >>> Lo interesante sería si los mod3/mod4 aportan señal estructural.")

    # Gráfico pred vs real
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(yte, pred, s=8, alpha=0.3, c='steelblue')
    lim = [min(yte.min(), pred.min()), max(yte.max(), pred.max())]
    ax.plot(lim, lim, 'r--', label='Predicción perfecta')
    ax.set_xlabel('Pasos reales hasta 1')
    ax.set_ylabel('Pasos predichos (Random Forest)')
    ax.set_title(f'ML Exploratorio: R²={r2:.3f}, MAE={mae:.1f}')
    ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\n  [Plot] Guardado: {save_path}")
    plt.close()

# ============================================================
# MAIN
# ============================================================
def main():
    OUT = Path("./output_apendice_B")
    OUT.mkdir(exist_ok=True)
    L = 32
    N_START, N_END = 1, 100001   # 1..10^5

    csv = OUT / f"datos_L{L}_n{N_END-1}.csv"
    df = generate(N_START, N_END, L, csv)

    print("\n" + "="*60)
    print(f"RESUMEN: {len(df):,} trayectorias, L={L}")
    print("="*60)
    print(f"  Convergieron: {df['converged'].sum():,}")
    print(f"  Max global de max(N): {df['max_N'].max():,}")
    print(f"  Pasos máximos: {df[df['converged']]['steps_to_1'].max()}")
    print(f"  Con truncamiento (N>=2^{L}): {df['truncated'].sum():,}")

    sanity_check(df, L)
    alignment_analysis(df)
    ml_explore(df, OUT / "fig_ml_pred_vs_real.png")

    print("\n[FIN] Archivos en:", OUT)

if __name__ == '__main__':
    main()
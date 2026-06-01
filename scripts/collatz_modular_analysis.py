#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
collatz_modular_analysis.py - Versión Corregida
===============================================
Análisis modular profundo de Collatz + Dualidad Binaria.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    from scipy.stats import kruskal
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    print("Instala scipy para tests estadísticos: pip install scipy")

# ====================== CORE ======================
def collatz_step(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

def full_analysis(n0, L=32, max_steps=100000):
    mask = (1 << L) - 1
    N = n0
    max_N = N
    k = 0
    even_steps = 0
    odd_steps = 0
    while N != 1 and k < max_steps:
        if N % 2 == 0:
            even_steps += 1
        else:
            odd_steps += 1
        N = collatz_step(N)
        k += 1
        if N > max_N:
            max_N = N
    return {
        'n0': n0,
        'steps_to_1': k if N == 1 else -1,
        'max_N': max_N,
        'log2_max_N': np.log2(max_N) if max_N > 0 else 0,
        'even_steps': even_steps,
        'odd_steps': odd_steps,
        'even_ratio': even_steps / k if k > 0 else 0,
        'n0_mod2': n0 % 2,
        'n0_mod3': n0 % 3,
        'n0_mod4': n0 % 4,
        'n0_mod6': n0 % 6,
        'n0_mod8': n0 % 8,
        'n0_mod12': n0 % 12,
        'n0_mod16': n0 % 16,
        'n0_mod24': n0 % 24,
        'converged': (N == 1)
    }

# ====================== GENERACIÓN ======================
def generate_modular_data(n_end, csv_path):
    if csv_path.exists():
        print(f"[Info] Cargando datos existentes: {csv_path}")
        return pd.read_csv(csv_path)

    print(f"[Gen] Analizando n=1..{n_end-1}...")
    try:
        from tqdm import tqdm
        rows = [full_analysis(n) for n in tqdm(range(1, n_end))]
    except ImportError:
        rows = [full_analysis(n) for n in range(1, n_end)]

    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)
    print(f"[Gen] Guardado: {csv_path} ({len(df)} filas)")
    return df

# ====================== GRÁFICOS CORREGIDOS ======================
def plot_steps_by_modclass(df, mod_col, save_dir):
    m = int(mod_col.split('mod')[1])
    groups = df.groupby(mod_col)['steps_to_1']
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Boxplot (corregido: tick_labels en vez de labels)
    ax = axes[0]
    data_boxes = [g.values for _, g in groups]
    labels = [str(k) for k, _ in groups]
    bp = ax.boxplot(data_boxes, tick_labels=labels, patch_artist=True,
                    showfliers=False, medianprops=dict(color='red', linewidth=2))
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
    ax.set_xlabel(f'$n_0 \\,(\\mathrm{{mod}}\\, {m})$', fontsize=12)
    ax.set_ylabel('Pasos hasta 1', fontsize=12)
    ax.set_title(f'Distribución de Tiempo de Parada por $n_0 \\,(\\mathrm{{mod}}\\, {m})$',
                 fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    # Media vs Mediana
    ax = axes[1]
    stats = groups.agg(['mean', 'median', 'std', 'count']).reset_index()
    x = range(len(stats))
    ax.bar([i-0.15 for i in x], stats['mean'], 0.3, label='Media', color='steelblue', alpha=0.8)
    ax.bar([i+0.15 for i in x], stats['median'], 0.3, label='Mediana', color='coral', alpha=0.8)
    ax.set_xticks(list(x))
    ax.set_xticklabels(stats[mod_col].astype(int))
    ax.set_xlabel(f'$n_0 \\,(\\mathrm{{mod}}\\, {m})$', fontsize=12)
    ax.set_ylabel('Pasos hasta 1', fontsize=12)
    ax.set_title(f'Media vs Mediana por Clase Modular (mod {m})', fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    path = save_dir / f"fig_steps_mod{m}.png"
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[Plot] Guardado: {path}")
    return stats

# ====================== TESTS ESTADÍSTICOS ======================
def modular_stat_tests(df, mod_col):
    m = int(mod_col.split('mod')[1])
    groups = [g['steps_to_1'].values for _, g in df.groupby(mod_col)]
    
    print(f"\n  --- Test Kruskal-Wallis para n mod {m} ---")
    if not HAS_SCIPY:
        print("  [Omitido] scipy no instalado.")
        return {'mod': m, 'H': 0, 'p': 1.0}
    
    stat, p = kruskal(*groups)
    print(f"  H-statistic = {stat:.4f}")
    print(f"  p-value     = {p:.2e}")
    
    if p < 0.001:
        print("  >>> ALTAMENTE SIGNIFICATIVO (p < 0.001)")
    elif p < 0.05:
        print("  >>> Significativo (p < 0.05)")
    else:
        print("  >>> No significativo")
    return {'mod': m, 'H': stat, 'p': p}

# ====================== RATIO PAR/IMPAR ======================
def plot_even_ratio(df, save_dir):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    theoretical = np.log2(3)/(1 + np.log2(3))
    
    ax = axes[0]
    ax.hist(df['even_ratio'], bins=80, color='steelblue', alpha=0.85, edgecolor='white')
    ax.axvline(theoretical, color='red', linestyle='--', linewidth=2.5,
               label=f'Teórico ≈ {theoretical:.4f}')
    ax.set_xlabel('Fracción de pasos pares', fontsize=11)
    ax.set_ylabel('Frecuencia', fontsize=11)
    ax.set_title('Distribución del Ratio Par/Total', fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)

    ax = axes[1]
    sample = df.sample(min(8000, len(df)), random_state=42)
    ax.scatter(sample['even_ratio'], sample['steps_to_1'], s=6, alpha=0.4, c='teal')
    ax.axvline(theoretical, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.set_xlabel('Fracción de pasos pares', fontsize=11)
    ax.set_ylabel('Pasos hasta 1', fontsize=11)
    ax.set_title('Ratio Par vs Tiempo de Parada', fontsize=12, fontweight='bold')
    ax.grid(alpha=0.3)

    plt.tight_layout()
    path = save_dir / "fig_even_ratio_analysis.png"
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[Plot] Guardado: {path}")

# ====================== MAIN ======================
def main():
    OUT = Path("./output_modular")
    OUT.mkdir(exist_ok=True)

    N_END = 100001
    csv = OUT / "datos_modulares.csv"
    df = generate_modular_data(N_END, csv)
    df = df[df['converged']].copy()

    print(f"\n{'='*70}")
    print(f"RESUMEN - {len(df):,} trayectorias")
    print(f"{'='*70}")
    print(f"  Media pasos     : {df['steps_to_1'].mean():.2f}")
    print(f"  Mediana         : {df['steps_to_1'].median():.0f}")
    print(f"  Máx pasos       : {df['steps_to_1'].max()}")
    print(f"  even_ratio medio: {df['even_ratio'].mean():.4f}  (teórico = 0.6131)")

    mods = ['n0_mod2', 'n0_mod3', 'n0_mod4', 'n0_mod6', 'n0_mod8', 'n0_mod12']

    print(f"\n{'='*70}")
    print("ANÁLISIS MODULAR")
    print(f"{'='*70}")

    test_results = []
    for mod_col in mods:
        stats = plot_steps_by_modclass(df, mod_col, OUT)
        test = modular_stat_tests(df, mod_col)
        test_results.append(test)

    plot_even_ratio(df, OUT)

    print(f"\n[FIN] Todos los gráficos y análisis guardados en: {OUT}")
    print("Puedes ahora añadir el Apéndice C al artículo.")

if __name__ == '__main__':
    main()
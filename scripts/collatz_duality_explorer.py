#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
collatz_duality_explorer.py
---------------------------
Marco computacional para la Dualidad Binaria en la Conjetura de Collatz.

Funciones principales:
- Generar la trayectoria estándar de Collatz (N_k).
- Generar la trayectoria espejo M_k = NOT_L(N_k) con longitud fija de bits L.
- Verificar teorema principal: cuando N_k=1, M_k = 2^L - 2.
- Calcular métricas informacionales (entropía binaria, peso de Hamming, distancia Hamming).
- Visualizar evolución, retrato de fase y métricas (matplotlib).
- Modo batch para barrido de números y generación de CSV con estadísticas.

Requisitos: numpy, matplotlib, pandas
Instalación: pip install numpy matplotlib pandas
"""

import argparse
import sys
import math
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.collections import LineCollection

# ---------------------------------------------------------------------------
# 1. Funciones de Collatz y transformación binaria
# ---------------------------------------------------------------------------

def collatz_step(n: int) -> int:
    """Un paso de la función de Collatz C(n)."""
    return n // 2 if (n & 1) == 0 else 3 * n + 1


def collatz_trajectory(n: int, max_steps: int = 10000) -> List[int]:
    """Genera la trayectoria completa hasta 1 o max_steps (detecta ciclos)."""
    traj = [n]
    seen = {n: 0}
    for step in range(1, max_steps + 1):
        n = collatz_step(n)
        traj.append(n)
        if n == 1:
            break
        if n in seen:  # ciclo que no incluye 1
            break
        seen[n] = step
    return traj


def bit_not_fixed_L(x: int, L: int) -> int:
    """Invierte los bits de x en una longitud fija L (trunca a L bits menos significativos)."""
    if L <= 0:
        raise ValueError("L must be >= 1")
    mask = (1 << L) - 1
    return mask ^ (x & mask)


def mirror_trajectory(N_traj: List[int], L: int) -> List[int]:
    """Aplica la inversión de bits L a cada elemento de N_traj."""
    return [bit_not_fixed_L(n, L) for n in N_traj]

# ---------------------------------------------------------------------------
# 2. Métricas informacionales
# ---------------------------------------------------------------------------

def hamming_weight(x: int) -> int:
    return x.bit_count()

def hamming_distance(x: int, y: int, L: int) -> int:
    mask = (1 << L) - 1
    return hamming_weight((x ^ y) & mask)

def binary_entropy(x: int, L: int) -> float:
    if L == 0:
        return 0.0
    ones = hamming_weight(x & ((1 << L) - 1))
    p = ones / L
    if p == 0.0 or p == 1.0:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

@dataclass
class StepMetrics:
    k: int
    N: int
    M: int
    H_N: float      # Entropía N
    H_M: float      # Entropía M
    H_sum: float    # H_N + H_M
    H_diff: float   # |H_N - H_M|
    hw_N: int       # Hamming weight N
    hw_M: int       # Hamming weight M
    ham_dist: int    # Distancia Hamming(N, M)
    N_norm: float   # N / 2^L
    M_norm: float   # M / 2^L

def compute_metrics_series(N_traj: List[int], M_traj: List[int], L: int) -> List[StepMetrics]:
    max_val = 1 << L
    series = []
    for k, (n, m) in enumerate(zip(N_traj, M_traj)):
        h_n = binary_entropy(n, L)
        h_m = binary_entropy(m, L)
        series.append(
            StepMetrics(
                k=k,
                N=n,
                M=m,
                H_N=h_n,
                H_M=h_m,
                H_sum=h_n + h_m,
                H_diff=abs(h_n - h_m),
                hw_N=hamming_weight(n),
                hw_M=hamming_weight(m),
                ham_dist=hamming_distance(n, m, L),
                N_norm=n / max_val,
                M_norm=m / max_val,
            )
        )
    return series

def generate_appendix(L: int = 20, n_max: int = 10000, max_steps: int = 5000,
                      output_csv: Path = Path('appendix_table.csv'),
                      plot_path: Path = Path('appendix_scatter.png')) -> None:
    """
    Genera tabla de max(N_k) vs min(M_k) para n=1..n_max y L bits,
    y gráfico de |N_k - midpoint| vs |M_k - midpoint| para visualizar anti‑correlación.
    """
    midpoint = (2 ** L - 1) / 2
    rows = []
    diffs_N = []
    diffs_M = []
    for n in range(1, n_max + 1):
        N_traj = collatz_trajectory(n, max_steps)
        M_traj = mirror_trajectory(N_traj, L)
        rows.append({'n': n, 'max_N': max(N_traj), 'min_M': min(M_traj)})
        for Nk, Mk in zip(N_traj, M_traj):
            diffs_N.append(abs(Nk - midpoint))
            diffs_M.append(abs(Mk - midpoint))
    # Guardar tabla
    df_tbl = pd.DataFrame(rows)
    df_tbl.to_csv(output_csv, index=False, float_format='%.6f')
    print(f"[Appendix] Tabla guardada en {output_csv}")
    # Graficar dispersión
    plt.figure(figsize=(6, 6))
    plt.scatter(diffs_N, diffs_M, s=5, alpha=0.4, color='tab:blue')
    plt.xlabel('|N_k - midpoint|')
    plt.ylabel('|M_k - midpoint|')
    plt.title(f'Anti‑correlación N vs M (L={L})')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"[Appendix] Gráfico guardado en {plot_path}")
    plt.close()

# ---------------------------------------------------------------------------
# 3. Verificación del teorema principal
# ---------------------------------------------------------------------------

def verify_main_theorem(N_traj: List[int], M_traj: List[int], L: int) -> Dict:
    target_M = (1 << L) - 2
    for k, (n, m) in enumerate(zip(N_traj, M_traj)):
        if n == 1:
            return {
                "theorem_holds": m == target_M,
                "step_k": k,
                "N_k": n,
                "M_k_observed": m,
                "M_k_expected": target_M,
                "L": L,
                "initial_n": N_traj[0],
            }
    return {
        "theorem_holds": False,
        "error": "N never reached 1 within generated trajectory",
        "final_N": N_traj[-1],
        "steps": len(N_traj),
        "L": L,
        "initial_n": N_traj[0],
    }

# ---------------------------------------------------------------------------
# 4. Visualizaciones (estilo paper)
# ---------------------------------------------------------------------------

def _setup_axes(ax, title, xlabel, ylabel, logy=False):
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    if logy:
        ax.set_yscale('log')
        ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

COLORS = {
    'N': '#0072B2',
    'M': '#D55E00',
    'sum': '#009E73',
    'diff': '#CC79A7',
}

def plot_dual_evolution(metrics: List[StepMetrics], L: int, n0: int, save_path: Path | None = None):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    k_vals = [m.k for m in metrics]
    N_vals = [m.N for m in metrics]
    M_vals = [m.M for m in metrics]
    ax.plot(k_vals, N_vals, 'o-', color=COLORS['N'], label='N_k (Collatz)', markersize=3, linewidth=1.5)
    ax.plot(k_vals, M_vals, 's-', color=COLORS['M'], label='M_k = NOT_L(N_k)', markersize=3, linewidth=1.5)
    try:
        k_th = next(i for i, m in enumerate(metrics) if m.N == 1)
        ax.axvline(k_th, color='gray', linestyle=':', linewidth=1.5)
        ax.plot(k_th, metrics[k_th].M, 'o', ms=10, mfc='none', mec='red', mew=2,
                label=f'Teorema: N=1 → M=2^{L}-2={2**L-2}')
    except StopIteration:
        pass
    _setup_axes(ax, f'Dualidad Binaria (n0={n0}, L={L})', 'Paso k', 'Valor (escala log)', logy=True)
    ax.legend(frameon=True, fancybox=True, framealpha=0.9, fontsize=9)
    fig.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[Guardado] {save_path}")
    plt.show()

def plot_phase_portrait(metrics: List[StepMetrics], L: int, n0: int, save_path: Path | None = None):
    fig, ax = plt.subplots(figsize=(6, 6))
    x = [m.N_norm for m in metrics]
    y = [m.M_norm for m in metrics]
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segs = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segs, cmap='viridis', norm=plt.Normalize(0, len(metrics)))
    lc.set_array(np.arange(len(metrics)))
    lc.set_linewidth(1.5)
    ax.add_collection(lc)
    fig.colorbar(lc, ax=ax, label='Paso k')
    ax.plot(x[0], y[0], 'o', ms=10, color=COLORS['N'], label='Inicio')
    try:
        k_th = next(i for i, m in enumerate(metrics) if m.N == 1)
        ax.plot(x[k_th], y[k_th], 's', ms=10, color=COLORS['M'], label='Fin Teorema')
    except StopIteration:
        pass
    ax.plot([0, 1], [1, 0], 'k--', alpha=0.3, label='Anti-diagonal')
    ax.plot([0, 1], [0, 1], 'k:', alpha=0.2)
    _setup_axes(ax, f'Retrato de fase (L={L})', r'N_k / 2^L', r'M_k / 2^L')
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.set_aspect('equal')
    ax.legend(fontsize=9, loc='upper right')
    fig.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[Guardado] {save_path}")
    plt.show()

def plot_complexity_metrics(metrics: List[StepMetrics], L: int, n0: int, save_path: Path | None = None):
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), sharex=True)
    k = [m.k for m in metrics]
    # Entropías
    ax = axes[0, 0]
    ax.plot(k, [m.H_N for m in metrics], color=COLORS['N'], label='H(N)')
    ax.plot(k, [m.H_M for m in metrics], color=COLORS['M'], label='H(M)')
    ax.plot(k, [m.H_sum for m in metrics], color=COLORS['sum'], linestyle='--', label='H(N)+H(M)')
    _setup_axes(ax, 'Entropía binaria', 'Paso k', 'Entropía')
    ax.set_ylim(-0.05, 1.05)
    ax.legend(fontsize=9)
    # Diferencia entropía
    ax = axes[0, 1]
    ax.plot(k, [m.H_diff for m in metrics], color=COLORS['diff'])
    ax.fill_between(k, 0, [m.H_diff for m in metrics], color=COLORS['diff'], alpha=0.1)
    _setup_axes(ax, 'Desbalance informacional', 'Paso k', '|H(N)-H(M)|')
    ax.legend(fontsize=9)
    # Peso Hamming
    ax = axes[1, 0]
    ax.plot(k, [m.hw_N for m in metrics], color=COLORS['N'], label='w_H(N)')
    ax.plot(k, [m.hw_M for m in metrics], color=COLORS['M'], label='w_H(M)')
    ax.axhline(L/2, color='gray', ls=':', alpha=0.5, label='L/2 esperado')
    _setup_axes(ax, 'Peso de Hamming', 'Paso k', 'Bits a 1')
    ax.legend(fontsize=9)
    # Distancia Hamming
    ax = axes[1, 1]
    ax.plot(k, [m.ham_dist for m in metrics], color='purple')
    ax.axhline(L/2, color='gray', ls=':', alpha=0.5, label='L/2 esperado')
    _setup_axes(ax, 'Distancia Hamming N↔M', 'Paso k', 'Bits diferentes')
    ax.legend(fontsize=9)
    fig.suptitle(f'Métricas de complejidad (n0={n0}, L={L})', fontsize=12, fontweight='bold')
    fig.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[Guardado] {save_path}")
    plt.show()

# ---------------------------------------------------------------------------
# 5. Modo batch
# ---------------------------------------------------------------------------
@dataclass
class BatchResult:
    n0: int
    L: int
    steps_to_1: int
    max_N: int
    max_M: int
    theorem_ok: bool
    avg_H_N: float
    avg_H_M: float
    avg_H_diff: float
    avg_ham_dist: float
    final_M_at_N1: int

def run_batch(n_range: range, L: int, max_steps: int, output_csv: Path) -> List[BatchResult]:
    results = []
    print(f"[Batch] Ejecutando n={n_range.start}..{n_range.stop-1}, L={L}")
    for n0 in n_range:
        N_traj = collatz_trajectory(n0, max_steps)
        M_traj = mirror_trajectory(N_traj, L)
        metrics = compute_metrics_series(N_traj, M_traj, L)
        verification = verify_main_theorem(N_traj, M_traj, L)
        avg_H_N = np.mean([m.H_N for m in metrics])
        avg_H_M = np.mean([m.H_M for m in metrics])
        avg_H_diff = np.mean([m.H_diff for m in metrics])
        avg_ham = np.mean([m.ham_dist for m in metrics])
        res = BatchResult(
            n0=n0,
            L=L,
            steps_to_1=len(N_traj)-1 if N_traj[-1] == 1 else -1,
            max_N=max(N_traj),
            max_M=max(M_traj),
            theorem_ok=verification.get('theorem_holds', False),
            avg_H_N=avg_H_N,
            avg_H_M=avg_H_M,
            avg_H_diff=avg_H_diff,
            avg_ham_dist=avg_ham,
            final_M_at_N1=verification.get('M_k_observed', -1),
        )
        results.append(res)
        if n0 % 100 == 0:
            print(f"  ... n={n0} procesado")
    df = pd.DataFrame([asdict(r) for r in results])
    df.to_csv(output_csv, index=False, float_format='%.6f')
    print(f"[Batch] CSV guardado en {output_csv}")
    return results

# ---------------------------------------------------------------------------
# 6. CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description='Explorador Dualidad Binaria Collatz (teorema, métricas, visualizaciones, batch)',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest='cmd', required=True)

    # run subcommand
    run_p = subparsers.add_parser('run', help='Analiza un n0 específico y genera visualizaciones')
    run_p.add_argument('n0', type=int, help='Semilla inicial > 0')
    run_p.add_argument('-L', '--bits', type=int, default=20, help='Longitud fija L en bits')
    run_p.add_argument('--max-steps', type=int, default=5000, help='Límite de pasos de Collatz')
    run_p.add_argument('--no-plots', action='store_true', help='Solo texto, sin abrir figuras')
    run_p.add_argument('--save-plots', type=Path, help='Directorio donde guardar PNGs (prefijo n_L)')
    run_p.add_argument('--save-metrics', type=Path, help='CSV con métricas paso a paso')

    # batch subcommand
    batch_p = subparsers.add_parser('batch', help='Ejecuta un barrido de varios n y exporta CSV')
    batch_p.add_argument('start', type=int, help='Valor inicial (incluido)')
    batch_p.add_argument('end', type=int, help='Valor final (excluido)')
    batch_p.add_argument('-L', '--bits', type=int, default=20, help='Longitud L')
    batch_p.add_argument('--max-steps', type=int, default=5000, help='Límite de pasos')
    batch_p.add_argument('-o', '--output', type=Path, default=Path('batch_results.csv'), help='Archivo CSV de salida')

    # test subcommand
    subparsers.add_parser('appendix', help='Genera tabla y gráfico del apéndice computacional')
    subparsers.add_parser('test', help='Ejecuta pruebas internas de consistencia')

    args = parser.parse_args()

    if args.cmd == 'test':
        # Simple sanity checks
        assert bit_not_fixed_L(0, 4) == 0b1111
        assert bit_not_fixed_L(5, 4) == 0b1010
        print('Tests básicos OK')
        sys.exit(0)

    if args.cmd == 'run':
        n0, L = args.n0, args.bits
        if n0 <= 0:
            sys.exit('n0 debe ser > 0')
        if L <= 0:
            sys.exit('L debe ser >= 1')
        print(f"[Run] n0={n0}, L={L}")
        N_traj = collatz_trajectory(n0, args.max_steps)
        M_traj = mirror_trajectory(N_traj, L)
        metrics = compute_metrics_series(N_traj, M_traj, L)
        verification = verify_main_theorem(N_traj, M_traj, L)
        print('\nVerificación del teorema principal:')
        print(f"  Paso donde N=1: {verification.get('step_k', 'N/A')}")
        print(f"  M observado: {verification.get('M_k_observed', 'N/A')}")
        print(f"  M esperado : {verification.get('M_k_expected', 2**L-2)}")
        print('  [OK] Teorema cumplido' if verification.get('theorem_holds') else '  [FAIL] Teorema falló')
        print('\nResumen de trayectoria:')
        print(f"  Pasos totales hasta 1: {len(N_traj)-1 if N_traj[-1]==1 else 'No alcanza 1'}")
        print(f"  Máximo N: {max(N_traj)} (bits: {max(N_traj).bit_length()})")
        print(f"  Máximo M: {max(M_traj)}")
        print(f"  Entropía media N: {np.mean([m.H_N for m in metrics]):.4f}, M: {np.mean([m.H_M for m in metrics]):.4f}")
        print(f"  Distancia Hamming media: {np.mean([m.ham_dist for m in metrics]):.2f} / {L}")
        if args.save_metrics:
            df = pd.DataFrame([asdict(m) for m in metrics])
            df.to_csv(args.save_metrics, index=False, float_format='%.6f')
            print(f"[Guardado] Métricas CSV -> {args.save_metrics}")
        if not args.no_plots:
            save_dir = args.save_plots
            if save_dir:
                save_dir.mkdir(parents=True, exist_ok=True)
                prefix = save_dir / f"n{n0}_L{L}"
                p1, p2, p3 = f"{prefix}_evol.png", f"{prefix}_phase.png", f"{prefix}_metrics.png"
            else:
                p1 = p2 = p3 = None
            print('\nGenerando visualizaciones...')
            plot_dual_evolution(metrics, L, n0, Path(p1) if p1 else None)
            plot_phase_portrait(metrics, L, n0, Path(p2) if p2 else None)
            plot_complexity_metrics(metrics, L, n0, Path(p3) if p3 else None)
        sys.exit(0)

    # Apéndice computacional
    if args.cmd == 'appendix':
        generate_appendix()
        sys.exit(0)

    if args.cmd == 'batch':
        n_range = range(args.start, args.end)
        run_batch(n_range, args.bits, args.max_steps, args.output)
        sys.exit(0)

if __name__ == '__main__':
    main()

import matplotlib.pyplot as plt
import numpy as np
from scripts.collatz_entropy_analysis import collatz_steps
import random

# Semilla para reproducibilidad
random.seed(42)

def plot_entropy_evolution(n):
    """Grafica la evolución de la entropía de un número."""
    seq, entropy_hist, v2_hist = collatz_steps(n, max_steps=2000)
    
    plt.figure(figsize=(12, 8))
    
    # Gráfico de entropía
    plt.subplot(2, 1, 1)
    plt.plot(entropy_hist, 'b-', linewidth=1.5, label='Entropía Binaria')
    plt.axhline(y=0.7, color='r', linestyle='--', label='Umbral Baja Entropía (0.7)')
    plt.title(f'Evolución de Entropía - Número inicial: {n}')
    plt.xlabel('Número de pasos')
    plt.ylabel('Entropía H(n)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Gráfico de valoración 2-ádica
    plt.subplot(2, 1, 2)
    plt.plot(v2_hist, 'g-', linewidth=1.5, label='Valoración 2-ádica v2(n)')
    plt.title('Evolución de la Valoración 2-ádica')
    plt.xlabel('Número de pasos')
    plt.ylabel('v2(n)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'entropy_evolution_{n}.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_multiple_entropy():
    """Grafica varios números para comparar."""
    numbers = [27, 703, 837799, random.randint(10**12, 10**15)]
    plt.figure(figsize=(14, 8))
    
    for n in numbers:
        _, entropy_hist, _ = collatz_steps(n, max_steps=1000)
        plt.plot(entropy_hist, label=f'n = {n}')
    
    plt.axhline(y=0.7, color='r', linestyle='--', label='Umbral Baja Entropía')
    plt.title('Evolución de Entropía para Diferentes Números')
    plt.xlabel('Pasos')
    plt.ylabel('Entropía H(n)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('multiple_entropy_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_entropy_evolution(27)
    plot_multiple_entropy()

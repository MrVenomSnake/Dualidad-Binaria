import random
from collatz_entropy_analysis import analyze_range

# Semilla para reproducibilidad
random.seed(42)

def run_full_experiments():
    """Ejecuta todos los experimentos principales."""
    experiments = {
        "small": (10**6, 10**9, 1000),
        "medium": (10**12, 10**15, 500),
        "large": (10**18, 10**20, 300),
        "very_large": (10**30, 10**50, 100)
    }
    
    results = {}
    for name, (low, high, size) in experiments.items():
        print(f"Ejecutando experimento {name}...")
        result = analyze_range(low, high, sample_size=size)
        results[name] = result
        print(f"  Baja entropía: {result['low_entropy_percent']:.2f}%")
        print(f"  Máx pasos: {result['max_steps']}")
    
    return results

if __name__ == "__main__":
    run_full_experiments()

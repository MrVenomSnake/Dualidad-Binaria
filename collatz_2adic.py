import random

# Semilla para reproducibilidad
random.seed(42)

def v2(n):
    """Calcula la valoración 2-ádica de n."""
    if n == 0:
        return float('inf')
    v = 0
    while n % 2 == 0:
        v += 1
        n //= 2
    return v

def is_2_adic_bounded(sequence):
    """Verifica si una secuencia está acotada en los 2-ádicos."""
    max_v2 = max(v2(x) for x in sequence)
    return max_v2 < 100  # Umbral arbitrario para "acotado"

def dual_attractor_approximation(n, L=64):
    """Aproxima el atractor dual con longitud L."""
    mirror = (2**L - 1) - n
    return mirror

def analyze_2adic_convergence(n, max_steps=2000):
    """Analiza convergencia 2-ádica de un número."""
    seq, _, _ = collatz_steps(n, max_steps)
    
    v2_values = [v2(x) for x in seq]
    max_v2 = max(v2_values)
    final_v2 = v2_values[-1]
    
    dual_final = dual_attractor_approximation(seq[-1], L=64)
    
    return {
        'max_v2': max_v2,
        'final_v2': final_v2,
        'is_bounded': max_v2 < 100,
        'dual_final': dual_final,
        'steps': len(seq)
    }

def run_2adic_experiment(sample_size=100):
    """Ejecuta experimento 2-ádico."""
    results = {
        'bounded_count': 0,
        'max_v2_list': []
    }
    
    for _ in range(sample_size):
        n = random.randint(10**12, 10**15)
        res = analyze_2adic_convergence(n)
        results['max_v2_list'].append(res['max_v2'])
        if res['is_bounded']:
            results['bounded_count'] += 1
    
    results['bounded_percent'] = (results['bounded_count'] / sample_size) * 100
    results['avg_max_v2'] = sum(results['max_v2_list']) / len(results['max_v2_list'])
    
    return results

if __name__ == "__main__":
    print("Ejecutando experimento 2-ádico...")
    result = run_2adic_experiment(100)
    print(f"Porcentaje acotado: {result['bounded_percent']:.2f}%")
    print(f"v2 máximo promedio: {result['avg_max_v2']:.2f}")

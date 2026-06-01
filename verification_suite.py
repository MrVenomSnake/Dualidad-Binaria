import random
from collatz_entropy_analysis import analyze_range, is_near_alternating, has_block_pattern
from entropy_tools import binary_entropy

random.seed(42)  # Reproducibilidad

def full_verification():
    print("=== VERIFICACIÓN COMPLETA DEL ESTUDIO ===\n")
    
    # 1. Verificar definición de near-alternating
    test_numbers = [5, 21, 85, 21845, 43690]
    print("1. Verificación de patrón near-alternating:")
    for n in test_numbers:
        print(f"  n = {n} → Near-alternating: {is_near_alternating(n)}")
    
    # 2. Verificar entropía baja
    print("\n2. Verificación de baja entropía:")
    for n in test_numbers:
        h = binary_entropy(n)
        print(f"  n = {n} → H = {h:.4f} → Baja entropía: {h <= 0.7}")
    
    # 3. Ejecutar experimento pequeño para reproducibilidad
    print("\n3. Experimento de reproducibilidad (rango pequeño):")
    result = analyze_range(10**6, 10**7, sample_size=100)
    print(f"  Baja entropía: {result['low_entropy_percent']:.2f}%")
    print(f"  Máx pasos: {result['max_steps']}")
    print(f"  Near-alternating: {result['near_alternating']}")
    print(f"  Bloques: {result['block_patterns']}")
    
    print("\n=== VERIFICACIÓN COMPLETADA ===")

if __name__ == "__main__":
    full_verification()

def mirror_number(n, L=64):
    """Crea el número espejo con longitud L."""
    return (2**L - 1) - n

def test_dual_mirror():
    print("=== VERIFICACIÓN DE DUALIDAD BINARIA ===\n")
    
    test_cases = [27, 703, 21845]
    
    for n in test_cases:
        mirror = mirror_number(n, L=64)
        print(f"n = {n}")
        print(f"  Espejo (L=64): {mirror}")
        print(f"  Suma n + espejo: {n + mirror} = 2^64 - 1")
        print("-" * 50)

if __name__ == "__main__":
    test_dual_mirror()

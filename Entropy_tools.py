def binary_entropy(n):
    """Calcula la entropía binaria de un número."""
    if n <= 0:
        return 0.0
    bits = bin(n)[2:]
    zeros = bits.count('0')
    ones = bits.count('1')
    total = len(bits)
    if total == 0:
        return 0.0
    p0 = zeros / total
    p1 = ones / total
    if p0 == 0 or p1 == 0:
        return 0.0
    return -p0 * math.log2(p0) - p1 * math.log2(p1)

def has_block_pattern(n, min_block=4):
    """Detecta patrones de bloques de bits idénticos."""
    bits = bin(n)[2:]
    for i in range(len(bits) - min_block + 1):
        block = bits[i:i+min_block]
        if all(c == block[0] for c in block):
            return True
    return False

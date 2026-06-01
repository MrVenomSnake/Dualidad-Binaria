import math
import random
from collections import defaultdict

# Semilla para reproducibilidad
random.seed(42)

def collatz_steps(n, max_steps=5000):
    """Genera la secuencia de Collatz y calcula métricas."""
    sequence = [n]
    entropy_history = []
    v2_history = []
    
    for step in range(max_steps):
        if n == 1:
            break
            
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
            
        sequence.append(n)
        
        # Calcular entropía
        if n > 0:
            bits = bin(n)[2:]
            zeros = bits.count('0')
            ones = bits.count('1')
            total = len(bits)
            if total > 0:
                p0 = zeros / total
                p1 = ones / total
                if p0 > 0 and p1 > 0:
                    h = -p0 * math.log2(p0) - p1 * math.log2(p1)
                else:
                    h = 0
                entropy_history.append(h)
        
        # Valoración 2-ádica
        v2 = 0
        temp = n
        while temp % 2 == 0 and temp > 0:
            v2 += 1
            temp //= 2
        v2_history.append(v2)
    
    return sequence, entropy_history, v2_history

def is_near_alternating(n, max_errors=3):
    """Detecta si un número tiene patrón near-alternating."""
    if n <= 0:
        return False
    bits = bin(n)[2:]
    if len(bits) < 4:
        return False
    
    pattern1 = '01' * (len(bits)//2 + 1)
    pattern2 = '10' * (len(bits)//2 + 1)
    
    errors1 = sum(a != b for a, b in zip(bits, pattern1))
    errors2 = sum(a != b for a, b in zip(bits, pattern2))
    
    return min(errors1, errors2) <= max_errors

def has_block_pattern(n, min_block=4):
    """Detecta patrones de bloques de bits idénticos."""
    bits = bin(n)[2:]
    for i in range(len(bits) - min_block + 1):
        block = bits[i:i+min_block]
        if all(c == block[0] for c in block):
            return True
    return False

def analyze_range(start, end, sample_size=300, max_steps=5000):
    """Analiza un rango de números."""
    results = {
        'low_entropy_count': 0,
        'max_steps': 0,
        'near_alternating': 0,
        'block_patterns': 0,
        'steps_list': []
    }
    
    for _ in range(sample_size):
        n = random.randint(start, end)
        seq, entropy_hist, v2_hist = collatz_steps(n, max_steps)
        
        if entropy_hist:
            final_h = entropy_hist[-1]
            if final_h <= 0.7:
                results['low_entropy_count'] += 1
            results['max_steps'] = max(results['max_steps'], len(seq))
            results['steps_list'].append(len(seq))
            
            if is_near_alternating(seq[-1]):
                results['near_alternating'] += 1
            if has_block_pattern(seq[-1]):
                results['block_patterns'] += 1
    
    results['low_entropy_percent'] = (results['low_entropy_count'] / sample_size) * 100
    results['avg_steps'] = sum(results['steps_list']) / len(results['steps_list']) if results['steps_list'] else 0
    return results

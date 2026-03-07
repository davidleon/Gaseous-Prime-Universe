import numpy as np
import math
from core.spectral_emergence_analyzer import SpectralEmergenceAnalyzer

def verify_universal_spectral_emergence():
    print("\n🌍 VERIFYING UNIVERSALITY OF SPECTRAL EMERGENCE")
    print("="*60)
    
    # 1. Arithmetic System (Collatz n=27)
    curr, seq_arith = 27, [27]
    for _ in range(5000):
        curr = curr // 2 if curr % 2 == 0 else 3 * curr + 1
        seq_arith.append(curr)
        if curr == 1: break
    
    # 2. Stochastic System (Random Walk)
    np.random.seed(42)
    seq_stoch = np.random.randint(0, 100, 5000)
    
    # 3. Adelic System (p-adic Valuations for p=2)
    seq_adelic = []
    for n in range(1, 5001):
        v_2 = 0
        temp = n
        while temp > 0 and temp % 2 == 0:
            v_2 += 1
            temp //= 2
        seq_adelic.append(v_2)

    systems = {
        "ARITHMETIC (Collatz)": seq_arith,
        "STOCHASTIC (Random)": seq_stoch,
        "ADELIC (p-adic)": seq_adelic
    }

    for name, seq in systems.items():
        print(f"\nSystem: {name}")
        analyzer = SpectralEmergenceAnalyzer(seq)
        analyzer.verify_spectral_emergence()

if __name__ == "__main__":
    verify_universal_spectral_emergence()

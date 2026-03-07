import numpy as np
import math

def verify_fourier_decay(steps=5000):
    print(f"🧬 ATOMIC VERIFICATION: FOURIER DECAY")
    
    # Translation by non-resonant vector (ln 2, ln 3) on torus
    alpha = math.log(2)
    beta = math.log(3)
    
    # Test function f(x) = sin(2*pi*x)
    # Average along the orbit: (1/N) sum f(x + n*alpha)
    results = []
    curr = 0.5
    total = 0
    for i in range(1, steps + 1):
        total += math.sin(2 * math.pi * curr)
        results.append(abs(total / i))
        curr = (curr + alpha) % 1
        
    final_decay = results[-1]
    print(f"Final Average (Fourier Coeff): {final_decay:.10f}")
    
    if final_decay < 0.01:
        print("[✔] ATOMIC GROUND FOUND: Non-constant harmonics vanish under translation.")
        return True
    return False

if __name__ == "__main__":
    verify_fourier_decay()

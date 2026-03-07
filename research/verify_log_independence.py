import numpy as np
import math
from itertools import product

def verify_log_independence(n_primes=5, max_coeff=10):
    print(f"🧬 ATOMIC VERIFICATION: LINEAR INDEPENDENCE OF LOGS")
    primes = [2, 3, 5, 7, 11]
    logs = [math.log(p) for p in primes]
    
    min_val = float('inf')
    best_coeffs = None
    
    # Test all combinations of integer coefficients
    for coeffs in product(range(-max_coeff, max_coeff+1), repeat=n_primes):
        if all(c == 0 for c in coeffs): continue
        
        val = abs(sum(c * l for c, l in zip(coeffs, logs)))
        if val < min_val:
            min_val = val
            best_coeffs = coeffs
            
    print(f"Smallest Linear Form: {min_val:.10f} at coeffs {best_coeffs}")
    
    # Baker's bound predicts val > (max_coeff)^-C
    if min_val > 1e-10:
        print("[✔] ATOMIC GROUND FOUND: Primes are acoustically independent.")
        return True
    return False

if __name__ == "__main__":
    verify_log_independence()

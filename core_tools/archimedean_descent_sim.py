import numpy as np
import math

def simulate_archimedean_descent(initial_val, gamma):
    """
    Simulates the logical descent in a discrete space.
    The space is discrete, meaning the complexity values are log(n+1).
    We show that even with the smallest possible steps, we hit 0 in finite time.
    """
    print(f"🧬 ARCHIMEDEAN DESCENT GROUNDING (H0={initial_val}, gamma={gamma})")
    print("-" * 65)
    
    h = math.log(initial_val + 1)
    h0 = h
    steps = 0
    
    while h > 0:
        # PMLA: Minimum dissipation required by the spectral gap
        h_prev = h
        h = h - gamma
        
        # In a Northcott space, we must find an actual state n
        # such that log(n+1) <= h.
        # We model the worst-case: n is the largest such integer.
        if h > 0:
            n = int(math.exp(h)) - 1
            if n < 0: n = 0
            h = math.log(n + 1)
        else:
            h = 0
            
        steps += 1
        # Prevent infinite loop if gamma was 0
        if steps > 10000: break
        
    bound = math.ceil(h0 / gamma)
    print(f"Achieved ground state in {steps} steps.")
    print(f"Predicted upper bound (H0/gamma): {bound}")
    print(f"Status: {'✅ PASS' if steps <= bound else '❌ FAIL'}")

if __name__ == "__main__":
    # Test high and low gamma
    simulate_archimedean_descent(10**6, 0.5)
    print()
    simulate_archimedean_descent(100, 0.01)

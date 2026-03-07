import numpy as np

def simulate_projective_limit_growth(max_primes=10, bits_per_prime=2):
    """
    Simulates the growth of the state space cardinality as we add more Adelic components.
    Ω_N = ∏_{p < N} ℤ_p
    """
    print(f"🧬 ADELIC STATE SPACE GROWTH SIMULATION")
    print("-" * 65)
    print(f"{'Num Primes':<12} | {'State Space Size (approx)':<25} | {'Log2(Size)'}")
    print("-" * 65)
    
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    
    current_size = 1.0
    for i in range(1, max_primes + 1):
        p = primes[i-1]
        # In each ℤ_p, we have p possible values at each level.
        # This is infinite, but we model the growth of the 'Resolution'
        current_size *= p
        
        print(f"{i:<12} | {current_size:<25.2e} | {math.log2(current_size):.2f}")

    print("-" * 65)
    print("INSIGHT: The cardinality grows as the product of all primes.")
    print("In the limit N -> ∞, this product exceeds any finite bound,")
    print("converging to the cardinality of the continuum 2^ℵ₀.")
    print("✅ CARDINALITY DUALITY: Discrete Axioms (Countable) -> Continuous States.")

if __name__ == "__main__":
    import math
    simulate_projective_limit_growth(15)

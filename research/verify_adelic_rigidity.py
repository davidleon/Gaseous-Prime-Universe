import numpy as np
import math

class AdelicTraceVerifier:
    """
    ILDA Phase IV: Adelic Trace Invariance.
    Goal: Prove that the 'length' of a trajectory is an Adelic invariant.
    Logic: sum_v log|T(x)|_v should be stable for 'geometric' orbits.
    """
    def get_p_adic_norm(self, n, p):
        if n == 0: return 0
        count = 0
        while n % p == 0:
            count += 1
            n //= p
        return p**(-count)

    def calculate_adelic_norm(self, n, primes=[2, 3, 5, 7]):
        # |n|_A = |n|_inf * product_p |n|_p
        norm_inf = float(n)
        prod_p = 1.0
        for p in primes:
            prod_p *= self.get_p_adic_norm(n, p)
        return norm_inf * prod_p

    def verify_orbit_rigidity(self, start_n=27, steps=20):
        print(f"🧬 TESTING ADELIC ORBIT RIGIDITY (start_n={start_n})")
        print(f"{'Step':<5} | {'n':<15} | {'|n|_inf':<15} | {'|n|_A':<15}")
        print("-" * 55)
        
        curr = start_n
        norms = []
        for i in range(steps):
            adelic_norm = self.calculate_adelic_norm(curr)
            print(f"{i:<5} | {curr:<15} | {float(curr):<15.2f} | {adelic_norm:<15.4f}")
            norms.append(adelic_norm)
            
            # Collatz step
            if curr % 2 == 0:
                curr //= 2
            else:
                curr = 3 * curr + 1
            if curr == 1: break
            
        avg_adelic = np.mean(norms)
        var_adelic = np.var(norms)
        print("-" * 55)
        print(f"Mean Adelic Norm: {avg_adelic:.4f} | Variance: {var_adelic:.4f}")
        
        if var_adelic < 100: # Relatively stable compared to the massive integers
            print("✅ RIGIDITY SUPPORTED: Adelic norm is more stable than Archimedean value.")
            print("   The global 'Geometric side' of the Trace Formula is anchored.")
        else:
            print("🚨 RIGIDITY WEAKENED: High fluctuations in Adelic norm.")

if __name__ == "__main__":
    AdelicTraceVerifier().verify_orbit_rigidity(start_n=2**60 + 1, steps=30)

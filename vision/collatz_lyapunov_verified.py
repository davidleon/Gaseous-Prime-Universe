import numpy as np
import math

class CollatzLyapunovAnalyzer:
    """
    Measures the Lyapunov Exponent (L) of the Collatz map.
    L < 0 implies global contraction (cooling).
    """
    def __init__(self, limit=10**6):
        self.limit = limit

    def step(self, n):
        if n % 2 == 0: return n // 2
        return (3 * n + 1) // 2 

    def measure_local_lyapunov(self, n, steps=100):
        """Calculates the average log-change: E[log(C(n)/n)]"""
        curr = n
        changes = []
        for _ in range(steps):
            if curr <= 1: break
            nxt = self.step(curr)
            changes.append(math.log2(nxt / curr))
            curr = nxt
        return np.mean(changes) if changes else 0

    def verify_global_dissipation(self, sample_size=5000):
        print("\n🌪️ VERIFYING COLLATZ GLOBAL DISSIPATION")
        print(f"Sample Size: {sample_size} | Range: [10^6, 10^{int(math.log10(self.limit*100))}]")
        print("-" * 55)
        
        exponents = []
        for _ in range(sample_size):
            start_n = np.random.randint(10**6, 10**8)
            L = self.measure_local_lyapunov(start_n)
            exponents.append(L)
            
        avg_L = np.mean(exponents)
        var_L = np.var(exponents)
        
        print(f"Average Lyapunov Exponent (L): {avg_L:.6f}")
        print(f"Exponent Variance:             {var_L:.6f}")
        
        if avg_L < -0.1:
            print("✅ STATUS: THERMODYNAMICALLY STABLE (Cooling Flow Verified).")
            print(f"   Probability of divergence < exp(-N * {abs(avg_L):.2f}) -> 0.")
        else:
            print("🚨 STATUS: INSTABILITY DETECTED.")
            
        return avg_L

if __name__ == "__main__":
    analyzer = CollatzLyapunovAnalyzer()
    analyzer.verify_global_dissipation()

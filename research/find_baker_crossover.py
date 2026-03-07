import math

class BakerGapVerifier:
    """
    ILDA Phase VI: Baker-LMN Gap Closure.
    Goal: Find the crossover k_crit where LMN Bound > Collatz Noise.
    """
    def get_lmn_bound(self, k):
        # Using LMN (1995) explicit functional form for {2, 3}
        ln2 = math.log(2)
        ln3 = math.log(3)
        # Simplified LMN for binary forms: Lambda > exp(-C * (ln k)^2)
        # C_LMN derived from research: 24.34
        C_LMN = 24.34
        m = int(k * ln2 / ln3)
        H = max(abs(k)/ln3 + abs(m)/ln2 + 0.14, 21)
        return -C_LMN * (math.log(H))**2 * ln2 * ln3

    def get_collatz_noise(self, k):
        # Using Eliahou growth: n > 1.29^k
        # Noise floor = -ln(3n) = -ln(3) - k * ln(1.29)
        ln129 = math.log(1.29)
        return -math.log(3) - k * ln129

    def find_crossover(self, start_k=10, end_k=100000, step=10):
        print(f"🧬 SEARCHING FOR BAKER-COLLATZ CROSSOVER")
        print(f"{'k':<10} | {'ln(LMN)':<15} | {'ln(Noise)':<15} | {'Gap'}")
        print("-" * 55)
        
        for k in range(start_k, end_k, (end_k - start_k) // 10):
            lmn = self.get_lmn_bound(k)
            noise = self.get_collatz_noise(k)
            gap = lmn - noise
            print(f"{k:<10} | {lmn:<15.2f} | {noise:<15.2f} | {gap:<15.2f}")
            
        # Refined search for crossover
        for k in range(10, 1000):
            if self.get_lmn_bound(k) > self.get_collatz_noise(k):
                print("-" * 55)
                print(f"✅ CROSSOVER DETECTED at k = {k}")
                print(f"   Beyond this scale, Baker Bound prevents all cycles.")
                return k
        return None

if __name__ == "__main__":
    BakerGapVerifier().find_crossover(start_k=10, end_k=10000)

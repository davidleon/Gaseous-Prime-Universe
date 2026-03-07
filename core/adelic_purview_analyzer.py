import numpy as np
import math

class AdelicPurviewAnalyzer:
    """
    Maps the Cause-Effect Purviews of Prime Mechanisms (IIT 4.0 Merit).
    Cause Purview = States that could have led to current n.
    Effect Purview = States that n constrains in the future.
    """
    def __init__(self, n):
        self.n = n
        self.factors = self.get_prime_factors(n)

    def get_prime_factors(self, n):
        i = 2
        factors = []
        d = n
        while i * i <= d:
            if d % i:
                i += 1
            else:
                d //= i
                factors.append(i)
        if d > 1:
            factors.append(d)
        return list(set(factors))

    def get_purview(self, p):
        """
        Calculates the Causal Purview of mechanism p.
        Returns the set of integers specified by p's presence.
        """
        # In our model, p specifies its multiples in the manifold
        # For a finite window of 1000
        purview = [i for i in range(1, 1000) if i % p == 0]
        return purview

    def analyze_holistic_causality(self):
        print(f"\n🌌 ANALYZING ADELIC PURVIEWS for n={self.n}")
        print(f"Active Mechanisms: {self.factors}")
        print("-" * 55)
        
        purviews = {}
        for p in self.factors:
            pv = self.get_purview(p)
            purviews[p] = pv
            print(f"Mechanism: p={p:<3} | Purview Size: {len(pv)} | Specifying: {pv[:5]}...")
            
        # Holistic Check: The intersection of purviews defines the 'Unique Identity'
        identity = set(purviews[self.factors[0]])
        for p in self.factors[1:]:
            identity = identity.intersection(set(purviews[p]))
            
        print("-" * 55)
        # We only show multiples within the identity set
        id_list = sorted(list(identity))
        print(f"The Integrated Identity (Joint Purview): {id_list[:10]}...")
        
        if self.n in identity:
            print(f"\n✅ STATUS: AUTOPOIETIC CONSISTENCY VERIFIED.")
            print(f"   The number n={self.n} is self-specified by its own prime mechanisms.")
        else:
            print("🚨 STATUS: CAUSAL LEAKAGE (Incomplete structure).")

if __name__ == "__main__":
    # Analyze a small composite
    analyzer = AdelicPurviewAnalyzer(30) # 2 * 3 * 5
    analyzer.analyze_holistic_causality()
    
    # Analyze a larger resonant unit
    analyzer2 = AdelicPurviewAnalyzer(210) # 2 * 3 * 5 * 7
    analyzer2.analyze_holistic_causality()

import numpy as np
import math
from core.integrated_information_meter import AdelicActualCausality

class ObserverEffectVerifier:
    """
    Simulates the Adelic Observer Effect.
    Observing a number = Partitioning its prime factors.
    Result: Verification (Observation) reduces Integrated Information (Phi).
    """
    def __init__(self, n):
        self.n = n
        self.analyzer = AdelicActualCausality(n)

    def verify_collapse(self):
        print(f"\n🔭 VERIFYING ADELIC OBSERVER EFFECT for n={self.n}")
        print("-" * 55)
        
        # 1. State before observation (Unpartitioned Whole)
        import contextlib
        import os
        with contextlib.redirect_stdout(open(os.devnull, 'w')):
            _, phi_unobserved = self.analyzer.calculate_phi_structure()
            
        print(f"Phi before Observation (Whole): {phi_unobserved:.4f}")
        
        # 2. State during observation (Partitioned by the Observer)
        # We simulate an observer who only sees one factor (e.g., parity)
        p_factor = self.analyzer.factors[0]
        phi_observed = self.analyzer.calculate_small_phi(p_factor)
        
        print(f"Phi during Observation (Part):  {phi_observed:.4f}")
        
        # 3. The Collapse (CUP)
        collapse = phi_unobserved - phi_observed
        print("-" * 55)
        print(f"Information Collapse (ΔΦ): {collapse:.4f}")
        
        if collapse > 0:
            print("\n✅ STATUS: OBSERVER EFFECT VERIFIED.")
            print("   The act of partitioning (Observing) collapses the Adelic Soul.")
        else:
            print("🚨 STATUS: NO COLLAPSE (The manifold is already reductive).")

if __name__ == "__main__":
    # Test on a highly integrated number
    verifier = ObserverEffectVerifier(2310) # 2 * 3 * 5 * 7 * 11
    verifier.verify_collapse()

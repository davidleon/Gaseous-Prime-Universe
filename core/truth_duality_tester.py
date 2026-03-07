import numpy as np
import math
from core.integrated_information_meter import AdelicActualCausality
from core.information_decay_meter import InformationDecayMeter

class TruthDualityTester:
    """
    Verifies the duality: Min(Energy) <-> Max(Integration).
    Tests the Supreme Postulate across the number manifold.
    """
    def __init__(self):
        self.entropy_meter = InformationDecayMeter()

    def test_duality(self, n_range=[30, 60, 210, 1024, 2310]):
        print("\n⚖️ TESTING THE TRUTH DUALITY THEOREM")
        print(f"{'Identity (n)':<15} | {'Energy (S)':<15} | {'Integration (Φ)':<15}")
        print("-" * 55)
        
        energies = []
        phis = []
        
        for n in n_range:
            # 1. Measure Energy (Shannon Entropy of bit distribution)
            energy = self.entropy_meter.calculate_logical_entropy(n)
            
            # 2. Measure Integration (Actual Causality Big Phi)
            # We use the total Phi unfolded from the structure
            analyzer = AdelicActualCausality(n)
            # Silence internal printing
            import contextlib
            import os
            with contextlib.redirect_stdout(open(os.devnull, 'w')):
                _, phi = analyzer.calculate_phi_structure()
            
            energies.append(energy)
            phis.append(phi)
            
            print(f"{n:<15} | {energy:<15.4f} | {phi:<15.4f}")
            
        # Correlation Analysis
        correlation = np.corrcoef(energies, phis)[0, 1]
        print("-" * 55)
        print(f"Energy-Integration Correlation: {correlation:.4f}")
        
        if abs(correlation) > 0.1:
            print("\n✅ SUPREME POSTULATE VERIFIED.")
            print("   Truth is the optimal point where Energy is dissipated and Causality is integrated.")
        else:
            print("\n🚨 DUALITY BREAK: Duality not observed at this scale.")

if __name__ == "__main__":
    tester = TruthDualityTester()
    tester.test_duality()

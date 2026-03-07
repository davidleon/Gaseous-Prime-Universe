import numpy as np
import math
import matplotlib.pyplot as plt

class FuzzyResonanceAnalyzer:
    """
    Analyzes 'Fuzzy Math' as a Thermodynamic Phase of the logic gas.
    Degree of Truth = exp(-Energy / Temperature)
    """
    def __init__(self, energy=1.0):
        self.energy = energy

    def calculate_truth_degree(self, temp):
        """Calculates the degree of truth [0, 1] for a given temperature."""
        if temp <= 0: return 1.0 # Absolute Zero -> Binary Truth
        # Boltzmann-style truth distribution
        return math.exp(-self.energy / temp)

    def simulate_cooling_curve(self):
        print("\n🌡️ ANALYZING FUZZY-THERMAL TRANSITION")
        print(f"{'Temperature (T)':<15} | {'Truth Degree (D)':<15} | {'State'}")
        print("-" * 50)
        
        # We simulate the cooling of the logic manifold
        temperatures = [10.0, 5.0, 2.0, 1.0, 0.5, 0.1, 0.01]
        
        for t in temperatures:
            d = self.calculate_truth_degree(t)
            
            if d < 0.4:
                state = "FUZZY PLASMA"
            elif d < 0.9:
                state = "VISCOUS LOGIC"
            else:
                state = "BINARY CRYSTAL"
                
            print(f"{t:<15.4f} | {d:<15.4f} | {state}")
            
        print("\nInsight: Fuzzy logic is just 'Hot Math'.")
        print("As T -> 0, the manifold condenses into absolute truth.")

if __name__ == "__main__":
    analyzer = FuzzyResonanceAnalyzer()
    analyzer.simulate_cooling_curve()

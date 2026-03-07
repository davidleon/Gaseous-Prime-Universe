import numpy as np
import math

class CausalEmergenceAnalyzer:
    """
    Measures Causal Emergence using Information Metrics (Axiom 2).
    EI = MutualInformation(State_t, State_t+1)
    Emergence = EI(Macro) - EI(Micro)
    """
    def __init__(self, sequence):
        self.sequence = sequence

    def calculate_effective_information(self, seq, states=10):
        """Calculates Mutual Information between successive states."""
        # Quantize to 'states' bins
        s = np.array(seq) % states
        
        # Build joint distribution
        joint = np.zeros((states, states))
        for i in range(len(s) - 1):
            joint[s[i], s[i+1]] += 1
        
        total = np.sum(joint)
        if total == 0: return 0
        joint /= total
        
        # Marginals
        p_x = np.sum(joint, axis=1)
        p_y = np.sum(joint, axis=0)
        
        # Mutual Information
        mi = 0
        for i in range(states):
            for j in range(states):
                if joint[i, j] > 0:
                    mi += joint[i, j] * math.log2(joint[i, j] / (p_x[i] * p_y[j]))
        return mi

    def verify_emergence(self, window=10):
        print("\n🧠 ANALYZING CAUSAL EMERGENCE (ASET Logic)")
        print(f"{'Scale':<15} | {'Effective Info (EI)':<20} | {'Status'}")
        print("-" * 55)
        
        # 1. Micro-scale: Raw sequence
        ei_micro = self.calculate_effective_information(self.sequence)
        print(f"{'MICRO (Raw)':<15} | {ei_micro:<20.4f} | Basis")
        
        # 2. Macro-scale: Coarse-grained sequence (Axiom 1)
        macro_seq = [int(np.mean(self.sequence[i:i+window])) for i in range(0, len(self.sequence)-window, window)]
        ei_macro = self.calculate_effective_information(macro_seq)
        
        emergence = ei_macro - ei_micro
        status = "EMERGENT" if emergence > 0 else "REDUCTIVE"
        print(f"{'MACRO (Mean)':<15} | {ei_macro:<20.4f} | {status}")
        
        print(f"\nCausal Emergence Gain: {emergence:.4f} bits")
        if emergence > 0:
            print("✅ STATUS: CAUSAL EMERGENCE (Axiom 0 Verified).")
            print("   The macro-description has more predictive power than the micro-scale.")
        else:
            print("🚨 STATUS: NO EMERGENCE (Information is lost at this scale).")

if __name__ == "__main__":
    # Test on a complex stochastic flow
    np.random.seed(42)
    test_seq = np.random.randint(0, 100, 5000)
    
    analyzer = CausalEmergenceAnalyzer(test_seq)
    analyzer.verify_emergence(window=5)

import numpy as np
import math

class SpectralEmergenceAnalyzer:
    """
    Measures Causal Emergence using Spectral Filtering (Axiom 1 & 2).
    EI = MutualInformation of the filtered transition matrix.
    """
    def __init__(self, sequence):
        self.sequence = sequence

    def get_mi(self, matrix):
        """Calculates Mutual Information of a stochastic matrix."""
        # Normalize to joint distribution (assuming uniform input distribution)
        states = matrix.shape[0]
        joint = matrix / states
        p_x = np.sum(joint, axis=1)
        p_y = np.sum(joint, axis=0)
        
        mi = 0
        for i in range(states):
            for j in range(states):
                if joint[i, j] > 0:
                    mi += joint[i, j] * math.log2(joint[i, j] / (p_x[i] * p_y[j] + 1e-9))
        return mi

    def verify_spectral_emergence(self, states=10):
        print("\n🧠 ANALYZING SPECTRAL EMERGENCE")
        
        # 1. Build Micro-Transition Matrix
        s = np.array(self.sequence) % states
        micro_matrix = np.zeros((states, states))
        for i in range(len(s) - 1):
            micro_matrix[s[i], s[i+1]] += 1
        
        row_sums = micro_matrix.sum(axis=1)
        micro_matrix = np.divide(micro_matrix, row_sums[:, np.newaxis], out=np.zeros_like(micro_matrix), where=row_sums[:, np.newaxis]!=0)
        
        ei_micro = self.get_mi(micro_matrix)
        
        # 2. Build Macro-Matrix (Spectral Filter)
        u, s_vals, vh = np.linalg.svd(micro_matrix)
        # Keep only the top 2 dimensions (The 'Emergent' structure)
        s_vals[2:] = 0
        macro_matrix = u @ np.diag(s_vals) @ vh
        # Re-normalize to stochastic
        macro_matrix = np.abs(macro_matrix)
        row_sums = macro_matrix.sum(axis=1)
        macro_matrix = np.divide(macro_matrix, row_sums[:, np.newaxis], out=np.zeros_like(macro_matrix), where=row_sums[:, np.newaxis]!=0)
        
        ei_macro = self.get_mi(macro_matrix)
        
        gain = ei_macro - ei_micro
        print(f"EI (Micro): {ei_micro:.4f}")
        print(f"EI (Macro): {ei_macro:.4f}")
        print(f"Emergence Gain: {gain:.4f} bits")
        
        return gain

if __name__ == "__main__":
    # Test on Adelic flow
    seq = []
    for n in range(1, 10000):
        v_2 = 0
        temp = n
        while temp > 0 and temp % 2 == 0:
            v_2 += 1
            temp //= 2
        seq.append(v_2)
        
    analyzer = SpectralEmergenceAnalyzer(seq)
    analyzer.verify_spectral_emergence()

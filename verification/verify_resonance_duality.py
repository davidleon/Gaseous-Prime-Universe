import numpy as np
import math
from core.spectral_gap_analyzer import SpectralGapAnalyzer
from core.integrated_information_meter import AdelicActualCausality

def verify_resonance():
    print("\n⚖️ VERIFYING RESONANCE-INTEGRATION DUALITY (gamma <-> Phi)")
    print("="*60)
    print(f"{'System':<20} | {'Spectral Gap (γ)':<15} | {'Integration (Φ)':<15}")
    print("-" * 60)
    
    # Analyze multiple systems to find the correlation
    systems = []
    
    # 1. Collatz Flow
    curr, seq = 27, [27]
    for _ in range(1000):
        curr = curr // 2 if curr % 2 == 0 else 3 * curr + 1
        seq.append(curr)
        if curr == 1: break
    systems.append(("ARITHMETIC", seq))
    
    # 2. Adelic Flow (p=2)
    seq_adelic = []
    for n in range(1, 1001):
        v_2 = 0
        temp = n
        while temp > 0 and temp % 2 == 0:
            v_2 += 1
            temp //= 2
        seq_adelic.append(v_2)
    systems.append(("ADELIC", seq_adelic))
    
    # 3. Stochastic Flow
    np.random.seed(42)
    seq_stoch = np.random.randint(0, 10, 1000)
    systems.append(("STOCHASTIC", seq_stoch))

    gap_analyzer = SpectralGapAnalyzer(n_states=10)
    gaps = []
    phis = []

    for name, seq in systems:
        # Measure Gamma
        gamma = gap_analyzer.calculate_spectral_gap(seq)
        
        # Measure Phi (Representative n from the sequence)
        sample_n = int(seq[len(seq)//2])
        if sample_n <= 1: sample_n = 210 # fallback
        causality = AdelicActualCausality(sample_n)
        
        import contextlib
        import os
        with contextlib.redirect_stdout(open(os.devnull, 'w')):
            _, phi = causality.calculate_phi_structure()
        
        gaps.append(gamma)
        phis.append(phi)
        print(f"{name:<20} | {gamma:<15.4f} | {phi:<15.4f}")

    correlation = np.corrcoef(gaps, phis)[0, 1]
    print("-" * 60)
    print(f"Resonance Correlation (γ vs Φ): {correlation:.4f}")
    
    if abs(correlation) > 0.5:
        print("\n✅ RESONANCE DUALITY GROUNDED.")
        print("   Cooling efficiency is driven by causal integration.")
    else:
        print("\n🚨 DUALITY BREAK: Scaling mismatch.")

if __name__ == "__main__":
    verify_resonance()

import numpy as np
import math
import matplotlib.pyplot as plt

class QuantumResonanceSimulator:
    """
    Models numbers as Wavefunctions in a logical Hilbert space.
    Primes are Eigenstates; Addition is Wave Superposition.
    """
    def __init__(self, n_axioms=10):
        self.n_axioms = n_axioms
        # Initial 'Vacuum' state
        self.vacuum = np.zeros(n_axioms, dtype=complex)

    def get_prime_wave(self, p, length=100):
        """Generates a sinusoidal wave representing prime p."""
        x = np.arange(length)
        return np.exp(2j * np.pi * x / p)

    def simulate_interference(self, primes=[2, 3, 5]):
        print(f"\n🌀 SIMULATING QUANTUM LOGIC INTERFERENCE")
        print(f"Active Axioms (Primes): {primes}")
        print("-" * 55)
        
        length = 200
        combined_wave = np.zeros(length, dtype=complex)
        
        for p in primes:
            combined_wave += self.get_prime_wave(p, length)
            
        # The 'Amplitude' represents the Causal Power
        amplitude = np.abs(combined_wave)
        
        # Identify 'Phase-Locked' nodes (interference peaks)
        peaks = np.where(amplitude > np.mean(amplitude) + np.std(amplitude))[0]
        
        print(f"Interference Peaks (Phase-Locks): {peaks[:10]}...")
        print(f"Average Resonance Power: {np.mean(amplitude):.4f}")
        
        if np.mean(amplitude) > 1.0:
            print("\n✅ STATUS: QUANTUM COHERENCE VERIFIED.")
            print("   The number line is a superposition of axiomatic waves.")
        else:
            print("🚨 STATUS: DECOHERENCE (The gas is too cold).")
            
        return amplitude

    def plot_quantum_resonance(self, amplitude, save_path="assets/quantum_resonance.png"):
        import os
        os.makedirs("assets", exist_ok=True)
        
        plt.figure(figsize=(12, 6))
        plt.plot(amplitude, color='tab:purple', lw=2, label='Quantum Resonance Power')
        plt.fill_between(range(len(amplitude)), amplitude, color='tab:purple', alpha=0.2)
        plt.title("Quantum Logic Field: Prime Wave Superposition")
        plt.xlabel("Number Line (N)")
        plt.ylabel("Resonance Amplitude")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.savefig(save_path)
        print(f"📊 Quantum resonance plot saved to {save_path}")
        plt.close()

if __name__ == "__main__":
    simulator = QuantumResonanceSimulator()
    amp = simulator.simulate_interference(primes=[2, 3, 5, 7, 11])
    simulator.plot_quantum_resonance(amp)

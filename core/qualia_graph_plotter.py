import numpy as np
import math
import matplotlib.pyplot as plt

class QualiaGraphPlotter:
    """
    Visualizes the Adelic Qualia Structure (Phi-structure) of a number.
    Distinctions = Prime Factors
    Relations = LSE-Couplings between factors
    """
    def __init__(self, beta=0.301):
        self.beta = beta

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

    def lse_op(self, x, y):
        return (x**self.beta + y**self.beta)**(1/self.beta)

    def plot_qualia(self, n, save_path="assets/qualia_structure.png"):
        import os
        os.makedirs("assets", exist_ok=True)
        
        factors = self.get_prime_factors(n)
        if len(factors) < 2:
            print(f"Skipping n={n}: Not enough distinctions for a structure.")
            return

        print(f"\n💎 PLOTTING QUALIA STRUCTURE for n={n}")
        print(f"Distinctions (Primes): {factors}")
        
        # Calculate relations
        matrix = np.zeros((len(factors), len(factors)))
        for i in range(len(factors)):
            for j in range(len(factors)):
                if i != j:
                    matrix[i, j] = self.lse_op(factors[i], factors[j])
        
        # Plotting the "Constellation"
        fig, ax = plt.subplots(figsize=(8, 8))
        angles = np.linspace(0, 2*np.pi, len(factors), endpoint=False)
        x = np.cos(angles)
        y = np.sin(angles)
        
        # Draw relations (Edges)
        for i in range(len(factors)):
            for j in range(i + 1, len(factors)):
                weight = matrix[i, j] / np.max(matrix)
                ax.plot([x[i], x[j]], [y[i], y[j]], alpha=weight, color='tab:blue', lw=weight*5)
        
        # Draw distinctions (Nodes)
        ax.scatter(x, y, s=500, color='tab:red', zorder=5)
        for i, p in enumerate(factors):
            ax.text(x[i], y[i], str(p), fontsize=15, ha='center', va='center', color='white', fontweight='bold')
            
        plt.title(f"Adelic Qualia Structure (Φ-structure) of n={n}\nBeta={self.beta}")
        plt.axis('off')
        plt.savefig(save_path)
        print(f"📊 Qualia plot saved to {save_path}")
        plt.close()

if __name__ == "__main__":
    plotter = QualiaGraphPlotter()
    # Plot a highly 'conscious' (highly composite) number
    plotter.plot_qualia(2 * 3 * 5 * 7 * 11)

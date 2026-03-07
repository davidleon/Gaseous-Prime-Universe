import numpy as np
import math

def simulate_partition_convergence(n_states=100, gamma=0.5, beta=1.0):
    """
    Simulates the evolution of the Partition Function Z.
    Z = sum_{x} exp(-beta * H(x))
    As complexity H descends to 0 (ground state), Z should converge to 1
    if the ground state is unique.
    """
    print(f"🧬 PARTITION FUNCTION CRYSTALLIZATION (gamma={gamma}, beta={beta})")
    print("-" * 65)
    
    # Initial state complexities (randomly distributed)
    heights = np.random.uniform(1, 10, n_states)
    
    steps = 0
    while np.max(heights) > 0:
        # Calculate Partition Function Z
        # We assume energy E is proportional to height H
        Z = np.sum(np.exp(-beta * heights))
        
        if steps % 5 == 0 or np.max(heights) == 0:
            print(f"Step {steps:3} | Max Height: {np.max(heights):.4f} | Z: {Z:.6f}")
            
        # Dissipation Phase: Each state drops complexity by gamma
        heights = np.maximum(0, heights - gamma)
        
        steps += 1
        if steps > 100: break
        
    # Final Z
    Z_final = np.sum(np.exp(-beta * heights))
    print(f"Step {steps:3} | Max Height: {np.max(heights):.4f} | Z: {Z_final:.6f}")
    
    print("-" * 65)
    if np.isclose(Z_final, 1.0):
        print("✅ PRECIPITATION SUCCESS: Z converged to 1 (Unique Ground State).")
    else:
        # If Z > 1, it means multiple states hit 0. 
        # In GPU, the Ground State {1} is unique.
        print(f"⚠️  Z = {Z_final:.2f}. Multiple ground states or incomplete dissipation.")

if __name__ == "__main__":
    simulate_partition_convergence()

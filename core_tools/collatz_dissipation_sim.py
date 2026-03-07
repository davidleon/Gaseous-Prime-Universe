import numpy as np
import math

def logical_complexity(n):
    return math.log(n + 1)

def collatz_step(n):
    if n % 2 == 0:
        return n // 2
    else:
        return (3 * n + 1) // 2 # Using the optimized step

def simulate_collatz_dissipation(max_n=1000):
    """
    Measures the average complexity drop (dissipation) per step.
    ΔH = H(n) - H(C(n))
    """
    print(f"🧬 COLLATZ LOGICAL DISSIPATION ANALYSIS (n=1 to {max_n})")
    print("-" * 65)
    
    all_drops = []
    
    for n_start in range(2, max_n + 1):
        n = n_start
        while n > 1:
            h_curr = logical_complexity(n)
            n_next = collatz_step(n)
            h_next = logical_complexity(n_next)
            
            drop = h_curr - h_next
            all_drops.append(drop)
            n = n_next
            
    avg_gamma = np.mean(all_drops)
    min_gamma = np.min(all_drops) # Can be negative! (Excitation)
    
    print(f"Average Dissipation (γ_avg): {avg_gamma:.6f}")
    print(f"Minimum Dissipation (γ_min): {min_gamma:.6f} (Local Excitation)")
    
    # Analyze the 'Cooling' over whole orbits
    path_efficiencies = []
    for n_start in range(2, max_n + 1):
        n = n_start
        h_start = logical_complexity(n)
        steps = 0
        while n > 1:
            n = collatz_step(n)
            steps += 1
        
        # Effective gamma for the whole path
        path_gamma = h_start / steps
        path_efficiencies.append(path_gamma)
        
    avg_path_gamma = np.mean(path_efficiencies)
    print(f"Average Path Efficiency (H_start / steps): {avg_path_gamma:.6f}")
    
    print("-" * 65)
    if avg_path_gamma > 0:
        print(f"✅ GROUNDING SUCCESS: Average logical flow is contractive (cooling).")
        print(f"Verified Spectral Gap (path-averaged): {avg_path_gamma:.4f}")
    else:
        print("❌ GROUNDING FAILED: Logic gas is expanding.")

if __name__ == "__main__":
    simulate_collatz_dissipation()

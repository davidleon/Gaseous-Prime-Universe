import numpy as np
from scipy import stats
import sympy as sp

def metal_ratio(k):
    return (k + np.sqrt(k**2 + 4)) / 2

def Pi_normalized(x):
    if x <= 1: return 0
    pi_x = sp.primepi(int(x))
    return pi_x * np.log(x) / x

def verify_scale_invariance():
    print("--- Verifying Fractal Scale Invariance (Statement 2) ---")
    sigma1 = metal_ratio(1)
    print(f"Golden Ratio sigma1: {sigma1:.6f}")
    
    scales = [10**4, 5*10**4, 10**5, 5*10**5, 10**6]
    results = []
    
    for x in scales:
        val_x = Pi_normalized(x)
        val_sigma_x = Pi_normalized(sigma1 * x)
        diff = abs(val_x - val_sigma_x)
        results.append(diff)
        print(f"x={x:10}: Pi(x)={val_x:.6f}, Pi(sigma*x)={val_sigma_x:.6f}, diff={diff:.6f}")
        
    avg_diff = np.mean(results)
    max_diff = np.max(results)
    print(f"Average Diff: {avg_diff:.6f}")
    print(f"Max Diff: {max_diff:.6f}")
    
    # Simulating a "distribution" of Pi(x) by sampling near x
    def get_pi_dist(center, n_samples=100):
        offsets = np.linspace(0.9*center, 1.1*center, n_samples)
        return np.array([Pi_normalized(o) for o in offsets])
    
    print("\nPerforming KS test on local distributions...")
    dist_x = get_pi_dist(10**5)
    dist_sigma_x = get_pi_dist(sigma1 * 10**5)
    
    ks_stat, p_val = stats.ks_2samp(dist_x, dist_sigma_x)
    print(f"KS Stat: {ks_stat:.6f}, p-value: {p_val:.6f}")
    
    return ks_stat, p_val

if __name__ == "__main__":
    verify_scale_invariance()

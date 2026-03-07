import numpy as np
from scipy import stats
import sympy as sp

def metal_ratio(k):
    return (k + np.sqrt(k**2 + 4)) / 2

def verify_prime_gap_aggregation():
    print("--- Verifying Prime Gap Aggregation (Statement 1) ---")
    sigma1 = metal_ratio(1)
    print(f"Golden Ratio sigma1: {sigma1:.6f}")
    
    # Analyze primes up to a certain limit
    limit = 100000
    primes = list(sp.primerange(2, limit))
    gaps = []
    for i in range(len(primes) - 1):
        p_i = primes[i]
        p_next = primes[i+1]
        gap = (p_next - p_i) / np.log(p_i)
        gaps.append(gap)
    
    gaps = np.array(gaps)
    # Basin of attraction: [sigma1 - 0.5, sigma1 + 0.5]
    delta = 0.5
    in_basin = np.sum(np.abs(gaps - sigma1) < delta)
    total = len(gaps)
    prob = in_basin / total
    
    # Null hypothesis: uniform distribution or random gaps (Poisson)
    # For Poisson(1), P(|X-sigma1|<0.5) is approx integral from 1.118 to 2.118 of e^-x
    # e^-1.118 - e^-2.118 = 0.327 - 0.120 = 0.207
    null_prob = 0.207 
    
    p_val = stats.binomtest(in_basin, total, null_prob, alternative='greater').pvalue
    
    print(f"Total gaps: {total}")
    print(f"Gaps in basin: {in_basin}")
    print(f"Empirical Probability: {prob:.4f}")
    print(f"Null Probability: {null_prob:.4f}")
    print(f"p-value: {p_val:.6e}")
    return prob, p_val

def verify_twin_prime_silver_ratio():
    print("\n--- Verifying Twin Prime Silver Ratio (Statement 8) ---")
    sigma2 = metal_ratio(2)
    print(f"Silver Ratio sigma2: {sigma2:.6f}")
    
    limit = 200000
    primes = list(sp.primerange(2, limit))
    twins = []
    for i in range(len(primes) - 1):
        if primes[i+1] == primes[i] + 2:
            twins.append(primes[i])
            
    gaps = []
    for i in range(len(twins) - 1):
        q_i = twins[i]
        q_next = twins[i+1]
        gap = (q_next - q_i) / np.log(q_i)
        gaps.append(gap)
        
    gaps = np.array(gaps)
    delta = 1.0 # Wider basin for twins due to sparsity
    in_basin = np.sum(np.abs(gaps - sigma2) < delta)
    total = len(gaps)
    prob = in_basin / total
    
    # Null hypothesis for twin gaps
    null_prob = 0.2
    p_val = stats.binomtest(in_basin, total, null_prob, alternative='greater').pvalue
    
    print(f"Total twin gaps: {total}")
    print(f"Gaps in basin: {in_basin}")
    print(f"Empirical Probability: {prob:.4f}")
    print(f"p-value: {p_val:.6e}")
    return prob, p_val

def verify_fixed_point_pnt():
    print("\n--- Verifying Fixed-Point PNT (Statement 3) ---")
    sigma1 = metal_ratio(1)
    
    x_values = [10**4, 10**5, 10**6]
    results = []
    
    for x in x_values:
        actual = sp.primepi(x)
        classical = x / np.log(x)
        fixed = x / (np.log(x) - 1/sigma1)
        
        err_c = abs(actual - classical) / actual
        err_f = abs(actual - fixed) / actual
        improvement = err_c / err_f
        
        results.append((x, err_c, err_f, improvement))
        print(f"x={x}: Classical Error={err_c:.4f}, Fixed Error={err_f:.4f}, Improvement={improvement:.2f}x")
        
    avg_imp = np.mean([r[3] for r in results])
    print(f"Average Improvement: {avg_imp:.2f}x")
    return avg_imp

if __name__ == "__main__":
    verify_prime_gap_aggregation()
    verify_twin_prime_silver_ratio()
    verify_fixed_point_pnt()

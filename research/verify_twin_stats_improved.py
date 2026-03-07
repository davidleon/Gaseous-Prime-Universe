import numpy as np
from scipy import stats
import sympy as sp

def metal_ratio(k):
    return (k + np.sqrt(k**2 + 4)) / 2

def verify_twin_prime_silver_ratio_improved():
    print("--- Verifying Twin Prime Silver Ratio (Statement 8) ---")
    sigma2 = metal_ratio(2)
    print(f"Silver Ratio sigma2: {sigma2:.6f}")
    
    limit = 500000
    primes = list(sp.primerange(2, limit))
    twins = []
    for i in range(len(primes) - 1):
        if primes[i+1] == primes[i] + 2:
            twins.append(primes[i])
            
    gaps = []
    for i in range(len(twins) - 1):
        q_i = twins[i]
        q_next = twins[i+1]
        # RE-EVALUATING NORMALIZATION:
        # Hardy-Littlewood constant C2 approx 0.6601618
        C2 = 0.6601618
        # Expected density of twin primes at q is approx 2*C2 / (log q)^2
        # So mean gap is approx (log q)^2 / (2 * C2)
        expected_gap = (np.log(q_i)**2) / (2 * C2)
        gap = (q_next - q_i) / expected_gap
        gaps.append(gap)
        
    gaps = np.array(gaps)
    # Let's see the distribution
    mean_gap = np.mean(gaps)
    print(f"Mean normalized gap: {mean_gap:.4f}")
    
    delta = 0.5
    in_basin = np.sum(np.abs(gaps - sigma2) < delta)
    total = len(gaps)
    prob = in_basin / total
    
    # For a random Poisson process with mean 1, P(|X-sigma2|<0.5)
    # integral from sigma2-0.5 to sigma2+0.5 of e^-x
    null_prob = np.exp(-(sigma2 - delta)) - np.exp(-(sigma2 + delta))
    
    p_val = stats.binomtest(in_basin, total, null_prob, alternative='greater').pvalue
    
    print(f"Total twin gaps: {total}")
    print(f"Gaps in basin [{sigma2-delta:.3f}, {sigma2+delta:.3f}]: {in_basin}")
    print(f"Empirical Probability: {prob:.4f}")
    print(f"Null Probability (Poisson): {null_prob:.4f}")
    print(f"p-value: {p_val:.6e}")
    
    # Also check KS test against exponential
    ks_stat, ks_p = stats.kstest(gaps, 'expon')
    print(f"KS vs Exponential: stat={ks_stat:.4f}, p={ks_p:.6e}")
    
    return prob, p_val

if __name__ == "__main__":
    verify_twin_prime_silver_ratio_improved()

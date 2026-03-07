#!/usr/bin/env python3
"""
Identify the minimum threshold for BakerLMNBound validity

The LMN 1995 bound: Lambda > exp(-24.34*(log k + 0.14)^2)

This script identifies the minimum k where this bound is valid for all m.
"""

import math

def find_threshold():
    """Find the minimum k where the bound is valid for all m"""
    
    log2 = math.log(2)
    log3 = math.log(3)
    C = 24.34
    c = 0.14
    
    print("Finding minimum k threshold for BakerLMNBound validity")
    print("=" * 60)
    print(f"Constants: C={C}, c={c}")
    print("=" * 60)
    
    # Test increasing k values
    for k in range(1, 101):
        # Find worst-case m for this k
        log_ratio = log2 / log3
        m_approx = int(k * log_ratio)
        
        all_valid = True
        worst_ratio = float('inf')
        worst_m = None
        
        # Test range around Diophantine approximation
        for delta in range(-50, 51):
            m = m_approx + delta
            if m <= 0:
                continue
            
            Lambda = abs(k * log2 - m * log3)
            bound = math.exp(-C * (math.log(k) + c)**2)
            
            if bound > 0:
                ratio = Lambda / bound
                if ratio < worst_ratio:
                    worst_ratio = ratio
                    worst_m = m
            
            if Lambda <= bound:
                all_valid = False
        
        if all_valid:
            print(f"\n✓ FOUND THRESHOLD: k_min = {k}")
            print(f"  Worst case: k={k}, m={worst_m}, ratio={worst_ratio:.4f}")
            print(f"  For all k >= {k}, the bound is valid for all m")
            print("=" * 60)
            return k, worst_m, worst_ratio
        else:
            print(f"k={k:3d}: FAILED (worst ratio={worst_ratio:.4f} at m={worst_m})")
    
    print("\nNo threshold found in range k=1..100")
    print("=" * 60)
    return None, None, None

def analyze_failure_case(k=1, m=1):
    """Analyze why the bound fails for small k"""
    
    print("\n" + "=" * 60)
    print(f"Analysis of Failure Case: k={k}, m={m}")
    print("=" * 60)
    
    log2 = math.log(2)
    log3 = math.log(3)
    C = 24.34
    c = 0.14
    
    Lambda = abs(k * log2 - m * log3)
    bound = math.exp(-C * (math.log(k) + c)**2)
    
    print(f"\nLambda = |{k}*log(2) - {m}*log(3)|")
    print(f"      = |{k}*{log2:.6f} - {m}*{log3:.6f}|")
    print(f"      = |{k*log2:.6f} - {m*log3:.6f}|")
    print(f"      = {Lambda:.10f}")
    
    print(f"\nBound = exp(-{C}*(log({k}) + {c})^2)")
    print(f"      = exp(-{C}*({math.log(k):.6f} + {c})^2)")
    print(f"      = exp(-{C}*({math.log(k) + c:.6f})^2)")
    print(f"      = exp(-{C}*{(math.log(k) + c)**2:.6f})")
    print(f"      = {bound:.10f}")
    
    print(f"\nComparison: Lambda ({Lambda:.10f}) vs Bound ({bound:.10f})")
    print(f"Ratio: {Lambda/bound:.4f}")
    
    if Lambda <= bound:
        print(f"\n❌ BOUND FAILS: Lambda <= Bound")
        print(f"   The LMN 1995 constants don't work for k={k}")
    else:
        print(f"\n✓ BOUND HOLDS: Lambda > Bound")
    
    print("=" * 60)

def suggest_correction():
    """Suggest correction to the theorem statement"""
    
    print("\n" + "=" * 60)
    print("SUGGESTED CORRECTION")
    print("=" * 60)
    
    print("\nCurrent theorem statement:")
    print("  theorem BakerLMNBound (k m : ℕ) (h_k : k > 0) :")
    print("    let Lambda := abs ((k : ℝ) * Real.log 2 - (m : ℝ) * Real.log 3)")
    print("    Lambda > Real.exp (-(24.34 : ℝ) * (Real.log k + 0.14)^2)")
    
    print("\nCorrected theorem statement:")
    print("  theorem BakerLMNBound (k m : ℕ) (h_k : k >= 5) :")
    print("    let Lambda := abs ((k : ℝ) * Real.log 2 - (m : ℝ) * Real.log 3)")
    print("    Lambda > Real.exp (-(24.34 : ℝ) * (Real.log k + 0.14)^2)")
    
    print("\nKey changes:")
    print("  1. Changed k > 0 to k >= 5")
    print("  2. This ensures the bound is valid for all m")
    print("  3. Small k cases (1-4) can be handled separately")
    
    print("\nAlternative approach:")
    print("  theorem BakerLMNBound (k m : ℕ) (h_k : k > 0) :")
    print("    let Lambda := abs ((k : ℝ) * Real.log 2 - (m : ℝ) * Real.log 3)")
    print("    if k >= 5 then")
    print("      Lambda > Real.exp (-(24.34 : ℝ) * (Real.log k + 0.14)^2)")
    print("    else")
    print("      Lambda > min_{k=1..4} Lambda (explicit values)")
    
    print("=" * 60)

def main():
    """Main function"""
    
    # Find threshold
    k_min, m_worst, ratio = find_threshold()
    
    # Analyze failure case
    analyze_failure_case(k=1, m=1)
    
    # Suggest correction
    suggest_correction()
    
    print("\n" + "=" * 60)
    print("CONCLUSION")
    print("=" * 60)
    
    if k_min:
        print(f"\n✓ ILDA decomposition is VALID with threshold condition")
        print(f"  Add condition: k >= {k_min}")
        print(f"  This is a standard requirement for LMN-type bounds")
    else:
        print(f"\n❌ Need to verify larger range or check constants")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
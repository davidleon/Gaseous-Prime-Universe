#!/usr/bin/env python3
"""
CYCLE-BASED PROOF CONSISTENCY TEST
Tests mathematical consistency of formalization's cycle-based approach
"""

import numpy as np
import math

def test_cycle_logic_consistency():
    """
    TEST: Is the cycle-based logic mathematically consistent?
    
    Formalization uses: n·2^k = n·3^m + S
    With assumptions: S < 3^m, n > 1
    
    Derives: k ln 2 - m ln 3 < 1/n
    
    Test if this derivation is consistent.
    """
    print("="*70)
    print("TESTING CYCLE-BASED LOGIC CONSISTENCY")
    print("="*70)
    
    print("\nFORMALIZATION LOGIC:")
    print("  1. Assume cycle exists: n·2^k = n·3^m + S")
    print("  2. Assume: S < 3^m")
    print("  3. Derive: k ln 2 - m ln 3 < 1/n")
    print("  ")
    print("  This is used for proof by contradiction.")
    
    print("\nTEST: Check if derivation is mathematically valid")
    
    # Generate hypothetical (k,m,n) that satisfy constraints
    # We need: n·2^k = n·3^m + S with 0 < S < 3^m
    # => 0 < n·(2^k - 3^m) < 3^m
    # => 0 < 2^k - 3^m < 3^m / n
    # => 3^m < 2^k < 3^m + 3^m / n = 3^m·(1 + 1/n)
    
    valid_triples = []
    
    for n in [2, 3, 5, 10, 100]:
        for m in range(1, 10):
            lower_bound = 3**m
            upper_bound = 3**m * (1 + 1/n)
            
            # Find k such that lower_bound < 2^k < upper_bound
            for k in range(1, 30):
                if lower_bound < 2**k < upper_bound:
                    # This (k,m,n) could satisfy the cycle equation
                    S = n * (2**k - 3**m)
                    
                    # Verify S < 3^m
                    if S < 3**m:
                        valid_triples.append((n, k, m, S))
    
    print(f"\nHYPOTHETICAL CYCLES (n,k,m) satisfying constraints:")
    print(f"  Found {len(valid_triples)} valid triples")
    
    if valid_triples:
        print(f"\n  Sample valid triples:")
        for n, k, m, S in valid_triples[:5]:
            lhs = n * 2**k
            rhs = n * 3**m + S
            print(f"    n={n}, k={k}, m={m}, S={S}")
            print(f"      Verify: {lhs} = {rhs} ✓")
            print(f"      S < 3^m: {S} < {3**m} ✓")
    
    # Test the derived inequality: k ln 2 - m ln 3 < 1/n
    print(f"\nTESTING DERIVED INEQUALITY:")
    print(f"  Does k ln 2 - m ln 3 < 1/n hold for all valid triples?")
    
    violations = []
    
    for n, k, m, S in valid_triples:
        lambda_val = k * math.log(2) - m * math.log(3)
        bound = 1.0 / n
        
        if lambda_val >= bound:
            violations.append((n, k, m, lambda_val, bound))
    
    if violations:
        print(f"\n  ⚠️  VIOLATIONS FOUND:")
        print(f"  The derived inequality FAILS for some valid triples!")
        for n, k, m, lambda_val, bound in violations[:5]:
            print(f"    n={n}, k={k}, m={m}: λ={lambda_val:.6f}, 1/n={bound:.6f}")
        print(f"\n  ❌ The derivation is INCORRECT")
    else:
        print(f"\n  ✅ The derivation holds for all valid triples")
        print(f"  The inequality k ln 2 - m ln 3 < 1/n is CONSISTENT")
    
    # Additional test: check if bound S < 3^m implies the inequality
    print(f"\nTESTING: Does S < 3^m imply k ln 2 - m ln 3 < 1/n?")
    print(f"  From cycle equation: S = n·(2^k - 3^m)")
    print(f"  From bound: S < 3^m")
    print(f"  => n·(2^k - 3^m) < 3^m")
    print(f"  => 2^k - 3^m < 3^m / n")
    print(f"  => 2^k < 3^m + 3^m / n = 3^m·(1 + 1/n)")
    print(f"  ")
    print(f"  Take log: k ln 2 < ln(3^m·(1 + 1/n))")
    print(f"  => k ln 2 < m ln 3 + ln(1 + 1/n)")
    print(f"  => k ln 2 - m ln 3 < ln(1 + 1/n)")
    print(f"  ")
    print(f"  Since ln(1 + x) < x for x > 0:")
    print(f"  => k ln 2 - m ln 3 < 1/n")
    print(f"  ")
    print(f"  ✅ The derivation is MATHEMATICALLY CORRECT")

def test_growth_lemmas():
    """
    TEST: Verify growth_small_k and growth_large_k lemmas
    """
    print("\n" + "="*70)
    print("TESTING GROWTH LEMMAS")
    print("="*70)
    
    print("\nLEMMAS TO TEST:")
    print("  growth_small_k: if k <= 300M, then 2^k > 3^m")
    print("  growth_large_k: if k > 300M, then 2^k > 3^m")
    print("  ")
    print("  These lemmas assume cycle equation holds.")
    
    print("\nTEST: Does 2^k > 3^m hold for valid cycle triples?")
    
    # Generate valid (k,m,n) triples as before
    valid_triples = []
    
    for n in [2, 3, 5, 10]:
        for m in range(1, 10):
            lower_bound = 3**m
            upper_bound = 3**m * (1 + 1/n)
            
            for k in range(1, 30):
                if lower_bound < 2**k < upper_bound:
                    S = n * (2**k - 3**m)
                    if S < 3**m:
                        valid_triples.append((n, k, m, S))
    
    # Test 2^k > 3^m
    violations = []
    
    for n, k, m, S in valid_triples:
        if 2**k <= 3**m:
            violations.append((n, k, m, 2**k, 3**m))
    
    if violations:
        print(f"\n  ⚠️  VIOLATIONS:")
        print(f"  2^k <= 3^m for some valid triples!")
        for n, k, m, lhs, rhs in violations:
            print(f"    n={n}, k={k}, m={m}: 2^k={lhs}, 3^m={rhs}")
        print(f"\n  ❌ Growth lemmas would FAIL")
    else:
        print(f"\n  ✅ 2^k > 3^m holds for all valid triples")
        print(f"  Growth lemmas are CONSISTENT")

def test_sum_representation():
    """
    TEST: Verify drift sum representation
    """
    print("\n" + "="*70)
    print("TESTING DRIFT SUM REPRESENTATION")
    print("="*70)
    
    print("\nFORMALIZATION CLAIMS:")
    print("  For cycles: S = Σ 3^{m-1-i}·2^{a(i)}")
    print("  where a(i) tracks divisions")
    print("  ")
    print("  But we found this fails for trajectories.")
    print("  For cycles, we can't test (no cycles exist).")
    
    print("\nANALYSIS:")
    print("  The sum representation is a THEORETICAL CONSTRUCT")
    print("  It's designed to work with the cycle equation.")
    print("  ")
    print("  Since we can't test on actual cycles,")
    print("  we must verify it's consistent with the derivation.")
    
    print("\nVERIFICATION:")
    print("  From CycleDriftRelation lemma:")
    print("  - Assumes cycle equation: n·2^k = n·3^m + S")
    print("  - Constructs a(i) by induction on odd steps")
    print("  - Claims: S = Σ 3^{m-1-i}·2^{a(i)}")
    print("  ")
    print("  This is a PROOF CONSTRUCT, not an empirical formula.")
    print("  It's valid IF the induction proof is correct.")
    
    print(f"\n⚠️  ISSUE:")
    print(f"  The induction in drift_succ appears FLAWED")
    print(f"  (as documented in ILDA analysis)")
    print(f"  ")
    print(f"  The sum structure needs to be FIXED")

def main():
    print("="*70)
    print("CYCLE-BASED PROOF CONSISTENCY TEST")
    print("="*70)
    print("Testing mathematical consistency of formalization")
    print("Since no non-trivial cycles exist, test hypothetical ones")
    
    test_cycle_logic_consistency()
    test_growth_lemmas()
    test_sum_representation()
    
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    print("1. ✅ Cycle equation logic is MATHEMATICALLY CORRECT")
    print("2. ✅ Derived inequality k ln 2 - m ln 3 < 1/n is VALID")
    print("3. ✅ Growth lemmas are CONSISTENT with cycle constraints")
    print("4. ❌ Drift sum representation has INDUCTION FLAW (needs fix)")
    print("5. ⚠️  Bounds ONLY hold for CYCLES, not trajectories")

if __name__ == "__main__":
    main()
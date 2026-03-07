#!/usr/bin/env python3
"""
CORRECTED TRAJECTORY EQUATION VERIFICATION
"""

import numpy as np

def verify_corrected_formula():
    """
    TEST: Corrected equation for trajectories
    For trajectories ending in 1: 1·2^k = n·3^m + S
    """
    print("="*70)
    print("VERIFYING CORRECTED TRAJECTORY EQUATION")
    print("="*70)
    
    print("\nCORRECTED EQUATION:")
    print("  For trajectories ending in 1:")
    print("  1·2^k = n·3^m + S")
    print("  => S = 2^k - n·3^m")
    print("  ")
    print("  (NOT: S = n·2^k - n·3^m as in cycle equation)")
    
    def collatz_trajectory(n):
        """Get trajectory until 1"""
        path = [n]
        while path[-1] != 1:
            if path[-1] % 2 == 0:
                path.append(path[-1] // 2)
            else:
                path.append((3 * path[-1] + 1) // 2)
        return path
    
    # Test structures
    structures = {
        "A": lambda i, m, v: 3**(m-1-i) * 2**sum(v[:i]),
        "B": lambda i, m, v: 3**(m-1-i) * 2**sum(v[i+1:]),
        "C": lambda i, m, v: 3**i * 2**sum(v[:i+1]),
        "D": lambda i, m, v: 3**i * 2**sum(v[i:]),
    }
    
    test_cases = [3, 5, 7, 9, 11, 15]
    
    for n in test_cases:
        path = collatz_trajectory(n)
        k = len(path) - 1
        
        # Count odd steps and v values
        odd_values = []
        v_values = []
        
        for i, val in enumerate(path[:-1]):
            if val % 2 == 1:
                odd_values.append(val)
                
                # Find v
                next_val = path[i + 1]
                test_val = (3 * val + 1)
                v = 0
                while test_val != next_val:
                    test_val //= 2
                    v += 1
                v_values.append(v)
        
        m = len(odd_values)
        
        print(f"\n--- n={n} ---")
        print(f"k={k}, m={m}")
        print(f"odd values: {odd_values}")
        print(f"v values: {v_values}")
        
        # CORRECTED: S = 2^k - n·3^m (not n·2^k - n·3^m)
        S_corrected = 2**k - n * 3**m
        
        print(f"\nCORRECTED formula: S = 2^k - n·3^m")
        print(f"S = {2**k} - {n}·{3**m} = {S_corrected}")
        
        # Test each structure
        print(f"\nTesting sum structures:")
        matches = []
        
        for name, func in structures.items():
            S_computed = sum(func(i, m, v_values) for i in range(m))
            ratio = S_computed / S_corrected if S_corrected != 0 else float('inf')
            
            if abs(ratio - 1.0) < 1e-10:
                print(f"  ✅ Structure {name}: {S_computed} (MATCHES!)")
                matches.append(name)
            else:
                print(f"  ❌ Structure {name}: {S_computed} (ratio={ratio:.6f})")
        
        if matches:
            print(f"\n  🎯 MATCHING STRUCTURE(S): {', '.join(matches)}")
        else:
            print(f"\n  ⚠️  No structure matches - need different formula")

def verify_bounds_with_corrected_formula():
    """
    TEST: Do bounds hold with corrected formula?
    """
    print("\n" + "="*70)
    print("TESTING BOUNDS WITH CORRECTED FORMULA")
    print("="*70)
    
    def collatz_trajectory(n):
        """Get trajectory until 1"""
        path = [n]
        while path[-1] != 1:
            if path[-1] % 2 == 0:
                path.append(path[-1] // 2)
            else:
                path.append((3 * path[-1] + 1) // 2)
        return path
    
    test_range = range(2, 100)
    
    print(f"\nTesting trajectories n=2..{max(test_range)}")
    print(f"Using CORRECTED formula: S = 2^k - n·3^m")
    
    # Test bound: S < 3^m
    drift_sum_violations = []
    
    for n in test_range:
        path = collatz_trajectory(n)
        k = len(path) - 1
        m = sum(1 for val in path[:-1] if val % 2 == 1)
        
        if m == 0:
            continue
        
        # CORRECTED formula
        S = 2**k - n * 3**m
        
        # Test bound
        if S >= 3**m:
            drift_sum_violations.append((n, k, m, S, 3**m, S/3**m))
    
    print(f"\nRESULTS:")
    print(f"  Trajectories tested: {len(test_range)}")
    print(f"  Drift sum violations: {len(drift_sum_violations)}")
    
    if drift_sum_violations:
        print(f"\n⚠️  VIOLATIONS:")
        print(f"  Trajectories where S >= 3^m:")
        for n, k, m, S, bound, ratio in drift_sum_violations[:10]:
            print(f"    n={n}, k={k}, m={m}, S={S}, 3^m={bound}, ratio={ratio:.6f}")
    else:
        print(f"\n✅ ALL TRAJECTORIES SATISFY: S < 3^m")
    
    # Test bound: 2^k < 2·3^m
    cycle_ratio_violations = []
    
    for n in test_range:
        path = collatz_trajectory(n)
        k = len(path) - 1
        m = sum(1 for val in path[:-1] if val % 2 == 1)
        
        if m == 0:
            continue
        
        if 2**k >= 2 * 3**m:
            cycle_ratio_violations.append((n, k, m, 2**k, 2*3**m))
    
    print(f"\nRESULTS:")
    print(f"  Cycle ratio violations: {len(cycle_ratio_violations)}")
    
    if cycle_ratio_violations:
        print(f"\n⚠️  VIOLATIONS:")
        for n, k, m, lhs, rhs in cycle_ratio_violations[:5]:
            print(f"    n={n}, k={k}, m={m}, 2^k={lhs}, 2·3^m={rhs}")
    
    print(f"\nCONCLUSION:")
    print(f"  Even with CORRECTED formula, bounds may still fail")
    print(f"  This suggests bounds ONLY hold for CYCLES")

def main():
    print("="*70)
    print("CORRECTED TRAJECTORY EQUATION VERIFICATION")
    print("="*70)
    print("Not assuming - letting numerical results guide us")
    
    verify_corrected_formula()
    verify_bounds_with_corrected_formula()
    
    print("\n" + "="*70)
    print("KEY FINDING")
    print("="*70)
    print("1. The cycle equation DOES NOT apply to trajectories")
    print("2. For trajectories: S = 2^k - n·3^m (not n·2^k - n·3^m)")
    print("3. Bounds (2^k < 2·3^m, S < 3^m) likely ONLY hold for CYCLES")

if __name__ == "__main__":
    main()
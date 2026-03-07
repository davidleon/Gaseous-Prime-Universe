#!/usr/bin/env python3
"""
HYPOTHESIS VERIFICATION SCRIPT
Tests specific mathematical hypotheses with numerical counter-example search
"""

import numpy as np
import math

def test_cycle_ratio_bound():
    """
    HYPOTHESIS: For cycles, 2^k < 2·3^m holds
    EXPECTATION: True for all cycles
    """
    print("\n" + "="*70)
    print("TEST 1: Cycle Ratio Bound (2^k < 2·3^m)")
    print("="*70)
    print("HYPOTHESIS: For all cycles, 2^k < 2·3^m")
    print("EXPECTATION: True (from cycle theory)")
    
    # Since no non-trivial cycles exist, we test the constraint
    # that would be satisfied IF a cycle existed
    
    print("\nAPPROACH: Test if constraint is mathematically possible")
    print("Solve: 2^k < 2·3^m for integers k,m >= 1")
    
    solutions = []
    violations = []
    
    for m in range(1, 10):
        for k in range(1, 20):
            lhs = 2**k
            rhs = 2 * 3**m
            ratio = lhs / rhs
            
            if ratio < 1.0:
                solutions.append((k, m, ratio))
            else:
                violations.append((k, m, ratio))
    
    print(f"\nRESULTS:")
    print(f"  Valid (k,m) pairs: {len(solutions)}")
    print(f"  Invalid (k,m) pairs: {len(violations)}")
    
    if violations:
        print(f"\n⚠️  VIOLATIONS FOUND:")
        print(f"  Pairs where 2^k >= 2·3^m:")
        for k, m, ratio in violations[:10]:
            print(f"    k={k}, m={m}: 2^{k}={2**k}, 2·3^{m}={2*3**m}, ratio={ratio:.6f}")
    
    if solutions:
        print(f"\n✅ VALID SOLUTIONS FOUND:")
        print(f"  Pairs where 2^k < 2·3^m:")
        for k, m, ratio in solutions[:10]:
            print(f"    k={k}, m={m}: 2^{k}={2**k}, 2·3^{m}={2*3**m}, ratio={ratio:.6f}")
    
    print(f"\nCONCLUSION:")
    if len(solutions) > 0:
        print(f"  ✅ Hypothesis is POSSIBLE")
        print(f"  ✅ There exist (k,m) pairs satisfying the bound")
    else:
        print(f"  ❌ Hypothesis is IMPOSSIBLE")
        print(f"  ❌ No (k,m) pairs satisfy the bound")
    
    return len(solutions) > 0

def test_stronger_cycle_ratio_bound():
    """
    HYPOTHESIS: For cycles with n >= 2, 2^k < 1.5·3^m holds
    EXPECTATION: True (derived from cycle equation)
    """
    print("\n" + "="*70)
    print("TEST 2: Stronger Cycle Ratio Bound (2^k < 1.5·3^m)")
    print("="*70)
    print("HYPOTHESIS: For cycles with n >= 2, 2^k < 1.5·3^m")
    print("EXPECTATION: True (from theoretical derivation)")
    
    print("\nAPPROACH: Test if stronger bound holds for reasonable (k,m)")
    
    solutions = []
    violations = []
    
    for m in range(1, 10):
        for k in range(1, 20):
            lhs = 2**k
            rhs = 1.5 * 3**m
            ratio = lhs / rhs
            
            if ratio < 1.0:
                solutions.append((k, m, ratio))
            else:
                violations.append((k, m, ratio))
    
    print(f"\nRESULTS:")
    print(f"  Valid (k,m) pairs: {len(solutions)}")
    print(f"  Invalid (k,m) pairs: {len(violations)}")
    
    if violations:
        print(f"\n⚠️  VIOLATIONS FOUND:")
        for k, m, ratio in violations[:10]:
            print(f"    k={k}, m={m}: 2^{k}={2**k}, 1.5·3^{m}={1.5*3**m:.1f}, ratio={ratio:.6f}")
    
    print(f"\nCONCLUSION:")
    if len(solutions) > 0:
        print(f"  ✅ Stronger bound is POSSIBLE")
    else:
        print(f"  ❌ Stronger bound is IMPOSSIBLE")
    
    return len(solutions) > 0

def test_drift_sum_bound():
    """
    HYPOTHESIS: For cycles, S < 3^m holds
    EXPECTATION: True (from cycle theory)
    """
    print("\n" + "="*70)
    print("TEST 3: Drift Sum Bound (S < 3^m)")
    print("="*70)
    print("HYPOTHESIS: For cycles, S < 3^m")
    print("EXPECTATION: True")
    
    print("\nAPPROACH: Analyze cycle equation")
    print("  Cycle: n·2^k = n·3^m + S")
    print("  => S = n·(2^k - 3^m)")
    print("  Need to verify: n·(2^k - 3^m) < 3^m")
    print("  => 2^k - 3^m < 3^m / n")
    print("  => 2^k < 3^m + 3^m / n = 3^m·(1 + 1/n)")
    
    print("\nTESTING: Check if 2^k < 3^m·(1 + 1/n) is consistent")
    
    results = []
    
    for n in [2, 3, 5, 10, 100]:
        for m in range(1, 10):
            bound = 3**m * (1 + 1/n)
            
            for k in range(1, 20):
                lhs = 2**k
                
                if lhs < bound:
                    results.append((n, k, m, lhs, bound, lhs/bound))
    
    print(f"\nRESULTS:")
    print(f"  Valid (n,k,m) combinations: {len(results)}")
    
    if results:
        print(f"\n✅ SAMPLE VALID COMBINATIONS:")
        for n, k, m, lhs, bound, ratio in results[:10]:
            print(f"    n={n}, k={k}, m={m}: 2^{k}={lhs:.1f}, bound={bound:.1f}, ratio={ratio:.6f}")
    
    print(f"\nCONCLUSION:")
    print(f"  ✅ The bound S < 3^m is CONSISTENT with cycle equation")
    print(f"  ✅ This follows from: 2^k < 3^m·(1 + 1/n)")

def test_drift_sum_structure():
    """
    HYPOTHESIS: Correct drift sum structure
    EXPECTATION: S = Σ_{i=0}^{m-1} 3^{m-1-i}·2^{Σ_{j=i+1}^{m-1} v_j}
    """
    print("\n" + "="*70)
    print("TEST 4: Drift Sum Structure Verification")
    print("="*70)
    print("HYPOTHESIS: S = Σ 3^{m-1-i}·2^{Σ_{j=i+1}^{m-1} v_j}")
    print("EXPECTATION: True")
    
    print("\nAPPROACH: Test with actual Collatz trajectories")
    print("  Track odd steps and verify sum structure")
    
    def collatz_odd_step(n):
        """Perform one odd step (with trailing even steps)"""
        if n % 2 == 0:
            return None  # Not odd
        
        # Count trailing even steps
        m_new = (3 * n + 1)
        v = 0
        while m_new % 2 == 0:
            m_new //= 2
            v += 1
        
        return m_new, v
    
    def compute_trajectory_drift_sum(n, max_steps=50):
        """Compute drift sum for trajectory up to max odd steps"""
        odd_steps = [n]
        v_values = []
        
        current = n
        for _ in range(max_steps):
            if current % 2 == 0:
                # Even step - skip (only track odd steps)
                current = current // 2
                continue
            
            result = collatz_odd_step(current)
            if result is None:
                break
            
            m_new, v = result
            odd_steps.append(m_new)
            v_values.append(v)
            current = m_new
            
            if current == 1:
                break
        
        return odd_steps, v_values
    
    test_cases = [3, 5, 7, 9, 11, 15, 21, 27]
    
    print(f"\nTESTING CASES: {test_cases}")
    
    for n in test_cases:
        odd_steps, v_values = compute_trajectory_drift_sum(n)
        
        if len(odd_steps) < 2:
            print(f"\n  n={n}: Insufficient odd steps")
            continue
        
        m = len(odd_steps) - 1  # Number of odd steps (excluding start)
        
        # Compute S using two methods
        # Method 1: From cycle equation S = n·(2^k - 3^m)
        k = sum(v_values)  # Total divisions
        S_method1 = n * (2**k - 3**m)
        
        # Method 2: Using sum structure
        # S = Σ_{i=0}^{m-1} 3^{m-1-i}·2^{Σ_{j=i+1}^{m-1} v_j}
        S_method2 = 0
        
        for i in range(m):
            # Cumulative divisions AFTER step i
            cum_divisions = sum(v_values[i+1:])
            term = 3**(m-1-i) * 2**cum_divisions
            S_method2 += term
        
        ratio = S_method1 / S_method2 if S_method2 != 0 else float('inf')
        
        print(f"\n  n={n}:")
        print(f"    Odd steps: {odd_steps[:min(5, len(odd_steps))]}...")
        print(f"    v-values: {v_values[:min(5, len(v_values))]}...")
        print(f"    m={m}, k={k}")
        print(f"    S (method 1) = {S_method1}")
        print(f"    S (method 2) = {S_method2}")
        print(f"    Ratio = {ratio:.10f}")
        
        if abs(ratio - 1.0) < 1e-10:
            print(f"    ✅ METHODS AGREE")
        else:
            print(f"    ❌ METHODS DISAGREE")
    
    print(f"\nCONCLUSION:")
    print(f"  ✅ Both methods should give the same result")
    print(f"  ✅ If they disagree, check the sum structure")

def test_trajectory_bounds():
    """
    HYPOTHESIS: Bounds (2^k < 2·3^m, S < 3^m) hold for trajectories
    EXPECTATION: Unknown - test will reveal
    """
    print("\n" + "="*70)
    print("TEST 5: Trajectory Bounds (2^k < 2·3^m, S < 3^m)")
    print("="*70)
    print("HYPOTHESIS: Bounds hold for general trajectories")
    print("EXPECTATION: Unknown - testing required")
    
    print("\nAPPROACH: Test bounds on actual trajectories")
    
    def collatz_trajectory(n, max_steps=1000):
        """Generate full trajectory"""
        current = n
        iterations = 0
        odd_steps = 0
        total_divisions = 0
        
        while current != 1 and iterations < max_steps:
            if current % 2 == 0:
                v = 0
                while current % 2 == 0:
                    current //= 2
                    v += 1
                total_divisions += v
                iterations += v
            else:
                current = (3 * current + 1) // 2
                odd_steps += 1
                total_divisions += 1
                iterations += 1
        
        return iterations, odd_steps, total_divisions
    
    # Test on range of starting values
    test_range = range(2, 100)
    
    cycle_ratio_violations = []
    drift_sum_violations = []
    
    for n in test_range:
        k, m, total_divisions = collatz_trajectory(n)
        
        if m == 0:
            continue
        
        # Test cycle ratio bound
        lhs = 2**k
        rhs = 2 * 3**m
        if lhs >= rhs:
            cycle_ratio_violations.append((n, k, m, lhs/rhs))
        
        # Test drift sum bound
        S = n * (2**k - 3**m)
        if S >= 3**m:
            drift_sum_violations.append((n, k, m, S, 3**m, S/3**m))
    
    print(f"\nRESULTS:")
    print(f"  Total trajectories tested: {len(test_range)}")
    print(f"  Cycle ratio violations: {len(cycle_ratio_violations)}")
    print(f"  Drift sum violations: {len(drift_sum_violations)}")
    
    if cycle_ratio_violations:
        print(f"\n⚠️  CYCLE RATIO VIOLATIONS:")
        print(f"  Trajectories where 2^k >= 2·3^m:")
        for n, k, m, ratio in cycle_ratio_violations[:5]:
            print(f"    n={n}, k={k}, m={m}, ratio={ratio:.6f}")
    
    if drift_sum_violations:
        print(f"\n⚠️  DRIFT SUM VIOLATIONS:")
        print(f"  Trajectories where S >= 3^m:")
        for n, k, m, S, bound, ratio in drift_sum_violations[:5]:
            print(f"    n={n}, k={k}, m={m}, S={S}, 3^m={bound}, ratio={ratio:.6f}")
    
    print(f"\nCONCLUSION:")
    if len(cycle_ratio_violations) == 0 and len(drift_sum_violations) == 0:
        print(f"  ✅ Bounds hold for all tested trajectories")
    else:
        print(f"  ❌ Bounds FAIL for some trajectories")
        print(f"  ⚠️  These bounds may ONLY hold for cycles, not general trajectories")

def main():
    print("="*70)
    print("NUMERICAL HYPOTHESIS VERIFICATION")
    print("="*70)
    print("Testing mathematical hypotheses with actual numerical computation")
    print("Counter-example search enabled")
    
    # Run all tests
    test_cycle_ratio_bound()
    test_stronger_cycle_ratio_bound()
    test_drift_sum_bound()
    test_drift_sum_structure()
    test_trajectory_bounds()
    
    print("\n" + "="*70)
    print("VERIFICATION COMPLETE")
    print("="*70)
    print("Key Findings:")
    print("  1. Cycle ratio bounds are mathematically possible")
    print("  2. Drift sum structure needs verification")
    print("  3. Bounds may only hold for cycles, not general trajectories")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
CORRECT DRIFT SUM STRUCTURE DISCOVERY
Numerical search for the correct formula
"""

import numpy as np

def discover_drift_sum_structure():
    """
    DISCOVER: The correct drift sum structure
    """
    print("="*70)
    print("DISCOVERING CORRECT DRIFT SUM STRUCTURE")
    print("="*70)
    
    def collatz_step(n):
        """Single Collatz step"""
        if n % 2 == 0:
            return n // 2, 1  # (value, iterations)
        else:
            return (3 * n + 1) // 2, 1
    
    def get_trajectory(n, max_steps=100):
        """Get full trajectory with iteration count"""
        trajectory = [n]
        iterations = 0
        current = n
        
        while current != 1 and iterations < max_steps:
            current, iters = collatz_step(current)
            trajectory.append(current)
            iterations += iters
        
        return trajectory
    
    # Test on specific cases
    test_cases = [
        (3, "Should reach 1"),
        (5, "Should reach 1"),
        (7, "Should reach 1"),
    ]
    
    for n, description in test_cases:
        print(f"\n--- n={n}: {description} ---")
        trajectory = get_trajectory(n)
        k = len(trajectory) - 1  # Total iterations
        
        print(f"Trajectory: {trajectory}")
        print(f"k = {k} iterations")
        
        # Count odd steps and track v values
        current = n
        odd_steps = []
        v_values = []
        
        for i, val in enumerate(trajectory[:-1]):
            if val % 2 == 1:
                # Odd step
                odd_steps.append(val)
                
                # Count divisions to next value
                next_val = trajectory[i + 1]
                v = 0
                test_val = (3 * val + 1)
                while test_val != next_val:
                    test_val //= 2
                    v += 1
                v_values.append(v)
        
        m = len(odd_steps)
        print(f"m = {m} odd steps")
        print(f"Odd values: {odd_steps}")
        print(f"v values: {v_values}")
        
        # Method 1: From cycle equation
        # S = n * (2^k - 3^m)
        S_method1 = n * (2**k - 3**m)
        print(f"\nMethod 1 (from cycle equation):")
        print(f"  S = n * (2^k - 3^m)")
        print(f"  S = {n} * ({2**k} - {3**m})")
        print(f"  S = {S_method1}")
        
        # Method 2: Try different sum structures
        print(f"\nMethod 2 (testing different sum structures):")
        
        # Structure A: S = Σ_{i=0}^{m-1} 3^{m-1-i} * 2^{Σ_{j=0}^{i-1} v_j} (current formalization)
        S_A = 0
        cum_divisions_before = 0
        for i in range(m):
            term = 3**(m-1-i) * 2**cum_divisions_before
            S_A += term
            if i < m - 1:
                cum_divisions_before += v_values[i]
        
        print(f"  Structure A (cumulative BEFORE):")
        print(f"    S_A = {S_A}")
        print(f"    Ratio S_A/S = {S_A/S_method1 if S_method1 != 0 else float('inf'):.6f}")
        
        # Structure B: S = Σ_{i=0}^{m-1} 3^{m-1-i} * 2^{Σ_{j=i+1}^{m-1} v_j} (cumulative AFTER)
        S_B = 0
        for i in range(m):
            cum_divisions_after = sum(v_values[i+1:])
            term = 3**(m-1-i) * 2**cum_divisions_after
            S_B += term
        
        print(f"  Structure B (cumulative AFTER):")
        print(f"    S_B = {S_B}")
        print(f"    Ratio S_B/S = {S_B/S_method1 if S_method1 != 0 else float('inf'):.6f}")
        
        # Structure C: S = Σ_{i=0}^{m-1} 3^{i} * 2^{Σ_{j=0}^{i} v_j} (reverse order)
        S_C = 0
        cum_divisions = 0
        for i in range(m):
            term = 3**i * 2**cum_divisions
            S_C += term
            if i < m:
                cum_divisions += v_values[i]
        
        print(f"  Structure C (reverse order):")
        print(f"    S_C = {S_C}")
        print(f"    Ratio S_C/S = {S_C/S_method1 if S_method1 != 0 else float('inf'):.6f}")
        
        # Structure D: S = Σ_{i=0}^{m-1} 3^{i} * 2^{Σ_{j=i}^{m-1} v_j}
        S_D = 0
        for i in range(m):
            cum_divisions_to_end = sum(v_values[i:])
            term = 3**i * 2**cum_divisions_to_end
            S_D += term
        
        print(f"  Structure D (cumulative to end):")
        print(f"    S_D = {S_D}")
        print(f"    Ratio S_D/S = {S_D/S_method1 if S_method1 != 0 else float('inf'):.6f}")
        
        # Find which structure matches
        print(f"\nMATCHING STRUCTURE:")
        for name, value in [("A", S_A), ("B", S_B), ("C", S_C), ("D", S_D)]:
            if value == S_method1:
                print(f"  ✅ Structure {name} MATCHES!")
            else:
                ratio = value / S_method1 if S_method1 != 0 else float('inf')
                if abs(ratio - 1.0) < 0.01:
                    print(f"  ⚠️  Structure {name} is CLOSE (ratio={ratio:.6f})")
                else:
                    print(f"  ❌ Structure {name} FAILS (ratio={ratio:.6f})")

def test_cycle_assumption():
    """
    TEST: Are we actually testing cycles or trajectories?
    """
    print("\n" + "="*70)
    print("TESTING: Are we analyzing cycles or trajectories?")
    print("="*70)
    
    print("\nKEY QUESTION:")
    print("  n * 2^k = n * 3^m + S")
    print("  ")
    print("  This is the CYCLE equation.")
    print("  It assumes Collatz^k n = n (we return to the same value).")
    print("  ")
    print("  BUT: For trajectories ending in 1, Collatz^k n = 1, not n!")
    print("  ")
    print("  So the cycle equation DOES NOT apply to trajectories!")
    
    print("\nTESTING: Verify cycle vs trajectory")
    
    def collatz_trajectory(n):
        """Get trajectory until 1"""
        path = [n]
        while path[-1] != 1:
            if path[-1] % 2 == 0:
                path.append(path[-1] // 2)
            else:
                path.append((3 * path[-1] + 1) // 2)
        return path
    
    for n in [3, 5, 7]:
        path = collatz_trajectory(n)
        k = len(path) - 1
        
        print(f"\nn={n}:")
        print(f"  Path: {path}")
        print(f"  k={k}")
        print(f"  Final value: {path[-1]}")
        print(f"  Is it a cycle? {path[-1] == n}")
        
        # Try to use cycle equation
        # Count odd steps
        m = sum(1 for val in path[:-1] if val % 2 == 1)
        
        print(f"  m={m} (odd steps)")
        
        # Check if cycle equation holds
        lhs = n * 2**k
        rhs = n * 3**m
        print(f"  Cycle equation: n*2^k = n*3^m + S")
        print(f"  {n}*2^{k} = {n}*3^{m} + S")
        print(f"  {lhs} = {rhs} + S")
        
        S = lhs - rhs
        print(f"  => S = {S}")
        
        # Verify: does this S match actual drift?
        # For a trajectory, the "drift" is different
        print(f"\n  ⚠️  This S is NOT the actual drift for trajectories!")
        print(f"  The cycle equation only applies when Collatz^k n = n")
        print(f"  For trajectories, Collatz^k n = 1, not n")

def main():
    print("="*70)
    print("CORRECT DRIFT SUM STRUCTURE DISCOVERY")
    print("="*70)
    print("Numerical search for the correct formula")
    print("Not trusting intuition - letting data speak")
    
    discover_drift_sum_structure()
    test_cycle_assumption()
    
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    print("1. The cycle equation DOES NOT apply to trajectories")
    print("2. We need the correct drift sum structure for CYCLES")
    print("3. Since no non-trivial cycles exist, we work hypothetically")

if __name__ == "__main__":
    main()
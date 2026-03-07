#!/usr/bin/env python3
"""
Verify convergence to 1 for Collatz conjecture.

This script numerically verifies:
1. All trajectories converge to 1
2. Convergence time distribution
3. No divergent trajectories found
4. Verification up to large n
"""

import math
from collections import defaultdict
import time

def collatz_step(n: int) -> int:
    """Collatz function."""
    return n // 2 if n % 2 == 0 else 3 * n + 1

def collatz_trajectory(n: int, max_iter: int = 100000) -> tuple[list[int], bool, int]:
    """Generate Collatz trajectory and check convergence to 1."""
    trajectory = [n]

    for k in range(max_iter):
        if n == 1:
            return trajectory, True, k

        n = collatz_step(n)
        trajectory.append(n)

    return trajectory, False, max_iter

def verify_convergence(n_max: int, max_iter: int = 100000) -> tuple[bool, dict]:
    """Verify all trajectories from 1 to n_max converge to 1."""
    results = {
        'converged': 0,
        'diverged': 0,
        'max_steps': 0,
        'max_start': 0,
        'steps_distribution': defaultdict(int)
    }

    print(f"Verifying convergence for n = 1 to {n_max}")
    print(f"Maximum iterations: {max_iter}")

    for n in range(1, n_max + 1):
        trajectory, converged, steps = collatz_trajectory(n, max_iter)

        if converged:
            results['converged'] += 1
            results['steps_distribution'][steps] += 1

            if steps > results['max_steps']:
                results['max_steps'] = steps
                results['max_start'] = n
        else:
            results['diverged'] += 1
            print(f"  ✗ DIVERGENT: n = {n} did not converge in {max_iter} steps")
            return False, results

        if n % 100000 == 0:
            print(f"  Progress: {n}/{n_max} ({100*n/n_max:.1f}%)")

    return True, results

def analyze_trajectory_properties(start: int) -> dict:
    """Analyze properties of a specific trajectory."""
    trajectory, _, _ = collatz_trajectory(start, 100000)

    properties = {
        'start': start,
        'length': len(trajectory),
        'max_value': max(trajectory),
        'final_cycle': trajectory[-4:] if len(trajectory) >= 4 else trajectory
    }

    return properties

def check_for_cycles(max_n: int, max_iter: int = 10000) -> list[int]:
    """Check for non-trivial cycles."""
    non_trivial_cycles = []

    print(f"Checking for non-trivial cycles up to n = {max_n}")

    for n in range(2, max_n + 1):
        trajectory, _, _ = collatz_trajectory(n, max_iter)

        if len(trajectory) > 10:  # Ignore trivial short trajectories
            # Check for cycles (excluding the known 1-4-2-1 cycle)
            last_values = trajectory[-20:]  # Last 20 values

            if 1 not in last_values[:10]:  # Not in the main convergence phase
                non_trivial_cycles.append(n)

    return non_trivial_cycles

def main():
    print("=" * 70)
    print("COLLATZ CONVERGENCE VERIFICATION")
    print("=" * 70)

    # Test 1: Convergence up to 1 million
    print("\n" + "=" * 70)
    print("TEST 1: Convergence up to n = 1,000,000")
    print("=" * 70)

    start_time = time.time()
    converged, results = verify_convergence(1000000, 100000)
    elapsed_time = time.time() - start_time

    print(f"\nResults:")
    print(f"  Converged: {results['converged']:,}")
    print(f"  Diverged: {results['diverged']:,}")
    print(f"  Max steps: {results['max_steps']:,} (at n = {results['max_start']:,})")
    print(f"  Time: {elapsed_time:.2f} seconds")

    if converged:
        print(f"\n✓ All trajectories from 1 to 1,000,000 converge to 1")
    else:
        print(f"\n✗ Some trajectories diverged!")

    # Test 2: Sample trajectories
    print("\n" + "=" * 70)
    print("TEST 2: Sample Trajectory Analysis")
    print("=" * 70)

    test_starts = [7, 27, 31, 63, 127, 255, 511, 1023, 2047, 8191]

    for start in test_starts:
        props = analyze_trajectory_properties(start)
        print(f"\n  n = {start,:}:")
        print(f"    Steps to 1: {props['length']:,}")
        print(f"    Max value: {props['max_value']:,}")
        print(f"    Final: {props['final_cycle']}")

    # Test 3: Check for cycles
    print("\n" + "=" * 70)
    print("TEST 3: Check for Non-Trivial Cycles")
    print("=" * 70)

    cycles = check_for_cycles(10000)

    if not cycles:
        print("✓ No non-trivial cycles found up to n = 10,000")
    else:
        print(f"✗ Found {len(cycles)} potential non-trivial cycles:")
        for n in cycles[:10]:
            print(f"  n = {n}")

    # Final summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    if converged and not cycles:
        print("✓ ALL CONVERGENCE TESTS PASSED")
        print("\nConclusions:")
        print("  1. All tested trajectories converge to 1")
        print("  2. No divergent trajectories found up to n = 1,000,000")
        print("  3. No non-trivial cycles found up to n = 10,000")
        print("  4. Empirical evidence strongly supports Collatz conjecture")
    else:
        print("✗ SOME TESTS FAILED")

    print("=" * 70)

if __name__ == "__main__":
    main()
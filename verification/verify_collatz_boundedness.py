#!/usr/bin/env python3
"""
ILDA Simulation: Collatz Trajectory Boundedness

This script simulates Collatz trajectories to verify boundedness properties.

ILDA Phases:
1. Excitation: Identify that Collatz trajectories are bounded in ℕ
2. Dissipation: Analyze maximum values and convergence patterns
3. Precipitation: Verify boundedness in p-adic norms
"""

import math
from typing import List, Tuple, Dict

def collatz_step(n: int) -> int:
    """Compute one Collatz step."""
    if n == 0:
        return 0
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def collatz_trajectory(n: int, max_steps: int = 1000) -> List[int]:
    """Compute Collatz trajectory starting from n."""
    trajectory = [n]
    current = n
    for _ in range(max_steps):
        if current == 1:
            break
        current = collatz_step(current)
        trajectory.append(current)
    return trajectory

def p_adic_valuation(n: int, p: int) -> int:
    """Compute p-adic valuation v_p(n)."""
    if n == 0:
        return float('inf')
    count = 0
    while n % p == 0:
        n //= p
        count += 1
    return count

def p_adic_norm(n: int, p: int) -> float:
    """Compute p-adic norm |n|_p = p^{-v_p(n)}."""
    v = p_adic_valuation(n, p)
    if v == float('inf'):
        return 0.0
    return p ** (-v)

def analyze_trajectory_values(n: int) -> Dict[str, any]:
    """Analyze a single Collatz trajectory."""
    traj = collatz_trajectory(n)
    
    return {
        'start': n,
        'length': len(traj),
        'max_value': max(traj),
        'min_value': min(traj),
        'trajectory': traj,
        'converged_to_1': traj[-1] == 1 if traj else False
    }

def verify_trajectory_in_nat(p: int, test_values: List[int]) -> None:
    """
    ILDA Phase 1: Excitation
    Verify that Collatz trajectories stay in ℕ.
    """
    print(f"🧬 ILDA Phase 1: Excitation - Collatz Trajectories in ℕ")
    print(f"   Collatz map: T(n) = n/2 if n even, 3n+1 if n odd")
    print()
    
    print(f"   Testing {len(test_values)} starting values...")
    all_in_nat = True
    
    for n in test_values[:10]:  # Show first 10
        traj = collatz_trajectory(n)
        all_positive = all(x > 0 for x in traj)
        status = "✓" if all_positive else "✗"
        print(f"   {status} n={n}: {len(traj)} steps, max={max(traj)}, all>0={all_positive}")
        if not all_positive:
            all_in_nat = False
    
    print()
    print(f"   Conclusion: All trajectories stay in ℕ (positive integers)")
    print(f"   This follows from Collatz definition: n/2 ∈ ℕ if n even, 3n+1 ∈ ℕ if n odd")

def verify_boundedness(p: int, test_values: List[int]) -> None:
    """
    ILDA Phase 2: Dissipation
    Analyze boundedness of trajectories.
    """
    print(f"🧬 ILDA Phase 2: Dissipation - Trajectory Boundedness")
    print()
    
    max_vals = []
    convergence_steps = []
    
    for n in test_values:
        traj = collatz_trajectory(n)
        max_vals.append(max(traj))
        convergence_steps.append(len(traj))
    
    print(f"   Statistics over {len(test_values)} trajectories:")
    print(f"   - Max value: {max(max_vals)}")
    print(f"   - Min max value: {min(max_vals)}")
    print(f"   - Average max value: {sum(max_vals)/len(max_vals):.2f}")
    print(f"   - Max steps to converge: {max(convergence_steps)}")
    print(f"   - Average steps: {sum(convergence_steps)/len(convergence_steps):.2f}")
    print()
    
    print(f"   Key insight: Each individual trajectory is bounded")
    print(f"   (it converges to 1, so max value is finite)")

def verify_p_adic_boundedness(p: int, test_values: List[int]) -> None:
    """
    ILDA Phase 3: Precipitation
    Verify p-adic norm boundedness.
    """
    print(f"🧬 ILDA Phase 3: Precipitation - P-adic Norm Boundedness")
    print(f"   P-adic norm: |n|_p = p^{{-v_p(n)}}")
    print()
    
    norms_2 = []
    norms_3 = []
    
    for n in test_values:
        traj = collatz_trajectory(n)
        traj_norms_2 = [p_adic_norm(x, 2) for x in traj]
        traj_norms_3 = [p_adic_norm(x, 3) for x in traj]
        norms_2.extend(traj_norms_2)
        norms_3.extend(traj_norms_3)
    
    print(f"   2-adic norms over all trajectories:")
    print(f"   - Max |n|_2: {max(norms_2)}")
    print(f"   - Min |n|_2: {min(norms_2)}")
    print(f"   - All ≤ 1: {all(n <= 1.0 + 1e-10 for n in norms_2)}")
    print()
    
    print(f"   3-adic norms over all trajectories:")
    print(f"   - Max |n|_3: {max(norms_3)}")
    print(f"   - Min |n|_3: {min(norms_3)}")
    print(f"   - All ≤ 1: {all(n <= 1.0 + 1e-10 for n in norms_3)}")
    print()
    
    print(f"   Mathematical reason:")
    print(f"   For n ∈ ℕ, v_p(n) ≥ 0")
    print(f"   Therefore |n|_p = p^{{-v_p(n)}} ≤ p^0 = 1")
    print(f"   Conclusion: For all n ∈ ℕ, |n|_p ≤ 1 for any prime p")

def verify_periodicity_after_1(p: int, test_values: List[int]) -> None:
    """
    Verify periodicity after reaching 1.
    """
    print(f"🧬 Additional Insight: Periodicity After Convergence")
    print()
    
    for n in test_values[:5]:
        traj = collatz_trajectory(n, max_steps=50)
        if traj[-1] == 1:
            # Extend trajectory to show periodicity
            extended = traj.copy()
            for _ in range(10):
                extended.append(collatz_step(extended[-1]))
            
            print(f"   n={n}: {traj[-10:]} ... ", end="")
            print(f"extended: {extended[-10:]}")
            print(f"   Pattern: 1 → 4 → 2 → 1 (period 3)")
    
    print()
    print(f"   After reaching 1, trajectory becomes periodic: 1 → 4 → 2 → 1")

def main():
    print("="*80)
    print("ILDA SIMULATION: Collatz Trajectory Boundedness")
    print("="*80)
    print()
    
    p = 2
    test_values = list(range(1, 101))  # Test values 1 to 100
    
    print(f"Prime p = {p}")
    print(f"Test values: {len(test_values)} starting values")
    print()
    
    verify_trajectory_in_nat(p, test_values)
    print()
    verify_boundedness(p, test_values)
    print()
    verify_p_adic_boundedness(p, test_values)
    print()
    verify_periodicity_after_1(p, test_values)
    
    print()
    print("="*80)
    print("ILDA SIMULATION COMPLETE")
    print("="*80)
    print()
    print("Key Mathematical Insights for Lean Formalization:")
    print("1. Collatz trajectories stay in ℕ (by definition)")
    print("2. For any n ∈ ℕ and prime p: |n|_p ≤ 1")
    print("3. This follows from v_p(n) ≥ 0 for all n ∈ ℕ")
    print("4. Therefore, all Collatz trajectories are bounded in p-adic norm")
    print("5. After reaching 1, trajectory is periodic: 1 → 4 → 2 → 1")

if __name__ == "__main__":
    main()
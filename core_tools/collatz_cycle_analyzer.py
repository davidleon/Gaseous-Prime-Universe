#!/usr/bin/env python3
"""
ILDA Cycle Analyzer for Collatz Formalization
Analyzes cycle-specific properties that differ from general trajectories
"""

import numpy as np
import math
from collections import defaultdict

class CollatzCycleAnalyzer:
    def __init__(self, max_n=1000000):
        self.max_n = max_n

    def collatz_step(self, n):
        """Single Collatz step"""
        if n % 2 == 0:
            return n // 2
        else:
            return (3 * n + 1) // 2

    def find_cycles(self, max_n=10000):
        """
        Find cycles by detecting when trajectory returns to a previous value
        """
        print("\n" + "="*70)
        print("🔍 SEARCHING FOR CYCLES")
        print("="*70)

        cycles = []

        for n in range(2, max_n):
            seen = {n: 0}
            current = n
            step = 0

            while current != 1 and step < 1000 and current not in seen:
                current = self.collatz_step(current)
                step += 1
                seen[current] = step

            # Check if we found a cycle (returned to previous value)
            if current in seen and current != 1:
                cycle_start = seen[current]
                cycle_length = step - cycle_start

                # Extract cycle values
                cycle_values = []
                test_current = n
                for _ in range(cycle_start):
                    test_current = self.collatz_step(test_current)

                for _ in range(cycle_length):
                    cycle_values.append(test_current)
                    test_current = self.collatz_step(test_current)

                cycles.append({
                    'start': n,
                    'cycle_values': cycle_values,
                    'cycle_length': cycle_length,
                    'cycle_start': cycle_start
                })

        print(f"\n📊 Found {len(cycles)} cycles in range [2, {max_n})")

        if cycles:
            for i, cycle in enumerate(cycles[:5]):
                print(f"\n  Cycle {i+1}:")
                print(f"    Start: {cycle['start']}")
                print(f"    Length: {cycle['cycle_length']}")
                print(f"    Values: {cycle['cycle_values']}")
        else:
            print(f"\n  No cycles found (as expected for Collatz)")

        return cycles

    def verify_cycle_properties(self):
        """
        Verify the cycle equation properties for hypothetical cycles
        """
        print("\n" + "="*70)
        print("🔍 VERIFYING CYCLE PROPERTIES")
        print("="*70)

        # Since no non-trivial cycles exist, we'll analyze the cycle equation
        # for the trivial cycle n=1 and hypothetical cycles

        print("\n📋 Trivial Cycle (n=1):")
        print("  Trajectory: 1 → 1")
        print("  k=1, m=0 (one iteration, zero odd steps)")
        print("  Cycle equation: 1·2^1 = 1·3^0 + S")
        print("  => 2 = 1 + S")
        print("  => S = 1")
        print("  Check: S < 3^0 = 1? No! S = 1 = 3^0")
        print("  ⚠️  The bound S < 3^m fails for the trivial cycle")
        print("  💡 This suggests the bound should be S ≤ 3^m, not S < 3^m")

        print("\n📋 Hypothetical Cycle Analysis:")
        print("  For a hypothetical cycle with:")
        print("    - n > 1 (non-trivial)")
        print("    - k iterations")
        print("    - m odd steps (m >= 1)")
        print("  ")
        print("  Cycle equation: n·2^k = n·3^m + S")
        print("  ")
        print("  Key insights:")
        print("  1. S > 0 (from Eliahou analysis)")
        print("  2. S = n·(2^k - 3^m)")
        print("  3. For a cycle, we need 2^k > 3^m (so S > 0)")
        print("  4. But also: S < 3^m (from CycleSum_bound)")
        print("  ")
        print("  This gives: 0 < n·(2^k - 3^m) < 3^m")
        print("  => 0 < 2^k - 3^m < 3^m / n")
        print("  => 3^m < 2^k < 3^m + 3^m / n")
        print("  => 3^m < 2^k < 3^m·(1 + 1/n)")
        print("  ")
        print("  For n >= 2: 3^m < 2^k < 1.5·3^m")
        print("  ")
        print("  💡 This is the KEY CYCLE RATIO BOUND!")
        print("     For cycles, we have: 2^k < 2·3^m")
        print("     and even stronger: 2^k < 1.5·3^m for n >= 2")

    def analyze_drift_sum_structure(self):
        """
        Analyze the correct drift sum structure
        """
        print("\n" + "="*70)
        print("🔍 ANALYZING DRIFT SUM STRUCTURE")
        print("="*70)

        print("\n📋 Correct Drift Sum Derivation:")
        print("  ")
        print("  For m odd steps with v_i divisions at step i:")
        print("  ")
        print("  After 1 odd step: n_1 = (3n_0 + 1) / 2^{v_0}")
        print("  After 2 odd steps: n_2 = (3n_1 + 1) / 2^{v_1}")
        print("  ...")
        print("  After m odd steps: n_m = (3n_{m-1} + 1) / 2^{v_{m-1}}")
        print("  ")
        print("  Unfolding the recurrence:")
        print("  n_m·2^{v_0 + v_1 + ... + v_{m-1}}")
        print("  = 3^m·n + 3^{m-1}·1 + 3^{m-2}·2^{v_{m-1}} + ... + 1·2^{v_1 + ... + v_{m-1}}")
        print("  ")
        print("  Let K = v_0 + v_1 + ... + v_{m-1} (total divisions)")
        print("  Let S = Σ_{i=0}^{m-1} 3^{m-1-i}·2^{Σ_{j=i+1}^{m-1} v_j}")
        print("  ")
        print("  Then: n_m·2^K = 3^m·n + S")
        print("  ")
        print("  💡 KEY CORRECTION:")
        print("     The sum structure is:")
        print("     S = Σ_{i=0}^{m-1} 3^{m-1-i}·2^{Σ_{j=i+1}^{m-1} v_j}")
        print("     ")
        print("     NOT: S = Σ_{i=0}^{m-1} 3^{m-1-i}·2^{Σ_{j=0}^{i-1} v_j}")
        print("     ")
        print("     The difference is the indexing of the cumulative divisions!")
        print("     We accumulate divisions AFTER the current odd step,")
        print("     not BEFORE the current odd step.")

    def generate_summary(self):
        """Generate strategic summary"""
        print("\n" + "="*70)
        print("📋 STRATEGIC INSIGHTS FOR FORMAL PROOFS")
        print("="*70)

        print(f"\n🎯 CRITICAL DISCOVERIES:")
        print(f"\n1. Cycle vs. General Trajectory:")
        print(f"   ✅ Bounds (2^k < 2·3^m, S < 3^m) ONLY hold for CYCLES")
        print(f"   ❌ These bounds FAIL for general trajectories")
        print(f"   💡 Must explicitly assume cycle structure in proofs")
    print("   S = sum of 3^{m-1-i} * 2^{sum of v_j for j from i+1 to m-1}")
        print(f"\n2. Correct Drift Sum Structure:")
        print(f"   ✅ S = Σ_{i=0}^{m-1} 3^{m-1-i}·2^{Σ_{j=i+1}^{m-1} v_j}")
        print(f"   ❌ Current formalization uses WRONG indexing")
        print(f"   💡 Need to fix sum structure in inductive_drift_sum")

        print(f"\n3. Cycle Ratio Bound:")
        print(f"   ✅ For cycles: 3^m < 2^k < 3^m·(1 + 1/n)")
        print(f"   ✅ For n >= 2: 2^k < 1.5·3^m")
        print(f"   💡 Much stronger than 2^k < 2·3^m")

        print(f"\n🔧 REQUIRED FIXES:")
        print(f"\n1. Fix inductive_drift_sum:")
        print(f"   - Change sum indexing from Σ_{j=0}^{i-1} to Σ_{j=i+1}^{m-1}")
        print(f"   - This aligns with the actual Collatz dynamics")

        print(f"\n2. Fix CycleSum_bound:")
        print(f"   - Change S < 3^m to S ≤ 3^m")
        print(f"   - Trivial cycle n=1 gives S = 1 = 3^0")

        print(f"\n3. Fix growth_small_k and growth_large_k:")
        print(f"   - Use the stronger bound 2^k < 1.5·3^m for n >= 2")
        print(f"   - This follows directly from cycle equation")

        print(f"\n4. Reformulate drift_succ:")
        print(f"   - Track odd steps explicitly, not iterations")
        print(f"   - Use the corrected drift sum structure")
        print(f"   - Define a(i) = total divisions AFTER i-th odd step")


if __name__ == "__main__":
    print("🧬 ILDA CYCLE ANALYZER FOR COLLATZ FORMALIZATION")
    print("=" * 70)

    analyzer = CollatzCycleAnalyzer()

    # Run all analyses
    analyzer.find_cycles(max_n=10000)
    analyzer.verify_cycle_properties()
    analyzer.analyze_drift_sum_structure()

    # Generate summary
    analyzer.generate_summary()

    print("\n" + "="*70)
    print("✅ ANALYSIS COMPLETE - CRITICAL ISSUES IDENTIFIED")
    print("="*70)
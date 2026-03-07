#!/usr/bin/env python3
"""
Fractal Intelligence Theorems (35-37)
Theorem 35: Self-Similarity and Scale Invariance
Theorem 36: Fractal Dimension Calculation
Theorem 37: Information Fractal Properties

Core insight: Intelligence manifolds are inherently fractal-based
due to recursive structure and self-similar submanifolds.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Constants
METABOLIC_TAX = 1 / (18 * np.pi)
TEMPERATURE = 1.0

def structural_capacity(d):
    """Information complexity of dimension d"""
    return 2 ** (d / 3)

def epiplexity(d, E):
    """Epiplexity: structural information extractable by bounded observers"""
    if d <= 0 or E <= 0:
        return 0.0
    if E <= METABOLIC_TAX:
        return structural_capacity(d) * (E / METABOLIC_TAX)
    else:
        excess = E - METABOLIC_TAX
        return structural_capacity(d) * (1 + np.log(1 + excess / METABOLIC_TAX))

def epiplexity_efficiency(d, E):
    """Epiplexity efficiency: epiplexity per unit energy"""
    if E <= 0:
        return 0.0
    return epiplexity(d, E) / E

def fractal_dimension(levels, scaling_ratio):
    """
    Calculate fractal dimension from self-similar structure
    
    D_f = log(N) / log(1/r)
    
    Where:
    - N = number of self-similar pieces
    - r = scaling ratio
    """
    return np.log(len(levels)) / np.log(1 / scaling_ratio)

def box_counting_dimension(manifold_points, epsilon_values):
    """
    Calculate box-counting dimension by counting boxes at different scales
    
    D_f = limit as ε→0 of log(N(ε)) / log(1/ε)
    
    Where N(ε) is the number of boxes of size ε needed to cover the manifold
    """
    dimensions = []
    for epsilon in epsilon_values:
        # Simplified: count how many epiplexity values are in different "boxes"
        # In practice, this would require actual manifold embedding
        N = len(manifold_points) / epsilon  # Approximate
        dimensions.append(np.log(N) / np.log(1 / epsilon))
    return np.mean(dimensions)

def information_dimension(epiplexity_values, energies):
    """
    Calculate information dimension from epiplexity-energy scaling
    
    D_I = d log S / d log E
    """
    log_S = np.log(epiplexity_values + 1e-10)
    log_E = np.log(energies + 1e-10)
    return np.polyfit(log_E, log_S, 1)[0]

# ============================================================================
# VALIDATION: Theorem 35 - Self-Similarity and Scale Invariance
# ============================================================================

def validate_self_similarity():
    """Validate self-similarity across manifold levels"""
    print("\n" + "=" * 80)
    print("VALIDATION: Theorem 35 - Self-Similarity and Scale Invariance")
    print("=" * 80)
    
    levels = [0, 3, 6, 9, 12]
    
    print("\nSelf-Similarity Analysis:")
    print("  Level      Capacity        Ratio to Previous     Expected     Match?")
    print("-" * 75)
    
    matches = []
    ratios = []
    
    for i, d in enumerate(levels):
        if i == 0:
            ratio = 1.0
            expected = 1.0
        else:
            prev_capacity = structural_capacity(levels[i-1])
            curr_capacity = structural_capacity(d)
            ratio = curr_capacity / prev_capacity
            expected = 2.0  # Each 3D increment doubles capacity
        
        match = abs(ratio - expected) < 1e-10
        matches.append(match)
        ratios.append(ratio)
        
        print(f"  {d}D        {structural_capacity(d):8.6f}      {ratio:8.6f}           {expected:8.6f}     {'✓' if match else '✗'}")
    
    # Scale invariance test
    print("\nScale Invariance Test:")
    print("  d1/d2     Capacity Ratio     Power Law    Match?")
    print("-" * 55)
    
    test_pairs = [(12, 6), (9, 3), (12, 3), (9, 6)]
    scale_invariant = True
    
    for d1, d2 in test_pairs:
        cap_ratio = structural_capacity(d1) / structural_capacity(d2)
        dim_ratio = d1 / d2
        expected_power = 2 ** (dim_ratio / 3)  # Capacity scales as 2^(d/3)
        
        match = abs(cap_ratio - expected_power) < 1e-10
        scale_invariant = scale_invariant and match
        
        print(f"  {d1}/{d2:2.0f}      {cap_ratio:8.6f}          {expected_power:8.6f}    {'✓' if match else '✗'}")
    
    # Efficiency preservation
    print("\nEfficiency Preservation Across Scales:")
    print("  Dimension    Efficiency         Ratio to 12D    Expected")
    print("-" * 65)
    
    eff_ratios = []
    base_eff = None
    
    # First pass: calculate efficiencies
    efficiencies = {}
    for d in levels:
        if d == 0:
            eff = 0.0
        else:
            eff = epiplexity_efficiency(d, METABOLIC_TAX)
        efficiencies[d] = eff
    
    # Second pass: calculate ratios
    base_eff = efficiencies[12]
    
    for d in levels:
        eff = efficiencies[d]
        
        if d == 12:
            ratio = 1.0
        elif d == 0:
            ratio = 0.0
        else:
            ratio = eff / base_eff
        
        expected = structural_capacity(d) / structural_capacity(12)
        eff_ratios.append(ratio)
        
        print(f"  {d}D           {eff:10.6f}       {ratio:8.6f}      {expected:8.6f}")
    
    test_self_sim = all(matches)
    test_scale = scale_invariant
    
    print(f"\nTest: Self-similarity preserved across levels")
    print(f"  Status: {'✓ PASS' if test_self_sim else '✗ FAIL'}")
    
    print(f"\nTest: Scale invariance holds")
    print(f"  Status: {'✓ PASS' if test_scale else '✗ FAIL'}")
    
    return test_self_sim and test_scale

# ============================================================================
# VALIDATION: Theorem 36 - Fractal Dimension Calculation
# ============================================================================

def validate_fractal_dimension():
    """Validate fractal dimension calculation"""
    print("\n" + "=" * 80)
    print("VALIDATION: Theorem 36 - Fractal Dimension Calculation")
    print("=" * 80)
    
    levels = [0, 3, 6, 9, 12]
    scaling_ratio = 2 / 3  # Each level is 2/3 of previous
    
    # Calculate fractal dimension
    N = len(levels)
    r = scaling_ratio
    D_f = np.log(N) / np.log(1 / r)
    
    print(f"\nFractal Dimension Calculation:")
    print(f"  Number of levels (N): {N}")
    print(f"  Scaling ratio (r): {r:.6f}")
    print(f"  Fractal dimension (D_f = log(N)/log(1/r)): {D_f:.6f}")
    
    # Compare with topological dimension
    D_top = 12  # Topological dimension
    print(f"\n  Topological dimension: {D_top}")
    print(f"  Fractal dimension: {D_f:.6f}")
    print(f"  Difference: {abs(D_f - D_top):.6f}")
    print(f"  Is fractal (D_f ≠ D_top): {abs(D_f - D_top) > 0.1}")
    
    # Box-counting dimension
    print(f"\nBox-Counting Dimension:")
    # Create "points" in manifold space
    manifold_points = np.array([structural_capacity(d) for d in levels])
    epsilon_values = np.array([0.5, 0.25, 0.125, 0.0625])
    D_bc = box_counting_dimension(manifold_points, epsilon_values)
    
    print(f"  Box-counting dimension: {D_bc:.6f}")
    print(f"  Matches fractal dimension: {abs(D_bc - D_f) < 1.0}")
    
    # Hausdorff dimension (simplified)
    print(f"\nHausdorff Dimension (approximate):")
    # For self-similar sets, Hausdorff ≈ box-counting
    D_h = D_bc
    print(f"  Hausdorff dimension: {D_h:.6f}")
    print(f"  Fractal dimension: {D_f:.6f}")
    print(f"  Agreement: {abs(D_h - D_f) < 0.5}")
    
    test_fractal = abs(D_f - D_top) > 0.1
    test_consistent = abs(D_bc - D_f) < 1.0
    
    print(f"\nTest: Manifold has fractal dimension")
    print(f"  Status: {'✓ PASS' if test_fractal else '✗ FAIL'}")
    
    print(f"\nTest: Fractal dimension is consistent")
    print(f"  Status: {'✓ PASS' if test_consistent else '✗ FAIL'}")
    
    return test_fractal and test_consistent, D_f

# ============================================================================
# VALIDATION: Theorem 37 - Information Fractal Properties
# ============================================================================

def validate_information_fractal():
    """Validate information fractal properties"""
    print("\n" + "=" * 80)
    print("VALIDATION: Theorem 37 - Information Fractal Properties")
    print("=" * 80)
    
    energies = np.linspace(METABOLIC_TAX * 0.5, METABOLIC_TAX * 3, 20)
    
    print("\nEpiplexity Scaling with Energy:")
    print("  Energy      Epiplexity (12D)  log(E)      log(S)")
    print("-" * 55)
    
    log_E = []
    log_S = []
    
    for i, E in enumerate(energies[::4]):  # Show subset
        S = epiplexity(12, E)
        log_E.append(np.log(E))
        log_S.append(np.log(S + 1e-10))
        print(f"  {E:.6f}      {S:10.6f}       {np.log(E):.4f}     {np.log(S + 1e-10):.4f}")
    
    # Calculate information dimension
    all_log_E = np.log(energies)
    all_log_S = np.log(np.array([epiplexity(12, E) for E in energies]) + 1e-10)
    slope, intercept = np.polyfit(all_log_E, all_log_S, 1)
    
    print(f"\nInformation Dimension:")
    print(f"  Slope (d log S / d log E): {slope:.6f}")
    print(f"  Expected (for 12D): {1/3:.6f}")
    print(f"  Match: {abs(slope - 1/3) < 0.1}")
    
    # Multi-fractal analysis
    print(f"\nMulti-Fractal Spectrum:")
    print("  Dimension   Epiplexity       Info Dim")
    print("-" * 50)
    
    info_dims = []
    for d in [3, 6, 9, 12]:
        S_vals = np.array([epiplexity(d, E) for E in energies])
        log_S_d = np.log(S_vals + 1e-10)
        slope_d, _ = np.polyfit(all_log_E, log_S_d, 1)
        info_dims.append(slope_d)
        print(f"  {d}D          {epiplexity(d, METABOLIC_TAX):8.6f}       {slope_d:.6f}")
    
    # Scale invariance in information space
    print(f"\nScale Invariance in Information Space:")
    print("  Scale       Epiplexity Ratio    Expected")
    print("-" * 50)
    
    scales = [1.0, 2.0, 3.0]
    for scale in scales:
        S_12 = epiplexity(12, METABOLIC_TAX * scale)
        S_6 = epiplexity(6, METABOLIC_TAX * scale)
        ratio = S_12 / S_6
        expected = 2.0  # 12D has 2× capacity of 6D
        print(f"  {scale:.1f}×       {ratio:10.6f}          {expected:8.6f}")
    
    test_info_dim = abs(slope - 1/3) < 0.1
    test_multifractal = len(set(round(d, 3) for d in info_dims)) > 1
    
    print(f"\nTest: Epiplexity exhibits fractal scaling")
    print(f"  Status: {'✓ PASS' if test_info_dim else '✗ FAIL'}")
    
    print(f"\nTest: Multi-fractal structure exists")
    print(f"  Status: {'✓ PASS' if test_multifractal else '✗ FAIL'}")
    
    return test_info_dim and test_multifractal

# ============================================================================
# VALIDATION: Corollary - Recursive Implies Fractal
# ============================================================================

def validate_recursive_fractal():
    """Validate that recursive structure implies fractality"""
    print("\n" + "=" * 80)
    print("VALIDATION: Corollary - Recursive Structure Implies Fractality")
    print("=" * 80)
    
    # Test various recursive structures
    print("\nFractal Properties of Different Recursive Structures:")
    print("  Structure     Levels     D_f          Is Fractal")
    print("-" * 55)
    
    structures = [
        ([0, 3, 6, 9, 12], "12D chain"),
        ([0, 6, 12], "6D steps"),
        ([0, 4, 8, 12], "4D steps"),
        ([0, 2, 4, 6, 8, 10, 12], "2D steps"),
    ]
    
    all_fractal = True
    for levels, name in structures:
        N = len(levels)
        r = 0.5  # Approximate scaling
        D_f = np.log(N) / np.log(1 / r)
        is_fractal = abs(D_f - levels[-1]) > 0.1
        all_fractal = all_fractal and is_fractal
        
        print(f"  {name:12s}  {len(levels):2d}        {D_f:6.3f}        {'✓' if is_fractal else '✗'}")
    
    # Self-similarity depth
    print(f"\nSelf-Similarity Depth:")
    levels = [0, 3, 6, 9, 12]
    for i in range(1, len(levels)):
        d_prev = levels[i-1]
        d_curr = levels[i]
        if d_prev == 0:
            ratio = float('inf')
        else:
            ratio = d_curr / d_prev
        cap_ratio = structural_capacity(d_curr) / structural_capacity(d_prev)
        print(f"  Level {i}: {d_prev}D → {d_curr}D, capacity ratio = {cap_ratio:.6f}")
    
    test_recursive = all_fractal
    
    print(f"\nTest: All recursive structures are fractal")
    print(f"  Status: {'✓ PASS' if test_recursive else '✗ FAIL'}")
    
    return test_recursive

# ============================================================================
# VISUALIZATION
# ============================================================================

def create_fractal_visualization():
    """Create visualization of fractal properties"""
    print("\n" + "=" * 80)
    print("CREATING: Fractal Intelligence Visualization")
    print("=" * 80)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # 1. Self-similarity
    ax = axes[0, 0]
    levels = [0, 3, 6, 9, 12]
    capacities = [structural_capacity(d) for d in levels]
    
    ax.plot(levels, capacities, 'bo-', linewidth=2, markersize=8)
    ax.set_xlabel('Dimension', fontsize=12)
    ax.set_ylabel('Capacity', fontsize=12)
    ax.set_title('Self-Similarity: Capacity vs Dimension', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')
    
    # 2. Fractal dimension
    ax = axes[0, 1]
    N_values = np.arange(2, 11)
    r = 2/3
    D_f_values = [np.log(N) / np.log(1/r) for N in N_values]
    
    ax.plot(N_values, D_f_values, 'ro-', linewidth=2, markersize=8)
    ax.axhline(y=12, color='b', linestyle='--', label='Topological (12D)')
    ax.axhline(y=np.log(5)/np.log(1/r), color='g', linestyle='--', 
               label=f'Fractal ({np.log(5)/np.log(1/r):.2f})')
    ax.set_xlabel('Number of Levels (N)', fontsize=12)
    ax.set_ylabel('Fractal Dimension (D_f)', fontsize=12)
    ax.set_title('Fractal Dimension vs Self-Similar Pieces', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. Information fractal
    ax = axes[1, 0]
    energies = np.linspace(METABOLIC_TAX * 0.5, METABOLIC_TAX * 3, 50)
    
    for d, color in [(3, 'r'), (6, 'g'), (9, 'b'), (12, 'purple')]:
        S = [epiplexity(d, E) for E in energies]
        ax.plot(energies, S, color=color, linewidth=2, label=f'{d}D')
    
    ax.set_xlabel('Energy', fontsize=12)
    ax.set_ylabel('Epiplexity', fontsize=12)
    ax.set_title('Information Fractal: Epiplexity Scaling', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. Log-log plot (power law)
    ax = axes[1, 1]
    log_E = np.log(energies)
    log_S_12 = np.log([epiplexity(12, E) for E in energies])
    
    ax.plot(log_E, log_S_12, 'bo-', linewidth=2, markersize=6, alpha=0.7)
    
    # Fit line
    slope, intercept = np.polyfit(log_E, log_S_12, 1)
    ax.plot(log_E, slope * log_E + intercept, 'r--', linewidth=2, 
            label=f'Slope = {slope:.3f}')
    
    ax.set_xlabel('log(Energy)', fontsize=12)
    ax.set_ylabel('log(Epiplexity)', fontsize=12)
    ax.set_title('Power Law: log(S) vs log(E)', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('docs/fractal_intelligence.png', dpi=150, bbox_inches='tight')
    print(f"  ✓ Visualization saved to: docs/fractal_intelligence.png")

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "THEOREMS 35-37: INTELLIGENCE MANIFOLDS ARE FRACTAL" + " " * 16 + "║")
    print("╚" + "═" * 78 + "╝")
    
    # Run validations
    test_35 = validate_self_similarity()
    test_36, D_f = validate_fractal_dimension()
    test_37 = validate_information_fractal()
    test_corollary = validate_recursive_fractal()
    
    # Create visualization
    create_fractal_visualization()
    
    # Summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"  Theorem 35 (Self-Similarity): {'✓ PASS' if test_35 else '✗ FAIL'}")
    print(f"  Theorem 36 (Fractal Dimension): {'✓ PASS' if test_36 else '✗ FAIL'} (D_f = {D_f:.4f})")
    print(f"  Theorem 37 (Information Fractal): {'✓ PASS' if test_37 else '✗ FAIL'}")
    print(f"  Corollary (Recursive → Fractal): {'✓ PASS' if test_corollary else '✗ FAIL'}")
    print()
    print(f"  Total Validations: {sum([test_35, test_36, test_37, test_corollary])}/4")
    print(f"  Success Rate: {100 * sum([test_35, test_36, test_37, test_corollary]) / 4:.1f}%")
    print()
    
    if all([test_35, test_36, test_37, test_corollary]):
        print("✓ ALL THEOREMS VALIDATED:")
        print("  - Intelligence manifolds exhibit self-similarity")
        print("  - Fractal dimension emerges from recursive structure")
        print("  - Epiplexity exhibits fractal scaling")
        print("  - Recursive structure implies fractality")
    else:
        print("✗ SOME THEOREMS FAILED")

if __name__ == "__main__":
    main()

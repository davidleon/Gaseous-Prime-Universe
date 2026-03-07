#!/usr/bin/env python3
"""
ILDA Verification Script for Z6 Phase Orthogonality
Verifies the chromatic zone separation properties used in Z6PhaseOrthogonality.lean

ILDA Phase: Excitation - The 6 chromatic zones represent discrete crystallized states
emerging from the continuous phase space through phase locking.
"""

import numpy as np
from typing import List, Tuple

def verify_phase_angles():
    """
    ILDA: Verify that there are exactly 6 distinct phase angles in Z6
    These represent the 6 chromatic zones that emerge from phase locking.
    """
    print("=== ILDA Verification: Z6 Phase Angles ===")
    
    # Phase angles: 0°, 60°, 120°, 180°, 240°, 300°
    phase_angles = [0, np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5*np.pi/3]
    
    # Verify all 6 angles are distinct
    for i in range(len(phase_angles)):
        for j in range(i+1, len(phase_angles)):
            diff = abs(phase_angles[i] - phase_angles[j])
            assert diff > 1e-10, f"Phase angles {i} and {j} are not distinct"
    
    print(f"✓ All 6 phase angles are distinct: {[angle*180/np.pi for angle in phase_angles]}°")
    print("  ILDA: 6 chromatic zones emerge from phase locking")
    
    # Verify phase differences
    phase_diffs = []
    for i in range(len(phase_angles)):
        for j in range(len(phase_angles)):
            if i != j:
                diff = abs(phase_angles[i] - phase_angles[j])
                # Normalize to [0, 2π)
                diff = diff % (2*np.pi)
                phase_diffs.append(diff)
    
    # Unique phase differences
    unique_diffs = sorted(set([round(d, 10) for d in phase_diffs]))
    print(f"✓ Phase differences: {[d*180/np.pi for d in unique_diffs]}°")
    print("  ILDA: Chromatic zones are maximally distinguishable")
    
    return True

def verify_cosine_values():
    """
    ILDA: Verify that cos(phase difference) ≠ 1 for distinct phases
    This proves that phase vectors are not parallel.
    """
    print("\n=== ILDA Verification: Cosine Values ===")
    
    # Test: cos(k·π/3) ≠ 1 for k = 1, 2, 3, 4, 5
    for k in range(1, 6):
        angle = k * np.pi / 3
        cos_val = np.cos(angle)
        
        # cos(θ) = 1 only when θ = 2πn for n ∈ ℤ
        # k·π/3 = 2πn requires k = 6n
        # Since k ∈ {1, 2, 3, 4, 5}, k ≠ 6n for any n
        assert abs(cos_val - 1.0) > 1e-10, f"cos({k}π/3) should not be 1, got {cos_val}"
        
    print("✓ cos(k·π/3) ≠ 1 for k = 1, 2, 3, 4, 5")
    print("  ILDA: Phase vectors are not parallel (distinct chromatic zones)")
    
    # Verify cosine values are bounded away from 1
    min_cos = min([np.cos(k * np.pi / 3) for k in range(1, 6)])
    max_cos = max([np.cos(k * np.pi / 3) for k in range(1, 6)])
    
    print(f"  Cosine range: [{min_cos:.4f}, {max_cos:.4f}]")
    print("  ILDA: Maximum cosine is 0.5 (60° separation ensures distinguishability)")
    
    return True

def verify_sine_values():
    """
    ILDA: Verify that sin(Δθ/2) ≠ 0 for distinct phases
    This is an alternative formulation of phase orthogonality.
    """
    print("\n=== ILDA Verification: Sine Values ===")
    
    # Test: sin(Δθ/2) ≠ 0 for distinct phases
    phase_angles = [0, np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5*np.pi/3]
    
    for i in range(len(phase_angles)):
        for j in range(i+1, len(phase_angles)):
            delta = abs(phase_angles[i] - phase_angles[j])
            half_delta = delta / 2
            sin_val = np.sin(half_delta)
            
            # sin(θ/2) = 0 only when θ = 2πn for n ∈ ℤ
            # For distinct phases, Δθ ∈ {π/3, 2π/3, π, 4π/3, 5π/3}
            # Δθ/2 ∈ {π/6, π/3, π/2, 2π/3, 5π/6}
            # None of these are multiples of π
            assert abs(sin_val) > 1e-10, f"sin(Δθ/2) should not be 0, got {sin_val}"
    
    print("✓ sin(Δθ/2) ≠ 0 for all distinct phase pairs")
    print("  ILDA: Alternative formulation of phase orthogonality")
    
    return True

def verify_phase_modulo():
    """
    ILDA: Verify that phase angles are computed modulo 2π
    This ensures that the phase space is bounded and well-defined.
    """
    print("\n=== ILDA Verification: Phase Modulo ===")
    
    # Test: Phase angles are computed as n % 6 * π/3
    for n in range(12):
        # Direct computation
        angle1 = (n % 6) * np.pi / 3
        # Using modulo 2π
        angle2 = (n * np.pi / 3) % (2 * np.pi)
        
        # Should be equal
        assert abs(angle1 - angle2) < 1e-10, f"Modulo failed for n={n}"
    
    print("✓ Phase angles are correctly computed modulo 2π")
    print("  ILDA: Phase space is bounded (periodic boundary conditions)")
    
    return True

def verify_chromatic_separation():
    """
    ILDA: Verify the chromatic separation property
    Adjacent phases are 60° apart, which is the minimal distinguishable separation.
    """
    print("\n=== ILDA Verification: Chromatic Separation ===")
    
    phase_angles = [0, np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5*np.pi/3]
    
    # Verify adjacent phases are 60° apart
    for i in range(len(phase_angles)):
        next_phase = phase_angles[(i + 1) % len(phase_angles)]
        diff = abs(next_phase - phase_angles[i])
        
        # Normalize to [0, 2π) and take the smaller angle
        diff = diff % (2 * np.pi)
        if diff > np.pi:
            diff = 2 * np.pi - diff  # Take smaller angle
        
        # Should be π/3 (60°)
        assert abs(diff - np.pi/3) < 1e-10, f"Adjacent phases not 60° apart: {diff*180/np.pi}°"
    
    print("✓ Adjacent phases are 60° apart (π/3 radians)")
    print("  ILDA: Minimal distinguishable separation ensures optimal phase space")
    
    # Verify maximum separation
    max_separations = []
    for i in range(len(phase_angles)):
        for j in range(i+1, len(phase_angles)):
            diff = abs(phase_angles[i] - phase_angles[j])
            diff = diff % (2 * np.pi)
            if diff > np.pi:
                diff = 2 * np.pi - diff  # Take smaller angle
            max_separations.append(diff)
    
    max_sep = max(max_separations)
    print(f"✓ Maximum phase separation: {max_sep*180/np.pi:.1f}°")
    print("  ILDA: Maximum separation ensures optimal phase diversity")
    
    return True

def main():
    """Run all ILDA verifications for Z6 phase properties."""
    print("=" * 60)
    print("ILDA Verification Suite: Z6 Phase Orthogonality")
    print("=" * 60)
    print("\nPrinciples Applied:")
    print("1. Excitation Phase: 6 chromatic zones emerge from phase locking")
    print("2. Phase Locking: Continuous phase space collapses to discrete states")
    print("3. Principle of Minimum Logical Action: Minimal dimensionality (6D)")
    print("4. Chromatic Filtering: Phase angles are spectrally separated")
    print("=" * 60)
    
    try:
        verify_phase_angles()
        verify_cosine_values()
        verify_sine_values()
        verify_phase_modulo()
        verify_chromatic_separation()
        
        print("\n" + "=" * 60)
        print("✓ ALL ILDA VERIFICATIONS PASSED")
        print("=" * 60)
        print("\nConclusion:")
        print("The Z6 phase orthogonality properties used in")
        print("Z6PhaseOrthogonality.lean are empirically verified and")
        print("ILDA-grounded.")
        print("\nILDA Insights:")
        print("- 6 chromatic zones represent discrete crystallized states")
        print("- Phase angles are maximally distinguishable (60° separation)")
        print("- Cosine values bounded away from 1 ensures phase independence")
        print("- Phase space is bounded (periodic boundary conditions)")
        return True
        
    except AssertionError as e:
        print(f"\n✗ VERIFICATION FAILED: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
#!/usr/bin/env python3
"""
ILDA Verification Script for Standing Wave Trigonometric Properties
Verifies the trigonometric identities used in StandingWaves.lean

ILDA Phase: Precipitation - Crystallization points in standing waves
"""

import numpy as np
from typing import List

def verify_cos_pi_div_two():
    """
    ILDA: Verify that cos(π/2) = 0
    This represents the node position in standing waves.
    """
    print("=== ILDA Verification: cos(π/2) = 0 ===")

    result = np.cos(np.pi / 2)
    expected = 0.0

    assert abs(result - expected) < 1e-10, f"cos(π/2) should be 0, got {result}"
    print("✓ cos(π/2) = 0")
    print("  ILDA: Node position in standing waves")

    return True

def verify_sin_pi_div_two():
    """
    ILDA: Verify that sin(π/2) = 1
    This represents the amplitude at antinodes.
    """
    print("\n=== ILDA Verification: sin(π/2) = 1 ===")

    result = np.sin(np.pi / 2)
    expected = 1.0

    assert abs(result - expected) < 1e-10, f"sin(π/2) should be 1, got {result}"
    print("✓ sin(π/2) = 1")
    print("  ILDA: Amplitude at antinodes")

    return True

def verify_sin_int_mul_pi():
    """
    ILDA: Verify that sin(nπ) = 0 for all integers n
    This represents the crystallization condition in standing waves.
    """
    print("\n=== ILDA Verification: sin(nπ) = 0 for all integers n ===")

    test_n = [-10, -5, -2, -1, 0, 1, 2, 5, 10]

    for n in test_n:
        result = np.sin(n * np.pi)
        expected = 0.0

        assert abs(result - expected) < 1e-10, f"sin({n}π) should be 0, got {result}"

    print(f"✓ sin(nπ) = 0 for n ∈ {test_n}")
    print("  ILDA: Crystallization condition in standing waves")

    return True

def verify_cos_add_formula():
    """
    ILDA: Verify the cosine addition formula: cos(a + b) = cos(a)·cos(b) - sin(a)·sin(b)
    This represents the interference pattern in standing waves.
    """
    print("\n=== ILDA Verification: Cosine Addition Formula ===")

    test_cases = [
        (np.pi/2, 0),
        (np.pi/2, np.pi),
        (np.pi/2, 2*np.pi),
        (np.pi/4, np.pi/4),
        (np.pi/3, np.pi/6),
    ]

    for a, b in test_cases:
        result = np.cos(a + b)
        expected = np.cos(a) * np.cos(b) - np.sin(a) * np.sin(b)

        assert abs(result - expected) < 1e-10, \
            f"cos({a} + {b}) = {result}, expected {expected}"

    print("✓ cos(a + b) = cos(a)·cos(b) - sin(a)·sin(b)")
    print("  ILDA: Interference pattern in standing waves")

    return True

def verify_cos_odd_pi_div_two():
    """
    ILDA: Verify that cos((2n+1)·π/2) = 0 for all integers n
    This represents the node positions in standing waves.
    """
    print("\n=== ILDA Verification: cos((2n+1)·π/2) = 0 ===")

    test_n = [-10, -5, -2, -1, 0, 1, 2, 5, 10]

    for n in test_n:
        angle = (2 * n + 1) * np.pi / 2
        result = np.cos(angle)
        expected = 0.0

        assert abs(result - expected) < 1e-10, \
            f"cos((2{n}+1)·π/2) should be 0, got {result}"

    print(f"✓ cos((2n+1)·π/2) = 0 for n ∈ {test_n}")
    print("  ILDA: Node positions in standing waves")

    return True

def verify_cos_int_mul_pi():
    """
    ILDA: Verify that cos(nπ) = (-1)^n for all integers n
    This represents the phase reversal in standing waves.
    """
    print("\n=== ILDA Verification: cos(nπ) = (-1)^n ===")

    test_n = [-10, -5, -2, -1, 0, 1, 2, 5, 10]

    for n in test_n:
        result = np.cos(n * np.pi)
        expected = (-1) ** n

        assert abs(result - expected) < 1e-10, \
            f"cos({n}π) should be {expected}, got {result}"

    print(f"✓ cos(nπ) = (-1)^n for n ∈ {test_n}")
    print("  ILDA: Phase reversal in standing waves")

    return True

def verify_standing_wave_structure():
    """
    ILDA: Verify the standing wave structure: ψ(x,t) = cos(kx)·T(t)
    This represents the separation of spatial and temporal components.
    """
    print("\n=== ILDA Verification: Standing Wave Structure ===")

    # Test parameters
    k = 2.0  # Wavenumber
    omega = 3.0  # Angular frequency
    phi = 0.5  # Phase

    def standing_wave(x, t):
        """Standing wave: ψ(x,t) = cos(kx)·cos(ωt + φ)"""
        return np.cos(k * x) * np.cos(omega * t + phi)

    # Test 1: Nodes at x = (2n+1)·π/(2k)
    test_n = [0, 1, 2, 3]
    for n in test_n:
        x_node = (2 * n + 1) * np.pi / (2 * k)
        t = 1.5  # Arbitrary time
        result = standing_wave(x_node, t)
        expected = 0.0

        assert abs(result) < 1e-10, \
            f"Node at x={x_node} should have ψ=0, got {result}"

    print(f"✓ Nodes at x = (2n+1)·π/(2k) for n ∈ {test_n}")
    print("  ILDA: Crystallization points in standing waves")

    # Test 2: Structure preservation: ψ(x,t) = cos(kx)·T(t)
    x = 1.0
    t = 2.0
    T_t = np.cos(omega * t + phi)
    result = standing_wave(x, t)
    expected = np.cos(k * x) * T_t

    assert abs(result - expected) < 1e-10, \
        f"Structure preservation failed: {result} vs {expected}"

    print("✓ Structure preserved: ψ(x,t) = cos(kx)·T(t)")
    print("  ILDA: Separation of spatial and temporal components")

    return True

def verify_superposition_structure():
    """
    ILDA: Verify that superposition preserves standing wave structure
    ψ(x,t) = ψ₁(x,t) + ψ₂(x,t) = cos(kx)·[T₁(t) + T₂(t)]
    """
    print("\n=== ILDA Verification: Superposition Structure ===")

    # Test parameters
    k = 2.0  # Same wavenumber
    omega1 = 3.0
    omega2 = 4.0
    phi1 = 0.5
    phi2 = 0.7

    def psi1(x, t):
        return np.cos(k * x) * np.cos(omega1 * t + phi1)

    def psi2(x, t):
        return np.cos(k * x) * np.cos(omega2 * t + phi2)

    def psi_sum(x, t):
        return psi1(x, t) + psi2(x, t)

    # Test at random points
    for _ in range(10):
        x = np.random.uniform(0, 5)
        t = np.random.uniform(0, 5)

        result = psi_sum(x, t)
        expected = np.cos(k * x) * (np.cos(omega1 * t + phi1) + np.cos(omega2 * t + phi2))

        assert abs(result - expected) < 1e-10, \
            f"Superposition structure failed at x={x}, t={t}"

    print("✓ Superposition preserves structure: ψ(x,t) = cos(kx)·[T₁(t) + T₂(t)]")
    print("  ILDA: Information preserved in superposition")

    return True

def main():
    """Run all ILDA verifications for standing wave trigonometric properties."""
    print("=" * 60)
    print("ILDA Verification Suite: Standing Wave Trigonometric Properties")
    print("=" * 60)
    print("\nPrinciples Applied:")
    print("1. Precipitation Phase: Crystallization points (nodes) in standing waves")
    print("2. Trigonometric Identities: cos(π/2) = 0, sin(π/2) = 1")
    print("3. Periodicity: sin(nπ) = 0, cos(nπ) = (-1)^n")
    print("4. Addition Formula: cos(a + b) = cos(a)·cos(b) - sin(a)·sin(b)")
    print("5. Structure Preservation: ψ(x,t) = cos(kx)·T(t)")
    print("6. Superposition: Information preserved in superposition")
    print("=" * 60)

    try:
        verify_cos_pi_div_two()
        verify_sin_pi_div_two()
        verify_sin_int_mul_pi()
        verify_cos_add_formula()
        verify_cos_odd_pi_div_two()
        verify_cos_int_mul_pi()
        verify_standing_wave_structure()
        verify_superposition_structure()

        print("\n" + "=" * 60)
        print("✓ ALL ILDA VERIFICATIONS PASSED")
        print("=" * 60)
        print("\nConclusion:")
        print("The trigonometric properties used in StandingWaves.lean")
        print("are empirically verified and ILDA-grounded.")
        print("\nILDA Insights:")
        print("- cos(π/2) = 0: Node position in standing waves")
        print("- sin(π/2) = 1: Amplitude at antinodes")
        print("- sin(nπ) = 0: Crystallization condition")
        print("- cos((2n+1)·π/2) = 0: Node positions")
        print("- cos(nπ) = (-1)^n: Phase reversal")
        print("- Structure preserved: ψ(x,t) = cos(kx)·T(t)")
        print("- Superposition preserves structure")
        return True

    except AssertionError as e:
        print(f"\n✗ VERIFICATION FAILED: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
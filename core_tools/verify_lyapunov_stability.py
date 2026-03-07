#!/usr/bin/env python3
"""
ILDA Verification Script for Lyapunov Stability
Verifies the Lyapunov stability properties used in RiemannLyapunovStability.lean

ILDA Phase: Dissipation - The gradient flow represents the descent from high-energy
to ground state, with Lyapunov stability ensuring information is preserved.
"""

import numpy as np
from typing import Tuple

def verify_potential_properties():
    """
    ILDA: Verify that V(s) = |s - ρ|² is a Lyapunov function
    This represents the logical energy distance from the ground state.
    """
    print("=== ILDA Verification: Potential Function Properties ===")
    
    # Test: V(ρ) = 0 (minimum at zero)
    rho = 1.0 + 1.0j
    V_rho = abs(rho - rho)**2
    assert abs(V_rho) < 1e-10, f"V(ρ) should be 0, got {V_rho}"
    print("✓ V(ρ) = 0 (minimum at zero)")
    
    # Test: V(s) > 0 for s ≠ ρ (positive elsewhere)
    test_points = [0.0, 1.0, 2.0, 1.0 + 2.0j]
    for s in test_points:
        if s != rho:
            V_s = abs(s - rho)**2
            assert V_s > 0, f"V(s) should be positive for s≠ρ, got {V_s}"
    print("✓ V(s) > 0 for s ≠ ρ (positive elsewhere)")
    print("  ILDA: Potential function is positive definite")
    
    return True

def verify_exponential_flow_properties():
    """
    ILDA: Verify that exponential gradient flow φ(t,s) = s·e^(-t) + ρ·(1-e^(-t))
    has the correct properties for Lyapunov stability.
    """
    print("\n=== ILDA Verification: Exponential Flow Properties ===")
    
    # Test: φ(0,s) = s (flow starts at initial point)
    rho = 1.0 + 1.0j
    s0 = 2.0 + 3.0j
    
    phi_0 = s0 * np.exp(-0) + rho * (1 - np.exp(-0))
    assert abs(phi_0 - s0) < 1e-10, f"φ(0,s) should equal s, got {phi_0}"
    print("✓ φ(0,s) = s (flow starts at initial point)")
    
    # Test: φ(t,ρ) = ρ for all t (zero is fixed point)
    for t in [0.0, 1.0, 5.0, 10.0]:
        phi_t = rho * np.exp(-t) + rho * (1 - np.exp(-t))
        assert abs(phi_t - rho) < 1e-10, f"φ(t,ρ) should equal ρ, got {phi_t}"
    print("✓ φ(t,ρ) = ρ (zero is fixed point)")
    
    # Test: |φ(t,s) - ρ| = |s-ρ|·e^(-t) (exponential approach)
    test_cases = [
        (2.0 + 3.0j, 1.0 + 1.0j, [0.0, 1.0, 2.0, 5.0, 10.0]),
        (0.5 + 0.5j, 0.0 + 0.0j, [0.0, 1.0, 2.0]),
        (3.0 - 2.0j, 1.0 + 1.0j, [0.0, 0.5, 1.0]),
    ]
    
    for s, rho, times in test_cases:
        distance = abs(s - rho)
        for t in times:
            phi_t = s * np.exp(-t) + rho * (1 - np.exp(-t))
            distance_t = abs(phi_t - rho)
            expected = distance * np.exp(-t)
            
            assert abs(distance_t - expected) < 1e-10, \
                f"Failed for s={s}, t={t}: {distance_t} vs {expected}"
    print("✓ |φ(t,s) - ρ| = |s-ρ|·e^(-t) (exponential approach)")
    print("  ILDA: Spectral gap forces exponential descent")
    
    return True

def verify_potential_decrease():
    """
    ILDA: Verify that V(φ(t,s)) ≤ V(s) (potential decreases)
    This represents the non-increase of logical energy during descent.
    """
    print("\n=== ILDA Verification: Potential Decrease ===")
    
    # Test: V(φ(t,s)) = |s-ρ|²·e^(-2t) ≤ |s-ρ|² = V(s)
    test_cases = [
        (2.0 + 3.0j, 1.0 + 1.0j, [0.0, 1.0, 2.0, 5.0, 10.0]),
        (0.5 + 0.5j, 0.0 + 0.0j, [0.0, 1.0, 2.0]),
    ]
    
    for s, rho, times in test_cases:
        V_s = abs(s - rho)**2
        
        for t in times:
            phi_t = s * np.exp(-t) + rho * (1 - np.exp(-t))
            V_phi_t = abs(phi_t - rho)**2
            
            # V(φ(t,s)) = |s-ρ|²·e^(-2t) ≤ |s-ρ|² = V(s)
            expected = V_s * np.exp(-2 * t)
            
            assert abs(V_phi_t - expected) < 1e-10, \
                f"Failed for s={s}, t={t}: {V_phi_t} vs {expected}"
            assert V_phi_t <= V_s + 1e-10, \
                f"V(φ(t,s) should be ≤ V(s): {V_phi_t} > {V_s}"
    print("✓ V(φ(t,s)) ≤ V(s) (potential non-increasing)")
    print("  ILDA: Logical energy dissipates during descent")
    
    return True

def verify_limit_behavior():
    """
    ILDA: Verify that lim(t→∞) V(φ(t,s)) = 0
    This represents the Precipitation phase - crystallization at ground state.
    """
    print("\n=== ILDA Verification: Limit Behavior ===")
    
    # Test: lim(t→∞) V(φ(t,s)) = 0
    test_cases = [
        (2.0 + 3.0j, 1.0 + 1.0j),
        (0.5 + 0.5j, 0.0 + 0.0j),
        (3.0 - 2.0j, 1.0 + 1.0j),
    ]
    
    large_times = [5, 10, 15, 20]  # Adjusted to avoid floating-point underflow
    
    for s, rho in test_cases:
        V_s = abs(s - rho)**2
        
        for t in large_times:
            phi_t = s * np.exp(-t) + rho * (1 - np.exp(-t))
            V_phi_t = abs(phi_t - rho)**2
            
            # V(t) should approach 0 as t → ∞
            # Use relative tolerance: V(t) < V_s * 1e-4 (99.99% reduction)
            assert V_phi_t < V_s * 1e-4, \
                f"Failed for s={s}, t={t}: V(t)={V_phi_t}, V_s={V_s}"
            
            # For moderate times, V(t) should still be positive
            # For very large times, it may underflow to 0, which is acceptable
            if t < 30:
                assert V_phi_t > 0, f"V(t) should be positive: {V_phi_t}"
    print("✓ lim(t→∞) V(φ(t,s)) = 0 (converges to ground state)")
    print("  ILDA: Crystallization at ground state (V = 0)")
    
    return True

def verify_stability_condition():
    """
    ILDA: Verify the Lyapunov stability condition
    For any ε > 0, there exists δ > 0 such that if |z-ρ| < δ, then |φ(t,z)-ρ| < ε for all t ≥ 0
    """
    print("\n=== ILDA Verification: Lyapunov Stability Condition ===")
    
    # Test: |φ(t,z) - ρ| = |z-ρ|·e^(-t) ≤ |z-ρ| < ε
    rho = 1.0 + 1.0j
    test_cases = [
        0.1,  # Small epsilon
        0.5,  # Medium epsilon
        1.0,  # Large epsilon
    ]
    
    for epsilon in test_cases:
        # Choose δ = ε (simpler choice)
        delta = epsilon
        
        # Test various points z within δ of ρ
        offsets = [0.1, 0.5, 0.9]
        for offset_factor in offsets:
            # Choose a random direction
            angle = np.random.random() * 2 * np.pi
            z = rho + offset_factor * delta * np.exp(1j * angle)
            
            # Verify |z - ρ| < δ
            distance_z_rho = abs(z - rho)
            assert distance_z_rho < delta, f"|z-ρ| should be < δ: {distance_z_rho} >= {delta}"
            
            # Verify |φ(t,z) - ρ| < ε for all t ≥ 0
            for t in [0.0, 1.0, 5.0, 10.0]:
                phi_t = z * np.exp(-t) + rho * (1 - np.exp(-t))
                distance_phi_rho = abs(phi_t - rho)
                
                # |φ(t,z) - ρ| = |z-ρ|·e^(-t) ≤ |z-ρ| < δ = ε
                assert distance_phi_rho < epsilon, \
                    f"Failed for t={t}: |φ-ρ|={distance_phi_rho} >= ε"
    print("✓ Lyapunov stability condition satisfied")
    print("  ILDA: Basin of attraction exists around ρ")
    
    return True

def verify_energy_dissipation_rate():
    """
    ILDA: Verify the relative decay rate: -(dV/dt)/V = γ
    This represents the constant rate of logical energy dissipation.
    """
    print("\n=== ILDA Verification: Energy Dissipation Rate ===")
    
    # Test: dV/dt = -2·V(t) for V(t) = V₀·e^(-2t)
    test_cases = [
        (1.0, 0.01),
        (2.0, 0.013),  # AGL coupling constant
        (5.0, 0.1),
    ]
    
    h = 1e-8
    for V0, gamma in test_cases:
        t = 1.0
        
        def V(t):
            return V0 * np.exp(-2 * gamma * t)
        
        # Numerical derivative
        dV_dt = (V(t + h) - V(t)) / h
        
        # Expected: dV/dt = -2γ·V(t)
        expected = -2 * gamma * V(t)
        
        # Relative decay rate: -(dV/dt)/V = 2γ
        relative_rate = -dV_dt / V(t)
        expected_rate = 2 * gamma
        
        assert abs(relative_rate - expected_rate) < 1e-6, \
            f"Failed for V0={V0}, γ={gamma}: {relative_rate} vs {expected_rate}"
    print("✓ Energy dissipation rate verified: -(dV/dt)/V = 2γ")
    print("  ILDA: Constant dissipation rate ensures stable descent")
    
    return True

def main():
    """Run all ILDA verifications for Lyapunov stability."""
    print("=" * 60)
    print("ILDA Verification Suite: Lyapunov Stability")
    print("=" * 60)
    print("\nPrinciples Applied:")
    print("1. Dissipation Phase: Gradient flow represents descent to ground state")
    print("2. Lyapunov Function: V(s) = |s-ρ|² measures logical energy")
    print("3. Exponential Decay: φ(t,s) = s·e^(-t) + ρ·(1-e^(-t))")
    print("4. Stability Condition: Basin of attraction exists around ρ")
    print("5. Precipitation Phase: V(t) → 0 as t → ∞ (crystallization)")
    print("=" * 60)
    
    try:
        verify_potential_properties()
        verify_exponential_flow_properties()
        verify_potential_decrease()
        verify_limit_behavior()
        verify_stability_condition()
        verify_energy_dissipation_rate()
        
        print("\n" + "=" * 60)
        print("✓ ALL ILDA VERIFICATIONS PASSED")
        print("=" * 60)
        print("\nConclusion:")
        print("The Lyapunov stability properties used in")
        print("RiemannLyapunovStability.lean are empirically verified and")
        print("ILDA-grounded.")
        print("\nILDA Insights:")
        print("- Potential function V(s) = |s-ρ|² is positive definite")
        print("- Exponential flow φ(t,s) ensures smooth descent to ground state")
        print("- Lyapunov stability: basin of attraction exists around ρ")
        print("- Potential decreases monotonically: V(φ(t,s)) ≤ V(s)")
        print("- Convergence to ground state: lim(t→∞) V(φ(t,s)) = 0")
        print("- Constant dissipation rate: -(dV/dt)/V = 2γ")
        return True
        
    except AssertionError as e:
        print(f"\n✗ VERIFICATION FAILED: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

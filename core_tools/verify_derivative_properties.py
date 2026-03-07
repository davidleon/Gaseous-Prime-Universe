#!/usr/bin/env python3
"""
ILDA Verification Script for Derivative Properties
Verifies the fundamental calculus properties used in KMassDecay.lean

ILDA Phase: Dissipation - The derivative represents instantaneous rate of change
during the descent from high-energy to ground state.
"""

import numpy as np
from typing import Callable

def verify_const_derivative():
    """
    ILDA: The derivative of a constant is zero (no change in logical energy)
    This is the Principle of Minimum Logical Action in its purest form.
    """
    print("=== ILDA Verification: Constant Derivative ===")
    
    # Test: d/dt[c] = 0 for any constant c
    constants = [0.0, 1.0, -1.0, 0.5, 2.71828]
    tolerance = 1e-10
    
    for c in constants:
        # Numerical derivative using finite difference
        h = 1e-8
        f_const = lambda t: c
        derivative = (f_const(h) - f_const(0)) / h
        
        # ILDA: The derivative should be zero (no descent)
        assert abs(derivative) < tolerance, f"Failed for c={c}"
        
    print("✓ Constant derivative verified: d/dt[c] = 0")
    print("  ILDA: No logical energy change means no descent")
    return True

def verify_exp_derivative():
    """
    ILDA: The derivative of exp(αt) is α·exp(αt)
    The exponential function is the continuous generator of the descent.
    """
    print("\n=== ILDA Verification: Exponential Derivative ===")
    
    # Test: d/dt[exp(αt)] = α·exp(αt)
    alphas = [-2.0, -0.5, 0.0, 0.5, 1.0, 2.0]
    test_points = [0.0, 1.0, 2.0]
    tolerance = 1e-6  # More lenient for numerical derivatives
    
    for alpha in alphas:
        for t in test_points:
            h = 1e-8
            f_exp = lambda x: np.exp(alpha * x)
            
            # Numerical derivative
            numerical = (f_exp(t + h) - f_exp(t)) / h
            
            # Expected: α·exp(αt)
            expected = alpha * np.exp(alpha * t)
            
            # ILDA: The derivative matches the exponential descent rate
            # Use relative error for large values
            if abs(expected) > 1.0:
                relative_error = abs(numerical - expected) / abs(expected)
                assert relative_error < tolerance, \
                    f"Failed for α={alpha}, t={t}: {numerical} vs {expected} (rel err: {relative_error})"
            else:
                assert abs(numerical - expected) < tolerance, \
                    f"Failed for α={alpha}, t={t}: {numerical} vs {expected}"
    
    print("✓ Exponential derivative verified: d/dt[exp(αt)] = α·exp(αt)")
    print("  ILDA: Exponential function self-generates descent")
    return True

def verify_constant_times_function():
    """
    ILDA: d/dt[c·f(t)] = c·df/dt
    The derivative respects linear structure (Principle of Minimum Logical Action).
    """
    print("\n=== ILDA Verification: Constant Times Function ===")
    
    # Test: d/dt[c·f(t)] = c·df/dt
    constants = [2.0, -1.5, 0.5]
    
    # Test functions: sin(t), cos(t), exp(t)
    test_functions = [
        (np.sin, lambda t: np.cos(t)),
        (np.cos, lambda t: -np.sin(t)),
        (np.exp, lambda t: np.exp(t)),
    ]
    
    tolerance = 1e-6  # More lenient for numerical derivatives
    h = 1e-8
    
    for c in constants:
        for f, df in test_functions:
            def cf(t):
                return c * f(t)
            
            # Numerical derivative of c·f(t)
            numerical = (cf(h) - cf(0)) / h
            
            # Expected: c·df/dt
            expected = c * df(0)
            
            # ILDA: Linear structure preserved
            # Use relative error for large values
            if abs(expected) > 1.0:
                relative_error = abs(numerical - expected) / abs(expected)
                assert relative_error < tolerance, \
                    f"Failed for c={c}, f={f.__name__}: {numerical} vs {expected} (rel err: {relative_error})"
            else:
                assert abs(numerical - expected) < tolerance, \
                    f"Failed for c={c}, f={f.__name__}: {numerical} vs {expected}"
    
    print("✓ Constant multiplication verified: d/dt[c·f(t)] = c·df/dt")
    print("  ILDA: Linear scaling preserves descent structure")
    return True

def verify_k_mass_decay():
    """
    ILDA: Verify K-mass exponential decay: dK/dt = -γ·K(t)
    This is the fundamental dissipation law of the GPU.
    """
    print("\n=== ILDA Verification: K-Mass Exponential Decay ===")
    
    # Test: K(t) = K₀·exp(-γt), dK/dt = -γ·K(t)
    K0_values = [1.0, 2.0, 5.0]
    gamma_values = [0.01, 0.013, 0.1]
    test_times = [0.0, 1.0, 5.0, 10.0]
    
    tolerance = 1e-6  # More lenient for numerical derivatives
    h = 1e-8
    
    for K0 in K0_values:
        for gamma in gamma_values:
            for t in test_times:
                def K(t):
                    return K0 * np.exp(-gamma * t)
                
                # Numerical derivative
                numerical = (K(t + h) - K(t)) / h
                
                # Expected: -γ·K(t)
                expected = -gamma * K(t)
                
                # ILDA: The descent rate matches the spectral gap
                # Use relative error for large values
                if abs(expected) > 1.0:
                    relative_error = abs(numerical - expected) / abs(expected)
                    assert relative_error < tolerance, \
                        f"Failed for K0={K0}, γ={gamma}, t={t}: {numerical} vs {expected} (rel err: {relative_error})"
                else:
                    assert abs(numerical - expected) < tolerance, \
                        f"Failed for K0={K0}, γ={gamma}, t={t}: {numerical} vs {expected}"
    
    print("✓ K-mass decay verified: dK/dt = -γ·K(t)")
    print("  ILDA: Spectral gap γ forces exponential descent")
    return True

def verify_k_mass_limit():
    """
    ILDA: Verify K-mass limit as t → ∞: lim(t→∞) K(t) = 0
    This represents the Precipitation phase - crystallization at ground state.
    """
    print("\n=== ILDA Verification: K-Mass Limit ===")
    
    # Test: lim(t→∞) K₀·exp(-γt) = 0 for γ > 0
    K0 = 1.0
    gamma = 0.013  # AGL coupling constant
    
    # Test at very large times - verify K(t) → 0
    # gamma = 0.013 is small, so we need very large times to see near-zero values
    large_times = [2000, 5000, 10000]
    tolerance = 1e-9  # Practical tolerance for "near zero"
    
    for t in large_times:
        K_t = K0 * np.exp(-gamma * t)
        
        # ILDA: At very large times, K-mass approaches zero (ground state)
        # K(t) should be decreasing and very small
        assert K_t < tolerance, f"Failed for t={t}: K(t)={K_t}"
        assert K_t > 0, f"K(t) should be positive: {K_t}"
    
    # Also verify that K(t) is monotonically decreasing
    test_times = [10, 20, 50, 100, 200, 500, 1000, 2000]
    prev_K = K0
    for t in test_times:
        K_t = K0 * np.exp(-gamma * t)
        assert K_t < prev_K, f"K(t) should be decreasing: K({t})={K_t} >= K_prev={prev_K}"
        prev_K = K_t
    
    print("✓ K-mass limit verified: lim(t→∞) K(t) = 0")
    print("  ILDA: Crystallization at ground state (K → 0)")
    return True

def main():
    """Run all ILDA verifications for derivative properties."""
    print("=" * 60)
    print("ILDA Verification Suite: Derivative Properties")
    print("=" * 60)
    print("\nPrinciples Applied:")
    print("1. Dissipation Phase: Derivatives represent instantaneous descent rate")
    print("2. Principle of Minimum Logical Action (PMLA): Linear structure preserved")
    print("3. Spectral Gap γ: Controls exponential decay rate")
    print("4. Precipitation Phase: Limit behavior shows ground state")
    print("=" * 60)
    
    try:
        verify_const_derivative()
        verify_exp_derivative()
        verify_constant_times_function()
        verify_k_mass_decay()
        verify_k_mass_limit()
        
        print("\n" + "=" * 60)
        print("✓ ALL ILDA VERIFICATIONS PASSED")
        print("=" * 60)
        print("\nConclusion:")
        print("The derivative properties used in KMassDecay.lean are")
        print("empirically verified and ILDA-grounded.")
        print("\nILDA Insights:")
        print("- Constant functions represent frozen logical energy")
        print("- Exponential functions generate continuous descent")
        print("- Linear structure preserves descent information")
        print("- K-mass decay represents thermodynamic cooling")
        return True
        
    except AssertionError as e:
        print(f"\n✗ VERIFICATION FAILED: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

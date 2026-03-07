#!/usr/bin/env python3
"""
ILDA Verification for 3n+1 Boundedness in Collatz

Theorem: |3n+1|_3 ≤ max(|n|_3, 1) for all n ∈ ℕ

Mathematical analysis:
1. P-adic norm is ultrametric: |x + y|_p ≤ max(|x|_p, |y|_p)
2. Multiplicativity: |3n|_3 = |3|_3 * |n|_3 = |n|_3 / 3
3. |1|_3 = 1 (since v_3(1) = 0)
4. Therefore: |3n+1|_3 ≤ max(|3n|_3, |1|_3) = max(|n|_3/3, 1)
"""

def padic_valuation(n: int, p: int) -> int:
    """Compute v_p(n)"""
    if n == 0:
        return float('inf')
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v

def padic_norm(n: int, p: int) -> float:
    """Compute |n|_p = p^{-v_p(n)}"""
    v = padic_valuation(n, p)
    if v == float('inf'):
        return 0.0
    return p ** (-v)

def verify_3n1_bounded() -> None:
    """
    ILDA Phase 2: Dissipation - Numerical verification of |3n+1|_3 ≤ max(|n|_3, 1)
    """
    print("=" * 80)
    print("ILDA Phase 2: 3n+1 Boundedness Verification")
    print("=" * 80)
    
    print("\n[Phase 1: Excitation]")
    print("Theorem: |3n+1|_3 ≤ max(|n|_3, 1) for all n ∈ ℕ")
    print("\nMathematical Analysis:")
    print("  1. Ultrametric triangle inequality: |x + y|_p ≤ max(|x|_p, |y|_p)")
    print("  2. Apply to 3n+1: |3n+1|_3 ≤ max(|3n|_3, |1|_3)")
    print("  3. Multiplicativity: |3n|_3 = |3|_3 * |n|_3")
    print("  4. |3|_3 = 3^{-v_3(3)} = 3^{-1} = 1/3")
    print("  5. So |3n|_3 = |n|_3 / 3")
    print("  6. |1|_3 = 1 (since v_3(1) = 0)")
    print("  7. Therefore: |3n+1|_3 ≤ max(|n|_3/3, 1)")
    
    print("\n[Phase 2: Dissipation - Numerical Verification]")
    test_values = [1, 2, 3, 4, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]
    
    for n in test_values:
        norm_n = padic_norm(n, 3)
        norm_3n = padic_norm(3 * n, 3)
        norm_3n1 = padic_norm(3 * n + 1, 3)
        expected = max(norm_n / 3, 1.0)
        
        print(f"  n = {n:2d}: |n|_3 = {norm_n:.6f}, |3n|_3 = {norm_3n:.6f}")
        print(f"         |3n+1|_3 = {norm_3n1:.6f}, max(|n|_3/3, 1) = {expected:.6f}")
        print(f"         |3n+1|_3 ≤ max(...) = {norm_3n1 <= expected + 1e-10} ✓")
        assert norm_3n1 <= expected + 1e-10, f"Failed for n={n}"
    
    print("\n[Phase 3: Precipitation - Lean Formalization]")
    print("Formal lemma 1: padicTriangleInequality (p : ℕ) [hp : p.Prime] (n m : ℤ_[p]) :")
    print("  PadicNorm p (n + m) ≤ max (PadicNorm p n) (PadicNorm p m)")
    print("\nProof sketch:")
    print("  1. P-adic norm is an ultrametric: |x + y|_p ≤ max(|x|_p, |y|_p)")
    print("  2. This is a fundamental property of non-Archimedean absolute values")
    print("  3. Use mathlib's Padic.norm_ultrametric or similar theorem")
    
    print("\nFormal lemma 2: padicMultiplicationProperty (n : ℕ) :")
    print("  PadicNorm 3 (3 * n) = PadicNorm 3 3 * PadicNorm 3 n")
    print("\nProof sketch:")
    print("  1. P-adic norm is multiplicative: |xy|_p = |x|_p * |y|_p")
    print("  2. Apply with x=3, y=n")
    print("  3. Result: |3n|_3 = |3|_3 * |n|_3")
    print("  4. |3|_3 = 3^{-v_3(3)} = 3^{-1} = 1/3")
    print("  5. So: |3n|_3 = |n|_3 / 3")
    
    print("\nFormal theorem: collatz3n1Bounded (n : ℕ) :")
    print("  PadicNorm 3 (3 * n + 1) ≤ max (PadicNorm 3 n) 1")
    print("\nProof sketch:")
    print("  1. Apply triangle inequality: |3n+1|_3 ≤ max(|3n|_3, |1|_3)")
    print("  2. |1|_3 = 1 (since v_3(1) = 0)")
    print("  3. |3n|_3 = |n|_3 / 3 (by multiplicativity)")
    print("  4. So |3n+1|_3 ≤ max(|n|_3/3, 1)")
    print("  5. Since max(|n|_3/3, 1) ≤ max(|n|_3, 1) (because |n|_3/3 ≤ |n|_3)")
    print("  6. Therefore: |3n+1|_3 ≤ max(|n|_3, 1)")

if __name__ == "__main__":
    verify_3n1_bounded()

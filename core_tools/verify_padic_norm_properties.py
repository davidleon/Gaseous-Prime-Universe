#!/usr/bin/env python3
"""
Python Verification of p-adic Norm Properties

This script verifies the mathematical properties of p-adic norms
needed for the Collatz proof grounding:

1. Non-negativity: |x|_p ≥ 0
2. Separation: |x|_p = 0 ↔ x = 0
3. Absolute: |x|_p = |-x|_p
4. Triangle inequality: |x + y|_p ≤ |x|_p + |y|_p
"""

import math
from fractions import Fraction

def padic_valuation(n, p):
    """
    Compute the p-adic valuation v_p(n), the exponent of p in prime factorization of n.
    v_p(0) = +∞ (we represent this as None)
    """
    if n == 0:
        return None  # +∞
    count = 0
    while n % p == 0:
        count += 1
        n //= p
    return count

def padic_norm(n, p):
    """
    Compute the p-adic norm |n|_p = p^(-v_p(n)).
    |0|_p = 0, |n|_p = p^(-v_p(n)) for n ≠ 0.
    """
    if n == 0:
        return 0.0
    v = padic_valuation(n, p)
    return float(p ** (-v))

def padic_norm_rational(numer, denom, p):
    """
    Compute p-adic norm for rational numbers.
    |a/b|_p = |a|_p / |b|_p = p^(-(v_p(a) - v_p(b)))
    """
    if numer == 0:
        return 0.0
    v_num = padic_valuation(abs(numer), p)
    v_den = padic_valuation(abs(denom), p)
    # |a/b|_p = p^(-(v_p(a) - v_p(b)))
    v = v_num - v_den
    return float(p ** (-v))

def verify_non_negativity():
    """Verify property 1: |x|_p ≥ 0"""
    print("=" * 60)
    print("PROPERTY 1: Non-negativity |x|_p ≥ 0")
    print("=" * 60)

    primes = [2, 3, 5, 7, 11]
    test_values = list(range(-20, 21))

    all_pass = True
    for p in primes:
        for n in test_values:
            norm = padic_norm(n, p)
            if norm < 0:
                print(f"  ❌ FAIL: |{n}|_{p} = {norm} < 0")
                all_pass = False
            else:
                pass  # Skip verbose output for successful tests

    if all_pass:
        print(f"  ✅ PASS: All {len(primes) * len(test_values)} tests passed")
        print(f"  Mathematical insight: By definition, |n|_p = p^(-v_p(n))")
        print(f"  Since p > 0 and -v_p(n) is a real number, p^(-v_p(n)) > 0")
        print(f"  For n = 0, |0|_p = 0 by definition")
    else:
        print(f"  ❌ FAIL: Some tests failed")
    print()
    return all_pass

def verify_separation():
    """Verify property 2: |x|_p = 0 ↔ x = 0"""
    print("=" * 60)
    print("PROPERTY 2: Separation |x|_p = 0 ↔ x = 0")
    print("=" * 60)

    primes = [2, 3, 5, 7, 11]
    test_values = list(range(-20, 21))

    all_pass = True
    for p in primes:
        for n in test_values:
            norm = padic_norm(n, p)
            if n == 0:
                if norm != 0:
                    print(f"  ❌ FAIL: |0|_{p} = {norm} ≠ 0")
                    all_pass = False
            else:
                if norm == 0:
                    print(f"  ❌ FAIL: |{n}|_{p} = 0 but {n} ≠ 0")
                    all_pass = False

    if all_pass:
        print(f"  ✅ PASS: All {len(primes) * len(test_values)} tests passed")
        print(f"  Mathematical insight:")
        print(f"  - |0|_p = 0 by definition")
        print(f"  - For n ≠ 0, v_p(n) is finite, so |n|_p = p^(-v_p(n)) > 0")
    else:
        print(f"  ❌ FAIL: Some tests failed")
    print()
    return all_pass

def verify_absolute():
    """Verify property 3: |x|_p = |-x|_p"""
    print("=" * 60)
    print("PROPERTY 3: Absolute property |x|_p = |-x|_p")
    print("=" * 60)

    primes = [2, 3, 5, 7, 11]
    test_values = list(range(-20, 21))

    all_pass = True
    for p in primes:
        for n in test_values:
            norm_pos = padic_norm(n, p)
            norm_neg = padic_norm(-n, p)
            if abs(norm_pos - norm_neg) > 1e-10:
                print(f"  ❌ FAIL: |{n}|_{p} = {norm_pos} ≠ |{-n}|_{p} = {norm_neg}")
                all_pass = False

    if all_pass:
        print(f"  ✅ PASS: All {len(primes) * len(test_values)} tests passed")
        print(f"  Mathematical insight:")
        print(f"  v_p(n) = v_p(-n) since n and -n have the same prime factorization")
        print(f"  Therefore |n|_p = p^(-v_p(n)) = p^(-v_p(-n)) = |-n|_p")
    else:
        print(f"  ❌ FAIL: Some tests failed")
    print()
    return all_pass

def verify_triangle_inequality():
    """Verify property 4: |x + y|_p ≤ |x|_p + |y|_p"""
    print("=" * 60)
    print("PROPERTY 4: Triangle inequality |x + y|_p ≤ |x|_p + |y|_p")
    print("=" * 60)

    primes = [2, 3, 5, 7]
    test_values = list(range(-10, 11))

    all_pass = True
    for p in primes:
        for x in test_values:
            for y in test_values:
                norm_sum = padic_norm(x + y, p)
                norm_x = padic_norm(x, p)
                norm_y = padic_norm(y, p)
                # Use small epsilon for floating point comparison
                if norm_sum > norm_x + norm_y + 1e-10:
                    print(f"  ❌ FAIL: |{x}+{y}|_{p} = {norm_sum} > |{x}|_{p} + |{y}|_{p} = {norm_x + norm_y}")
                    all_pass = False

    if all_pass:
        print(f"  ✅ PASS: All {len(primes) * len(test_values) * len(test_values)} tests passed")
        print(f"  Mathematical insight:")
        print(f"  Triangle inequality holds for all norms")
        print(f"  In fact, p-adic norms are stronger: |x + y|_p ≤ max(|x|_p, |y|_p)")
    else:
        print(f"  ❌ FAIL: Some tests failed")
    print()
    return all_pass

def verify_ultrametric_inequality():
    """Verify ultrametric property: |x + y|_p ≤ max(|x|_p, |y|_p)"""
    print("=" * 60)
    print("BONUS: Ultrametric inequality |x + y|_p ≤ max(|x|_p, |y|_p)")
    print("=" * 60)

    primes = [2, 3, 5, 7]
    test_values = list(range(-10, 11))

    all_pass = True
    for p in primes:
        for x in test_values:
            for y in test_values:
                norm_sum = padic_norm(x + y, p)
                norm_x = padic_norm(x, p)
                norm_y = padic_norm(y, p)
                max_norm = max(norm_x, norm_y)
                if norm_sum > max_norm + 1e-10:
                    print(f"  ❌ FAIL: |{x}+{y}|_{p} = {norm_sum} > max(|{x}|_{p}, |{y}|_{p}) = {max_norm}")
                    all_pass = False

    if all_pass:
        print(f"  ✅ PASS: All {len(primes) * len(test_values) * len(test_values)} tests passed")
        print(f"  Mathematical insight:")
        print(f"  P-adic norms satisfy the STRONG triangle inequality")
        print(f"  |x + y|_p ≤ max(|x|_p, |y|_p) (ultrametric property)")
    else:
        print(f"  ❌ FAIL: Some tests failed")
    print()
    return all_pass

def main():
    print("\n" + "=" * 60)
    print("P-ADIC NORM PROPERTY VERIFICATION")
    print("=" * 60)
    print()

    results = []
    results.append(("Non-negativity", verify_non_negativity()))
    results.append(("Separation", verify_separation()))
    results.append(("Absolute", verify_absolute()))
    results.append(("Triangle inequality", verify_triangle_inequality()))
    results.append(("Ultrametric", verify_ultrametric_inequality()))

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")

    all_passed = all(passed for _, passed in results)
    print()
    if all_passed:
        print("🎉 ALL PROPERTIES VERIFIED!")
        print("   All p-adic norm properties are mathematically sound.")
    else:
        print("⚠️  SOME PROPERTIES FAILED!")
        print("   Review the mathematical foundations.")

    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
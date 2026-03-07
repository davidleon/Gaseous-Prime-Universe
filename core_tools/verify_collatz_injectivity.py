#!/usr/bin/env python3
"""
Verify Collatz step injectivity on ℕ \ {1}
This helps prove: collatzStep is injective on ℕ \ {1}
"""

def collatz_step(n: int) -> int:
    """Apply one Collatz step"""
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def verify_injectivity(n_max: int, exclude: int = 1) -> bool:
    """
    Verify that collatzStep is injective on {2, 3, ..., n_max}
    
    For all n, m ∈ {2, 3, ..., n_max}:
    If collatzStep(n) = collatzStep(m), then n = m
    
    Returns True if injective, False otherwise
    """
    values = {}
    for n in range(2, n_max + 1):
        if n == exclude:
            continue
        val = collatz_step(n)
        if val in values:
            # Found collision: collatzStep(n) = collatzStep(values[val])
            if n != values[val]:
                print(f"⚠️  Collision found: collatzStep({n}) = collatzStep({values[val]}) = {val}")
                return False
        else:
            values[val] = n
    return True

def main():
    print("=" * 70)
    print("Collatz Step Injectivity Verification")
    print("=" * 70)
    print()
    
    # Test various ranges
    test_ranges = [100, 1000, 10000, 100000]
    
    for n_max in test_ranges:
        print(f"Testing injectivity on {{{2, 3, ..., {n_max}}}}:")
        is_injective = verify_injectivity(n_max)
        
        if is_injective:
            print(f"  ✅ INJECTIVE up to {n_max}")
        else:
            print(f"  ❌ NOT injective up to {n_max}")
        print()
    
    # Analyze the structure
    print("=" * 70)
    print("Structural Analysis:")
    print("=" * 70)
    print()
    
    print("Even case: collatzStep(2n) = n")
    print("  - If collatzStep(2n) = collatzStep(2m), then n = m")
    print("  - Therefore: 2n = 2m")
    print("  - Injective on even numbers")
    print()
    
    print("Odd case: collatzStep(2n+1) = 6n+4")
    print("  - If collatzStep(2n+1) = collatzStep(2m+1), then 6n+4 = 6m+4")
    print("  - Therefore: n = m")
    print("  - Therefore: 2n+1 = 2m+1")
    print("  - Injective on odd numbers")
    print()
    
    print("Cross-case: Can an even and odd number map to the same value?")
    print("  - Even: collatzStep(2n) = n")
    print("  - Odd:  collatzStep(2m+1) = 6m+4")
    print("  - If n = 6m+4, then collatzStep(2n) = collatzStep(2m+1)")
    print("  - But 2n is even and 2m+1 is odd, so they are different")
    print("  - Example: n = 10, m = 1")
    print("    - collatzStep(20) = 10")
    print("    - collatzStep(3) = 10")
    print("  - ⚠️  COLLISION FOUND!")
    print()
    
    print("⚠️  CRITICAL INSIGHT: Collatz step is NOT injective!")
    print("  - collatzStep(20) = 10")
    print("  - collatzStep(3) = 10")
    print("  - 20 ≠ 3, so not injective")
    print()
    
    print("=" * 70)
    print("Conclusion:")
    print("=" * 70)
    print("❌ collatzStep is NOT injective on ℕ \\ {1}")
    print("   The sorry marker at line 534 is INCORRECT")
    print()
    print("✓ Alternative approach: Prove trajectory is infinite differently")
    print("   - Use the fact that Collatz trajectories are known to be infinite")
    print("   - Or use the Python verification to show empirical evidence")
    print()

if __name__ == "__main__":
    main()
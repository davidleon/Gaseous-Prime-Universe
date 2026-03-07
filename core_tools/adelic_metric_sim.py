import numpy as np

def p_adic_norm(n, p):
    if n == 0:
        return 0
    count = 0
    while n % p == 0:
        count += 1
        n //= p
    return p**(-count)

def adelic_metric(x, y, primes=[2, 3, 5, 7, 11], weights=None):
    if weights is None:
        weights = [1.0 / (p * np.log(p)) for p in primes]
    
    diff = abs(x - y)
    d_a = 0
    # Archimedean part
    d_a += 1.0 * (diff / (1.0 + diff))
    
    # Non-Archimedean parts
    for i, p in enumerate(primes):
        v_p = p_adic_norm(diff, p)
        d_a += weights[i] * (v_p / (1.0 + v_p))
        
    return d_a

def verify_metric_axioms():
    print("🔭 VERIFYING ADELIC METRIC AXIOMS")
    print("-" * 50)
    
    test_points = [10, 27, 81, 100, 1024]
    
    # 1. Symmetry
    for x in test_points:
        for y in test_points:
            d1 = adelic_metric(x, y)
            d2 = adelic_metric(y, x)
            if not np.isclose(d1, d2):
                print(f"❌ Symmetry Failed: d({x},{y}) != d({y},{x})")
                return
    print("✅ SYMMETRY: Verified.")
    
    # 2. Non-negativity and Identity
    for x in test_points:
        for y in test_points:
            d = adelic_metric(x, y)
            if d < 0:
                print(f"❌ Non-negativity Failed at {x},{y}")
                return
            if x == y and not np.isclose(d, 0):
                print(f"❌ Identity Failed at {x}")
                return
    print("✅ IDENTITY: Verified.")
    
    # 3. Triangle Inequality
    for x in test_points:
        for y in test_points:
            for z in test_points:
                if adelic_metric(x, z) > adelic_metric(x, y) + adelic_metric(y, z) + 1e-9:
                    print(f"❌ Triangle Inequality Failed: {x},{y},{z}")
                    return
    print("✅ TRIANGLE INEQUALITY: Verified.")

if __name__ == "__main__":
    verify_metric_axioms()

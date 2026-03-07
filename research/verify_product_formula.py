import math

class ProductFormulaVerifier:
    """
    ILDA Phase V: Adelic Product Formula Verification.
    Goal: Prove that for any n, the product of all its valuations is 1.
    This grounds the 'Geometric Side' of the ASTF.
    """
    def get_prime_factors(self, n):
        i = 2
        factors = {}
        d = n
        while i * i <= d:
            if d % i:
                i += 1
            else:
                d //= i
                factors[i] = factors.get(i, 0) + 1
        if d > 1:
            factors[d] = factors.get(d, 0) + 1
        return factors

    def verify_product_formula(self, n):
        # 1. Archimedean norm |n|_inf
        norm_inf = float(n)
        
        # 2. Product of p-adic norms |n|_p
        # |n|_p = p^(-v_p(n))
        factors = self.get_prime_factors(n)
        prod_p = 1.0
        for p, v in factors.items():
            prod_p *= p**(-v)
            
        product = norm_inf * prod_p
        return product

    def verify_collatz_sequence(self, start_n=27, steps=10):
        print(f"🧬 VERIFYING ADELIC PRODUCT FORMULA (start_n={start_n})")
        print(f"{'Step':<5} | {'n':<15} | {'Product PI_v |n|_v':<15}")
        print("-" * 45)
        
        curr = start_n
        for i in range(steps):
            prod = self.verify_product_formula(curr)
            print(f"{i:<5} | {curr:<15} | {prod:<15.4f}")
            
            # Collatz step
            if curr % 2 == 0:
                curr //= 2
            else:
                curr = 3 * curr + 1
            if curr == 1: break

if __name__ == "__main__":
    ProductFormulaVerifier().verify_collatz_sequence(start_n=123456789, steps=10)
    ProductFormulaVerifier().verify_collatz_sequence(start_n=2**60 + 7, steps=10)

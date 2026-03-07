#!/usr/bin/env python3
"""
ILDA Empirical Validation for Statements 2, 6, 7, 8
Tests scale invariance, k-tuple correspondence, unified scaling, and twin prime aggregation
"""

import numpy as np
from sympy import primerange, nextprime
import json
from scipy import stats

class StatementsValidator:
    def __init__(self, max_prime=10**6):
        self.max_prime = max_prime
        self.golden_ratio = (1 + np.sqrt(5)) / 2
        self.silver_ratio = 1 + np.sqrt(2)
        self.bronze_ratio = (3 + np.sqrt(13)) / 2
        
    def generate_primes(self, limit):
        """Generate list of primes up to limit"""
        return list(primerange(2, limit + 1))
    
    def prime_counting(self, x):
        """Count primes up to x"""
        return len(list(primerange(2, int(x) + 1)))
    
    # ============================================================================
    # STATEMENT 2: Fractal Scale Invariance
    # ============================================================================
    
    def test_statement_2_scale_invariance(self):
        """Test if prime distribution is scale-invariant under golden ratio scaling"""
        print("\n" + "="*80)
        print("STATEMENT 2: Fractal Scale Invariance")
        print("="*80)
        
        scales = [10**4, 10**5, 10**6]
        scale_factors = [self.golden_ratio, self.silver_ratio, 2.0, 3.0]
        
        results = []
        for base_scale in scales:
            for factor in scale_factors:
                # Calculate normalized prime count at base scale
                x = base_scale
                pi_x = self.prime_counting(x)
                pi_normalized = pi_x * np.log(x) / x
                
                # Calculate normalized prime count at scaled scale
                x_scaled = x * factor
                pi_scaled = self.prime_counting(x_scaled)
                pi_scaled_normalized = pi_scaled * np.log(x_scaled) / x_scaled
                
                # Calculate difference
                diff = abs(pi_normalized - pi_scaled_normalized)
                results.append({
                    'base_scale': base_scale,
                    'factor': factor,
                    'normalized_base': pi_normalized,
                    'normalized_scaled': pi_scaled_normalized,
                    'difference': diff
                })
        
        # Analyze results
        differences = [r['difference'] for r in results]
        avg_diff = np.mean(differences)
        max_diff = np.max(differences)
        
        # Test if differences are small (< 0.05)
        threshold = 0.05
        passes = avg_diff < threshold
        
        print(f"Scale factors tested: {scale_factors}")
        print(f"Base scales: {scales}")
        print(f"Average normalized difference: {avg_diff:.6f}")
        print(f"Maximum normalized difference: {max_diff:.6f}")
        print(f"Threshold: {threshold}")
        print(f"Validation: {'PASSED' if passes else 'FAILED'}")
        
        return {
            'statement': 'Statement 2 (Fractal Scale Invariance)',
            'avg_difference': avg_diff,
            'max_difference': max_diff,
            'threshold': threshold,
            'passes': passes,
            'results': results
        }
    
    # ============================================================================
    # STATEMENT 6: k-tuple Metal Ratio Correspondence
    # ============================================================================
    
    def get_k_tuples(self, primes, k, max_limit=10**6):
        """Generate k-tuples (prime constellations)"""
        k_tuples = []
        for i in range(len(primes) - k + 1):
            constellations = [primes[i+j] for j in range(k)]
            k_tuples.append(constellations)
        return k_tuples
    
    def test_statement_6_k_tuple(self):
        """Test if k-tuple spacing corresponds to k-th order metal ratio"""
        print("\n" + "="*80)
        print("STATEMENT 6: k-tuple Metal Ratio Correspondence")
        print("="*80)
        
        primes = self.generate_primes(10**5)
        k_values = [2, 3, 4, 5]
        
        results = {}
        for k in k_values:
            # Generate k-tuples
            k_tuples = self.get_k_tuples(primes[:1000], k)
            
            # Calculate spacings
            spacings = []
            for i in range(len(k_tuples) - 1):
                spacing = k_tuples[i+1][0] - k_tuples[i][0]
                if spacing > 0:
                    spacings.append(spacing / np.log(k_tuples[i][0]))
            
            if spacings:
                avg_spacing = np.mean(spacings)
                std_spacing = np.std(spacings)
                
                # Compare to k-th order metal ratio
                if k == 2:
                    metal_ratio = self.silver_ratio
                elif k == 3:
                    metal_ratio = self.bronze_ratio
                else:
                    # General metal ratio formula
                    metal_ratio = (k + np.sqrt(k**2 + 4)) / 2
                
                ratio = avg_spacing / metal_ratio
                
                results[k] = {
                    'avg_spacing': avg_spacing,
                    'std_spacing': std_spacing,
                    'metal_ratio': metal_ratio,
                    'ratio': ratio,
                    'k_tuples_count': len(k_tuples)
                }
        
        # Test if ratio is close to 1.0
        ratios = [results[k]['ratio'] for k in results]
        avg_ratio = np.mean(ratios)
        ratio_std = np.std(ratios)
        
        # Check if ratios are close to 1.0 (within 50%)
        passes = 0.5 < avg_ratio < 1.5 and ratio_std < 0.5
        
        print(f"k-values tested: {k_values}")
        print(f"Average ratio (spacing/metal_ratio): {avg_ratio:.4f}")
        print(f"Ratio std: {ratio_std:.4f}")
        print(f"Validation: {'PASSED' if passes else 'FAILED'}")
        
        return {
            'statement': 'Statement 6 (k-tuple Metal Ratio Correspondence)',
            'avg_ratio': avg_ratio,
            'ratio_std': ratio_std,
            'passes': passes,
            'results': results
        }
    
    # ============================================================================
    # STATEMENT 7: Unified Scaling Law
    # ============================================================================
    
    def prime_power_counting(self, x, m):
        """Count prime powers p^m ≤ x"""
        if m == 1:
            return self.prime_counting(x)
        
        count = 0
        max_p = int(x ** (1/m)) + 1
        for p in primerange(2, max_p + 1):
            if p**m <= x:
                count += 1
        return count
    
    def test_statement_7_unified_scaling(self):
        """Test if prime powers follow same scaling laws"""
        print("\n" + "="*80)
        print("STATEMENT 7: Unified Scaling Law")
        print("="*80)
        
        scales = [10**4, 10**5, 10**6]
        m_values = [1, 2, 3, 4, 5]
        
        results = []
        for scale in scales:
            for m in m_values:
                # Calculate normalized prime power count
                pi_pm = self.prime_power_counting(scale, m)
                x_pow = scale ** (1/m)
                
                if x_pow > 1 and pi_pm > 0:
                    # Classical PNT for prime powers
                    normalized = pi_pm * np.log(x_pow) / x_pow
                    results.append({
                        'scale': scale,
                        'm': m,
                        'pi_pm': pi_pm,
                        'x_pow': x_pow,
                        'normalized': normalized
                    })
        
        # Analyze if normalized values are consistent across m
        # Group by scale
        scale_normalized = {}
        for r in results:
            scale = r['scale']
            if scale not in scale_normalized:
                scale_normalized[scale] = []
            scale_normalized[scale].append(r['normalized'])
        
        # Calculate variance for each scale
        variances = {}
        for scale, values in scale_normalized.items():
            if len(values) > 1:
                variances[scale] = np.var(values)
        
        # Test if variances are small
        avg_variance = np.mean(list(variances.values()))
        passes = avg_variance < 0.1
        
        print(f"Scales tested: {scales}")
        print(f"m-values tested: {m_values}")
        print(f"Average variance across m: {avg_variance:.6f}")
        print(f"Validation: {'PASSED' if passes else 'FAILED'}")
        
        return {
            'statement': 'Statement 7 (Unified Scaling Law)',
            'avg_variance': avg_variance,
            'passes': passes,
            'results': results
        }
    
    # ============================================================================
    # STATEMENT 8: Twin Prime Silver Ratio Aggregation
    # ============================================================================
    
    def get_twin_primes(self, primes, limit=10**5):
        """Generate twin prime pairs (p, p+2)"""
        twin_primes = []
        for i in range(len(primes) - 1):
            if primes[i+1] - primes[i] == 2:
                twin_primes.append((primes[i], primes[i+1]))
        return twin_primes
    
    def test_statement_8_twin_prime(self):
        """Test if twin prime gaps cluster at silver ratio"""
        print("\n" + "="*80)
        print("STATEMENT 8: Twin Prime Silver Ratio Aggregation")
        print("="*80)
        
        primes = self.generate_primes(10**6)
        twin_primes = self.get_twin_primes(primes)
        
        if len(twin_primes) < 2:
            return {
                'statement': 'Statement 8 (Twin Prime Silver Ratio Aggregation)',
                'error': 'Not enough twin primes found',
                'passes': False
            }
        
        # Calculate normalized twin prime gaps
        normalized_gaps = []
        for p, p2 in twin_primes:
            gap = p2 - p
            normalized_gap = gap / np.log(p)
            normalized_gaps.append(normalized_gap)
        
        # Calculate statistics
        avg_gap = np.mean(normalized_gaps)
        std_gap = np.std(normalized_gaps)
        median_gap = np.median(normalized_gaps)
        
        # Check if gaps cluster near silver ratio
        silver_ratio = self.silver_ratio
        diff_from_silver = abs(avg_gap - silver_ratio)
        
        # Test if average is within 50% of silver ratio
        passes = 0.5 < avg_gap / silver_ratio < 1.5
        
        print(f"Silver ratio: {silver_ratio:.6f}")
        print(f"Average normalized twin gap: {avg_gap:.6f}")
        print(f"Median normalized twin gap: {median_gap:.6f}")
        print(f"Std: {std_gap:.6f}")
        print(f"Difference from silver ratio: {diff_from_silver:.6f}")
        print(f"Number of twin primes: {len(twin_primes)}")
        print(f"Validation: {'PASSED' if passes else 'FAILED'}")
        
        return {
            'statement': 'Statement 8 (Twin Prime Silver Ratio Aggregation)',
            'silver_ratio': silver_ratio,
            'avg_gap': avg_gap,
            'median_gap': median_gap,
            'std_gap': std_gap,
            'diff_from_silver': diff_from_silver,
            'twin_count': len(twin_primes),
            'passes': passes
        }
    
    # ============================================================================
    # Main Validation
    # ============================================================================
    
    def run_all_validations(self):
        """Run all validation tests"""
        print("="*80)
        print("ILDA EMPIRICAL VALIDATION: STATEMENTS 2, 6, 7, 8")
        print("="*80)
        
        results = {
            'test_2': self.test_statement_2_scale_invariance(),
            'test_6': self.test_statement_6_k_tuple(),
            'test_7': self.test_statement_7_unified_scaling(),
            'test_8': self.test_statement_8_twin_prime()
        }
        
        # Summary
        passed = sum(1 for r in results.values() if r.get('passes', False))
        total = len(results)
        
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        print(f"Total tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success rate: {passed/total*100:.1f}%")
        
        return results

def convert_to_serializable(obj):
    """Convert numpy types to JSON serializable types"""
    if isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    else:
        return obj

if __name__ == "__main__":
    validator = StatementsValidator(max_prime=10**6)
    results = validator.run_all_validations()
    
    # Save results
    with open('statements_2_6_7_8_validation.json', 'w') as f:
        json.dump(convert_to_serializable(results), f, indent=2)
    
    print("\n✅ Validation complete. Results saved to statements_2_6_7_8_validation.json")

#!/usr/bin/env python3
"""
Prime Distribution Statement Validation
========================================
Empirical tests to validate or invalidate the 8 prime distribution statements.

This script implements high-priority tests that distinguish genuine patterns
from numerical coincidences using rigorous statistical methods.

Tests implemented:
- Test 3: Multiple Scale Factor Comparison (Statement 2 validation)
- Test 10: Mode Location Test (Statement 5 validation)
- Test 15: Random Shuffle Control (controls for all statements)
- Test 2: Scale-Dependence Check (Statement 1 validation)
- Test 6: PNT Correction Comparison (Statement 3 validation)
- Test 7: Oscillation Period Detection (Statement 4 validation)

Author: ILDA Autonomous System
Date: 2026-03-06
"""

import numpy as np
import scipy.stats as stats
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks
from scipy.optimize import minimize
from typing import Dict, List, Tuple
import json
import sys


class PrimeGenerator:
    """Generate primes up to a given limit using Sieve of Eratosthenes"""

    def __init__(self):
        self.primes_cache = {}

    def get_primes(self, limit: int) -> List[int]:
        """Generate primes up to limit"""
        if limit in self.primes_cache:
            return self.primes_cache[limit]

        sieve = np.ones(limit + 1, dtype=bool)
        sieve[0:2] = False
        for i in range(2, int(np.sqrt(limit)) + 1):
            if sieve[i]:
                sieve[i*i::i] = False

        primes = np.where(sieve)[0].tolist()
        self.primes_cache[limit] = primes
        return primes


class PrimeDistributionValidator:
    """
    Validate prime distribution statements using empirical tests
    """

    def __init__(self):
        self.prime_gen = PrimeGenerator()
        self.golden_ratio = (1 + np.sqrt(5)) / 2
        self.silver_ratio = 1 + np.sqrt(2)
        self.bronze_ratio = (3 + np.sqrt(13)) / 2

    def compute_normalized_gaps(self, primes: List[int]) -> np.ndarray:
        """Compute normalized gaps: δ_n = (p_{n+1} - p_n) / ln(p_n)"""
        gaps = []
        for i in range(len(primes) - 1):
            p_n = primes[i]
            p_n_plus_1 = primes[i + 1]
            delta = (p_n_plus_1 - p_n) / np.log(p_n)
            gaps.append(delta)
        return np.array(gaps)

    def normalized_prime_counting(self, x: float, primes: List[int]) -> float:
        """Compute Π(x) = π(x)·ln(x)/x"""
        pi_x = sum(1 for p in primes if p <= x)
        return pi_x * np.log(x) / x

    def ks_distance(self, data1: np.ndarray, data2: np.ndarray) -> float:
        """Compute Kolmogorov-Smirnov distance"""
        ks_stat, _ = stats.ks_2samp(data1, data2)
        return ks_stat

    def gue_distribution(self, s: np.ndarray) -> np.ndarray:
        """GUE spacing distribution: P(s) = (32/π²)s²exp(-4s²/π)"""
        return (32 / (np.pi**2)) * s**2 * np.exp(-4 * s**2 / np.pi)

    # ========================================================================
    # TEST 3: Multiple Scale Factor Comparison (Statement 2)
    # ========================================================================

    def test_multiple_scale_factors(self, max_prime: int = 10**6) -> Dict:
        """
        Test 3: Is scale invariance specific to σ₁ or general?

        Tests invariance at multiple scale factors to see if σ₁ is unique.
        """
        print("\n" + "="*80)
        print("TEST 3: Multiple Scale Factor Comparison")
        print("="*80)

        primes = self.prime_gen.get_primes(max_prime)

        scale_factors = [self.golden_ratio, 1.5, 2.0, 2.5, 3.0, 10.0]
        test_scales = [10**4, 10**5, 10**6]
        ks_distances = {}

        for sigma in scale_factors:
            ks_vals = []
            for x in test_scales:
                pi_x = self.normalized_prime_counting(x, primes)
                pi_sigma_x = self.normalized_prime_counting(sigma * x, primes)
                ks = self.ks_distance(np.array([pi_x]), np.array([pi_sigma_x]))
                ks_vals.append(ks)
            ks_distances[sigma] = {
                'mean': np.mean(ks_vals),
                'std': np.std(ks_vals),
                'values': ks_vals
            }

        # Analysis
        sigma_1_ks = ks_distances[self.golden_ratio]['mean']
        other_ks = [v['mean'] for k, v in ks_distances.items() if k != self.golden_ratio]
        min_other_ks = min(other_ks)

        result = {
            'test_name': 'Multiple Scale Factor Comparison',
            'statement': 'Statement 2 (Scale Invariance)',
            'ks_distances': ks_distances,
            'sigma_1_ks': sigma_1_ks,
            'min_other_ks': min_other_ks,
            'sigma_1_unique': sigma_1_ks < min_other_ks,
            'passes': sigma_1_ks < min_other_ks * 0.9  # 10% improvement threshold
        }

        print(f"\nKS Distances:")
        for sigma, data in ks_distances.items():
            print(f"  σ = {sigma:.3f}: {data['mean']:.6f} ± {data['std']:.6f}")

        print(f"\nValidation:")
        print(f"  σ₁ KS: {sigma_1_ks:.6f}")
        print(f"  Best other KS: {min_other_ks:.6f}")
        print(f"  σ₁ unique: {result['sigma_1_unique']}")
        print(f"  Test passes: {result['passes']}")

        return result

    # ========================================================================
    # TEST 10: Mode Location Test (Statement 5)
    # ========================================================================

    def test_mode_location(self, max_prime: int = 10**6) -> Dict:
        """
        Test 10: Where is the actual mode of gap distribution?

        Compares empirical mode to GUE theoretical mode and golden ratio.
        """
        print("\n" + "="*80)
        print("TEST 10: Mode Location Test")
        print("="*80)

        primes = self.prime_gen.get_primes(max_prime)
        gaps = self.compute_normalized_gaps(primes)

        # Estimate mode using kernel density estimation
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(gaps)
        xs = np.linspace(0, 5, 1000)
        densities = kde(xs)
        empirical_mode = xs[np.argmax(densities)]

        # GUE theoretical mode
        gue_mode = np.sqrt(np.pi) / 2  # ≈ 0.886

        result = {
            'test_name': 'Mode Location Test',
            'statement': 'Statement 5 (GUE Constraint)',
            'empirical_mode': empirical_mode,
            'gue_mode': gue_mode,
            'golden_ratio': self.golden_ratio,
            'dist_to_gue': abs(empirical_mode - gue_mode),
            'dist_to_golden': abs(empirical_mode - self.golden_ratio),
            'closer_to_gue': abs(empirical_mode - gue_mode) < abs(empirical_mode - self.golden_ratio),
            'passes': abs(empirical_mode - gue_mode) < abs(empirical_mode - self.golden_ratio)
        }

        print(f"\nMode Analysis:")
        print(f"  Empirical mode: {empirical_mode:.6f}")
        print(f"  GUE mode: {gue_mode:.6f}")
        print(f"  Golden ratio: {self.golden_ratio:.6f}")
        print(f"  Distance to GUE: {result['dist_to_gue']:.6f}")
        print(f"  Distance to golden: {result['dist_to_golden']:.6f}")
        print(f"  Closer to GUE: {result['closer_to_gue']}")
        print(f"  Test passes: {result['passes']}")

        return result

    # ========================================================================
    # TEST 15: Random Shuffle Control
    # ========================================================================

    def test_random_control(self, max_prime: int = 10**6) -> Dict:
        """
        Test 15: Are patterns specific to actual primes?

        Compares actual prime gaps to gaps from random numbers with same density.
        """
        print("\n" + "="*80)
        print("TEST 15: Random Shuffle Control")
        print("="*80)

        primes = self.prime_gen.get_primes(max_prime)
        actual_gaps = self.compute_normalized_gaps(primes)

        # Generate random "primes" with same density
        np.random.seed(42)
        random_numbers = sorted(np.random.uniform(2, max_prime, len(primes)))
        random_gaps = self.compute_normalized_gaps(random_numbers)

        # Compute basin probabilities at golden ratio
        basin_width = 0.5
        actual_in_basin = sum(abs(g - self.golden_ratio) < basin_width for g in actual_gaps)
        random_in_basin = sum(abs(g - self.golden_ratio) < basin_width for g in random_gaps)

        actual_prob = actual_in_basin / len(actual_gaps)
        random_prob = random_in_basin / len(random_gaps)

        # Statistical test
        n_actual = len(actual_gaps)
        n_random = len(random_gaps)
        p1 = actual_prob
        p2 = random_prob

        # Two-proportion z-test
        pooled_p = (actual_in_basin + random_in_basin) / (n_actual + n_random)
        se = np.sqrt(pooled_p * (1 - pooled_p) * (1/n_actual + 1/n_random))
        z_score = (p1 - p2) / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

        result = {
            'test_name': 'Random Shuffle Control',
            'statement': 'All statements (Control)',
            'actual_basin_prob': actual_prob,
            'random_basin_prob': random_prob,
            'actual_in_basin': actual_in_basin,
            'random_in_basin': random_in_basin,
            'total_gaps': n_actual,
            'z_score': z_score,
            'p_value': p_value,
            'significant': p_value < 0.01,
            'passes': p_value < 0.01
        }

        print(f"\nBasin Probability (Golden Ratio ± 0.5):")
        print(f"  Actual primes: {actual_prob:.4f} ({actual_in_basin}/{n_actual})")
        print(f"  Random numbers: {random_prob:.4f} ({random_in_basin}/{n_random})")
        print(f"\nStatistical Test:")
        print(f"  Z-score: {z_score:.4f}")
        print(f"  P-value: {p_value:.6f}")
        print(f"  Significant: {result['significant']}")
        print(f"  Test passes: {result['passes']}")

        return result

    # ========================================================================
    # TEST 2: Scale-Dependence Check (Statement 1)
    # ========================================================================

    def test_scale_dependence(self, max_prime: int = 10**7) -> Dict:
        """
        Test 2: Does the golden ratio basin pattern persist with scale?

        Tests if basin probability stabilizes or approaches random expectation.
        """
        print("\n" + "="*80)
        print("TEST 2: Scale-Dependence Check")
        print("="*80)

        scales = [10**5, 10**6, 10**7]
        basin_probs = []
        basin_width = 0.5

        for scale in scales:
            primes = self.prime_gen.get_primes(scale)
            gaps = self.compute_normalized_gaps(primes)
            prob = sum(abs(g - self.golden_ratio) < basin_width for g in gaps) / len(gaps)
            basin_probs.append(prob)
            print(f"  Scale {scale:.0e}: {prob:.4f}")

        # Check trend
        if len(basin_probs) >= 2:
            trend = basin_probs[-1] - basin_probs[0]
        else:
            trend = 0

        result = {
            'test_name': 'Scale-Dependence Check',
            'statement': 'Statement 1 (Prime Gap Aggregation)',
            'scales': scales,
            'basin_probabilities': basin_probs,
            'trend': trend,
            'final_prob': basin_probs[-1],
            'random_expectation': 0.5,  # Assuming uniform in [0, 5]
            'above_random': basin_probs[-1] > 0.5,
            'passes': basin_probs[-1] > 0.5 and trend >= 0
        }

        print(f"\nValidation:")
        print(f"  Trend: {trend:.4f}")
        print(f"  Final probability: {basin_probs[-1]:.4f}")
        print(f"  Above random (0.5): {result['above_random']}")
        print(f"  Test passes: {result['passes']}")

        return result

    # ========================================================================
    # TEST 6: PNT Correction Comparison (Statement 3)
    # ========================================================================

    def test_pnt_correction_comparison(self, max_prime: int = 10**6) -> Dict:
        """
        Test 6: Compare fixed-point PNT with other corrections.

        Tests if 1/σ₁ correction outperforms classical PNT.
        """
        print("\n" + "="*80)
        print("TEST 6: PNT Correction Comparison")
        print("="*80)

        primes = self.prime_gen.get_primes(max_prime)

        # Define correction functions
        def pnt_classical(x):
            return x / np.log(x)

        def pnt_fixed_point(x):
            return x / (np.log(x) - 1 / self.golden_ratio)

        def pnt_li(x):
            # Logarithmic integral approximation
            return x / (np.log(x) * (1 - 1/np.log(x) + 2/np.log(x)**2))

        corrections = [
            ("classical", pnt_classical),
            ("fixed_point", pnt_fixed_point),
            ("li", pnt_li)
        ]

        test_scales = [10**5, 10**6]
        errors = {name: [] for name, _ in corrections}

        for scale in test_scales:
            pi_actual = sum(1 for p in primes if p <= scale)
            for name, func in corrections:
                pi_approx = func(scale)
                error = abs(pi_actual - pi_approx)
                errors[name].append(error)

        # Calculate improvement factors
        avg_errors = {name: np.mean(errs) for name, errs in errors.items()}
        improvement = avg_errors['classical'] / avg_errors['fixed_point']
        li_improvement = avg_errors['classical'] / avg_errors['li']

        result = {
            'test_name': 'PNT Correction Comparison',
            'statement': 'Statement 3 (Fixed-Point PNT)',
            'errors': errors,
            'avg_errors': avg_errors,
            'improvement_factor': improvement,
            'li_improvement': li_improvement,
            'improves_over_classical': improvement > 1.0,
            'passes': improvement > 2.0  # Should be > 2x improvement
        }

        print(f"\nAverage Errors:")
        for name, err in avg_errors.items():
            print(f"  {name}: {err:.2f}")

        print(f"\nImprovement Factors:")
        print(f"  Fixed-point vs classical: {improvement:.2f}×")
        print(f"  Li vs classical: {li_improvement:.2f}×")
        print(f"  Test passes: {result['passes']}")

        return result

    # ========================================================================
    # TEST 7: Oscillation Period Detection (Statement 4)
    # ========================================================================

    def test_oscillation_period(self, max_prime: int = 10**6) -> Dict:
        """
        Test 7: Can we detect period T = ln(σ₁) in oscillations?

        Uses FFT to detect periodic structure in prime counting oscillations.
        """
        print("\n" + "="*80)
        print("TEST 7: Oscillation Period Detection")
        print("="*80)

        primes = self.prime_gen.get_primes(max_prime)

        # Compute oscillations: Δψ(x) = π(x) - x/ln(x)
        x_values = np.linspace(10**4, 10**6, 1000)
        oscillations = []
        for x in x_values:
            pi_actual = sum(1 for p in primes if p <= x)
            pi_classical = x / np.log(x)
            oscillations.append(pi_actual - pi_classical)

        oscillations = np.array(oscillations)

        # Compute power spectrum using FFT
        fft_result = fft(oscillations)
        power_spectrum = np.abs(fft_result)**2
        frequencies = fftfreq(len(x_values))

        # Find dominant frequencies (positive frequencies only)
        positive_freqs = frequencies[:len(frequencies)//2]
        positive_power = power_spectrum[:len(power_spectrum)//2]

        # Find peaks
        peaks, _ = find_peaks(positive_power, height=np.max(positive_power) * 0.1)

        if len(peaks) > 0:
            dominant_freq = positive_freqs[peaks[np.argmax(positive_power[peaks])]]
            period = 1 / abs(dominant_freq) if dominant_freq != 0 else np.inf
        else:
            dominant_freq = 0
            period = np.inf

        # Expected period from theory
        expected_period = np.log(self.golden_ratio)
        expected_freq = 1 / expected_period

        result = {
            'test_name': 'Oscillation Period Detection',
            'statement': 'Statement 4 (Complex Dimensions)',
            'dominant_frequency': float(abs(dominant_freq)),
            'dominant_period': float(period),
            'expected_frequency': expected_freq,
            'expected_period': expected_period,
            'freq_match': abs(abs(dominant_freq) - expected_freq) < 0.1,
            'passes': abs(abs(dominant_freq) - expected_freq) < 0.1
        }

        print(f"\nFrequency Analysis:")
        print(f"  Dominant frequency: {abs(dominant_freq):.6f}")
        print(f"  Expected frequency: {expected_freq:.6f}")
        print(f"  Measured period: {period:.6f}")
        print(f"  Expected period: {expected_period:.6f}")
        print(f"  Frequency matches: {result['freq_match']}")
        print(f"  Test passes: {result['passes']}")

        return result

    # ========================================================================
    # Main Validation
    # ========================================================================

    def run_all_tests(self, max_prime: int = 10**6) -> Dict:
        """Run all validation tests"""
        print("\n" + "="*80)
        print("PRIME DISTRIBUTION STATEMENT VALIDATION")
        print("="*80)
        print(f"Max prime: {max_prime:.0e}")
        print(f"Golden ratio: {self.golden_ratio:.6f}")
        print(f"Silver ratio: {self.silver_ratio:.6f}")
        print(f"Bronze ratio: {self.bronze_ratio:.6f}")

        results = {}

        # Run tests
        results['test_3'] = self.test_multiple_scale_factors(max_prime)
        results['test_10'] = self.test_mode_location(max_prime)
        results['test_15'] = self.test_random_control(max_prime)
        results['test_2'] = self.test_scale_dependence(max_prime)
        results['test_6'] = self.test_pnt_correction_comparison(max_prime)
        results['test_7'] = self.test_oscillation_period(max_prime)

        # Summary
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)

        passed = sum(1 for r in results.values() if r['passes'])
        total = len(results)

        for test_name, result in results.items():
            status = "✓ PASS" if result['passes'] else "✗ FAIL"
            print(f"{result['test_name']}: {status}")
            print(f"  → {result['statement']}")

        print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

        return results


def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(description='Validate prime distribution statements')
    parser.add_argument('--max-prime', type=int, default=10**6,
                       help='Maximum prime to generate (default: 10^6)')
    parser.add_argument('--output', type=str, default=None,
                       help='Output JSON file (default: stdout)')

    args = parser.parse_args()

    validator = PrimeDistributionValidator()
    results = validator.run_all_tests(args.max_prime)

    # Convert results to JSON-serializable format
    def convert_to_serializable(obj):
        if isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(item) for item in obj]
        elif isinstance(obj, bool):
            return bool(obj)
        return obj

    # Output results
    output_data = {
        'max_prime': args.max_prime,
        'golden_ratio': float(validator.golden_ratio),
        'silver_ratio': float(validator.silver_ratio),
        'bronze_ratio': float(validator.bronze_ratio),
        'results': convert_to_serializable(results),
        'summary': {
            'total_tests': len(results),
            'passed': sum(1 for r in results.values() if r['passes']),
            'failed': sum(1 for r in results.values() if not r['passes'])
        }
    }

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\nResults saved to {args.output}")
    else:
        print("\n" + "="*80)
        print("RESULTS (JSON)")
        print("="*80)
        print(json.dumps(output_data, indent=2))


if __name__ == "__main__":
    main()

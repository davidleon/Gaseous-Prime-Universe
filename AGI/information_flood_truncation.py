"""
Information Flood-Aware Truncation Strategy

Core Insight: "Evenly distributed bit streams is good, but if the baby has prior 
knowledge of incoming information, it would be better to be evenly spaced by the 
information floods in."

This means:
1. Information comes in "floods" (bursts of high-density information)
2. Baby should adapt truncation spacing to match these floods
3. Prior knowledge of information density → adaptive spacing
4. This is more efficient than uniform spacing when we know where info floods occur
"""

import numpy as np
from typing import List, Tuple
import re


class InformationFloodAnalyzer:
    """
    Analyze information floods in proofs
    
    Information floods are regions with high information density:
    - New definitions (theorem, lemma, definition)
    - Complex expressions (nested calc, induction)
    - Quantifiers (∀, ∃)
    - Abstractions (fun, λ, →)
    """
    
    def detect_information_density(self, tokens: List[str]) -> List[float]:
        """
        Detect information density at each position
        
        Returns: density array where density[i] = information at token i
        
        Information signals:
        - New definitions (theorem, lemma, definition)
        - Complex expressions (nested calc, induction)
        - Quantifiers (∀, ∃)
        - Abstractions (fun, λ, →)
        """
        n = len(tokens)
        density = np.zeros(n)
        
        # High-information keywords
        high_info_keywords = {
            'theorem', 'lemma', 'corollary', 'proposition', 'definition',
            'induction', 'recursion', 'cases', 'calc', 'simp', 'rw',
            '∀', '∃', '→', '↔', '∧', '∨', '¬', '≠', '≤', '≥',
            'fun', 'λ', '∞', '∑', '∏', '∂', '∇', '∫',
            '⟹', '⇒', '⇐', '⇔', '≡', '≈', '~'
        }
        
        # Mathematical operators
        math_operators = {'+', '-', '*', '/', '^', '=', ':=', '<-', '→'}
        
        # Structural markers
        structure_markers = {'with', 'by', 'if', 'then', 'else', 'have', 'show'}
        
        nesting_depth = 0
        for i, token in enumerate(tokens):
            token_lower = token.lower()
            
            # Track nesting
            if token in ['(', '[', '{']:
                nesting_depth += 1
                density[i] += 0.5  # Nesting increase adds info
            elif token in [')', ']', '}']:
                nesting_depth = max(0, nesting_depth - 1)
                density[i] += 0.5  # Unnesting adds info
            
            # High-information keywords
            if token in high_info_keywords:
                density[i] += 1.0
            
            # Mathematical operators
            if token in math_operators:
                density[i] += 0.3
            
            # Structural markers
            if token_lower in structure_markers:
                density[i] += 0.4
            
            # Numbers (indices, bounds)
            if token.isdigit():
                density[i] += 0.2
            
            # Add base density (every token has some information)
            density[i] += 0.3
        
        # Smooth density to detect floods (Gaussian smoothing)
        window_size = max(3, min(7, n // 10))
        if window_size > 1:
            smoothed_density = np.convolve(density, np.ones(window_size)/window_size, mode='same')
            density = smoothed_density
        
        return density
    
    def detect_information_floods(self, density: List[float], threshold: float = 0.5) -> List[Tuple[int, int]]:
        """
        Detect information floods
        
        Returns: list of (start, end) indices for each flood
        
        An information flood is a region where density exceeds threshold
        """
        n = len(density)
        floods = []
        in_flood = False
        flood_start = 0
        
        for i, d in enumerate(density):
            if d > threshold and not in_flood:
                # Start of new flood
                in_flood = True
                flood_start = i
            elif d <= threshold and in_flood:
                # End of flood
                in_flood = False
                floods.append((flood_start, i - 1))
        
        # Handle flood at end
        if in_flood:
            floods.append((flood_start, n - 1))
        
        return floods
    
    def calculate_flood_importance(self, density: List[float], flood: Tuple[int, int]) -> float:
        """
        Calculate importance of an information flood
        
        Higher importance = more information in this flood
        """
        start, end = flood
        flood_density = density[start:end+1]
        
        # Handle empty flood
        if len(flood_density) == 0:
            return 0.0
        
        # Total information in flood
        total_info = sum(flood_density)
        
        # Peak density
        peak_info = max(flood_density)
        
        # Flood size (weighted)
        size = (end - start + 1) / len(density)
        
        # Importance = total information * peak * size
        importance = total_info * peak_info * (1 + size)
        
        return importance
    
    def adaptive_truncation_points(self, proof_text: str, num_points: int = None) -> List[int]:
        """
        Generate adaptive truncation points based on information floods
        
        Key idea: Space points evenly by information floods, not by tokens
        
        Algorithm:
        1. Detect information density across proof
        2. Identify information floods
        3. Calculate flood importance
        4. Place points at:
           - Before each major flood (anticipate incoming info)
           - Within large floods (capture internal structure)
           - After floods (consolidate learning)
        
        This is optimal when baby has prior knowledge of information distribution
        """
        tokens = proof_text.split()
        n = len(tokens)
        
        if n <= 2:
            return [1]
        
        # Detect information density
        density = self.detect_information_density(tokens)
        
        # Detect information floods
        floods = self.detect_information_floods(density)
        
        # Calculate optimal number of points
        if num_points is None:
            num_points = int(np.log2(n))  # Default: log2(n) points
        
        # Ensure num_points is at least 2 and at most n-1
        num_points = max(2, min(num_points, n - 1))
        
        if not floods:
            # No floods detected, use uniform spacing
            return [1 + i * (n - 1) // (num_points - 1) for i in range(num_points)]
        
        # Calculate flood importance
        flood_importances = [
            (flood, self.calculate_flood_importance(density, flood))
            for flood in floods
        ]
        
        # Sort by importance
        flood_importances.sort(key=lambda x: x[1], reverse=True)
        
        # Allocate points to floods based on importance
        total_importance = sum(imp for _, imp in flood_importances)
        
        points = set()
        
        # Add points: before, during, after important floods
        for flood, importance in flood_importances:
            start, end = flood
            
            # Number of points for this flood
            flood_points = max(1, int(num_points * importance / total_importance))
            
            # Point before flood (anticipate)
            if start > 0:
                points.add(start - 1)
            
            # Points during flood (capture structure)
            for i in range(flood_points - 1):
                pos = start + i * (end - start) // max(1, flood_points - 1)
                points.add(pos)
            
            # Point after flood (consolidate)
            if end < n - 1:
                points.add(end + 1)
        
        # Ensure we have enough points
        while len(points) < num_points:
            # Add uniformly distributed points
            i = len(points)
            pos = 1 + i * (n - 1) // (num_points - 1)
            points.add(pos)
        
        # Remove points outside valid range
        points = [p for p in points if 1 <= p <= n - 1]
        
        # Sort and limit to num_points
        points = sorted(points)[:num_points]
        
        return points
    
    def explain_adaptive_spacing(self, proof_text: str) -> dict:
        """
        Explain why adaptive spacing chooses specific points
        
        Returns: explanation with flood analysis and point placement rationale
        """
        tokens = proof_text.split()
        n = len(tokens)
        
        # Analyze information floods
        density = self.detect_information_density(tokens)
        floods = self.detect_information_floods(density)
        
        # Generate adaptive points
        adaptive_points = self.adaptive_truncation_points(proof_text)
        
        # Compare with uniform points
        uniform_points = [1 + i * (n - 1) // max(1, len(adaptive_points) - 1) 
                         for i in range(len(adaptive_points))]
        
        # Explain differences
        explanation = {
            "proof_length": n,
            "information_density": density,
            "floods": [],
            "adaptive_points": adaptive_points,
            "uniform_points": uniform_points,
            "differences": [],
            "rationale": []
        }
        
        # Explain floods
        for i, (start, end) in enumerate(floods):
            flood_tokens = tokens[start:end+1]
            flood_importance = self.calculate_flood_importance(density, (start, end))
            peak_density = max(density[start:end+1]) if end - start + 1 > 0 else 0.0
            
            explanation["floods"].append({
                "index": i + 1,
                "position": f"[{start}, {end}]",
                "tokens": ' '.join(flood_tokens[:10]) + ('...' if len(flood_tokens) > 10 else ''),
                "importance": flood_importance,
                "peak_density": peak_density
            })
        
        # Explain point placement differences
        for point in adaptive_points:
            if point not in uniform_points:
                # Find which flood this point relates to
                related_flood = None
                for i, (start, end) in enumerate(floods):
                    if start - 1 <= point <= end + 1:
                        related_flood = i + 1
                        break
                
                explanation["differences"].append({
                    "point": point,
                    "type": "adaptive",
                    "related_flood": related_flood,
                    "reason": f"Placed {'before' if point < start else 'during' if point <= end else 'after'} flood {related_flood}"
                })
        
        # Explain uniform points that are not in adaptive
        for point in uniform_points:
            if point not in adaptive_points:
                explanation["differences"].append({
                    "point": point,
                    "type": "uniform",
                    "reason": "Removed (low information density)"
                })
        
        # Overall rationale
        explanation["rationale"] = [
            "Adaptive spacing aligns with information floods",
            "Points placed before floods anticipate incoming information",
            "Points within floods capture internal structure",
            "Points after floods consolidate learning",
            f"Detected {len(floods)} information floods in proof",
            f"Adaptive points: {len(adaptive_points)} vs Uniform points: {len(uniform_points)}"
        ]
        
        return explanation


def compare_strategies(proof_text: str):
    """
    Compare uniform vs adaptive truncation strategies
    """
    analyzer = InformationFloodAnalyzer()
    
    # Analyze information floods
    tokens = proof_text.split()
    n = len(tokens)
    
    density = analyzer.detect_information_density(tokens)
    floods = analyzer.detect_information_floods(density)
    
    # Generate strategies
    adaptive_points = analyzer.adaptive_truncation_points(proof_text)
    uniform_points = [1 + i * (n - 1) // max(1, len(adaptive_points) - 1) 
                     for i in range(len(adaptive_points))]
    
    # Get explanation
    explanation = analyzer.explain_adaptive_spacing(proof_text)
    
    return {
        "proof_length": n,
        "floods_detected": len(floods),
        "adaptive_points": adaptive_points,
        "uniform_points": uniform_points,
        "explanation": explanation
    }


# Demonstration
if __name__ == "__main__":
    # Test proofs with different information flood patterns
    simple_proof = "theorem simple : 1 = 1 := by rfl"
    
    medium_proof = """
    theorem add_comm (a b : Nat) : a + b = b + a := by
      induction b with
      | zero => simp
      | succ n ih => rw [Nat.add_succ, Nat.succ_add]
    """
    
    complex_proof = """
    theorem sum_nat (n : Nat) : ∑ i in Finset.range (n + 1), i = n * (n + 1) / 2 := by
      induction n with
      | zero => simp [Finset.range_succ, Finset.sum_singleton]
      | succ n ih =>
        calc ∑ i in Finset.range (n.succ + 1), i
           = ∑ i in Finset.range (n + 1) ∪ {n.succ}, i := by rw [Finset.range_succ]
        _ = (∑ i in Finset.range (n + 1), i) + (n.succ : ℤ) := by rw [Finset.sum_union]
        _ = (n * (n + 1) / 2) + (n.succ : ℤ) := by rw [ih]
        _ = ((n + 1) * (n.succ + 1)) / 2 := by ring
    """
    
    proofs = [
        ("Simple Proof", simple_proof),
        ("Medium Proof", medium_proof),
        ("Complex Proof", complex_proof)
    ]
    
    print("="*80)
    print("INFORMATION FLOOD-AWARE TRUNCATION")
    print("="*80)
    print()
    print("Core Insight: Space points evenly by information floods, not tokens")
    print("When baby has prior knowledge, adapt spacing to match information density")
    print()
    
    for name, proof in proofs:
        print(f"\n{name}:")
        result = compare_strategies(proof)
        
        print(f"  Length: {result['proof_length']} tokens")
        print(f"  Floods detected: {result['floods_detected']}")
        
        print(f"\n  Adaptive points: {result['adaptive_points']}")
        print(f"  Uniform points: {result['uniform_points']}")
        
        if result['explanation']['differences']:
            print(f"\n  Differences:")
            for diff in result['explanation']['differences'][:5]:
                print(f"    - Point {diff['point']} ({diff['type']}): {diff['reason']}")
        
        print(f"\n  Rationale:")
        for reason in result['explanation']['rationale'][:3]:
            print(f"    - {reason}")
    
    print()
    print("="*80)
    print("KEY INSIGHT")
    print("="*80)
    print()
    print("Uniform spacing is optimal WITHOUT prior knowledge")
    print("Adaptive spacing is optimal WITH prior knowledge of information floods")
    print()
    print("Baby's intuition:")
    print("  'I know where the information floods are coming!'")
    print("  'Let me space my learning points to match those floods!'")
    print()
    print("This creates a more efficient learning rhythm:")
    print("  - Anticipate: Place point BEFORE flood (prepare)")
    print("  - Capture: Place points WITHIN flood (learn)")
    print("  - Consolidate: Place point AFTER flood (integrate)")

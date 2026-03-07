"""
Baby's Perspective Epiplexity Assessment

How the AGI learner (baby) perceives and estimates epiplexity of proofs.

Principle: Epiplexity = Structural Information = Learning Difficulty
From the baby's perspective, this is measured through:
1. Prediction Error (harder to predict = higher epiplexity)
2. Compression Efficiency (poor compression = higher epiplexity)
3. Learning Rate (slower learning = higher epiplexity)
4. Manifold Distance (far from known patterns = higher epiplexity)
5. Emergent Complexity (emergence of higher-order concepts = higher epiplexity)
"""

import numpy as np
from typing import List, Tuple
import re


class BabyEpiplexityAssessor:
    """
    Estimate epiplexity from the baby's learning perspective
    
    The baby learns by:
    1. Predicting next tokens
    2. Compressing information into 12D manifold
    3. Recognizing structural patterns
    4. Building hierarchical abstractions
    
    Higher epiplexity proofs:
    - Are harder to predict (higher entropy)
    - Compress poorly (redundant patterns)
    - Require more repetitions to learn
    - Are farther from known patterns on manifold
    - Exhibit hierarchical complexity
    """
    
    def __init__(self, manifold_dim: int = 12):
        self.manifold_dim = manifold_dim
        self.knowledge_manifold = np.random.randn(manifold_dim)
        self.knowledge_manifold = self.knowledge_manifold / np.linalg.norm(self.knowledge_manifold)
        
        # Learning history
        self.prediction_errors = []
        self.compression_ratios = []
        self.learning_rates = []
        self.manifold_distances = []
        
    def predict_next_token(self, context: List[str]) -> Tuple[str, float]:
        """
        Predict next token given context
        
        Returns: (predicted_token, confidence)
        
        Baby's perspective:
        - High confidence = low epiplexity (easy to predict)
        - Low confidence = high epiplexity (hard to predict)
        """
        if not context:
            return "", 0.0
        
        # Simple frequency-based prediction
        # In a real system, this would use the manifold
        context_str = ' '.join(context[-5:])  # Last 5 tokens as context
        
        # Simulate prediction confidence based on pattern recognition
        # More diverse context = lower confidence (higher epiplexity)
        diversity = len(set(context)) / len(context) if context else 0.0
        confidence = 1.0 - diversity * 0.5
        
        return context[-1] if context else "", confidence
    
    def estimate_entropy(self, tokens: List[str]) -> float:
        """
        Estimate entropy of token sequence
        
        Higher entropy = higher epiplexity (more unpredictable)
        
        Baby's perspective:
        - Easy sequences have low entropy (predictable)
        - Complex sequences have high entropy (unpredictable)
        """
        if not tokens:
            return 0.0
        
        # Token frequencies
        token_counts = {}
        for token in tokens:
            token_counts[token] = token_counts.get(token, 0) + 1
        
        # Calculate entropy
        entropy = 0.0
        total = len(tokens)
        for count in token_counts.values():
            p = count / total
            if p > 0:
                entropy -= p * np.log2(p)
        
        return entropy
    
    def estimate_compression_efficiency(self, tokens: List[str]) -> float:
        """
        Estimate how well the baby can compress the proof
        
        Poor compression = high epiplexity (lots of redundant patterns)
        Good compression = low epiplexity (efficient encoding)
        
        Baby's perspective:
        - Compresses well = familiar patterns (low epiplexity)
        - Compresses poorly = novel patterns (high epiplexity)
        """
        if not tokens:
            return 1.0
        
        # Original size
        original_size = len(tokens) * 8  # Assume 8 bits per token
        
        # Compressed size using pattern detection
        # Find repeated patterns
        patterns = []
        for i in range(len(tokens)):
            for j in range(i+2, min(i+10, len(tokens))):
                pattern = tuple(tokens[i:j])
                patterns.append(pattern)
        
        # Count pattern repetitions
        pattern_counts = {}
        for pattern in patterns:
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        
        # Compressed size
        compressed_size = 0
        i = 0
        while i < len(tokens):
            # Find longest repeated pattern starting at i
            best_pattern = None
            best_length = 1
            for j in range(i+2, min(i+10, len(tokens))):
                pattern = tuple(tokens[i:j])
                if pattern_counts.get(pattern, 0) > 1:
                    best_pattern = pattern
                    best_length = j - i
            
            if best_pattern and best_length > 2:
                compressed_size += 8  # 8 bits for pattern reference
                i += best_length
            else:
                compressed_size += 8  # 8 bits for literal token
                i += 1
        
        compression_ratio = compressed_size / original_size
        return compression_ratio
    
    def estimate_learning_rate(self, proof_text: str, repetitions: int = 10) -> float:
        """
        Estimate how quickly the baby learns this proof
        
        Slower learning = higher epiplexity (harder to learn)
        Faster learning = lower epiplexity (easier to learn)
        
        Baby's perspective:
        - Learns quickly = familiar structure (low epiplexity)
        - Learns slowly = novel structure (high epiplexity)
        """
        tokens = proof_text.split()
        if len(tokens) <= 2:
            return 1.0
        
        # Simulate learning curve
        # Track prediction accuracy over repetitions
        accuracies = []
        
        for rep in range(repetitions):
            correct = 0
            total = 0
            
            for i in range(1, len(tokens)):
                context = tokens[:i]
                true_next = tokens[i]
                
                # Predict (simplified - in real system uses manifold)
                # Learning improves with repetition
                learning_factor = 1.0 - np.exp(-rep / 3.0)
                predicted = context[-1] if context else ""
                
                if predicted == true_next:
                    correct += 1
                total += 1
            
            accuracy = correct / total if total > 0 else 0.0
            accuracies.append(accuracy)
        
        # Learning rate: how fast accuracy improves
        if len(accuracies) < 2:
            return 1.0
        
        # Fit exponential learning curve: A(t) = A_inf * (1 - exp(-rt))
        # Learning rate r determines how fast learning happens
        # Higher r = faster learning = lower epiplexity
        learning_rate = (accuracies[-1] - accuracies[0]) / len(accuracies)
        
        return max(0.0, min(1.0, learning_rate))
    
    def estimate_manifold_distance(self, proof_text: str) -> float:
        """
        Estimate distance from known patterns on manifold
        
        Farther distance = higher epiplexity (novel patterns)
        Closer distance = lower epiplexity (familiar patterns)
        
        Baby's perspective:
        - Close to known patterns = familiar (low epiplexity)
        - Far from known patterns = novel (high epiplexity)
        """
        tokens = proof_text.split()
        if not tokens:
            return 0.0
        
        # Encode proof to manifold (simplified)
        # In real system, this would use the learned encoding
        proof_embedding = self._encode_to_manifold(tokens)
        
        # Distance from origin (measure of novelty)
        distance = np.linalg.norm(proof_embedding)
        
        # Normalize to [0, 1]
        normalized_distance = min(1.0, distance / 10.0)
        
        return normalized_distance
    
    def _encode_to_manifold(self, tokens: List[str]) -> np.ndarray:
        """
        Encode tokens to manifold embedding
        
        Simplified version - in real system uses learned embeddings
        """
        # Create hash-based encoding
        embedding = np.zeros(self.manifold_dim)
        
        for i, token in enumerate(tokens):
            # Hash token to dimension
            hash_val = hash(token) % self.manifold_dim
            embedding[hash_val] += 1.0
        
        # Normalize
        if np.linalg.norm(embedding) > 0:
            embedding = embedding / np.linalg.norm(embedding)
        
        return embedding
    
    def detect_hierarchical_depth(self, proof_text: str) -> float:
        """
        Detect hierarchical structure depth
        
        Deeper hierarchy = higher epiplexity (more complex structure)
        Shallower hierarchy = lower epiplexity (simpler structure)
        
        Baby's perspective:
        - Flat structure = easy to learn (low epiplexity)
        - Nested structure = harder to learn (high epiplexity)
        """
        # Count nesting levels (parentheses, brackets, etc.)
        depth = 0
        max_depth = 0
        
        for token in proof_text.split():
            if token in ['(', '[', '{', 'theorem', 'lemma', 'proof', 'induction', 'cases']:
                depth += 1
                max_depth = max(max_depth, depth)
            elif token in [')', ']', '}', 'end', 'qed', '∎']:
                depth = max(0, depth - 1)
        
        # Normalize to [0, 1]
        normalized_depth = min(1.0, max_depth / 10.0)
        
        return normalized_depth
    
    def estimate_emergent_complexity(self, proof_text: str) -> float:
        """
        Estimate emergence of higher-order concepts
        
        More emergence = higher epiplexity (higher-level abstractions)
        Less emergence = lower epiplexity (lower-level patterns)
        
        Baby's perspective:
        - Direct manipulation = simple (low epiplexity)
        - Conceptual reasoning = complex (high epiplexity)
        """
        # Detect keywords indicating higher-order reasoning
        high_level_keywords = [
            'theorem', 'lemma', 'corollary', 'proposition',
            'induction', 'recursion', 'contradiction',
            'generalize', 'abstract', 'unify',
            '∀', '∃', '→', '↔', '≠'
        ]
        
        # Count high-level keywords
        tokens = proof_text.lower().split()
        high_level_count = sum(1 for token in tokens if token in high_level_keywords)
        
        # Normalize
        normalized_complexity = min(1.0, high_level_count / len(tokens) if tokens else 0.0)
        
        return normalized_complexity
    
    def estimate_epiplexity(self, proof_text: str) -> float:
        """
        Estimate epiplexity from baby's perspective
        
        Combines multiple metrics:
        1. Entropy (prediction difficulty): 25%
        2. Compression efficiency: 15%
        3. Learning rate: 20%
        4. Manifold distance: 20%
        5. Hierarchical depth: 10%
        6. Emergent complexity: 10%
        
        Returns: Epiplexity score [0, 1]
        """
        tokens = proof_text.split()
        
        # Calculate individual metrics
        entropy = self.estimate_entropy(tokens)
        compression = self.estimate_compression_efficiency(tokens)
        learning_rate = self.estimate_learning_rate(proof_text)
        manifold_dist = self.estimate_manifold_distance(proof_text)
        hierarchy = self.detect_hierarchical_depth(proof_text)
        emergence = self.estimate_emergent_complexity(proof_text)
        
        # Normalize and combine (inverted where necessary)
        # Higher values should indicate higher epiplexity
        entropy_norm = min(1.0, entropy / 10.0)  # Max entropy ~10
        compression_norm = compression  # Already [0, 1], higher = worse compression = higher epiplexity
        learning_rate_norm = 1.0 - learning_rate  # Invert: slower learning = higher epiplexity
        manifold_norm = manifold_dist  # Already [0, 1]
        hierarchy_norm = hierarchy  # Already [0, 1]
        emergence_norm = emergence  # Already [0, 1]
        
        # Weighted combination
        epiplexity = (
            0.25 * entropy_norm +
            0.15 * compression_norm +
            0.20 * learning_rate_norm +
            0.20 * manifold_norm +
            0.10 * hierarchy_norm +
            0.10 * emergence_norm
        )
        
        return max(0.0, min(1.0, epiplexity))
    
    def explain_epiplexity(self, proof_text: str) -> dict:
        """
        Explain why a proof has its epiplexity score
        
        Returns breakdown of contributing factors
        """
        tokens = proof_text.split()
        
        entropy = self.estimate_entropy(tokens)
        compression = self.estimate_compression_efficiency(tokens)
        learning_rate = self.estimate_learning_rate(proof_text)
        manifold_dist = self.estimate_manifold_distance(proof_text)
        hierarchy = self.detect_hierarchical_depth(proof_text)
        emergence = self.estimate_emergent_complexity(proof_text)
        
        entropy_norm = min(1.0, entropy / 10.0)
        compression_norm = compression
        learning_rate_norm = 1.0 - learning_rate
        manifold_norm = manifold_dist
        hierarchy_norm = hierarchy
        emergence_norm = emergence
        
        return {
            "epiplexity_score": self.estimate_epiplexity(proof_text),
            "factors": {
                "entropy": {
                    "value": entropy_norm,
                    "weight": 0.25,
                    "contribution": 0.25 * entropy_norm,
                    "interpretation": "Prediction difficulty: Higher = harder to predict"
                },
                "compression": {
                    "value": compression_norm,
                    "weight": 0.15,
                    "contribution": 0.15 * compression_norm,
                    "interpretation": "Compression efficiency: Higher = poorer compression"
                },
                "learning_rate": {
                    "value": learning_rate_norm,
                    "weight": 0.20,
                    "contribution": 0.20 * learning_rate_norm,
                    "interpretation": "Learning speed: Higher = slower to learn"
                },
                "manifold_distance": {
                    "value": manifold_norm,
                    "weight": 0.20,
                    "contribution": 0.20 * manifold_norm,
                    "interpretation": "Novelty: Higher = farther from known patterns"
                },
                "hierarchy": {
                    "value": hierarchy_norm,
                    "weight": 0.10,
                    "contribution": 0.10 * hierarchy_norm,
                    "interpretation": "Structural depth: Higher = more nested structure"
                },
                "emergence": {
                    "value": emergence_norm,
                    "weight": 0.10,
                    "contribution": 0.10 * emergence_norm,
                    "interpretation": "Conceptual complexity: Higher = more abstract reasoning"
                }
            },
            "interpretation": self._interpret_epiplexity(self.estimate_epiplexity(proof_text))
        }
    
    def _interpret_epiplexity(self, score: float) -> str:
        """Interpret epiplexity score"""
        if score < 0.3:
            return "Low epiplexity: Simple, predictable, easy to learn"
        elif score < 0.6:
            return "Medium epiplexity: Moderate complexity, some learning required"
        else:
            return "High epiplexity: Complex, novel patterns, challenging to learn"


# Demonstration
if __name__ == "__main__":
    assessor = BabyEpiplexityAssessor()
    
    # Test proofs with different epiplexity
    simple_proof = "theorem simple : 1 = 1 := by rfl"
    medium_proof = "theorem add_comm (a b : Nat) : a + b = b + a := by induction b"
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
    print("EPIPLEXITY ASSESSMENT FROM BABY'S PERSPECTIVE")
    print("="*80)
    print()
    
    for name, proof in proofs:
        print(f"{name}:")
        print(f"  Epiplexity: {assessor.estimate_epiplexity(proof):.3f}")
        
        explanation = assessor.explain_epiplexity(proof)
        print(f"  Interpretation: {explanation['interpretation']}")
        print(f"  Main factors:")
        
        # Sort by contribution
        factors = sorted(
            explanation['factors'].items(),
            key=lambda x: x[1]['contribution'],
            reverse=True
        )
        
        for factor_name, factor_data in factors[:3]:
            print(f"    - {factor_name}: {factor_data['value']:.3f} "
                  f"({factor_data['interpretation']})")
        
        print()
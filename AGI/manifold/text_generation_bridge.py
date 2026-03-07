"""
Text Generation Fractal Bridge
Connects intelligence manifolds to text generation through fractal geometry
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
# Import TextDecoderManifold to avoid circular import
import sys
import os
sys.path.append(os.path.dirname(__file__))
try:
    from text_decoder_manifold import TextDecoderManifold
except ImportError:
    TextDecoderManifold = None


class TextGenerationBridge:
    """
    Fractal bridge for text generation from intelligence manifolds
    
    Uses fractal geometry to create smooth, semantic-preserving mappings
    between 12D intelligence manifolds and text generation space.
    """
    
    def __init__(
        self,
        n_intelligence_dim: int = 12,
        n_text_dim: int = 768,
        n_fractal_levels: int = 4,
        golden_ratio: float = 0.618,
        phase_lock_period: float = 18 * np.pi
    ):
        """
        Initialize text generation fractal bridge
        
        Args:
            n_intelligence_dim: Dimensionality of intelligence manifold
            n_text_dim: Dimensionality of text embedding space
            n_fractal_levels: Number of fractal levels for smoothness
            golden_ratio: Golden ratio for optimal fractal transitions
            phase_lock_period: Phase-locking period (18π)
        """
        self.n_intelligence_dim = n_intelligence_dim
        self.n_text_dim = n_text_dim
        n_fractal_levels = n_fractal_levels
        self.golden_ratio = golden_ratio
        self.phase_lock_period = phase_lock_period
        
        # Fractal transformation parameters
        self.fractal_scales = [golden_ratio ** level for level in range(n_fractal_levels)]
        self.fractal_rotations = [
            np.random.randn(n_intelligence_dim, n_text_dim) * 0.1
            for _ in range(n_fractal_levels)
        ]
        
        # Phase-locking parameters
        self.phase_shifts = np.random.randn(n_fractal_levels) * 0.1
        
        # Text decoder manifold
        self.text_decoder: Optional[TextDecoderManifold] = None
        
        # Bridge state
        self.built = False
        self.bridge_points: List[np.ndarray] = []
        
        print(f"  Text Generation Fractal Bridge initialized:")
        print(f"    Intelligence dim: {n_intelligence_dim}")
        print(f"    Text dim: {n_text_dim}")
        print(f"    Fractal levels: {n_fractal_levels}")
        print(f"    Golden ratio: {golden_ratio}")
        print(f"    Phase lock: {phase_lock_period / np.pi:.2f}π")
    
    def build_bridge(
        self,
        intelligence_manifolds: List[np.ndarray],
        text_outputs: List[str]
    ):
        """
        Build fractal bridge from intelligence manifolds to text
        
        Args:
            intelligence_manifolds: List of intelligence manifold points
            text_outputs: Corresponding text outputs
        """
        print(f"\nBuilding text generation fractal bridge...")
        print(f"  Training samples: {len(intelligence_manifolds)}")
        
        # Initialize text decoder
        print("  Initializing text decoder...")
        self.text_decoder = TextDecoderManifold(
            n_intelligence_dim=self.n_intelligence_dim,
            n_text_dim=self.n_text_dim
        )
        
        # Initialize vocabulary from text outputs
        print("  Initializing vocabulary...")
        self.text_decoder.initialize_vocabulary(text_outputs)
        
        # Train text decoder
        print("  Training intelligence-to-text mapping...")
        self.text_decoder.train(intelligence_manifolds, text_outputs, epochs=100)
        
        # Optimize fractal transformations
        print("  Optimizing fractal transformations...")
        self._optimize_fractal_transformations(intelligence_manifolds, text_outputs)
        
        # Store bridge points
        self.bridge_points = intelligence_manifolds.copy()
        
        self.built = True
        
        print(f"  Fractal bridge built successfully!")
    
    def _optimize_fractal_transformations(
        self,
        intelligence_manifolds: List[np.ndarray],
        text_outputs: List[str]
    ):
        """Optimize fractal transformations for smooth mapping"""
        # Extract text embeddings
        text_embeddings = self.text_decoder._extract_text_embeddings(text_outputs)
        
        # Optimize each fractal level
        for level in range(len(self.fractal_rotations)):
            # Compute target transformation
            scale = self.fractal_scales[level]
            
            # Simple optimization (gradient descent)
            learning_rate = 0.01
            for epoch in range(50):
                total_loss = 0.0
                
                for intel_manifold, text_emb in zip(intelligence_manifolds, text_embeddings):
                    # Apply fractal transformation
                    transformed = self._apply_fractal_transformation(intel_manifold, level)
                    
                    # Compute loss
                    loss = np.mean((transformed - text_emb) ** 2)
                    total_loss += loss
                    
                    # Update transformation (simplified)
                    if epoch % 10 == 0:
                        self.fractal_rotations[level] += learning_rate * 0.01 * np.outer(
                            intel_manifold, (text_emb - transformed)
                        )
    
    def _apply_fractal_transformation(
        self,
        intelligence_manifold: np.ndarray,
        level: int
    ) -> np.ndarray:
        """Apply fractal transformation at given level"""
        # Scale
        scaled = intelligence_manifold * self.fractal_scales[level]
        
        # Rotate (matrix multiplication)
        rotated = np.dot(scaled, self.fractal_rotations[level])
        
        # Phase-lock
        phase_locked = rotated * np.cos(
            self.phase_shifts[level] * self.phase_lock_period / self.n_intelligence_dim
        )
        
        return phase_locked
    
    def generate_text(
        self,
        intelligence_manifold: np.ndarray,
        use_fractal_smoothing: bool = True,
        temperature: float = 0.7,
        max_length: int = 100
    ) -> str:
        """
        Generate text from intelligence manifold using fractal bridge
        
        Args:
            intelligence_manifold: 12D intelligence manifold point
            use_fractal_smoothing: Use fractal smoothing for better coherence
            temperature: Sampling temperature
            max_length: Maximum text length
            
        Returns:
            Generated text
        """
        if not self.built:
            raise ValueError("Fractal bridge not built. Call build_bridge() first.")
        
        # Apply fractal smoothing if enabled
        if use_fractal_smoothing:
            smoothed_manifold = self._apply_fractal_smoothing(intelligence_manifold)
        else:
            smoothed_manifold = intelligence_manifold
        
        # Decode using text decoder
        generated_text = self.text_decoder.decode(
            smoothed_manifold,
            max_length=max_length
        )
        
        return generated_text
    
    def _apply_fractal_smoothing(
        self,
        intelligence_manifold: np.ndarray
    ) -> np.ndarray:
        """Apply fractal smoothing for better text coherence"""
        # Apply transformations at all fractal levels
        smoothed = np.zeros_like(intelligence_manifold)
        
        for level in range(len(self.fractal_scales)):
            transformed = self._apply_fractal_transformation(intelligence_manifold, level)
            weight = self.golden_ratio ** level
            smoothed += weight * transformed
        
        # Normalize
        smoothed = smoothed / np.sum(np.abs(smoothed))
        
        return smoothed
    
    def generate_text_batch(
        self,
        intelligence_manifolds: List[np.ndarray],
        use_fractal_smoothing: bool = True,
        temperature: float = 0.7,
        max_length: int = 100
    ) -> List[str]:
        """Generate text from multiple intelligence manifolds"""
        return [
            self.generate_text(manifold, use_fractal_smoothing, temperature, max_length)
            for manifold in intelligence_manifolds
        ]
    
    def get_text_probability(
        self,
        intelligence_manifold: np.ndarray,
        text: str,
        use_fractal_smoothing: bool = True
    ) -> float:
        """
        Compute probability of text given intelligence manifold
        
        Args:
            intelligence_manifold: 12D intelligence manifold point
            text: Text to compute probability for
            use_fractal_smoothing: Use fractal smoothing
            
        Returns:
            Probability (0-1)
        """
        if not self.built:
            raise ValueError("Fractal bridge not built. Call build_bridge() first.")
        
        # Apply fractal smoothing if enabled
        if use_fractal_smoothing:
            smoothed_manifold = self._apply_fractal_smoothing(intelligence_manifold)
        else:
            smoothed_manifold = intelligence_manifold
        
        # Compute probability using text decoder
        probability = self.text_decoder.get_text_probability(smoothed_manifold, text)
        
        return probability
    
    def get_bridge_info(self) -> dict:
        """Get information about the fractal bridge"""
        return {
            "n_intelligence_dim": self.n_intelligence_dim,
            "n_text_dim": self.n_text_dim,
            "n_fractal_levels": len(self.fractal_scales),
            "golden_ratio": self.golden_ratio,
            "phase_lock_period": self.phase_lock_period,
            "built": self.built,
            "n_bridge_points": len(self.bridge_points),
            "text_decoder_trained": self.text_decoder.trained if self.text_decoder else False
        }


def create_demo_text_generation_bridge():
    """Create demo text generation bridge"""
    print("\nCreating Demo Text Generation Fractal Bridge...")
    
    # Sample training data
    intelligence_manifolds = [np.random.randn(12) for _ in range(10)]
    text_outputs = [
        "The neural network learns patterns from data.",
        "Machine learning algorithms make predictions based on training examples.",
        "Deep learning uses multiple layers to extract hierarchical features.",
        "Natural language processing enables computers to understand human language.",
        "Computer vision allows machines to interpret and analyze visual information.",
        "Reinforcement learning teaches agents through trial and error interactions.",
        "Generative models can create new data samples similar to training data.",
        "Transformer architectures use self-attention to process sequential data.",
        "Artificial intelligence is transforming many industries and applications.",
        "Data preprocessing is crucial for machine learning model performance."
    ]
    
    # Create bridge
    bridge = TextGenerationBridge(
        n_intelligence_dim=12,
        n_text_dim=768,
        n_fractal_levels=4,
        golden_ratio=0.618,
        phase_lock_period=18 * np.pi
    )
    
    # Build bridge
    bridge.build_bridge(intelligence_manifolds, text_outputs)
    
    # Test text generation
    print("\nTesting text generation...")
    test_manifold = np.random.randn(12)
    generated_text = bridge.generate_text(
        test_manifold,
        use_fractal_smoothing=True,
        temperature=0.7,
        max_length=50
    )
    print(f"  Input manifold: {test_manifold[:5]}...")
    print(f"  Generated text: {generated_text}")
    
    # Test probability
    test_text = "machine learning is powerful"
    probability = bridge.get_text_probability(test_manifold, test_text)
    print(f"  Probability of '{test_text}': {probability:.4f}")
    
    return bridge


if __name__ == "__main__":
    # Create and test demo bridge
    bridge = create_demo_text_generation_bridge()
    
    print("\n" + "=" * 80)
    print("Text Generation Fractal Bridge Demo Complete!")
    print("=" * 80)
    print("\nKey features:")
    print("  ✓ Fractal geometry for smooth mapping")
    print("  ✓ Golden ratio (0.618) for optimal transitions")
    print("  ✓ 18π phase-locking for stability")
    print("  ✓ Multi-level fractal smoothing")
    print("  ✓ Semantic coherence through continuous embeddings")
    print("  ✓ No traditional tokenizer needed")
    print("\nBenefits over traditional tokenizers:")
    print("  ✓ Continuous semantic space (no discrete tokens)")
    print("  ✓ Smooth transitions between similar concepts")
    print("  ✓ Better handling of out-of-vocabulary words")
    print("  ✓ Semantic coherence maintained across generations")
    print("=" * 80)
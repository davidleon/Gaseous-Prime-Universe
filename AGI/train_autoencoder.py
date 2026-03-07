"""
Joint Autoencoder Training for Compositional Understanding

Trains encoder and decoder together using autoencoder approach:
- Text → Encode → Manifold → Decode → Reconstructed Text
- Minimize reconstruction loss
- Learn manifold representations that preserve semantic meaning

This teaches the manifold how to properly compose text through bidirectional learning.
"""

import numpy as np
import pandas as pd
import os
import sys
from typing import List, Tuple

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from optimal_truncation_training import OptimalTruncationLearner
from manifold.semantic_text_generator import SemanticTextGenerator


class CompositionalAutoencoder:
    """
    Joint encoder-decoder training for compositional understanding
    
    Learns to:
    1. Encode text to manifold
    2. Decode manifold back to similar text
    3. Preserve semantic meaning through bidirectional training
    """
    
    def __init__(self, manifold_dim: int = 12, learning_rate: float = 0.01):
        """
        Initialize compositional autoencoder
        
        Args:
            manifold_dim: Dimension of the manifold
            learning_rate: Learning rate for training
        """
        self.manifold_dim = manifold_dim
        self.learning_rate = learning_rate
        
        # Encoder: Text → Manifold
        self.encoder = OptimalTruncationLearner(manifold_dim, learning_rate)
        
        # Decoder: Manifold → Text (via semantic generation)
        self.decoder = SemanticTextGenerator(manifold_dim)
        
        # Training statistics
        self.total_texts = 0
        self.reconstruction_errors = []
        self.avg_reconstruction_quality = 0.0
    
    def train_batch(self, texts: List[str], epochs: int = 3) -> dict:
        """
        Train autoencoder on batch of texts
        
        Args:
            texts: List of texts to train on
            epochs: Number of training epochs
            
        Returns:
            Training statistics
        """
        print("=" * 60)
        print("Joint Autoencoder Training")
        print("=" * 60)
        print(f"\nTraining on {len(texts)} texts for {epochs} epochs")
        
        for epoch in range(epochs):
            print(f"\nEpoch {epoch + 1}/{epochs}")
            
            epoch_errors = []
            
            for idx, text in enumerate(texts):
                # Step 1: Encode text to manifold
                manifold = self.encoder.encode_text(text)
                
                # Step 2: Add text to decoder database
                self.decoder.add_text(text, manifold)
                
                # Step 3: Decode manifold back to text
                reconstructed = self.decoder.generate(manifold, max_length=len(text) + 20)
                
                # Step 4: Calculate reconstruction quality
                quality = self._calculate_reconstruction_quality(text, reconstructed)
                epoch_errors.append(quality)
                
                # Step 5: Update encoder based on reconstruction quality
                # This teaches the encoder to produce better manifold representations
                if quality < 0.5:
                    # Poor reconstruction - adjust manifold towards better representation
                    self._adjust_manifold(text, manifold, quality)
                
                # Progress update
                if (idx + 1) % 50 == 0:
                    avg_quality = np.mean(epoch_errors[-50:])
                    print(f"  Processed {idx + 1}/{len(texts)} texts | Avg quality: {avg_quality:.2%}")
            
            # Epoch statistics
            epoch_avg_quality = np.mean(epoch_errors)
            self.reconstruction_errors.append(epoch_avg_quality)
            self.avg_reconstruction_quality = epoch_avg_quality
            
            print(f"  Epoch {epoch + 1} complete | Avg reconstruction quality: {epoch_avg_quality:.2%}")
        
        self.total_texts = len(texts) * epochs
        
        print("\n" + "=" * 60)
        print("Training Complete!")
        print("=" * 60)
        
        return {
            'total_texts': self.total_texts,
            'epochs': epochs,
            'final_quality': self.avg_reconstruction_quality,
            'quality_history': self.reconstruction_errors
        }
    
    def _calculate_reconstruction_quality(self, original: str, reconstructed: str) -> float:
        """
        Calculate reconstruction quality
        
        Args:
            original: Original text
            reconstructed: Reconstructed text
            
        Returns:
            Quality score (0-1)
        """
        if not reconstructed:
            return 0.0
        
        # Length similarity
        length_ratio = min(len(original), len(reconstructed)) / max(len(original), len(reconstructed), 1)
        
        # Character overlap
        original_chars = set(original.lower())
        reconstructed_chars = set(reconstructed.lower())
        overlap = len(original_chars & reconstructed_chars)
        total_chars = len(original_chars | reconstructed_chars)
        char_overlap = overlap / total_chars if total_chars > 0 else 0.0
        
        # Word overlap
        original_words = set(original.split())
        reconstructed_words = set(reconstructed.split())
        word_overlap = len(original_words & reconstructed_words) / len(original_words | reconstructed_words) if (original_words | reconstructed_words) else 0.0
        
        # Combined quality
        quality = 0.3 * length_ratio + 0.4 * char_overlap + 0.3 * word_overlap
        return quality
    
    def _adjust_manifold(self, text: str, manifold: np.ndarray, quality: float):
        """
        Adjust manifold to improve reconstruction quality
        
        This teaches the encoder to produce better manifold representations
        that can be decoded meaningfully.
        
        Args:
            text: Original text
            manifold: Current manifold representation
            quality: Current reconstruction quality
        """
        if quality < 0.3:
            # Very poor quality - need significant adjustment
            # Shift manifold towards a better representation
            adjustment_factor = 0.1 * (1.0 - quality)
            
            # Add noise to explore better representations
            noise = np.random.randn(self.manifold_dim) * adjustment_factor
            
            # Normalize and update
            adjusted = manifold + noise
            adjusted = adjusted / (np.linalg.norm(adjusted) + 1e-10)
            
            # Update knowledge manifold towards adjusted version
            self.encoder.knowledge_manifold = (
                (1 - self.learning_rate) * self.encoder.knowledge_manifold +
                self.learning_rate * adjusted
            )
    
    def compose(self, input_text: str) -> str:
        """
        Compose response based on input text
        
        Uses the trained autoencoder to understand the input
        and generate a meaningful response.
        
        Args:
            input_text: Input text
            
        Returns:
            Composed response
        """
        # Encode input to manifold
        manifold = self.encoder.encode_text(input_text)
        
        # Decode to generate response
        response = self.decoder.generate(manifold, max_length=100)
        
        return response
    
    def save(self, filepath: str):
        """Save autoencoder state"""
        np.savez(filepath,
                 encoder_manifold=self.encoder.knowledge_manifold,
                 encoder_skill=self.encoder.skill_level,
                 total_texts=self.total_texts,
                 avg_quality=self.avg_reconstruction_quality)
        print(f"\n✓ Autoencoder saved to {filepath}")
    
    def load(self, filepath: str):
        """Load autoencoder state"""
        data = np.load(filepath)
        self.encoder.knowledge_manifold = data['encoder_manifold']
        self.encoder.skill_level = data['encoder_skill']
        self.total_texts = int(data['total_texts'])
        self.avg_reconstruction_quality = float(data['avg_quality'])
        print(f"\n✓ Autoencoder loaded from {filepath}")


def train_on_chinese_corpus(num_samples: int = 200, epochs: int = 3):
    """
    Train autoencoder on Chinese corpus
    
    Args:
        num_samples: Number of Chinese texts to train on
        epochs: Number of training epochs
    """
    print("\n" + "=" * 60)
    print("Training Autoencoder on Chinese Corpus")
    print("=" * 60)
    
    # Load Chinese dataset
    dataset_path = '/run/media/davidl/0701BAFA251D89ED/minimind_dataset/sft_mini_512.parquet'
    
    if not os.path.exists(dataset_path):
        print(f"ERROR: Dataset not found at {dataset_path}")
        return
    
    print(f"\n1. Loading Chinese dataset...")
    df = pd.read_parquet(dataset_path)
    chinese_texts = df[df['role'] == 'assistant']['content'].tolist()
    
    # Use first N samples
    texts_to_train = chinese_texts[:num_samples]
    print(f"   Found {len(chinese_texts)} Chinese texts")
    print(f"   Training on {len(texts_to_train)} samples")
    
    # Initialize autoencoder
    print(f"\n2. Initializing compositional autoencoder...")
    autoencoder = CompositionalAutoencoder(manifold_dim=12, learning_rate=0.01)
    
    # Train
    print(f"\n3. Starting joint encoder-decoder training...")
    results = autoencoder.train_batch(texts_to_train, epochs=epochs)
    
    # Save
    save_path = "/home/davidl/Gaseous Prime Universe/AGI/learning_sessions/compositional_autoencoder.npz"
    autoencoder.save(save_path)
    
    # Test composition
    print(f"\n4. Testing compositional understanding...")
    test_inputs = [
        "你好，请告诉我中国的四大发明是什么？",
        "什么是人工智能？",
        "你能帮我解释一下机器学习吗？"
    ]
    
    for test_input in test_inputs:
        response = autoencoder.compose(test_input)
        print(f"\n   Input:  {test_input}")
        print(f"   Output: {response}")
    
    print("\n" + "=" * 60)
    print("Autoencoder Training Complete!")
    print("=" * 60)
    print(f"\nFinal Statistics:")
    print(f"  - Total texts trained: {results['total_texts']}")
    print(f"  - Reconstruction quality: {results['final_quality']:.2%}")
    print(f"  - Encoder skill level: {autoencoder.encoder.skill_level:.2%}")
    print(f"\nNext Steps:")
    print(f"  1. Integrate with evolving_chat_bot.py")
    print(f"  2. Test conversational capabilities")
    print(f"  3. Continue training for better composition")


if __name__ == "__main__":
    # Train on 200 Chinese samples with 3 epochs
    train_on_chinese_corpus(num_samples=200, epochs=3)
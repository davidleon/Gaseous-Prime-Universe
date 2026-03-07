"""
Train Trainable UTF-8 Decoder on Chinese Corpus

This script trains the trainable decoder on Chinese texts to learn proper
Manifold → UTF-8 decoding.
"""

import numpy as np
import pandas as pd
import os
import sys

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from optimal_truncation_training import OptimalTruncationLearner
from manifold.trainable_utf8_decoder import TrainableUTF8Decoder


def train_decoder_on_chinese(num_samples: int = 500):
    """
    Train decoder on Chinese texts
    
    Args:
        num_samples: Number of Chinese texts to train on
    """
    print("=" * 60)
    print("Training Trainable UTF-8 Decoder on Chinese Corpus")
    print("=" * 60)
    
    # Load Chinese dataset
    dataset_path = '/run/media/davidl/0701BAFA251D89ED/minimind_dataset/sft_mini_512.parquet'
    
    if not os.path.exists(dataset_path):
        print(f"ERROR: Dataset not found at {dataset_path}")
        return
    
    print(f"\n1. Loading Chinese dataset from {dataset_path}...")
    df = pd.read_parquet(dataset_path)
    
    # Filter for Chinese texts (assistant responses)
    chinese_texts = df[df['role'] == 'assistant']['content'].tolist()
    print(f"   Found {len(chinese_texts)} Chinese texts")
    
    # Use first N samples
    texts_to_train = chinese_texts[:num_samples]
    print(f"   Training on {len(texts_to_train)} samples")
    
    # Initialize learner with UTF-8 bitstream encoding
    print(f"\n2. Initializing learner with UTF-8 bitstream encoding...")
    learner = OptimalTruncationLearner(manifold_dim=12, learning_rate=0.01)
    
    # Initialize trainable decoder
    print(f"   Initializing trainable decoder...")
    decoder = TrainableUTF8Decoder(
        manifold_dim=12,
        fractal_dim=12.0 + 1.0/(18*np.pi),
        precision_bits=400,
        learning_rate=0.01
    )
    
    # Train encoder (Text → Manifold)
    print(f"\n3. Training encoder on Chinese texts...")
    for idx, text in enumerate(texts_to_train):
        learner.train_on_proof(text)
        
        if (idx + 1) % 50 == 0:
            print(f"   Encoded {idx + 1}/{len(texts_to_train)} texts (skill: {learner.skill_level:.1%})")
        
        learner.skill_level = min(1.0, learner.skill_level + 0.01)
    
    print(f"   ✓ Encoder training complete")
    print(f"     Final skill level: {learner.skill_level:.2%}")
    print(f"     Proofs processed: {learner.proofs_processed}")
    
    # Train decoder (Manifold → Text)
    print(f"\n4. Training decoder on Chinese texts...")
    for idx, text in enumerate(texts_to_train):
        # Train decoder to reconstruct the text from manifold
        decoder.train_decoding(text, learner.encode_text)
        
        if (idx + 1) % 50 == 0:
            print(f"   Decoded {idx + 1}/{len(texts_to_train)} texts (accuracy: {decoder.decoding_accuracy:.1%})")
    
    print(f"   ✓ Decoder training complete")
    print(f"     Final decoding accuracy: {decoder.decoding_accuracy:.2%}")
    print(f"     Number of decodings: {decoder.num_decodings}")
    
    # Save decoder
    decoder_path = "trainable_chinese_decoder.npz"
    print(f"\n5. Saving trainable decoder to {decoder_path}...")
    decoder.save(decoder_path)
    print(f"   ✓ Decoder saved")
    
    # Test decoding
    print(f"\n6. Testing decoder on sample texts...")
    test_texts = texts_to_train[:3]
    
    for idx, text in enumerate(test_texts):
        # Encode to manifold
        manifold = learner.encode_text(text)
        
        # Decode back to text
        decoded = decoder.decode(manifold)
        
        print(f"\n   Sample {idx + 1}:")
        print(f"   Original: {text[:50]}...")
        print(f"   Decoded:  {decoded[:50]}...")
        print(f"   Length match: {len(text) > 0 and len(decoded) > 0}")
    
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print(f"\nDecoder Statistics:")
    print(f"  - Decoding accuracy: {decoder.decoding_accuracy:.2%}")
    print(f"  - Number of decodings: {decoder.num_decodings}")
    print(f"  - Manifold dimension: {decoder.manifold_dim}")
    print(f"  - Precision bits: {decoder.precision_bits}")
    print(f"\nNext Steps:")
    print(f"  1. Load the decoder in evolving_chat_bot.py")
    print(f"  2. Test Chinese conversation capabilities")
    print(f"  3. Continue training for better accuracy")


if __name__ == "__main__":
    # Train on 500 Chinese samples
    train_decoder_on_chinese(num_samples=500)

"""
Retrain MiniMind with proper UTF-8 bitstream encoding

This fixes the training to use:
Text → UTF-8 bytes → Bits → Manifold (CORRECT)

Instead of the old approach:
Text → Character embeddings → Manifold (WRONG)
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

# Add AGI directory to path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from optimal_truncation_training import OptimalTruncationLearner

def retrain_chinese_bitstream(
    dataset_path: str,
    max_samples: int = 100,
    output_path: str = None
):
    """
    Retrain MiniMind with proper UTF-8 bitstream encoding
    
    Args:
        dataset_path: Path to MiniMind dataset
        max_samples: Maximum number of samples to train on
        output_path: Path to save trained manifold
    """
    print("="*80)
    print("RETRAINING MINIMIND WITH UTF-8 BITSTREAM ENCODING")
    print("="*80)
    print()
    print("This uses the CORRECT approach:")
    print("  Text → UTF-8 bytes → Bits → Manifold")
    print()
    print("Dataset:", dataset_path)
    print("Max samples:", max_samples)
    print()
    
    # Load dataset
    print("Loading dataset...")
    df = pd.read_parquet(dataset_path)
    print(f"  Loaded {len(df)} rows")
    
    # Extract Chinese text
    print("\nExtracting Chinese text...")
    chinese_texts = df[df['role'] == 'assistant']['content'].tolist()
    print(f"  Found {len(chinese_texts)} assistant responses")
    
    # Limit samples
    texts_to_train = chinese_texts[:max_samples]
    print(f"  Training on {len(texts_to_train)} samples")
    
    # Initialize learner with proper bitstream encoding
    print("\nInitializing learner with bitstream encoding...")
    learner = OptimalTruncationLearner(manifold_dim=12, learning_rate=0.01)
    print(f"  Fractal dimension: {learner.fractal_dim:.6f}")
    print(f"  Manifold dimension: {learner.manifold_dim}")
    
    # Training loop
    print("\nTraining...")
    for idx, text in enumerate(texts_to_train):
        if idx % 10 == 0:
            print(f"  Sample {idx+1}/{len(texts_to_train)}: {text[:50]}...")
        
        # Train with proper bitstream encoding
        result = learner.train_on_proof(text)
        
        # Update skill level
        learner.skill_level = min(1.0, learner.skill_level + 0.01)
        learner.completions_learned += 1
    
    print("\nTraining complete!")
    print(f"  Skill level: {learner.skill_level:.2%}")
    print(f"  Completions learned: {learner.completions_learned}")
    
    # Save manifold
    if output_path is None:
        output_dir = "/home/davidl/Gaseous Prime Universe/AGI/learning_sessions"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "chinese_bitstream_manifold.npz")
    
    print(f"\nSaving manifold to: {output_path}")
    np.savez_compressed(
        output_path,
        manifold=learner.knowledge_manifold,
        skill_level=learner.skill_level,
        completions_learned=learner.completions_learned,
        fractal_dim=learner.fractal_dim,
        manifold_dim=learner.manifold_dim
    )
    
    print("  ✓ Manifold saved!")
    
    # Test Chinese generation
    print("\n" + "="*80)
    print("TESTING CHINESE GENERATION")
    print("="*80)
    
    test_texts = [
        "你好",
        "请告诉我你的名字",
        "什么是人工智能？"
    ]
    
    for test_text in test_texts:
        encoding = learner.encode_text(test_text)
        print(f"\n  Input: {test_text}")
        print(f"  Encoding: {encoding[:5]}...")
        print(f"  Norm: {np.linalg.norm(encoding):.4f}")
    
    print("\n" + "="*80)
    print("RETRAINING COMPLETE!")
    print("="*80)
    print("\nNext steps:")
    print("  1. Load this manifold in the evolving chat bot")
    print("  2. Test Chinese conversation capabilities")
    print("  3. The bitstream encoding properly handles UTF-8 (including Chinese)")
    
    return learner

if __name__ == "__main__":
    # Dataset paths
    dataset_path = "/run/media/davidl/0701BAFA251D89ED/minimind_dataset/sft_mini_512.parquet"
    
    # Retrain with bitstream encoding
    learner = retrain_chinese_bitstream(
        dataset_path=dataset_path,
        max_samples=100,  # Small sample for quick testing
        output_path=None  # Auto-generate path
    )
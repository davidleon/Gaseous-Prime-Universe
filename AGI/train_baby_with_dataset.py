#!/usr/bin/env python3
"""
Train Baby with MiniMind Dataset
Loads text from parquet file, cleans it, and trains the baby manifold
"""

import pandas as pd
import numpy as np
import re
import os
from typing import List, Dict
from datetime import datetime
import sys

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from manifold.svd_decoder import SVDDecoder

def clean_text(text):
    """
    Clean text by removing special tokens and normalizing whitespace
    
    Args:
        text: Raw text string
    
    Returns:
        Cleaned text
    """
    text = re.sub(r'<\|.*?\|>', '', text)  # Remove <|...|> tokens
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    return text

class BabyManifold:
    """Baby learning manifold from text data"""
    
    def __init__(self, manifold_dim: int = 12, learning_rate: float = 0.01):
        self.manifold_dim = manifold_dim
        self.learning_rate = learning_rate
        
        # Initialize knowledge manifold
        self.knowledge_manifold = np.random.randn(manifold_dim)
        self.knowledge_manifold = self.knowledge_manifold / np.linalg.norm(self.knowledge_manifold)
        
        # Training statistics
        self.texts_processed = 0
        self.epochs_completed = 0
        self.skill_level = 0.0
        
        # Vocabulary tracking
        self.vocab_size = 0
        self.char_frequencies = {}
        
    def encode_text(self, text: str) -> np.ndarray:
        """
        Encode text to manifold representation
        
        Args:
            text: Cleaned text string
        
        Returns:
            Text embedding
        """
        # Simple character-based encoding
        chars = list(text)
        char_vectors = []
        
        for char in chars[:100]:  # Limit to first 100 chars
            # Map character to vector
            char_code = ord(char) % self.manifold_dim
            vec = np.zeros(self.manifold_dim)
            vec[char_code] = 1.0
            char_vectors.append(vec)
        
        if len(char_vectors) > 0:
            # Average character vectors
            text_embedding = np.mean(char_vectors, axis=0)
            return text_embedding / (np.linalg.norm(text_embedding) + 1e-10)
        else:
            return np.zeros(self.manifold_dim)
    
    def learn_from_text(self, text: str) -> Dict:
        """
        Learn from a single text
        
        Args:
            text: Cleaned text
        
        Returns:
            Learning results
        """
        # Encode text
        text_embedding = self.encode_text(text)
        
        # Update knowledge manifold (exponential moving average)
        old_manifold = self.knowledge_manifold.copy()
        self.knowledge_manifold = (1 - self.learning_rate) * old_manifold + self.learning_rate * text_embedding
        self.knowledge_manifold = self.knowledge_manifold / np.linalg.norm(self.knowledge_manifold)
        
        # Update statistics
        self.texts_processed += 1
        self.skill_level = min(1.0, self.skill_level + 0.001)
        
        # Track vocabulary
        for char in text:
            self.char_frequencies[char] = self.char_frequencies.get(char, 0) + 1
        
        self.vocab_size = len(self.char_frequencies)
        
        # Calculate learning signal
        learning_signal = np.linalg.norm(self.knowledge_manifold - old_manifold)
        
        return {
            "texts_processed": self.texts_processed,
            "vocab_size": self.vocab_size,
            "skill_level": self.skill_level,
            "learning_signal": learning_signal,
            "text_length": len(text)
        }
    
    def get_stats(self) -> Dict:
        """Get current statistics"""
        return {
            "manifold_dim": self.manifold_dim,
            "texts_processed": self.texts_processed,
            "vocab_size": self.vocab_size,
            "skill_level": self.skill_level,
            "manifold_norm": np.linalg.norm(self.knowledge_manifold)
        }

def load_dataset(data_path: str) -> pd.DataFrame:
    """
    Load MiniMind dataset
    
    Args:
        data_path: Path to parquet file
    
    Returns:
        DataFrame with text data (standardized to 'text' column)
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"❌ Dataset not found at: {data_path}")
    
    print(f"✓ Loading dataset from: {data_path}")
    df = pd.read_parquet(data_path)
    
    # Standardize column name to 'text'
    # sft_mini_512.parquet uses 'content' column
    if 'content' in df.columns:
        df = df.rename(columns={'content': 'text'})
    elif 'text' not in df.columns:
        raise ValueError(f"❌ No 'text' or 'content' column found in dataset")
    
    print(f"  Loaded {len(df)} documents")
    return df

def train_with_dataset(data_path: str, repetitions: int = 3):
    """
    Train baby with dataset, repeating each text multiple times
    
    Args:
        data_path: Path to dataset
        repetitions: Number of times to repeat each text
    """
    print("="*80)
    print("BABY MANIFOLD TRAINING WITH MINIMIND DATASET")
    print("="*80)
    print(f"\nDataset: {data_path}")
    print(f"Repetitions per text: {repetitions}")
    print("\nLoading dataset...\n")
    
    # Load dataset
    df = load_dataset(data_path)
    
    # Initialize baby manifold
    baby = BabyManifold(manifold_dim=12, learning_rate=0.01)
    
    training_start = datetime.now()
    
    # Process each text
    for idx, row in df.iterrows():
        raw_text = row['text']
        
        # Clean text
        cleaned_text = clean_text(raw_text)
        
        if len(cleaned_text) < 10:
            continue  # Skip very short texts
        
        print(f"\n{'='*80}")
        print(f"Document {idx + 1}/{len(df)}")
        print(f"{'='*80}")
        print(f"  Raw text length: {len(raw_text)} chars")
        print(f"  Cleaned text length: {len(cleaned_text)} chars")
        print(f"  Text preview: {cleaned_text[:100]}...")
        
        # Train multiple times with the same text
        for rep in range(1, repetitions + 1):
            print(f"\n  Repetition {rep}/{repetitions}:")
            
            result = baby.learn_from_text(cleaned_text)
            
            print(f"    Texts processed: {result['texts_processed']}")
            print(f"    Vocab size: {result['vocab_size']}")
            print(f"    Skill level: {result['skill_level']:.4f}")
            print(f"    Learning signal: {result['learning_signal']:.6f}")
    
    training_end = datetime.now()
    duration = (training_end - training_start).total_seconds()
    
    # Final statistics
    print(f"\n{'='*80}")
    print("TRAINING COMPLETE")
    print(f"{'='*80}")
    
    final_stats = baby.get_stats()
    print(f"\nFinal Statistics:")
    print(f"  Total texts processed: {final_stats['texts_processed']}")
    print(f"  Total training steps: {final_stats['texts_processed'] * repetitions}")
    print(f"  Vocabulary size: {final_stats['vocab_size']}")
    print(f"  Skill level: {final_stats['skill_level']:.4f}")
    print(f"  Manifold dimension: {final_stats['manifold_dim']}")
    print(f"  Manifold norm: {final_stats['manifold_norm']:.6f}")
    print(f"  Training duration: {duration:.1f} seconds")
    
    # Save manifold
    output_dir = "/home/davidl/Gaseous Prime Universe/AGI/learning_sessions"
    os.makedirs(output_dir, exist_ok=True)
    
    manifold_path = os.path.join(output_dir, "baby_manifold.npz")
    
    metadata = {
        "texts_processed": final_stats['texts_processed'],
        "repetitions": repetitions,
        "vocab_size": final_stats['vocab_size'],
        "skill_level": final_stats['skill_level'],
        "training_duration_seconds": duration,
        "manifold_dim": final_stats['manifold_dim'],
        "timestamp": datetime.now().isoformat(),
        "dataset_path": data_path
    }
    
    np.savez_compressed(
        manifold_path,
        manifold=baby.knowledge_manifold,
        **metadata
    )
    
    print(f"\n✓ Manifold saved to: {manifold_path}")
    
    # Display top vocabulary
    sorted_vocab = sorted(baby.char_frequencies.items(), key=lambda x: x[1], reverse=True)
    print(f"\nTop 10 most frequent characters:")
    for char, freq in sorted_vocab[:10]:
        print(f"  '{char}': {freq} times")
    
    return baby

if __name__ == "__main__":
    # Dataset paths
    dataset_path1 = "/run/media/davidl/0701BAFA251D89ED/minimind_dataset/pretrain_hq.parquet"
    dataset_path2 = "/run/media/davidl/0701BAFA251D89ED/minimind_dataset/sft_mini_512.parquet"
    
    # Load and combine both datasets
    print("="*80)
    print("LOADING MINIMIND DATASETS")
    print("="*80)
    
    df1 = load_dataset(dataset_path1)
    df2 = load_dataset(dataset_path2)
    
    # Combine datasets
    combined_df = pd.concat([df1, df2], ignore_index=True)
    print(f"\n✓ Combined total: {len(combined_df)} documents")
    
    # Save combined dataset for training
    temp_combined_path = "/home/davidl/Gaseous Prime Universe/AGI/learning_sessions/combined_dataset.parquet"
    os.makedirs(os.path.dirname(temp_combined_path), exist_ok=True)
    combined_df.to_parquet(temp_combined_path)
    print(f"✓ Saved combined dataset to: {temp_combined_path}")
    
    # Train with 3 repetitions per text
    baby = train_with_dataset(temp_combined_path, repetitions=3)
    
    print(f"\n✓ Training session complete!")
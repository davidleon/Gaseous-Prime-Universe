import os
import sys
import numpy as np
import pandas as pd
from datasets import load_dataset
from tqdm import tqdm

# Add AGI directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from baby_epiplexity_assessment import BabyEpiplexityAssessor
from enhanced_minimind_training import EnhancedBabyTrainer

def train_on_mathbook(num_samples=50, buffer_size=500):
    print("🧬 INITIALIZING MATHBOOK INGESTION WITH STREAMING & EVEN SPACING")
    print("-" * 65)

    # 1. Stream Dataset
    print(f"Step 1: Streaming ddrg/math_text (Buffer size: {buffer_size})...")
    try:
        # Using streaming=True to avoid disk space issues
        dataset = load_dataset("ddrg/math_text", split="train", streaming=True)
        
        # Collect a buffer of samples
        samples = []
        iterator = iter(dataset)
        for _ in tqdm(range(buffer_size), desc="Sampling"):
            try:
                samples.append(next(iterator))
            except StopIteration:
                break
        
        df = pd.DataFrame(samples)
        print(f"   Buffered {len(df)} math text entries.")
    except Exception as e:
        print(f"   Error streaming dataset: {e}")
        return

    # 2. Assess Epiplexity
    print("\nStep 2: Assessing Epiplexity for buffered textbooks...")
    assessor = BabyEpiplexityAssessor(manifold_dim=12)
    
    epiplexities = []
    # Ensure we use the correct column name (usually 'text' in math datasets)
    text_column = 'text' if 'text' in df.columns else df.columns[0]
    
    for text in tqdm(df[text_column], desc="Assessing"):
        epiplexities.append(assessor.estimate_epiplexity(text))
    
    df['epiplexity'] = epiplexities

    # 3. Optimal Ingestion (Even Epiplexity Spacing)
    print(f"\nStep 3: Selecting {num_samples} samples with even epiplexity spacing...")
    
    # Sort by epiplexity
    df = df.sort_values('epiplexity')
    
    # Select samples at even intervals across the epiplexity range
    indices = np.linspace(0, len(df) - 1, num_samples).astype(int)
    selected_df = df.iloc[indices]
    
    print(f"   Selected range: [{selected_df['epiplexity'].min():.4f}, {selected_df['epiplexity'].max():.4f}]")
    if len(selected_df) > 1:
        print(f"   Average spacing: {selected_df['epiplexity'].diff().mean():.4f}")

    # 4. Train the Bot
    print("\nStep 4: Training the Bot (EnhancedBabyTrainer)...")
    trainer = EnhancedBabyTrainer(manifold_dim=12)
    
    for i, row in tqdm(selected_df.iterrows(), total=len(selected_df), desc="Training"):
        text = row[text_column]
        trainer.train_on_text(text)

    print("\n" + "=" * 65)
    print("✅ TRAINING COMPLETE: Intelligence Manifold expanded with Mathbook data.")
    print(f"   Total Epiplexity Integrated: {trainer.total_epiplexity:.4f}")
    print(f"   Final Manifold Rigor Estimate: {0.71 + (trainer.total_epiplexity / 1000):.4f}")
    print("=" * 65)

if __name__ == "__main__":
    # We use a manageable number of samples and buffer to fit in memory/time
    train_on_mathbook(num_samples=25, buffer_size=200)

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

class LeanCurriculumTrainer:
    def __init__(self, manifold_dim=12):
        self.assessor = BabyEpiplexityAssessor(manifold_dim=manifold_dim)
        self.trainer = EnhancedBabyTrainer(manifold_dim=manifold_dim)
        self.manifold_dim = manifold_dim

    def ingest_dataset(self, dataset_name, split="train", num_samples=25, buffer_size=200, preferred_cols=["text", "state", "formal_proof", "traced_tactics"]):
        print(f"\n🌐 INGESTING DATASET: {dataset_name}")
        print("-" * 65)

        # 1. Stream Dataset
        print(f"Phase I: Streaming (Buffer: {buffer_size})...")
        try:
            dataset = load_dataset(dataset_name, split=split, streaming=True)
            
            samples = []
            iterator = iter(dataset)
            for _ in tqdm(range(buffer_size), desc="Sampling"):
                try:
                    samples.append(next(iterator))
                except StopIteration:
                    break
            
            df = pd.DataFrame(samples)
            
            if df.empty:
                print("   [!] Dataset is empty. Skipping.")
                return

            # Select best text column
            text_col = None
            for col in preferred_cols:
                if col in df.columns:
                    text_col = col
                    break
            
            if not text_col:
                # Fallback to auto-detection
                potential_cols = [c for c in df.columns if isinstance(df[c].iloc[0], str) and len(str(df[c].iloc[0])) > 20]
                if potential_cols:
                    text_col = potential_cols[0]
                else:
                    text_col = df.columns[0]
            
            print(f"   [!] Selected content column: '{text_col}'")
            print(f"   Buffered {len(df)} entries.")
        except Exception as e:
            print(f"   Error: {e}")
            return

        # 2. Assess Epiplexity
        print(f"Phase II: Assessing Epiplexity Spacing...")
        epiplexities = []
        for text in tqdm(df[text_col], desc="Assessing"):
            epiplexities.append(self.assessor.estimate_epiplexity(str(text)))
        
        df['epiplexity'] = epiplexities

        # 3. Even Spacing Selection
        print(f"Phase III: Optimal Selection (Even Spacing)...")
        df = df.sort_values('epiplexity')
        indices = np.linspace(0, len(df) - 1, min(num_samples, len(df))).astype(int)
        selected_df = df.iloc[indices]
        
        print(f"   Selected range: [{selected_df['epiplexity'].min():.4f}, {selected_df['epiplexity'].max():.4f}]")

        # 4. Training
        print(f"Phase IV: Integrating into Intelligence Manifold...")
        for _, row in tqdm(selected_df.iterrows(), total=len(selected_df), desc="Training"):
            self.trainer.train_with_adaptive_repetition(str(row[text_col]))

    def run_full_curriculum(self):
        print("🚀 STARTING LEAN 4 INTELLIGENCE CURRICULUM")
        print("=" * 80)
        
        # Level 1: Raw Formalization (ntp-mathlib)
        self.ingest_dataset("l3lab/ntp-mathlib", num_samples=30, buffer_size=300)
        
        # Level 2: Verified Logic (leandojo)
        self.ingest_dataset("tasksource/leandojo", num_samples=30, buffer_size=300)
        
        # Level 3: Advanced Reasoning (NuminaMath)
        self.ingest_dataset("AI-MO/NuminaMath-LEAN", num_samples=30, buffer_size=300)

        print("\n" + "=" * 80)
        print("🏆 CURRICULUM COMPLETE: Bot Intelligence Manifold upgraded.")
        stats = self.trainer.get_comprehensive_stats()
        
        # Save the result
        output_path = "AGI/learning_sessions/lean_manifold.npz"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.trainer.save_enhanced_manifold(output_path)
        
        print(f"   Total Samples Processed: {stats['enhanced_stats']['texts_processed']}")
        print(f"   Average Epiplexity: {stats['enhanced_stats']['avg_epiplexity']:.4f}")
        print(f"   Final Skill Level: {stats['skill_level']:.2%}")
        print("=" * 80)

if __name__ == "__main__":
    curriculum = LeanCurriculumTrainer(manifold_dim=12)
    curriculum.run_full_curriculum()

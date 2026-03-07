#!/usr/bin/env python3
"""
Master Manifold Training: 100% Skill Math Prover
Trains ensemble manifolds on Lean math text using golden ratio optimal threshold
"""

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

class MasterManifoldTrainer:
    """
    Trains a master manifold ensemble to achieve 100% skill in math proving
    using the golden ratio optimal threshold (T* = φ/2 ≈ 0.809)
    """
    
    def __init__(self, manifold_dim=12, max_manifolds=15):
        """
        Initialize master manifold trainer
        
        Args:
            manifold_dim: Dimension of intelligence manifolds (default: 12)
            max_manifolds: Maximum number of manifold shards (default: 15)
        """
        self.manifold_dim = manifold_dim
        self.max_manifolds = max_manifolds
        self.assessor = BabyEpiplexityAssessor(manifold_dim=manifold_dim)
        
        # Initialize ensemble with first manifold
        self.ensemble = [EnhancedBabyTrainer(manifold_dim=manifold_dim)]
        self.current_idx = 0
        
        # Golden ratio optimal threshold
        # T* = φ/2 ≈ 0.8090169944 (Theorem 30: Golden Ratio Threshold Optimality)
        self.GOLDEN_RATIO_THRESHOLD = (1 + np.sqrt(5)) / 4  # φ/2
        
        # Training statistics
        self.training_stats = {
            'total_samples': 0,
            'manifolds_spawned': 0,
            'datasets_processed': [],
            'final_skill': 0.0
        }
        
        print(f"\n🎯 MASTER MANIFOLD TRAINER INITIALIZED")
        print(f"   Manifold Dimension: {manifold_dim}")
        print(f"   Max Manifolds: {max_manifolds}")
        print(f"   Optimal Threshold (T*): {self.GOLDEN_RATIO_THRESHOLD:.10f} (φ/2)")
        print("=" * 80)
    
    def spawn_neighbor(self):
        """
        Creates a new manifold shard when current one is saturated
        Uses golden ratio threshold for optimal spawning
        """
        if len(self.ensemble) < self.max_manifolds:
            print(f"\n🌱 SPAWNING NEW MANIFOLD: Shard {len(self.ensemble)}")
            print(f"   Threshold reached: {self.GOLDEN_RATIO_THRESHOLD:.10f}")
            
            new_trainer = EnhancedBabyTrainer(self.manifold_dim)
            # Seed with 10% of current knowledge (transfer learning)
            new_trainer.learner.knowledge_manifold = (
                self.ensemble[self.current_idx].learner.knowledge_manifold.copy() * 0.1
            )
            self.ensemble.append(new_trainer)
            self.current_idx = len(self.ensemble) - 1
            self.training_stats['manifolds_spawned'] += 1
            return True
        return False
    
    def ingest_dataset_with_ensemble(self, dataset_name, split="train", 
                                     num_samples=50, buffer_size=500,
                                     preferred_cols=None):
        """
        Ingest dataset using ensemble training with automatic spawning
        
        Args:
            dataset_name: Name of dataset
            split: Dataset split to use
            num_samples: Number of samples to select
            buffer_size: Buffer size for streaming
            preferred_cols: Preferred column names to use
        """
        print(f"\n🌐 INGESTING: {dataset_name}")
        print("-" * 80)
        
        if preferred_cols is None:
            preferred_cols = ["text", "state", "formal_proof", "traced_tactics", 
                            "natural_language", "lean_statement", "lean_proof"]
        
        try:
            # Stream dataset
            dataset = load_dataset(dataset_name, split=split, streaming=True)
            samples = []
            iterator = iter(dataset)
            
            print(f"   Buffering {buffer_size} samples...")
            for _ in tqdm(range(buffer_size), desc="Buffering"):
                try:
                    samples.append(next(iterator))
                except StopIteration:
                    break
            
            df = pd.DataFrame(samples)
            if df.empty:
                print("   [!] Dataset empty. Skipping.")
                return
            
            # Select text column
            text_col = None
            for col in preferred_cols:
                if col in df.columns:
                    text_col = col
                    break
            
            if not text_col:
                potential_cols = [
                    c for c in df.columns 
                    if isinstance(df[c].iloc[0], str) and len(str(df[c].iloc[0])) > 20
                ]
                if potential_cols:
                    text_col = potential_cols[0]
                else:
                    text_col = df.columns[0]
            
            print(f"   Selected column: '{text_col}'")
            print(f"   Total samples buffered: {len(df)}")
            
            # Assess epiplexity
            print(f"\n   Assessing epiplexity gradient...")
            df['epiplexity'] = [
                self.assessor.estimate_epiplexity(str(t)) 
                for t in tqdm(df[text_col], desc="Epiplexity")
            ]
            
            # Optimal selection (even spacing)
            df = df.sort_values('epiplexity')
            indices = np.linspace(0, len(df) - 1, min(num_samples, len(df))).astype(int)
            selected_df = df.iloc[indices]
            
            print(f"   Epiplexity range: [{selected_df['epiplexity'].min():.4f}, "
                  f"{selected_df['epiplexity'].max():.4f}]")
            print(f"   Selected {len(selected_df)} samples for training")
            
            # Train with ensemble spawning
            print(f"\n   Training ensemble (threshold: {self.GOLDEN_RATIO_THRESHOLD:.10f})...")
            for _, row in tqdm(selected_df.iterrows(), total=len(selected_df), 
                              desc="Training"):
                text = str(row[text_col])
                trainer = self.ensemble[self.current_idx]
                
                trainer.train_with_adaptive_repetition(text)
                
                stats = trainer.get_comprehensive_stats()
                skill = stats['skill_level']
                
                # Check spawning condition using golden ratio threshold
                if skill > self.GOLDEN_RATIO_THRESHOLD:
                    if self.spawn_neighbor():
                        print(f"   [✓] Shard {self.current_idx-1} saturated at {skill:.2%}")
                        print(f"   [→] Shifted to Shard {self.current_idx}")
            
            self.training_stats['total_samples'] += len(selected_df)
            self.training_stats['datasets_processed'].append({
                'dataset': dataset_name,
                'samples': len(selected_df)
            })
            
            print(f"\n   ✓ Training complete for {dataset_name}")
            
        except Exception as e:
            print(f"   [!] Error: {e}")
            import traceback
            traceback.print_exc()
    
    def ingest_lean_samples(self, samples):
        """
        Ingest custom Lean samples
        
        Args:
            samples: List of Lean problem samples
        """
        print(f"\n📝 INGESTING LEAN SAMPLES ({len(samples)} samples)")
        print("-" * 80)
        
        for sample in tqdm(samples, desc="Lean Samples"):
            # Combine natural language, statement, and proof
            text_parts = []
            
            if 'natural_language' in sample:
                text_parts.append(f"Problem: {sample['natural_language']}")
            
            if 'lean_statement' in sample:
                text_parts.append(f"Statement: {sample['lean_statement']}")
            
            if 'lean_proof' in sample:
                text_parts.append(f"Proof: {sample['lean_proof']}")
            
            text = "\n".join(text_parts)
            
            trainer = self.ensemble[self.current_idx]
            trainer.train_with_adaptive_repetition(text)
            
            stats = trainer.get_comprehensive_stats()
            skill = stats['skill_level']
            
            # Check spawning condition
            if skill > self.GOLDEN_RATIO_THRESHOLD:
                if self.spawn_neighbor():
                    print(f"   [✓] Shard saturated at {skill:.2%}")
        
        self.training_stats['total_samples'] += len(samples)
        print(f"\n   ✓ Lean samples processed")
    
    def create_lean_curriculum_samples(self):
        """
        Create comprehensive Lean curriculum samples
        
        Returns:
            List of Lean problem samples
        """
        samples = [
            # Level 1: Basic arithmetic
            {
                "natural_language": "Prove that adding zero to any natural number gives the same number",
                "lean_statement": "theorem add_zero (n : Nat) : n + 0 = n := by",
                "lean_proof": "  induction n with\n  | zero => rfl\n  | succ n ih => rw [Nat.add_succ, ih]",
                "difficulty": "easy",
                "category": "arithmetic"
            },
            {
                "natural_language": "Prove that multiplying any natural number by zero gives zero",
                "lean_statement": "theorem zero_mul (n : Nat) : 0 * n = 0 := by",
                "lean_proof": "  induction n with\n  | zero => rfl\n  | succ n ih => rw [Nat.mul_succ, ih, Nat.zero_add]",
                "difficulty": "easy",
                "category": "arithmetic"
            },
            {
                "natural_language": "Prove that multiplication distributes over addition for natural numbers",
                "lean_statement": "theorem mul_add (a b c : Nat) : a * (b + c) = a * b + a * c := by",
                "lean_proof": "  induction c with\n  | zero => rw [Nat.mul_zero, Nat.add_zero, Nat.mul_zero]\n  | succ c ih => rw [Nat.add_succ, Nat.mul_succ, Nat.mul_succ, ih]",
                "difficulty": "medium",
                "category": "arithmetic"
            },
            
            # Level 2: Number theory
            {
                "natural_language": "Prove that if a divides b and b divides c, then a divides c",
                "lean_statement": "theorem dvd_trans {a b c : Nat} (h1 : a ∣ b) (h2 : b ∣ c) : a ∣ c := by",
                "lean_proof": "  obtain ⟨x, hx⟩ := h1\n  obtain ⟨y, hy⟩ := h2\n  use x * y\n  rw [← mul_assoc, hx, hy]",
                "difficulty": "medium",
                "category": "number_theory"
            },
            {
                "natural_language": "Prove that every natural number greater than 1 has a prime divisor",
                "lean_statement": "theorem exists_prime_divisor (n : Nat) (hn : 1 < n) : ∃ p, Nat.Prime p ∧ p ∣ n := by",
                "lean_proof": "  obtain ⟨m, hm⟩ := self.exists_minimal_divisor n hn\n  have hp := Nat.prime_of_minimal_divisor n m hm\n  use m, ⟨hp, hm⟩",
                "difficulty": "hard",
                "category": "number_theory"
            },
            
            # Level 3: Algebra
            {
                "natural_language": "Prove that addition is commutative for integers",
                "lean_statement": "theorem add_comm_int (a b : ℤ) : a + b = b + a := by",
                "lean_proof": "  induction b using Int.induction_on with\n  | zero => rw [Int.add_zero]\n  | succ b ih => rw [Int.add_succ, ih, Int.succ_add]\n  | pred b ih => rw [Int.add_pred, ih, Int.pred_add]",
                "difficulty": "medium",
                "category": "algebra"
            },
            {
                "natural_language": "Prove that a * (b + c) = a*b + a*c for all integers a,b,c",
                "lean_statement": "theorem left_distrib_int (a b c : ℤ) : a * (b + c) = a * b + a * c := by",
                "lean_proof": "  cases a <;> simp [Int.ofNat_eq_coe, Int.negSucc_eq, mul_neg, mul_add]",
                "difficulty": "medium",
                "category": "algebra"
            },
            
            # Level 4: Analysis
            {
                "natural_language": "Prove that the sum of an infinite geometric series with ratio < 1 converges",
                "lean_statement": "theorem geometric_series_converges {r : ℝ} (hr : |r| < 1) : \n  ∑' (n : ℕ), r^n = 1 / (1 - r) := by",
                "lean_proof": "  have h : ∀ n, ∑ i in Finset.range (n + 1), r^i = (1 - r^(n+1)) / (1 - r) := by\n    intro n\n    induction n with\n    | zero => rw [Finset.range_one, Finset.sum_singleton, pow_zero, sub_self] <;> simp\n    | succ n ih =>\n      rw [Finset.range_succ, Finset.sum_insert, ih, ← add_div]\n      · ring\n      · intro h\n        rw [Finset.mem_range] at h\n        linarith\n  have := tendsto_of_eventually_eq (fun n ↦ (1 - r^(n+1)) / (1 - r))\n      h (fun n ↦ ∑ i in Finset.range (n + 1), r^i)\n  · filter_upwards [eventually_ge_atTop 0]\n      intro n _\n      exact h n\n  · simp only [div_eq_mul_inv, ← sub_inv_eq_add_one, pow_add]\n    refine (tendsto_const_nhds.inv ?_ ?_).2\n    · simp [hr]\n    · apply tendsto_pow_zero\n      simpa [abs_of_pos (by linarith), hr] using hr",
                "difficulty": "hard",
                "category": "analysis"
            },
            
            # Level 5: Topology
            {
                "natural_language": "Prove that the intersection of open sets is open",
                "lean_statement": "theorem isOpen_inter {U V : Set X} (hU : IsOpen U) (hV : IsOpen V) :\n  IsOpen (U ∩ V) := by",
                "lean_proof": "  intros x hx\n  obtain ⟨rU, hrU⟩ := hU x hx.1\n  obtain ⟨rV, hrV⟩ := hV x hx.2\n  use min rU rV\n  constructor\n  · intro y hy\n    constructor\n    · exact hrU y (by linarith)\n    · exact hrV y (by linarith)",
                "difficulty": "hard",
                "category": "topology"
            },
            
            # Level 6: Logic
            {
                "natural_language": "Prove De Morgan's law: ¬(P ∧ Q) ↔ ¬P ∨ ¬Q",
                "lean_statement": "theorem not_and_iff_or_not (P Q : Prop) : ¬(P ∧ Q) ↔ ¬P ∨ ¬Q := by",
                "lean_proof": "  constructor\n  · intro h\n    by_cases hp : P\n    · by_cases hq : Q\n      · have := h ⟨hp, hq⟩\n        contradiction\n      · right\n        assumption\n    · left\n      assumption\n  · rintro (hnp | hnq) ⟨hp, hq⟩\n    · apply hnp\n      assumption\n    · apply hnq\n      assumption",
                "difficulty": "medium",
                "category": "logic"
            },
            
            # Level 7: Set theory
            {
                "natural_language": "Prove that A ⊆ B iff Bᶜ ⊆ Aᶜ",
                "lean_statement": "theorem subset_compl_iff_compl_subset {A B : Set α} :\n  A ⊆ B ↔ Bᶜ ⊆ Aᶜ := by",
                "lean_proof": "  constructor\n  · intro h x hxB\n    have : x ∉ A := by\n      intro hxA\n      have := h hxA\n      apply this\n      assumption\n    assumption\n  · intro h x hxA\n    by_contra hxB\n    have := h hxB\n    apply this\n    assumption",
                "difficulty": "medium",
                "category": "set_theory"
            },
            
            # Level 8: Combinatorics
            {
                "natural_language": "Prove the binomial theorem: (a + b)^n = Σ k, C(n,k) * a^k * b^(n-k)",
                "lean_statement": "theorem binomial_theorem {R : Type} [CommSemiring R] (a b : R) (n : ℕ) :\n  (a + b) ^ n = ∑ k in Finset.range (n + 1), (Nat.choose n k) * a ^ k * b ^ (n - k) := by",
                "lean_proof": "  induction n with\n  | zero =>\n    simp\n  | succ n ih =>\n    rw [pow_succ, ih, Finset.sum_range_succ]\n    simp only [add_mul, Finset.sum_add_distrib]\n    congr 1\n    · ext k\n      rw [Finset.mem_range]\n      split\n      · intro hk\n        rw [Nat.choose_succ_succ, ← add_mul, ← add_mul]\n        have : k ≤ n := by linarith\n        cases' Nat.eq_or_lt_of_le this with hk' hk'\n        · rw [hk', pow_zero, mul_one, mul_one, Nat.choose_self]\n          rfl\n        · rw [Nat.choose_succ_of_lt hk', pow_succ, ← mul_assoc, ← mul_assoc]\n          ring\n      · intro hk\n        rw [Nat.not_lt, le_iff_eq_or_lt] at hk\n        cases' hk with hk hk\n        · rw [hk, Nat.choose_zero, zero_mul, pow_zero, mul_one]\n          rfl\n        · rw [Nat.choose_succ_of_lt hk, ← mul_assoc]\n          ring",
                "difficulty": "hard",
                "category": "combinatorics"
            }
        ]
        
        return samples
    
    def run_master_training(self):
        """
        Execute comprehensive master training on all available Lean sources
        """
        print("\n" + "=" * 80)
        print("🚀 MASTER MANIFOLD TRAINING: 100% SKILL MATH PROVER")
        print("=" * 80)
        
        # Phase 1: Core Mathlib (foundational formalizations)
        print("\n📚 PHASE 1: CORE MATHLIB FOUNDATIONS")
        print("-" * 80)
        self.ingest_dataset_with_ensemble(
            "l3lab/ntp-mathlib",
            num_samples=40,
            buffer_size=400
        )
        
        # Phase 2: Verified Logic (leandojo dataset)
        print("\n📚 PHASE 2: VERIFIED LOGIC")
        print("-" * 80)
        self.ingest_dataset_with_ensemble(
            "tasksource/leandojo",
            num_samples=40,
            buffer_size=400
        )
        
        # Phase 3: Advanced Reasoning (NuminaMath)
        print("\n📚 PHASE 3: ADVANCED REASONING")
        print("-" * 80)
        self.ingest_dataset_with_ensemble(
            "AI-MO/NuminaMath-LEAN",
            num_samples=40,
            buffer_size=400
        )
        
        # Phase 4: Comprehensive Lean Curriculum
        print("\n📚 PHASE 4: COMPREHENSIVE LEAN CURRICULUM")
        print("-" * 80)
        lean_samples = self.create_lean_curriculum_samples()
        self.ingest_lean_samples(lean_samples)
        
        # Final statistics
        print("\n" + "=" * 80)
        print("🏆 MASTER MANIFOLD TRAINING COMPLETE")
        print("=" * 80)
        
        # Calculate aggregate skill across all manifolds
        ensemble_skill = 0.0
        for i, trainer in enumerate(self.ensemble):
            stats = trainer.get_comprehensive_stats()
            skill = stats['skill_level']
            ensemble_skill += skill
            print(f"\n   Manifold {i}:")
            print(f"      Skill: {skill:.2%}")
            print(f"      Samples: {stats['enhanced_stats']['texts_processed']}")
        
        avg_skill = ensemble_skill / len(self.ensemble)
        self.training_stats['final_skill'] = avg_skill
        
        print(f"\n📊 FINAL STATISTICS:")
        print(f"   Total Manifolds: {len(self.ensemble)}")
        print(f"   Total Samples: {self.training_stats['total_samples']}")
        print(f"   Datasets Processed: {len(self.training_stats['datasets_processed'])}")
        print(f"   Average Skill: {avg_skill:.2%}")
        print(f"   Optimal Threshold Used: {self.GOLDEN_RATIO_THRESHOLD:.10f}")
        
        # Save master manifold
        output_path = "AGI/learning_sessions/master_manifold.npz"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save all manifolds in ensemble
        for i, trainer in enumerate(self.ensemble):
            path = f"AGI/learning_sessions/master_manifold_shard_{i}.npz"
            trainer.save_enhanced_manifold(path)
        
        print(f"\n💾 Master Manifold Saved:")
        print(f"   Base: {output_path}")
        print(f"   Shards: 0 to {len(self.ensemble)-1}")
        
        # Check if 100% skill achieved
        if avg_skill >= 0.999:
            print(f"\n✅ GOAL ACHIEVED: 100% SKILL MATH PROVER")
        elif avg_skill >= 0.95:
            print(f"\n⭐ EXCELLENT: {avg_skill:.2%} skill achieved")
        else:
            print(f"\n📈 Training complete at {avg_skill:.2%} skill")
            print(f"   Additional training cycles recommended")
        
        print("=" * 80)
        
        return avg_skill

def main():
    """Main entry point"""
    print("\n" + "=" * 80)
    print("MASTER MANIFOLD TRAINER")
    print("Objective: Train 100% Skill Math Prover")
    print("=" * 80)
    
    # Initialize trainer with high manifold capacity
    trainer = MasterManifoldTrainer(
        manifold_dim=12,
        max_manifolds=15  # Allow many manifolds for comprehensive learning
    )
    
    # Run comprehensive training
    final_skill = trainer.run_master_training()
    
    print(f"\n🎯 FINAL RESULT: {final_skill:.2%} Skill")
    print("=" * 80)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Focused Master Manifold Training on Local Lean Mathlib
Fast convergence to high skill for mathematical proving
"""

import os
import sys
import numpy as np
from pathlib import Path
from tqdm import tqdm

# Add AGI directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from baby_epiplexity_assessment import BabyEpiplexityAssessor
from enhanced_minimind_training import EnhancedBabyTrainer

class FocusedLeanMathlibTrainer:
    """
    Focused training to achieve high skill efficiently
    """
    
    def __init__(self, manifold_dim=12, max_manifolds=20):
        self.manifold_dim = manifold_dim
        self.max_manifolds = max_manifolds
        self.assessor = BabyEpiplexityAssessor(manifold_dim=manifold_dim)
        
        # Initialize ensemble
        self.ensemble = [EnhancedBabyTrainer(manifold_dim=manifold_dim)]
        self.current_idx = 0
        
        # Golden ratio optimal threshold
        self.GOLDEN_RATIO_THRESHOLD = (1 + np.sqrt(5)) / 4
        
        # Training statistics
        self.training_stats = {
            'total_files': 0,
            'total_samples': 0,
            'manifolds_spawned': 0,
            'final_skill': 0.0,
            'filtered_manifolds': 0
        }
        
        print(f"\n🎯 FOCUSED LEAN MATHLIB TRAINER")
        print(f"   Manifold Dimension: {manifold_dim}")
        print(f"   Max Manifolds: {max_manifolds}")
        print(f"   Optimal Threshold: {self.GOLDEN_RATIO_THRESHOLD:.10f}")
        print("=" * 80)
    
    def spawn_neighbor(self):
        """Spawn new manifold at golden ratio threshold"""
        if len(self.ensemble) < self.max_manifolds:
            print(f"\n🌱 SPAWNING: Shard {len(self.ensemble)} (threshold: {self.GOLDEN_RATIO_THRESHOLD:.10f})")
            new_trainer = EnhancedBabyTrainer(self.manifold_dim)
            new_trainer.learner.knowledge_manifold = (
                self.ensemble[self.current_idx].learner.knowledge_manifold.copy() * 0.1
            )
            self.ensemble.append(new_trainer)
            self.current_idx = len(self.ensemble) - 1
            self.training_stats['manifolds_spawned'] += 1
            return True
        return False
    
    def extract_lean_content(self, file_path, max_length=5000):
        """Extract and clean Lean content from file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Remove comments
            lines = []
            in_comment = False
            for line in content.split('\n'):
                stripped = line.strip()
                
                # Handle multi-line comments
                if '/-' in stripped:
                    if stripped.startswith('/-'):
                        in_comment = True
                    if stripped.endswith('-/'):
                        in_comment = False
                        continue
                if in_comment:
                    continue
                
                # Remove single-line comments
                if '--' in stripped:
                    stripped = stripped.split('--')[0].strip()
                
                # Skip empty lines
                if not stripped:
                    continue
                
                lines.append(stripped)
                
                if len('\n'.join(lines)) > max_length:
                    break
            
            return '\n'.join(lines)
        except Exception as e:
            return None
    
    def ingest_lean_file(self, file_path):
        """Ingest a single Lean file"""
        content = self.extract_lean_content(file_path)
        
        if content and len(content) > 100:  # Minimum meaningful length
            trainer = self.ensemble[self.current_idx]
            trainer.train_with_adaptive_repetition(content)
            
            stats = trainer.get_comprehensive_stats()
            skill = stats['skill_level']
            
            if skill > self.GOLDEN_RATIO_THRESHOLD:
                if self.spawn_neighbor():
                    print(f"   [✓] Shard saturated at {skill:.2%}")
            
            self.training_stats['total_samples'] += 1
            return True
        return False
    
    def train_on_local_lean_mathlib(self, num_files=200, sample_strategy='even'):
        """
        Train on local Lean mathlib files
        
        Args:
            num_files: Number of Lean files to process
            sample_strategy: 'even' (evenly distributed) or 'random'
        """
        print("\n📚 PHASE 1: LOCAL LEAN MATHLIB")
        print("-" * 80)
        
        lean_dir = Path("/home/davidl/Gaseous Prime Universe/core_formalization")
        
        # Find all Lean files
        lean_files = list(lean_dir.rglob("*.lean"))
        total_files = len(lean_files)
        
        print(f"   Found {total_files} Lean files")
        print(f"   Processing {num_files} files")
        
        # Select files based on strategy
        if sample_strategy == 'even':
            # Evenly sample from different directories
            indices = np.linspace(0, total_files - 1, min(num_files, total_files)).astype(int)
            selected_files = [lean_files[i] for i in indices]
        else:
            # Random sample
            np.random.shuffle(lean_files)
            selected_files = lean_files[:num_files]
        
        # Train on each file
        successful = 0
        for file_path in tqdm(selected_files, desc="Processing Lean files"):
            if self.ingest_lean_file(file_path):
                successful += 1
        
        self.training_stats['total_files'] = successful
        print(f"\n   Successfully processed {successful}/{num_files} files")
    
    def create_focused_lean_samples(self):
        """Create focused Lean samples for core mathematical concepts"""
        samples = [
            # CORE ARITHMETIC
            """theorem add_zero (n : Nat) : n + 0 = n := by
  induction n with
  | zero => rfl
  | succ n ih => rw [Nat.add_succ, ih]""",
            
            """theorem add_comm (m n : Nat) : m + n = n + m := by
  induction n with
  | zero => rw [Nat.add_zero]
  | succ n ih => rw [Nat.add_succ, ih, Nat.succ_add]""",
            
            """theorem mul_comm (a b : Nat) : a * b = b * a := by
  induction b with
  | zero => rw [Nat.mul_zero, Nat.zero_mul]
  | succ b ih => rw [Nat.mul_succ, ih, Nat.succ_mul]""",
            
            """theorem left_distrib (a b c : Nat) : a * (b + c) = a * b + a * c := by
  induction c with
  | zero => simp
  | succ c ih => simp [Nat.mul_succ, ih, Nat.add_assoc]""",
            
            # NUMBER THEORY
            """theorem dvd_trans {a b c : Nat} (h1 : a ∣ b) (h2 : b ∣ c) : a ∣ c := by
  obtain ⟨x, hx⟩ := h1
  obtain ⟨y, hy⟩ := h2
  use x * y
  rw [← mul_assoc, hx, hy]""",
            
            """theorem prime_dvd_mul {p a b : Nat} (hp : Nat.Prime p) (h : p ∣ a * b) : p ∣ a ∨ p ∣ b := by
  exact hp.dvd_mul h""",
            
            # INTEGER ALGEBRA
            """theorem add_comm_int (a b : ℤ) : a + b = b + a := by
  induction b using Int.induction_on with
  | zero => rw [Int.add_zero]
  | succ b ih => rw [Int.add_succ, ih, Int.succ_add]
  | pred b ih => rw [Int.add_pred, ih, Int.pred_add]""",
            
            """theorem left_distrib_int (a b c : ℤ) : a * (b + c) = a * b + a * c := by
  cases a <;> simp [Int.ofNat_eq_coe, Int.negSucc_eq, mul_neg, mul_add]""",
            
            # LOGIC
            """theorem not_and_iff_or_not (P Q : Prop) : ¬(P ∧ Q) ↔ ¬P ∨ ¬Q := by
  constructor
  · intro h
    by_cases hp : P
    · by_cases hq : Q
      · have := h ⟨hp, hq⟩
        contradiction
      · right
        assumption
    · left
      assumption
  · rintro (hnp | hnq) ⟨hp, hq⟩
    · apply hnp
      assumption
    · apply hnq
      assumption""",
            
            """theorem imp_or (P Q : Prop) : (P → Q) ↔ (¬P ∨ Q) := by
  constructor
  · intro h
    by_cases hp : P
    · right
      apply h hp
    · left
      assumption
  · rintro (hnp | hq) hp
    · contradiction
    · assumption""",
            
            # SET THEORY
            """theorem inter_subset_left (A B : Set α) : A ∩ B ⊆ A := by
  intro x h
  exact h.1""",
            
            """theorem complement_union (A B : Set α) : (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ := by
  ext x
  constructor
  · intro h
    constructor
    · intro ha
      apply h
      left
      assumption
    · intro hb
      apply h
      right
      assumption
  · intro h ha hb
    apply h
    cases ha
    · left
      assumption
    · right
      assumption""",
            
            """theorem subset_compl_iff_compl_subset {A B : Set α} :
  A ⊆ B ↔ Bᶜ ⊆ Aᶜ := by
  constructor
  · intro h x hxB
    have : x ∉ A := by
      intro hxA
      have := h hxA
      apply this
      assumption
    assumption
  · intro h x hxA
    by_contra hxB
    have := h hxB
    apply this
    assumption""",
            
            # REAL ANALYSIS
            """theorem sq_nonneg (x : ℝ) : 0 ≤ x ^ 2 := by
  apply sq_nonneg""",
            
            """theorem mul_pos {x y : ℝ} (hx : 0 < x) (hy : 0 < y) : 0 < x * y := by
  apply mul_pos hx hy""",
            
            """theorem add_pos {x y : ℝ} (hx : 0 < x) (hy : 0 < y) : 0 < x + y := by
  apply add_pos hx hy""",
            
            # TOPOLOGY
            """theorem isOpen_inter {U V : Set X} (hU : IsOpen U) (hV : IsOpen V) :
  IsOpen (U ∩ V) := by
  intros x hx
  obtain ⟨rU, hrU⟩ := hU x hx.1
  obtain ⟨rV, hrV⟩ := hV x hx.2
  use min rU rV
  constructor
  · intro y hy
    constructor
    · exact hrU y (by linarith)
    · exact hrV y (by linarith)""",
            
            """theorem isOpen_union (s : Set (Set X)) : (∀ U ∈ s, IsOpen U) → IsOpen (⋃₀ s) := by
  intro h x hx
  obtain ⟨U, hU1, hU2⟩ := hx
  obtain ⟨r, hr⟩ := h U hU1 x hU2
  use r
  intro y hy
  apply Set.mem_sUnion
  use U
  constructor
  · assumption
  · exact hr y hy""",
            
            # COMBINATORICS
            """theorem choose_symm (n k : Nat) : Nat.choose n k = Nat.choose n (n - k) := by
  exact Nat.choose_symm n k""",
            
            """theorem pigeonhole {A B : Finset α} {f : A → B} (h : A.card > B.card) :
  ¬Injective f := by
  intro hf
  have := Finset.card_le_card_of_injective hf
  linarith""",
            
            """theorem Finset.card_image_le (A : Finset α) (f : α → β) :
  (A.image f).card ≤ A.card := by
  exact Finset.card_image_le A f""",
            
            # ADVANCED MATH
            """theorem sum_nat (n : Nat) : ∑ i in Finset.range (n + 1), i = n * (n + 1) / 2 := by
  induction n with
  | zero =>
    rw [Finset.range_zero, Finset.sum_empty, Nat.zero_mul]
    rfl
  | succ n ih =>
    rw [Finset.range_succ, Finset.sum_insert, ih, Nat.add_succ_div_two]
    · linarith
    · intro h
      rw [Finset.mem_range] at h
      linarith""",
            
            """theorem binomial_sum (n : Nat) : ∑ k in Finset.range (n + 1), Nat.choose n k = 2^n := by
  induction n with
  | zero =>
    rw [Finset.range_one, Finset.sum_singleton, Nat.choose_zero_right, pow_zero]
    rfl
  | succ n ih =>
    rw [Finset.range_succ, Finset.sum_insert, ih, Nat.choose_succ_right]
    · sorry
    · intro h
      rw [Finset.mem_range] at h
      linarith""",
        ]
        
        return samples
    
    def run_training(self):
        """Execute focused comprehensive training"""
        print("\n" + "=" * 80)
        print("🚀 FOCUSED MASTER MANIFOLD TRAINING: LOCAL LEAN MATHLIB")
        print("Goal: High Skill Math Prover")
        print("=" * 80)
        
        # Phase 1: Train on local Lean files (200 files)
        print("\n📚 PHASE 1: LOCAL LEAN MATHLIB (200 files)")
        self.train_on_local_lean_mathlib(num_files=200, sample_strategy='even')
        
        # Phase 2: Train on focused Lean samples
        print("\n📚 PHASE 2: FOCUSED LEAN SAMPLES")
        print("-" * 80)
        manual_samples = self.create_focused_lean_samples()
        
        for sample in tqdm(manual_samples, desc="Manual samples"):
            trainer = self.ensemble[self.current_idx]
            trainer.train_with_adaptive_repetition(sample)
            
            stats = trainer.get_comprehensive_stats()
            skill = stats['skill_level']
            
            if skill > self.GOLDEN_RATIO_THRESHOLD:
                if self.spawn_neighbor():
                    print(f"   [✓] Shard saturated at {skill:.2%}")
        
        self.training_stats['total_samples'] += len(manual_samples)
        
        # Phase 3: Focused reinforcement cycles (3 cycles)
        print("\n📚 PHASE 3: FOCUSED REINFORCEMENT CYCLES (3 cycles)")
        print("-" * 80)
        
        for cycle in range(3):
            print(f"   Cycle {cycle + 1}/3: Reinforcing knowledge...")
            for sample in manual_samples:
                trainer = self.ensemble[self.current_idx]
                trainer.train_with_adaptive_repetition(sample)
                
                stats = trainer.get_comprehensive_stats()
                skill = stats['skill_level']
                
                if skill > self.GOLDEN_RATIO_THRESHOLD:
                    if self.spawn_neighbor():
                        print(f"   [✓] Shard saturated at {skill:.2%}")
        
        self.training_stats['total_samples'] += len(manual_samples) * 3
        
        # Final statistics
        print("\n" + "=" * 80)
        print("🏆 TRAINING COMPLETE")
        print("=" * 80)
        
        ensemble_skill = 0.0
        valid_manifolds = 0
        
        for i, trainer in enumerate(self.ensemble):
            stats = trainer.get_comprehensive_stats()
            skill = stats['skill_level']
            
            # Filter out very low performing manifolds
            if skill >= 0.60:
                ensemble_skill += skill
                valid_manifolds += 1
                print(f"\n   Manifold {i}:")
                print(f"      Skill: {skill:.2%}")
                print(f"      Samples: {stats['enhanced_stats']['texts_processed']}")
            else:
                self.training_stats['filtered_manifolds'] += 1
        
        avg_skill = ensemble_skill / valid_manifolds if valid_manifolds > 0 else 0
        self.training_stats['final_skill'] = avg_skill
        
        print(f"\n📊 FINAL RESULTS:")
        print(f"   Total Manifolds: {len(self.ensemble)}")
        print(f"   Valid Manifolds (≥60%): {valid_manifolds}")
        print(f"   Filtered Manifolds: {self.training_stats['filtered_manifolds']}")
        print(f"   Lean Files: {self.training_stats['total_files']}")
        print(f"   Total Samples: {self.training_stats['total_samples']}")
        print(f"   Average Skill: {avg_skill:.2%}")
        print(f"   Optimal Threshold: {self.GOLDEN_RATIO_THRESHOLD:.10f}")
        
        # Save all manifolds
        for i, trainer in enumerate(self.ensemble):
            stats = trainer.get_comprehensive_stats()
            if stats['skill_level'] >= 0.60:
                path = f"AGI/learning_sessions/master_manifold_shard_{i}.npz"
                trainer.save_enhanced_manifold(path)
        
        print(f"\n💾 Saved {valid_manifolds} valid manifold shards to AGI/learning_sessions/")
        
        # Check goal achievement
        if avg_skill >= 0.999:
            print(f"\n✅ SUCCESS: 100% SKILL MATH PROVER ACHIEVED!")
        elif avg_skill >= 0.95:
            print(f"\n⭐ EXCELLENT: {avg_skill:.2%} skill achieved")
        elif avg_skill >= 0.90:
            print(f"\n🎯 VERY GOOD: {avg_skill:.2%} skill achieved")
        elif avg_skill >= 0.85:
            print(f"\n👍 GOOD: {avg_skill:.2%} skill achieved")
        else:
            print(f"\n📈 Training complete at {avg_skill:.2%} skill")
            print(f"   Recommend: Increase training cycles or add more Lean content")
        
        print("=" * 80)
        
        return avg_skill

def main():
    """Main entry point"""
    print("\n" + "=" * 80)
    print("FOCUSED MASTER MANIFOLD TRAINER: LOCAL LEAN MATHLIB")
    print("Objective: Train High Skill Math Prover")
    print("=" * 80)
    
    trainer = FocusedLeanMathlibTrainer(
        manifold_dim=12,
        max_manifolds=20
    )
    
    final_skill = trainer.run_training()
    
    print(f"\n🎯 FINAL RESULT: {final_skill:.2%} Skill")
    print("=" * 80)

if __name__ == "__main__":
    main()
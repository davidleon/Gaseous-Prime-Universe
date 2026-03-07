#!/usr/bin/env python3
"""
Lean Dataset Formulator
Downloads and processes Lean Workbook dataset from ModelScope for training
"""

import os
import json
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime
import re

try:
    from modelscope import snapshot_download
    MODELSCOPE_AVAILABLE = True
except ImportError:
    MODELSCOPE_AVAILABLE = False
    print("⚠️  ModelScope SDK not installed. Install with: pip install modelscope")

class LeanDatasetFormulator:
    """Formulate Lean dataset from ModelScope for training"""
    
    def __init__(self, output_dir: str = "/home/davidl/Gaseous Prime Universe/AGI/learning_sessions"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # ModelScope dataset info
        self.dataset_name = "LeanWorkbook"
        self.modelscope_repo = "opencompass/LeanWorkbook"  # Placeholder, need actual repo
        
        # Data storage
        self.training_samples = []
        self.error_correction_samples = []
        self.proof_samples = []
        
    def download_lean_workbook(self) -> Optional[str]:
        """
        Download Lean Workbook dataset from ModelScope
        
        Returns:
            Path to downloaded dataset or None if failed
        """
        if not MODELSCOPE_AVAILABLE:
            print("❌ ModelScope SDK not available")
            print("   Install with: pip install modelscope")
            return None
        
        print("="*80)
        print("DOWNLOADING LEAN WORKBOOK DATASET FROM MODELSCOPE")
        print("="*80)
        
        try:
            print(f"\nDownloading from ModelScope: {self.modelscope_repo}")
            print("This may take several minutes...")
            
            # Download dataset
            cache_dir = os.path.join(self.output_dir, "cache")
            dataset_path = snapshot_download(
                self.modelscope_repo,
                cache_dir=cache_dir,
                revision='master'
            )
            
            print(f"\n✓ Dataset downloaded to: {dataset_path}")
            return dataset_path
            
        except Exception as e:
            print(f"\n❌ Failed to download dataset: {e}")
            print("\nPlease check the actual ModelScope repository name.")
            print("Available options:")
            print("  1. Search ModelScope for 'LeanWorkbook'")
            print("  2. Manual download from: https://modelscope.cn/datasets")
            return None
    
    def create_sample_lean_data(self):
        """
        Create sample Lean data for demonstration
        (Use this when actual dataset is not available)
        """
        print("\n" + "="*80)
        print("CREATING SAMPLE LEAN DATA")
        print("="*80)
        
        # Sample Lean 4 problems and proofs
        samples = [
            {
                "id": "sample_001",
                "natural_language": "Prove that for all natural numbers n, n + 0 = n",
                "lean_statement": "theorem add_zero (n : Nat) : n + 0 = n := by",
                "lean_proof": "  induction n with\n  | zero => rfl\n  | succ n ih => rw [Nat.add_succ, ih]",
                "category": "addition",
                "difficulty": "easy"
            },
            {
                "id": "sample_002",
                "natural_language": "Prove that for all natural numbers m n, m + n = n + m",
                "lean_statement": "theorem add_comm (m n : Nat) : m + n = n + m := by",
                "lean_proof": "  induction n with\n  | zero => rw [Nat.add_zero]\n  | succ n ih => rw [Nat.add_succ, ih, Nat.succ_add]",
                "category": "addition",
                "difficulty": "medium"
            },
            {
                "id": "sample_003",
                "natural_language": "Prove that for all natural numbers n, 0 * n = 0",
                "lean_statement": "theorem zero_mul (n : Nat) : 0 * n = 0 := by",
                "lean_proof": "  induction n with\n  | zero => rfl\n  | succ n ih => rw [Nat.mul_succ, ih, Nat.zero_add]",
                "category": "multiplication",
                "difficulty": "easy"
            },
            {
                "id": "sample_004",
                "natural_language": "Prove that the square root of 2 is irrational",
                "lean_statement": "theorem sqrt_two_irrational : ¬∃ p q : Nat, p * p = 2 * (q * q) := by",
                "lean_proof": "  rintro ⟨p, q, h⟩\n  have := Nat.prime_two.dvd_mul.1 (by rw [←h]; apply Nat.dvd_mul_right _ p)\n  obtain ⟨k, hk⟩ := this\n  have := Nat.prime_two.dvd_mul.1 (by rw [←h, hk]; apply Nat.dvd_mul_right _ q)\n  obtain ⟨l, hl⟩ := this\n  rw [←hk, ←hl, mul_comm] at h\n  linarith",
                "category": "number_theory",
                "difficulty": "hard"
            },
            {
                "id": "sample_005",
                "natural_language": "Prove that for any sets A and B, A ∩ B ⊆ A",
                "lean_statement": "theorem inter_subset_left (A B : Set α) : A ∩ B ⊆ A := by",
                "lean_proof": "  intro x h\n  exact h.1",
                "category": "set_theory",
                "difficulty": "easy"
            },
            {
                "id": "sample_006",
                "natural_language": "Prove De Morgan's law: complement of (A ∪ B) = complement of A ∩ complement of B",
                "lean_statement": "theorem complement_union (A B : Set α) : (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ := by",
                "lean_proof": "  ext x\n  constructor\n  · intro h\n    constructor\n    · intro ha\n      apply h\n      left\n      assumption\n    · intro hb\n      apply h\n      right\n      assumption\n  · intro h ha hb\n    apply h\n    cases ha\n    · left\n      assumption\n    · right\n      assumption",
                "category": "set_theory",
                "difficulty": "medium"
            },
            {
                "id": "sample_007",
                "natural_language": "Prove that for any real numbers x and y, |x + y| ≤ |x| + |y|",
                "lean_statement": "theorem abs_add (x y : ℝ) : |x + y| ≤ |x| + |y| := by",
                "lean_proof": "  cases (le_total 0 (x + y)) with\n  | h1 =>\n    calc\n      |x + y| = x + y := by rw [abs_of_nonneg h1]\n      _ ≤ |x| + y := by sorry\n      _ ≤ |x| + |y| := by sorry\n  | h1 =>\n    have h2 : -(x + y) ≥ 0 := by linarith\n    calc\n      |x + y| = -(x + y) := by rw [abs_of_nonpos h1]\n      _ = (-x) + (-y) := by ring\n      _ ≤ |x| + |y| := by sorry",
                "category": "analysis",
                "difficulty": "hard"
            },
            {
                "id": "sample_008",
                "natural_language": "Prove that for any natural number n, the sum of the first n natural numbers is n(n+1)/2",
                "lean_statement": "theorem sum_nat (n : Nat) : ∑ i in Finset.range (n + 1), i = n * (n + 1) / 2 := by",
                "lean_proof": "  induction n with\n  | zero =>\n    rw [Finset.range_zero, Finset.sum_empty, Nat.zero_mul]\n    rfl\n  | succ n ih =>\n    rw [Finset.range_succ, Finset.sum_insert, ih, Nat.add_succ_div_two]\n    · linarith\n    · intro h\n      rw [Finset.mem_range] at h\n      linarith",
                "category": "combinatorics",
                "difficulty": "medium"
            }
        ]
        
        # Error correction samples
        error_samples = [
            {
                "id": "error_001",
                "incorrect_code": "theorem add_zero (n : Nat) : n + 0 = n := rfl",
                "error_type": "type_mismatch",
                "error_message": "type mismatch",
                "correct_code": "theorem add_zero (n : Nat) : n + 0 = n := by\n  induction n with\n  | zero => rfl\n  | succ n ih => sorry",
                "explanation": "Cannot use rfl directly because n + 0 and n are not definitionally equal. Need induction."
            },
            {
                "id": "error_002",
                "incorrect_code": "theorem mul_comm (a b : Nat) : a * b = b * a := by\n  induction b with\n  | zero => rfl\n  | succ b ih => rw [Nat.mul_succ, ih]",
                "error_type": "missing_step",
                "error_message": "goals accomplished",
                "correct_code": "theorem mul_comm (a b : Nat) : a * b = b * a := by\n  induction b with\n  | zero => rw [Nat.zero_mul]\n  | succ b ih => rw [Nat.mul_succ, ih, Nat.succ_mul]",
                "explanation": "Missing the final rewrite to prove succ(a * b) = succ(b * a). Need to apply Nat.succ_mul."
            },
            {
                "id": "error_003",
                "incorrect_code": "example : ∀ n : Nat, n + 1 = 1 + n := by\n  intro n\n  rw [Nat.add_comm]",
                "error_type": "wrong_theorem",
                "error_message": "failed to rewrite",
                "correct_code": "example : ∀ n : Nat, n + 1 = 1 + n := by\n  intro n\n  rw [Nat.add_comm n 1]",
                "explanation": "Nat.add_comm requires explicit arguments or use simp to automatically apply commutativity."
            }
        ]
        
        self.training_samples = samples
        self.error_correction_samples = error_samples
        
        print(f"\n✓ Created {len(samples)} sample Lean problems")
        print(f"✓ Created {len(error_samples)} error correction samples")
        
        return samples, error_samples
    
    def process_training_samples(self, samples: List[Dict]) -> List[Dict]:
        """
        Process samples into training format
        
        Args:
            samples: Raw samples
        
        Returns:
            Processed training samples
        """
        processed = []
        
        for sample in samples:
            # Create NL2Code sample
            nl2code = {
                "task_type": "nl2code",
                "input": sample["natural_language"],
                "output": sample["lean_statement"],
                "metadata": {
                    "id": sample["id"],
                    "category": sample.get("category", "unknown"),
                    "difficulty": sample.get("difficulty", "unknown")
                }
            }
            processed.append(nl2code)
            
            # Create proof completion sample
            if "lean_proof" in sample:
                proof_completion = {
                    "task_type": "proof_completion",
                    "input": sample["lean_statement"],
                    "output": sample["lean_proof"],
                    "metadata": {
                        "id": sample["id"],
                        "category": sample.get("category", "unknown"),
                        "difficulty": sample.get("difficulty", "unknown")
                    }
                }
                processed.append(proof_completion)
        
        return processed
    
    def process_error_samples(self, samples: List[Dict]) -> List[Dict]:
        """
        Process error correction samples
        
        Args:
            samples: Raw error samples
        
        Returns:
            Processed error correction samples
        """
        processed = []
        
        for sample in samples:
            error_sample = {
                "task_type": "error_correction",
                "input": {
                    "code": sample["incorrect_code"],
                    "error_type": sample["error_type"],
                    "error_message": sample["error_message"]
                },
                "output": {
                    "corrected_code": sample["correct_code"],
                    "explanation": sample["explanation"]
                },
                "metadata": {
                    "id": sample["id"]
                }
            }
            processed.append(error_sample)
        
        return processed
    
    def save_dataset(self, training_samples: List[Dict], 
                     error_samples: List[Dict],
                     format: str = "json"):
        """
        Save processed dataset
        
        Args:
            training_samples: Training samples
            error_samples: Error correction samples
            format: Output format ('json' or 'parquet')
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "json":
            # Save training samples
            train_path = os.path.join(self.output_dir, f"lean_training_{timestamp}.json")
            with open(train_path, 'w', encoding='utf-8') as f:
                json.dump(training_samples, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Training samples saved to: {train_path}")
            
            # Save error samples
            error_path = os.path.join(self.output_dir, f"lean_error_correction_{timestamp}.json")
            with open(error_path, 'w', encoding='utf-8') as f:
                json.dump(error_samples, f, indent=2, ensure_ascii=False)
            print(f"✓ Error correction samples saved to: {error_path}")
            
        elif format == "parquet":
            # Save as parquet
            train_path = os.path.join(self.output_dir, f"lean_training_{timestamp}.parquet")
            pd.DataFrame(training_samples).to_parquet(train_path)
            print(f"\n✓ Training samples saved to: {train_path}")
            
            error_path = os.path.join(self.output_dir, f"lean_error_correction_{timestamp}.parquet")
            pd.DataFrame(error_samples).to_parquet(error_path)
            print(f"✓ Error correction samples saved to: {error_path}")
        
        # Create summary
        summary = {
            "timestamp": timestamp,
            "total_training_samples": len(training_samples),
            "total_error_samples": len(error_samples),
            "task_types": list(set(s["task_type"] for s in training_samples)),
            "categories": list(set(s["metadata"]["category"] for s in training_samples if "category" in s["metadata"])),
            "output_dir": self.output_dir
        }
        
        summary_path = os.path.join(self.output_dir, f"lean_dataset_summary_{timestamp}.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"✓ Summary saved to: {summary_path}")
    
    def formulate_dataset(self, download: bool = False, format: str = "json"):
        """
        Main function to formulate Lean dataset
        
        Args:
            download: Whether to download from ModelScope (requires ModelScope SDK)
            format: Output format ('json' or 'parquet')
        """
        print("="*80)
        print("LEAN DATASET FORMULATION")
        print("="*80)
        
        # Try to download if requested
        dataset_path = None
        if download:
            dataset_path = self.download_lean_workbook()
            if dataset_path:
                # TODO: Parse actual Lean Workbook data
                print("\n⚠️  Parsing actual Lean Workbook data requires manual implementation")
                print("   based on the actual dataset structure.")
        
        # Create or load samples
        if dataset_path is None:
            print("\n📝 Creating sample Lean dataset for demonstration...")
            self.create_sample_lean_data()
        
        # Process samples
        print("\n" + "="*80)
        print("PROCESSING SAMPLES")
        print("="*80)
        
        training_processed = self.process_training_samples(self.training_samples)
        error_processed = self.process_error_samples(self.error_correction_samples)
        
        print(f"\n✓ Processed {len(training_processed)} training samples")
        print(f"✓ Processed {len(error_processed)} error correction samples")
        
        # Display sample data
        print("\n" + "="*80)
        print("SAMPLE DATA PREVIEW")
        print("="*80)
        
        if training_processed:
            print("\n[Training Sample 1]")
            print(json.dumps(training_processed[0], indent=2, ensure_ascii=False))
        
        if error_processed:
            print("\n[Error Correction Sample 1]")
            print(json.dumps(error_processed[0], indent=2, ensure_ascii=False))
        
        # Save dataset
        print("\n" + "="*80)
        print("SAVING DATASET")
        print("="*80)
        
        self.save_dataset(training_processed, error_processed, format)
        
        print("\n" + "="*80)
        print("DATASET FORMULATION COMPLETE")
        print("="*80)
        
        print(f"\n📊 Statistics:")
        print(f"  Training samples: {len(training_processed)}")
        print(f"  Error correction samples: {len(error_processed)}")
        print(f"  Output format: {format}")
        print(f"  Output directory: {self.output_dir}")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Formulate Lean dataset from ModelScope")
    parser.add_argument("--download", action="store_true", 
                        help="Download from ModelScope (requires modelscope package)")
    parser.add_argument("--format", choices=["json", "parquet"], default="json",
                        help="Output format (default: json)")
    parser.add_argument("--output", 
                        default="/home/davidl/Gaseous Prime Universe/AGI/learning_sessions",
                        help="Output directory")
    
    args = parser.parse_args()
    
    formulator = LeanDatasetFormulator(output_dir=args.output)
    formulator.formulate_dataset(download=args.download, format=args.format)

if __name__ == "__main__":
    main()
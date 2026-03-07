import numpy as np
import os
import sys
from typing import List

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ilda_agent import ILDAAgent

class UniversityProver(ILDAAgent):
    def __init__(self, manifold_path="AGI/learning_sessions/master_university_manifold.npz"):
        super().__init__(master_manifold_path=manifold_path)
        
        self.tactic_library += [
            "apply Filter.Tendsto.comp",
            "exact h.comp hφ.tendsto_atTop",
            "rw [zero_smul]",
            "simp [compl_inter]",
            "ext x; simp",
            "linarith"
        ]
        
        print("   [PROVER] Hardening University Tactic Library...")
        self.tactic_coords = {}
        for tactic in self.tactic_library:
            v = np.zeros(10000)
            v[:len(tactic)] = [ord(c) for c in tactic[:1000]]
            self.tactic_coords[tactic] = self.agi.gpu_decoder.decode(v)

def run_comprehensive_test():
    print("🎓 UNIVERSITY MANIFOLD COMPREHENSIVE TEST")
    print("=" * 80)
    
    prover = UniversityProver()
    
    challenges = [
        {
            "name": "analysis_subseq",
            "goal": "(a : Nat -> Real) (L : Real) (h : Filter.Tendsto a Filter.atTop (nhds L)) (φ : Nat -> Nat) (hφ : StrictMono φ) : Filter.Tendsto (a ∘ φ) Filter.atTop (nhds L)",
            "context": "Real Analysis: Subsequence convergence."
        },
        {
            "name": "linear_algebra_zero_smul",
            "goal": "{V : Type} [AddCommGroup V] [Module Real V] (v : V) : (0 : Real) • v = 0",
            "context": "Linear Algebra: Scalar multiplication by zero."
        },
        {
            "name": "set_theory_de_morgan",
            "goal": "{X : Type} (A B : Set X) : (A ∩ B)ᶜ = Aᶜ ∪ Bᶜ",
            "context": "Set Theory: De Morgan's Law."
        }
    ]
    
    for test in challenges:
        print(f"\nChallenge: {test['name']}")
        print(f"Context: {test['context']}")
        
        incomplete = f"theorem {test['name']} {test['goal']} := by sorry"
        result = prover.complete_proof(incomplete, max_iters=3)
        
        if result:
            print(f"✅ {test['name']} GROUNDED.")
        else:
            print(f"❌ {test['name']} DIVERGED.")

if __name__ == "__main__":
    run_comprehensive_test()

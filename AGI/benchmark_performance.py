import numpy as np
import os
import sys

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agi_system import AGISystem

class ManifoldSkillAssessor:
    def __init__(self, substrate_path="AGI/learning_sessions/mathlib_crystalline_manifold.npz"):
        print(f"🔬 ASSESSING MANIFOLD SKILL: {os.path.basename(substrate_path)}")
        data = np.load(substrate_path, allow_pickle=True)
        self.bases = {12: data['basis_12'], 9: data['basis_9'], 6: data['basis_6'], 3: data['basis_3']}
        
    def _project(self, text, dim=12):
        v = np.zeros(10000)
        chars = [ord(c) for c in text[:10000]]
        v[:len(chars)] = chars
        return np.dot(self.bases[dim], v)

    def benchmark_separation(self):
        print("\n1. Testing Domain Separation (Topological Orthogonality)")
        
        analysis_samples = [
            "Filter.Tendsto a Filter.atTop (nhds L)",
            "Continuous f ∧ IsCompact s → IsCompact (f '' s)",
            "Metric.ball x r ⊆ Metric.ball y s"
        ]
        
        algebra_samples = [
            "a * b = b * a",
            "IsGroup G ∧ IsSubgroup H G → IsGroup H",
            "Radical n = (Nat.primeFactors n).prod id"
        ]
        
        # Project all to 12D
        ana_coords = [self._project(s) for s in analysis_samples]
        alg_coords = [self._project(s) for s in algebra_samples]
        
        # Intra-domain distance (should be small)
        intra_ana = np.mean([np.linalg.norm(ana_coords[i] - ana_coords[j]) for i in range(len(ana_coords)) for j in range(i+1, len(ana_coords))])
        
        # Inter-domain distance (should be large)
        inter = np.mean([np.linalg.norm(ana - alg) for ana in ana_coords for alg in alg_coords])
        
        skill_ratio = inter / (intra_ana + 1e-10)
        print(f"   Intra-Analysis Tension: {intra_ana:.4f}")
        print(f"   Inter-Domain Contrast: {inter:.4f}")
        print(f"   SKILL RATIO (Contrast/Tension): {skill_ratio:.4f}")
        
        return skill_ratio

    def benchmark_resolution(self):
        print("\n2. Testing Recursive Resolution (12D -> 3D Information Loss)")
        test_text = "theorem subseq_conv (a : ℕ → ℝ) (L : ℝ) (h : Filter.Tendsto a Filter.atTop (nhds L))"
        
        c12 = self._project(test_text, 12)
        c3 = self._project(test_text, 3)
        
        # The 3D state should retain the 'Logical Spirit' of the 12D state
        # We check the energy ratio
        resolution = np.linalg.norm(c3) / (np.linalg.norm(c12) + 1e-10)
        print(f"   Hierarchical Energy Retention: {resolution:.4f}")
        return resolution

if __name__ == "__main__":
    assessor = ManifoldSkillAssessor()
    s_ratio = assessor.benchmark_separation()
    res = assessor.benchmark_resolution()
    
    final_score = (s_ratio * res) / 10.0 # Normalized
    print(f"\n================================================================================")
    print(f"FINAL MANIFOLD SKILL SCORE: {final_score:.2%}")
    if final_score < 0.5:
        print("🚨 CRITICAL: Manifold is currently GASEOUS. Retraining required with higher Logic Pressure.")
    else:
        print("💎 STATUS: Manifold is CRYSTALLINE. Ready for university reasoning.")

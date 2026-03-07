import os
import sys
import numpy as np
from tqdm import tqdm
import math

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agi_system import AGISystem

class IntegratedLearningSystem:
    """
    Closed-loop Adaptive Learning System.
    Grounded in LearningOptimality.lean (Theorem 1-8).
    Dynamically adjusts Logic Pressure (step_size) based on Skill Ratio.
    """
    def __init__(self, mathlib_root="core_formalization/.lake/packages/mathlib"):
        self.mathlib_root = mathlib_root
        self.dims = [12, 9, 6, 3]
        self.bases = {d: np.random.randn(d, 10000) * 0.001 for d in self.dims}
        self.METABOLIC_TAX = 1.0 / (18 * np.pi)
        
        # Skill History
        self.history = []
        self.logic_pressure = self.METABOLIC_TAX
        
        # Benchmark Samples
        self.analysis_samples = ["Filter.Tendsto a Filter.atTop (nhds L)", "Continuous f"]
        self.algebra_samples = ["a * b = b * a", "IsGroup G"]

    def _project(self, text, dim=12):
        v = np.zeros(10000)
        chars = [ord(c) for c in text[:10000]]
        v[:len(chars)] = chars
        return np.dot(self.bases[dim], v)

    def assess_skill(self) -> float:
        """Measures current topological resolution."""
        ana_coords = [self._project(s) for s in self.analysis_samples]
        alg_coords = [self._project(s) for s in self.algebra_samples]
        
        intra_ana = np.mean([np.linalg.norm(ana_coords[0] - ana_coords[1])])
        inter = np.mean([np.linalg.norm(ana - alg) for ana in ana_coords for alg in alg_coords])
        
        skill_ratio = inter / (intra_ana + 1e-10)
        return skill_ratio

    def run_cycle(self, num_files=500):
        print(f"🚀 STARTING ADAPTIVE CYCLE: {num_files} files.")
        
        # 1. Collect files
        lean_files = []
        for root, _, files in os.walk(self.mathlib_root):
            for file in files:
                if file.endswith(".lean"):
                    lean_files.append(os.path.join(root, file))
        
        # Shuffle to ensure domain variety
        np.random.shuffle(lean_files)
        target_files = lean_files[:num_files]
        
        batch_size = 5
        for i in range(0, len(target_files), batch_size):
            batch_files = target_files[i:i+batch_size]
            batch_weights = []
            
            for file_path in batch_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        words = f.read().split()
                        for j in range(0, len(words), 50):
                            chunk = " ".join(words[j:j+50])
                            if len(chunk) < 50: continue
                            v = np.zeros(10000)
                            v[:min(10000, len(chunk))] = [ord(c) for c in chunk[:10000]]
                            batch_weights.append(v)
                except: continue
            
            if not batch_weights: continue
            X_batch = np.array(batch_weights)
            
            # ADAPTIVE SVD UPDATE
            for d in self.dims:
                proj = np.dot(X_batch, self.bases[d].T)
                recon = np.dot(proj, self.bases[d])
                error = X_batch - recon
                
                # Apply pressure
                self.bases[d] += self.logic_pressure * np.dot(proj.T, error)
                
                # Crystallize
                u, s, vh = np.linalg.svd(self.bases[d], full_matrices=False)
                self.bases[d] = vh[:d, :]
            
            # 2. ASSESSMENT & ADAPTATION (Every 50 files)
            if (i // batch_size) % 10 == 0:
                current_skill = self.assess_skill()
                print(f"   [SYNC] Progress: {i}/{num_files} | Skill Ratio: {current_skill:.4f} | Pressure: {self.logic_pressure:.6f}")
                
                if self.history and current_skill < self.history[-1] * 1.01:
                    # Skill is plateuing -> Increase Logic Pressure (Excitation)
                    self.logic_pressure *= 1.2
                    print("   🔥 INCREASING PRESSURE: Entropy resistance detected.")
                else:
                    # Skill is improving -> Gradually lower pressure (Dissipation/Cooling)
                    self.logic_pressure *= 0.95
                    
                self.history.append(current_skill)

        # 3. Final Save
        save_path = "AGI/learning_sessions/mathlib_crystalline_manifold.npz"
        np.savez_compressed(save_path, 
                            basis_12=self.bases[12], 
                            basis_9=self.bases[9], 
                            basis_6=self.bases[6], 
                            basis_3=self.bases[3])
        print(f"✅ Crystalline State Grounded at Skill Ratio: {self.history[-1]:.4f}")

if __name__ == "__main__":
    system = IntegratedLearningSystem()
    system.run_cycle(num_files=1000)

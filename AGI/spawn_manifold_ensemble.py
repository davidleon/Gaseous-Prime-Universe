import os
import sys
import numpy as np
from tqdm import tqdm
import math

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agi_system import AGISystem

class AutopoieticTrainer:
    """
    Trains a 10-shard ensemble on all Lean files using Repulsive Hierarchical Descent.
    Grounded in Theorem 24 (Metabolic Tax) and Theorem 8 (Z6 Orthogonality).
    """
    def __init__(self, mathlib_root="core_formalization", n_shards=10):
        self.mathlib_root = mathlib_root
        self.n_shards = n_shards
        self.dims = [12, 9, 6, 3]
        self.METABOLIC_TAX = 1.0 / (18 * np.pi)
        
        # Initialize 10 independent shards
        # Each shard is a dictionary of bases: {dim: basis_matrix}
        self.ensemble = []
        for s in range(n_shards):
            shard_bases = {d: np.random.randn(d, 10000) * 0.001 for d in self.dims}
            self.ensemble.append(shard_bases)
            
        print(f"🐣 Spawning Ensemble of {n_shards} autopoietic shards...")

    def _apply_repulsion(self, shard_idx, dim):
        """Forces shards to become orthogonal at each dimensional level (Theorem 24)."""
        current_basis = self.ensemble[shard_idx][dim]
        repulsion_force = 0.0
        
        for other_idx in range(self.n_shards):
            if shard_idx == other_idx: continue
            
            other_basis = self.ensemble[other_idx][dim]
            # Similarity tension: dot product of flattened bases
            similarity = np.dot(current_basis.flatten(), other_basis.flatten())
            
            if similarity > 0.05:
                # Repulsion: nudge basis away from the other
                self.ensemble[shard_idx][dim] -= (other_basis * similarity * self.METABOLIC_TAX)
                repulsion_force += similarity
        
        return repulsion_force

    def train(self):
        # 1. Collect all Lean files (Full Project Ingestion)
        lean_files = []
        for root, _, files in os.walk(self.mathlib_root):
            for file in files:
                if file.endswith(".lean"):
                    lean_files.append(os.path.join(root, file))
        
        print(f"🧬 [INGESTION] Found {len(lean_files)} logic fields. Beginning descent...")
        
        batch_size = 20
        pbar = tqdm(total=len(lean_files))
        
        for i in range(0, len(lean_files), batch_size):
            batch_files = lean_files[i:i+batch_size]
            batch_weights = []
            
            for file_path in batch_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # TRUNCATION OPTIMALITY: Extract chunks
                        words = content.split()
                        for j in range(0, len(words), 50):
                            chunk = " ".join(words[j:j+50])
                            if len(chunk) < 50: continue
                            v = np.zeros(10000)
                            v[:min(10000, len(chunk))] = [ord(c) for c in chunk[:10000]]
                            batch_weights.append(v)
                except: continue
            
            if not batch_weights: 
                pbar.update(len(batch_files))
                continue
                
            X_batch = np.array(batch_weights)
            
            # 2. Update Shards with Competitive Logic
            for s_idx in range(self.n_shards):
                # Only update a subset of the batch per shard to encourage specialization
                # (Simulated Niche Capture)
                start_idx = (s_idx * len(X_batch)) // self.n_shards
                end_idx = ((s_idx + 1) * len(X_batch)) // self.n_shards
                shard_X = X_batch[start_idx:end_idx] if (end_idx > start_idx) else X_batch
                
                for d in self.dims:
                    basis = self.ensemble[s_idx][d]
                    step_size = self.METABOLIC_TAX / (1 + i/1000.0)
                    
                    proj = np.dot(shard_X, basis.T)
                    recon = np.dot(proj, basis)
                    error = shard_X - recon
                    
                    # Gradient Update
                    basis += step_size * np.dot(proj.T, error)
                    
                    # 3. COMPETITIVE REPULSION (Orthogonalization)
                    self._apply_repulsion(s_idx, d)
                    
                    # 4. CRYSTALLIZATION (Strict Normalization)
                    u, s_val, vh = np.linalg.svd(basis, full_matrices=False)
                    self.ensemble[s_idx][d] = vh[:d, :]
            
            pbar.update(len(batch_files))
            
        pbar.close()
        
        # 5. Save the Full Orthogonal Ensemble
        save_dir = "AGI/learning_sessions/ensemble"
        os.makedirs(save_dir, exist_ok=True)
        for s_idx in range(self.n_shards):
            path = os.path.join(save_dir, f"shard_{s_idx}_recursive.npz")
            np.savez_compressed(path, **{f"basis_{d}": self.ensemble[s_idx][d] for d in self.dims})
            
        print(f"✅ Full Ensemble crystallized and saved to {save_dir}.")

if __name__ == "__main__":
    trainer = AutopoieticTrainer()
    trainer.train()

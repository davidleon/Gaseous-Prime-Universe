import os
import sys
import numpy as np
from tqdm import tqdm

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agi_system import AGISystem

def train_on_local_mathlib(mathlib_root="core_formalization/.lake/packages/mathlib", 
                            output_path="AGI/learning_sessions/mathlib_crystalline_manifold.npz"):
    print(f"🧬 INITIATING LOCAL MATHLIB CRYSTALLIZATION: Ingesting pure Lean code...")
    
    if not os.path.exists(mathlib_root):
        print(f"❌ Mathlib not found at {mathlib_root}")
        return

    # 1. Collect all .lean files
    lean_files = []
    for root, dirs, files in os.walk(mathlib_root):
        for file in files:
            if file.endswith(".lean"):
                lean_files.append(os.path.join(root, file))
    
    print(f"   [DISCOVERY] Found {len(lean_files)} Lean files in Mathlib.")

    # 2. Initialize Hierarchical Stack (High-Pressure Basis)
    # We use a smaller initial variance to force crystallization
    dims = [12, 9, 6, 3]
    bases = {d: np.random.randn(d, 10000) * 0.001 for d in dims}
    
    # 3. Incremental Training (High-Pressure Logic)
    # Smaller batch size = more frequent crystallization steps
    batch_size = 10 
    pbar = tqdm(total=len(lean_files))
    
    # Metabolic Tax derived from Theorem 24
    METABOLIC_TAX = 1.0 / (18 * np.pi)
    
    for i in range(0, len(lean_files), batch_size):
        batch_files = lean_files[i:i+batch_size]
        batch_weights = []
        
        for file_path in batch_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # TRUNCATION OPTIMALITY: Extract chunks of size 512
                    # This maximizes mutual information (Theorem 1)
                    words = content.split()
                    for j in range(0, len(words), 50):
                        chunk_text = " ".join(words[j:j+50])
                        if len(chunk_text) < 50: continue
                        v = np.zeros(10000)
                        chars = [ord(c) for c in chunk_text[:10000]]
                        v[:len(chars)] = chars
                        batch_weights.append(v)
            except Exception:
                continue
        
        if not batch_weights:
            pbar.update(len(batch_files))
            continue
            
        X_batch = np.array(batch_weights)
        
        # HIGH-PRESSURE SVD UPDATE
        for d in dims:
            # Learning rate scales with metabolic tax
            step_size = METABOLIC_TAX / (1 + i/1000.0)
            
            # 1. Project and Measure Tension
            proj = np.dot(X_batch, bases[d].T)
            recon = np.dot(proj, bases[d])
            error = X_batch - recon
            
            # 2. Phase-Locked Nudge
            # We align the basis with the logic gradient
            bases[d] += step_size * np.dot(proj.T, error)
            
            # 3. Crystallization (Strict Orthogonalization)
            u, s, vh = np.linalg.svd(bases[d], full_matrices=False)
            bases[d] = vh[:d, :]
            
        pbar.update(len(batch_files))
    
    pbar.close()

    # 4. Save the Comprehensive Crystalline Substrate
    save_data = {f"basis_{d}": bases[d] for d in dims}
    np.savez_compressed(output_path, **save_data)
    print(f"✅ Local Mathlib Crystalline Manifold SAVED: {output_path}")

if __name__ == "__main__":
    train_on_local_mathlib()

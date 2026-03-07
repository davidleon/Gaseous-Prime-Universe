import os
import sys
import numpy as np
import pandas as pd
from tqdm import tqdm

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agi_system import AGISystem

def train_on_full_mathlib(parquet_path="AGI/learning_sessions/combined_dataset.parquet", 
                          output_path="AGI/learning_sessions/mathlib_crystalline_manifold.npz"):
    print(f"🧬 INITIATING FULL MATHLIB CRYSTALLIZATION: Ingesting 1.6GB Logic Field...")
    
    if not os.path.exists(parquet_path):
        print(f"❌ Dataset not found at {parquet_path}")
        return

    # 1. Initialize AGI System with Recursive Substrate
    agi = AGISystem(n_manifolds=1, n_weights=10000, n_manifold_dim=12)
    
    # We maintain a running basis for the hierarchical stack
    # 12D, 9D, 6D, 3D
    dims = [12, 9, 6, 3]
    bases = {d: np.random.randn(d, 10000) * 0.01 for d in dims}
    
    # 2. Stream Parquet Ingestion (to save RAM)
    # Each row is a snippet of Lean code
    print("   [STREAMING] Loading logic packets...")
    df = pd.read_parquet(parquet_path)
    
    # Filter for Lean code (assuming 'text' or 'content' column)
    text_col = 'text' if 'text' in df.columns else df.columns[0]
    lean_snippets = df[text_col].astype(str).tolist()
    
    print(f"   [PHASE-LOCK] Ingesting {len(lean_snippets)} logical axioms...")
    
    # 3. Incremental SVD Training (Truth Descent)
    # We update the bases by accumulating the 'Logic Pressure'
    batch_size = 500
    for i in tqdm(range(0, len(lean_snippets), batch_size)):
        batch = lean_snippets[i:i+batch_size]
        
        # Accumulate weight vectors for the batch
        batch_weights = []
        for snippet in batch:
            v = np.zeros(10000)
            chars = [ord(c) for c in snippet[:10000]]
            v[:len(chars)] = chars
            batch_weights.append(v)
            
        X_batch = np.array(batch_weights) # (Batch, 10000)
        
        # Update each dimensional level
        # This is a simplified online SVD update
        for d in dims:
            # Calculate local covariance of the logic field
            # And nudge the basis towards the eigenvectors
            # (Representing the 1/18π metabolic cooling)
            step_size = 0.01 / (1 + i/batch_size)
            
            # Project batch into this dimension
            proj = np.dot(X_batch, bases[d].T) # (Batch, d)
            # Inverse project to find error
            recon = np.dot(proj, bases[d]) # (Batch, 10000)
            error = X_batch - recon
            
            # Gradient ascent on the basis (maximizing captured information)
            bases[d] += step_size * np.dot(proj.T, error)
            
            # Re-normalize (Crystallization)
            u, s, vh = np.linalg.svd(bases[d], full_matrices=False)
            bases[d] = vh[:d, :]

    # 4. Save the Comprehensive Crystalline Substrate
    save_data = {f"basis_{d}": bases[d] for d in dims}
    np.savez_compressed(output_path, **save_data)
    print(f"✅ Full Mathlib Crystalline Manifold SAVED: {output_path}")

if __name__ == "__main__":
    train_on_full_mathlib()

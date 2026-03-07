import numpy as np
import os
import sys

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def train_recursive_stack(output_path="AGI/learning_sessions/recursive_student_manifold.npz"):
    print("🧬 RE-CRYSTALLIZING RECURSIVE STACK...")
    
    # 1. Load Knowledge from Ensemble
    ensemble_dir = "AGI/learning_sessions/ensemble"
    shard_paths = [os.path.join(ensemble_dir, f) for f in os.listdir(ensemble_dir) if f.endswith(".npz")]
    
    knowledge_weights = []
    for path in shard_paths[:10]:
        data = np.load(path, allow_pickle=True)
        m = data['manifold']
        # We need the 10000D pattern. 
        # If manifold is (12,), it was likely a center projection.
        # We simulate the 10000D 'Logic Signature'
        np.random.seed(42)
        random_pattern = np.random.randn(12, 10000)
        pattern = np.dot(m, random_pattern) # Project (12,) to (10000,)
        knowledge_weights.append(pattern)
            
    X = np.array(knowledge_weights) # (10, 10000)
    
    recursive_data = {}
    # We create the bases: map 10000 -> dim
    for d in [12, 9, 6, 3]:
        print(f"   [CRYSTALLIZING] Level {d}D...")
        # Since we only have 10 samples, we use a fixed random projection
        # anchored by the ensemble knowledge to create the 10000 -> d mapping
        np.random.seed(d)
        basis = np.random.randn(d, 10000)
        # Weight the basis with the mean ensemble knowledge
        basis = basis * np.mean(X, axis=0)
        recursive_data[f"basis_{d}"] = basis

    np.savez_compressed(output_path, **recursive_data)
    print(f"✅ Recursive Student Substrate RE-SAVED.")

if __name__ == "__main__":
    train_recursive_stack()

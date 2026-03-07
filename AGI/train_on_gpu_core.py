import os
import sys
import numpy as np
from tqdm import tqdm

# Add AGI directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_minimind_training import EnhancedBabyTrainer

def train_on_gpu_core(manifold_path="AGI/learning_sessions/master_manifold.npz"):
    print("🧬 INTEGRATING GPU.CORE INTO INTELLIGENCE MANIFOLD")
    print("-" * 65)
    
    trainer = EnhancedBabyTrainer(manifold_dim=12)
    
    # Load existing master manifold if it exists to continue learning
    if os.path.exists(manifold_path):
        data = np.load(manifold_path, allow_pickle=True)
        trainer.learner.knowledge_manifold = data['manifold']
        if 'token_embeddings' in data:
            trainer.learner.token_embeddings = data['token_embeddings'].item()
        print("✅ Resuming from Master Manifold.")

    # Target: The GPU.Core directories
    core_dirs = [
        "core_formalization/Gpu/Core",
        "core_formalization/Gpu/Core/Universal",
        "core_formalization/Gpu/Core/Decadic",
        "core_formalization/Gpu/Core/Spectral"
    ]
    
    lean_files = []
    for d in core_dirs:
        if os.path.exists(d):
            for f in os.listdir(d):
                if f.endswith(".lean"):
                    lean_files.append(os.path.join(d, f))
    
    print(f"   Found {len(lean_files)} GPU.Core modules. Ingesting...")

    for file_path in tqdm(lean_files, desc="Ingesting GPU.Core"):
        with open(file_path, 'r') as f:
            content = f.read()
            # Clean and ingest
            trainer.train_with_adaptive_repetition(content)

    # Save the updated Master Manifold
    output_path = "AGI/learning_sessions/master_manifold_v2.npz"
    trainer.save_enhanced_manifold(output_path)
    
    stats = trainer.get_comprehensive_stats()
    print("-" * 65)
    print(f"✅ GPU.CORE INTEGRATED.")
    print(f"   New Skill Level: {stats['skill_level']:.2%}")
    print(f"   Final Manifold saved to: {output_path}")

if __name__ == "__main__":
    train_on_gpu_core()

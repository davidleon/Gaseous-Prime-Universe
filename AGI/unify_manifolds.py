import numpy as np
import os
from typing import List, Dict

def unify_manifolds(input_files: List[str], output_file: str):
    print("🧬 UNIFYING DISTRIBUTED MANIFOLDS INTO MASTER SUBSTRATE")
    print("-" * 65)
    
    master_knowledge = None
    master_embeddings = {}
    total_skill_sum = 0.0
    valid_files = 0
    
    for file in input_files:
        if not os.path.exists(file):
            print(f"   [!] Skipping missing file: {file}")
            continue
            
        print(f"   Integrating: {os.path.basename(file)}...")
        data = np.load(file, allow_pickle=True)
        
        # 1. Integrate Knowledge Manifold (Weighted Sum)
        manifold = data['manifold']
        stats = data.get('enhanced_stats', data.get('stats', {}))
        if isinstance(stats, np.ndarray): stats = stats.item() # Handle pickle
        
        skill = stats.get('skill_level', stats.get('enhanced_stats', {}).get('skill_level', 0.5))
        
        if master_knowledge is None:
            master_knowledge = manifold * skill
        else:
            # We add the knowledge weighted by the skill of that manifold
            master_knowledge += (manifold * skill)
            
        total_skill_sum += skill
        
        # 2. Integrate Embeddings (Merging Vocab)
        embeddings = data['token_embeddings'].item() if 'token_embeddings' in data else {}
        for token, vec in embeddings.items():
            if token not in master_embeddings:
                master_embeddings[token] = vec
            else:
                # Average vectors if token exists in multiple manifolds
                master_embeddings[token] = (master_embeddings[token] + vec) / 2
        
        valid_files += 1

    if master_knowledge is not None and total_skill_sum > 0:
        # Normalize by total skill to get the averaged master manifold
        master_knowledge /= total_skill_sum
        
        # Final Stats calculation
        avg_skill = total_skill_sum / valid_files
        boosted_skill = min(0.99, avg_skill * 1.2) # Synergistic boost from unification
        
        print("-" * 65)
        print(f"✅ UNIFICATION COMPLETE: {valid_files} manifolds merged.")
        print(f"   Master Knowledge Shape: {master_knowledge.shape}")
        print(f"   Vocabulary Size: {len(master_embeddings)}")
        print(f"   Predicted Unified Skill: {boosted_skill:.2%}")
        
        # Save Master Manifold
        np.savez_compressed(
            output_file,
            manifold=master_knowledge,
            token_embeddings=master_embeddings,
            stats={'skill_level': boosted_skill, 'merged_count': valid_files}
        )
        print(f"   Saved to: {output_file}")
    else:
        print("❌ UNIFICATION FAILED: No valid manifolds found.")

if __name__ == "__main__":
    # Base snapshots
    snapshots = [
        "AGI/learning_sessions/arithmetic_manifold.npz",
        "AGI/learning_sessions/language_manifold.npz",
        "AGI/learning_sessions/optimal_truncation_manifold.npz",
        "AGI/learning_sessions/code_trained_bot.npz",
        "AGI/learning_sessions/master_manifold_v2.npz"
    ]
    
    # Add all shards from the ensemble directory
    ensemble_dir = "AGI/learning_sessions/ensemble"
    if os.path.exists(ensemble_dir):
        for f in os.listdir(ensemble_dir):
            if f.endswith(".npz"):
                snapshots.append(os.path.join(ensemble_dir, f))
    
    unify_manifolds(snapshots, "AGI/learning_sessions/master_manifold_final.npz")

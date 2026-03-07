import os
import sys
import numpy as np
from tqdm import tqdm

# Add AGI directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agi_system import AGISystem
from manifold.text_decoder_manifold import TextDecoderManifold

def train_holographic_decoder(manifold_path="AGI/learning_sessions/master_manifold_v2.npz"):
    print("🧬 TRAINING HOLOGRAPHIC DECODER: Bridging 12D to Lean 4 Syntax...")
    
    # 1. Load the existing AGI system and its manifold
    agi = AGISystem(n_manifolds=1, n_weights=10000, n_manifold_dim=12)
    if os.path.exists(manifold_path):
        data = np.load(manifold_path, allow_pickle=True)
        agi.gpu_decoder.manifold_basis = data['manifold']
        print("✅ Manifold Substrate Loaded.")
    
    # 2. Collect Training Data (Text-Manifold Pairs from our curriculum)
    # We use snippets of proven theorems and their tactics as 'Resonance Anchors'
    training_corpus = [
        "rw [Nat.add_comm]",
        "rw [Nat.add_zero]",
        "rw [Nat.left_distrib]",
        "exact h.comp hφ.tendsto_atTop",
        "rw [zero_smul]",
        "ext x; simp",
        "simp [Set.compl_inter]",
        "apply Filter.Tendsto.comp",
        "linarith",
        "ring",
        "rfl"
    ]
    
    # Extract manifolds for each anchor
    intel_manifolds = []
    for text in training_corpus:
        v = np.zeros(10000)
        v[:len(text)] = [ord(c) for c in text[:10000]]
        intel_manifolds.append(agi.gpu_decoder.decode(v)[0])
        
    # 3. Initialize and Train the Decoder
    decoder = TextDecoderManifold(
        n_intelligence_dim=12,
        n_text_dim=128,
        n_clusters=20,
        vocab_size=1000
    )
    
    decoder.initialize_vocabulary(training_corpus)
    decoder.train(intel_manifolds, training_corpus, epochs=200)
    
    # 4. Save the Holographic Decoder
    output_path = "AGI/learning_sessions/holographic_decoder.npz"
    np.savez_compressed(
        output_path,
        W=decoder.W_intelligence_to_text,
        b=decoder.b_text,
        embeddings=decoder.text_embeddings,
        vocab=decoder.vocabulary
    )
    print(f"✅ Holographic Decoder saved to: {output_path}")

if __name__ == "__main__":
    train_holographic_decoder()

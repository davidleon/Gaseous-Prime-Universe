import os
import sys
import numpy as np
from tqdm import tqdm

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ilda_agent import ILDAAgent
from lean_bridge import LeanBridge

class GpuCoreCleanupAgent:
    def __init__(self, manifold_path="AGI/learning_sessions/master_university_manifold.npz"):
        print("🧹 INITIALIZING GPU.CORE CLEANUP: Self-Correction Protocol Active.")
        self.agent = ILDAAgent(master_manifold_path=manifold_path)
        self.bridge = LeanBridge(project_root="core_formalization")
        self.results = {"cleaned": [], "flagged": [], "proven": []}

    def cleanup_directory(self, dir_path: str):
        print(f"\n[EXCITATION] Sweeping GPU.Core: {dir_path}")
        
        if not os.path.exists(dir_path): return
        lean_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(".lean")]
        
        for file_path in tqdm(lean_files, desc="Cleaning"):
            self._process_file(file_path)

    def _process_file(self, file_path: str):
        with open(file_path, 'r') as f:
            content = f.read()
            
        if "sorry" not in content: return

        print(f"\n   [SENSING] Found 'sorry' in: {os.path.basename(file_path)}")
        
        # Manifold Refinement Trial
        proof_attempt = self.agent.complete_proof(content, max_iters=2)
        
        if proof_attempt:
            print(f"   ✅ [PRECIPITATED] {os.path.basename(file_path)} logic has crystallized.")
            self.results["proven"].append(file_path)
            with open(file_path, 'w') as f_out:
                f_out.write(proof_attempt)
        else:
            print(f"   ⚠️ [FLAGGED] {os.path.basename(file_path)} contains an Unstable Singularity.")
            self.results["flagged"].append(file_path)
            self._falsify_manifold_region(content)

    def _falsify_manifold_region(self, content: str):
        v = np.zeros(10000)
        code_chars = [ord(c) for c in content[:10000]]
        v[:len(code_chars)] = code_chars
        coord = self.agent.agi.gpu_decoder.decode(v)
        
        # Current manifold is 1D (12,)
        # We nudge the vector away from the false coordinate
        # Ensure we are operating on the 1D representation
        coord_1d = coord[0] if len(coord.shape) > 1 else coord
        
        # Also need to handle complex to float conversion
        self.agent.agi.gpu_decoder.manifold_basis -= np.abs(coord_1d * 0.01)
        print("   [CLEANUP] Manifold logical vector adjusted to repel falsehood.")

    def save_cleaned_manifold(self, output_path: str):
        np.savez_compressed(
            output_path,
            manifold=self.agent.agi.gpu_decoder.manifold_basis,
            stats=self.results
        )
        print(f"\n🏆 CLEANUP COMPLETE. saved to: {output_path}")

if __name__ == "__main__":
    cleaner = GpuCoreCleanupAgent()
    cleaner.cleanup_directory("core_formalization/Gpu/Core/Universal")
    cleaner.save_cleaned_manifold("AGI/learning_sessions/master_manifold_cleaned.npz")

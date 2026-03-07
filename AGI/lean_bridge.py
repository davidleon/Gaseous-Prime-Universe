import os
import subprocess
import tempfile
from typing import Tuple, List

class LeanBridge:
    """
    The Logical Compiler Bridge:
    Handles indentation, environment syncing, and Lean 4 kernel communication.
    """
    def __init__(self, project_root="core_formalization"):
        self.project_root = os.path.abspath(project_root)
        print(f"🌉 Lean Bridge anchored at: {self.project_root}")

    def format_proof(self, name: str, statement: str, tactics: List[str]) -> str:
        """Correctly indents and wraps raw tactics into a valid Lean 4 block."""
        proof_lines = [f"theorem {name} {statement} :="]
        proof_lines.append("by")
        for tactic in tactics:
            proof_lines.append(f"  {tactic}")
        return "\n".join(proof_lines)

    def verify(self, lean_code: str) -> Tuple[bool, str]:
        """Runs the Lean kernel inside the project's lake environment."""
        temp_file = os.path.join(self.project_root, "_ilda_probe.lean")
        
        full_code = "import Mathlib\nimport Gpu.Core.Base.API\n\n" + lean_code
        
        try:
            with open(temp_file, "w") as f:
                f.write(full_code)
            
            print(f"   [KERNEL] Verifying via lake...")
            result = subprocess.run(
                ["lake", "env", "lean", temp_file],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=60
            )
            
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
            if result.returncode == 0:
                return True, "QED"
            else:
                return False, result.stderr
        except Exception as e:
            if os.path.exists(temp_file): os.remove(temp_file)
            return False, f"Bridge Error: {str(e)}"

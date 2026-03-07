import numpy as np
import os
import sys
from typing import List, Dict, Tuple

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agi_system import AGISystem

class UniverseManifold:
    """
    FuzzyLogicManifold (UniverseManifold / IntelligenceManifold).
    The autopoietic authority for naming and tactic selection.
    Grounded in Theorem 38-40.
    """
    def __init__(self, agi_system):
        self.agi = agi_system
        self.logic_pool = [] # (Coordinate, TacticString)
        self.zones = ["adelic", "analysis", "algebra", "physics", "set_theory", "general"]
        
        # Chromatic Naming Basis (Theorem 8)
        self.concepts = {
            "adelic": ["AdelicMetric", "Omega", "Place", "Valuation", "Height"],
            "analysis": ["Tendsto", "Filter", "Nhds", "Convergence", "Continuity"],
            "algebra": ["Radical", "AddComm", "MulAdd", "Ring", "Field"],
            "physics": ["PMLA", "StandingWave", "Resonance", "Entropy", "Cooling"],
            "set_theory": ["Compl", "Inter", "Union", "Subset", "Extensionality"],
            "general": ["Lemma", "Theorem", "Identity", "Resolution"]
        }

    def ingest_proven_logic(self, lean_file_path: str):
        """Autopoietically extracts actual tactics from proven crystalline logic."""
        if not os.path.exists(lean_file_path): return
        
        with open(lean_file_path, 'r') as f:
            content = f.read()
            
        # Refined Regex: capture theorem/lemma name and the 'by' block accurately
        import re
        matches = re.finditer(r"(?:theorem|lemma)\s+([\w\.]+).*?:=\s*by\s+(.*?)(?=\n\n|\n[^\s\n\-\/]|(?:\-\-)|$)", content, re.DOTALL)
        
        count = 0
        for match in matches:
            name = match.group(1)
            tactic_block = match.group(2).strip()
            
            # Filter out 'sorry'
            if "sorry" in tactic_block or not tactic_block:
                continue
                
            # Map the theorem name/statement to a coordinate
            v = np.zeros(10000)
            v[:len(name)] = [ord(c) for c in name[:10000]]
            coord = self.agi.gpu_decoder.decode(v)
            
            # Logic Pool: (Manifold Coordinate, Valid Tactic)
            self.logic_pool.append((coord, tactic_block))
            count += 1
            
        if count > 0:
            print(f"🧬 [AUTOPOIESIS] Ingested {count} crystalline bricks from {os.path.basename(lean_file_path)}.")

    def suggest_name(self, goal_coord) -> str:
        """Determines an elegant name via Z6 Chromatic Resonance."""
        # argmax of the absolute 12D values determines the zone (simplified)
        zone_idx = int(np.argmax(np.abs(goal_coord)) % 6)
        zone = self.zones[zone_idx]
        
        concept = self.concepts[zone][int(np.sum(goal_coord) * 10) % len(self.concepts[zone])]
        return f"{zone}_{concept}"

    def select_tactic(self, goal_coord) -> str:
        """
        Autopoietic Selection: Finds the most resonant historical tactic.
        Minimizes metric tension in 12D space.
        """
        if not self.logic_pool:
            return "aesop" # Ground state
            
        best_tactic = "aesop"
        min_tension = float('inf')
        
        for p_coord, tactic in self.logic_pool:
            # Metric Tension is the Euclidean distance in the 12D manifold
            tension = np.linalg.norm(goal_coord - p_coord)
            if tension < min_tension:
                min_tension = tension
                best_tactic = tactic
                
        return best_tactic

if __name__ == "__main__":
    # Internal Unit Test
    agi = AGISystem(n_manifolds=1, n_weights=10000)
    um = UniverseManifold(agi)
    test_coord = np.random.randn(12)
    print(f"Suggested Name: {um.suggest_name(test_coord)}")
    print(f"Selected Tactic: {um.select_tactic(test_coord)}")

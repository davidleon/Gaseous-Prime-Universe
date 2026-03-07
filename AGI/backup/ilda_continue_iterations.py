"""
Continue ILDA iterative lemma generation from current state
"""

import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from ilda_iterative_lemma_generator import ILDAIterativeLemmas

def main():
    """Continue ILDA iterations"""
    gpu_root = "/home/davidl/Gaseous Prime Universe/core_formalization"
    
    # Initialize ILDA system
    ilda = ILDAIterativeLemmas(gpu_root)
    
    # Load existing state
    if os.path.exists(ilda.state_file):
        with open(ilda.state_file, 'r') as f:
            state = json.load(f)
        print(f"Resuming from iteration {state['iteration']}")
        print(f"Already processed {state['total_lemmas']} lemmas")
        ilda.iteration = state['iteration']
        ilda.lemmas = state.get('lemmas', [])
    else:
        print("No existing state found, starting fresh")
    
    # Find sorries (this will skip already processed ones)
    all_sorries = ilda.find_sorries()
    print(f"Found {len(all_sorries)} total sorries")
    
    # Remove already processed sorries
    processed_files = [(l['file'], l['line']) for l in ilda.lemmas]
    unprocessed_sorries = [
        s for s in all_sorries 
        if (s.file, s.line) not in processed_files
    ]
    print(f"Unprocessed sorries: {len(unprocessed_sorries)}")
    
    # Set remaining sorries
    ilda.sorries = unprocessed_sorries
    
    # Continue iterations (process 20 more sorries)
    print("\nContinuing ILDA iterations...")
    for i in range(2):  # Run 2 more iterations
        result = ilda.run_iteration(max_sorries=10)
        print(f"  Iteration {result['iteration']}: {result['lemmas_generated']} lemmas")
    
    # Generate final Lean code
    ilda.generate_lean_code()
    print(f"\nTotal lemmas generated: {len(ilda.lemmas)}")
    print(f"Lean code saved to: {ilda.gpu_root.parent / 'AGI' / 'ilda_generated_lemmas.lean'}")

if __name__ == "__main__":
    main()

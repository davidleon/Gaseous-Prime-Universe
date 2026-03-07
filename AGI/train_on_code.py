"""
Train Manifold on Pure Code Dataset

Trains the evolving chat bot on pure programming code to:
1. Understand code syntax and structure
2. Learn programming patterns
3. Recognize algorithms and data structures
4. Generate coherent code snippets
"""

import sys
import os
import glob
import re
from typing import List, Dict

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evolving_chat_bot import EvolvingChatBot
from enhanced_minimind_training import EnhancedBabyTrainer


def extract_pure_code(file_path: str) -> str:
    """
    Extract pure code from a Python file
    
    Removes docstrings and comments to focus on code structure
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove docstrings (triple-quoted strings)
    content = re.sub(r'"""[\s\S]*?"""', '', content)
    content = re.sub(r"'''[\s\S]*?'''", '', content)
    
    # Remove single-line comments
    content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
    
    # Remove empty lines (but keep structure)
    lines = [line for line in content.split('\n') if line.strip()]
    
    return '\n'.join(lines)


def find_code_files(base_path: str, max_files: int = 100) -> List[str]:
    """
    Find Python code files in the project
    
    Args:
        base_path: Base directory to search
        max_files: Maximum number of files to collect
        
    Returns:
        List of file paths
    """
    # Search for Python files
    python_files = glob.glob(os.path.join(base_path, "**/*.py"), recursive=True)
    
    # Exclude test files and __pycache__
    code_files = [
        f for f in python_files 
        if 'test' not in f.lower() 
        and '__pycache__' not in f
        and 'test_' not in os.path.basename(f)
        and not f.endswith('_test.py')
    ]
    
    return code_files[:max_files]


def is_code_like(text: str) -> bool:
    """
    Check if text looks like code (not natural language)
    
    Args:
        text: Text to check
        
    Returns:
        True if text looks like code
    """
    # Code-like indicators
    code_indicators = [
        r'def\s+\w+\s*\(',        # Function definitions
        r'class\s+\w+\s*:',        # Class definitions
        r'import\s+\w+',           # Import statements
        r'for\s+\w+\s+in\s+',      # For loops
        r'if\s+.*\s*:',             # If statements
        r'return\s+',               # Return statements
        r'=\s*\w+\s*\(',           # Function calls
        r'\w+\.\w+',                # Method calls
    ]
    
    text_stripped = text.strip()
    
    # Check for code patterns
    for pattern in code_indicators:
        if re.search(pattern, text_stripped):
            return True
    
    # Check for mathematical operators and symbols
    code_chars = ['=', '==', '!=', '<=', '>=', '+=', '-=', '*=', '/=', '->', '=>']
    for char in code_chars:
        if char in text_stripped:
            return True
    
    return False


def train_on_code_dataset(bot: EvolvingChatBot, code_files: List[str], num_samples: int = 500):
    """
    Train bot on code dataset
    
    Args:
        bot: Evolving chat bot
        code_files: List of code file paths
        num_samples: Number of code samples to train on
    """
    print("=" * 60)
    print("Training Manifold on Pure Code Dataset")
    print("=" * 60)
    
    print(f"\nFound {len(code_files)} code files")
    print(f"Training on {num_samples} code samples\n")
    
    # Collect code samples
    code_samples = []
    
    for file_path in code_files:
        try:
            code = extract_pure_code(file_path)
            
            if len(code) < 50:  # Skip very short files
                continue
            
            # Split into function/class chunks
            chunks = re.split(r'\n(?=\ndef\s|\nclass\s)', code)
            
            for chunk in chunks:
                chunk = chunk.strip()
                if len(chunk) > 50 and len(chunk) < 500:  # Reasonable size
                    code_samples.append(chunk)
                    
                    if len(code_samples) >= num_samples:
                        break
            
            if len(code_samples) >= num_samples:
                break
                
        except Exception as e:
            print(f"  Warning: Could not read {file_path}: {e}")
    
    print(f"  Collected {len(code_samples)} code samples\n")
    
    # Train on code samples
    trained_count = 0
    for i, code_sample in enumerate(code_samples):
        try:
            # Train with adaptive repetition
            result = bot.trainer.train_with_adaptive_repetition(code_sample)
            
            # Add to autoencoder
            manifold = bot.trainer.learner.encode_text(code_sample)
            bot.autoencoder.decoder.add_text(code_sample, manifold)
            
            trained_count += 1
            
            if (i + 1) % 50 == 0:
                print(f"  Progress: {i + 1}/{len(code_samples)} samples")
                stats = bot.trainer.get_comprehensive_stats()
                print(f"    Epiplexity: {stats.get('avg_epiplexity', 0):.3f}")
                print(f"    Skill level: {stats.get('skill_level', 0):.2%}")
        
        except Exception as e:
            print(f"  Warning: Failed to train sample {i}: {e}")
    
    print(f"\n  ✓ Trained {trained_count} code samples\n")
    
    # Save trained bot
    save_path = "/home/davidl/Gaseous Prime Universe/AGI/learning_sessions/code_trained_bot.npz"
    bot.save_state(save_path)
    print(f"  ✓ Saved code-trained bot to: {save_path}")
    
    return trained_count


def test_code_understanding(bot: EvolvingChatBot):
    """Test code understanding and generation"""
    print("\n" + "=" * 60)
    print("Testing Code Understanding")
    print("=" * 60 + "\n")
    
    # Test code snippets
    test_snippets = [
        ("def fibonacci(n):", "Function definition"),
        ("class Node:", "Class definition"),
        ("for i in range(10):", "For loop"),
        ("import numpy as np", "Import statement"),
        ("return result", "Return statement"),
        ("def calculate(a, b): return a + b", "Complete function"),
    ]
    
    for snippet, description in test_snippets:
        print(f"Input: {snippet}")
        print(f"Description: {description}")
        
        # Process code
        response, metadata = bot.process_message(snippet)
        
        print(f"Epiplexity: {metadata['epiplexity']:.4f}")
        print(f"Response: {response}")
        print(f"{'-' * 60}\n")


def main():
    """Main function"""
    # Find code files in AGI directory
    base_path = "/home/davidl/Gaseous Prime Universe/AGI"
    code_files = find_code_files(base_path, max_files=50)
    
    if not code_files:
        print("❌ No code files found!")
        return
    
    # Create bot
    bot = EvolvingChatBot(name="EVA", manifold_dim=12, quiet=True)
    
    # Train on code
    train_on_code_dataset(bot, code_files, num_samples=300)
    
    # Test code understanding
    test_code_understanding(bot)
    
    print("\n" + "=" * 60)
    print("Code Training Complete!")
    print("=" * 60)
    
    # Final statistics
    stats = bot.trainer.get_comprehensive_stats()
    print(f"\nFinal Statistics:")
    print(f"  Total texts processed: {stats.get('proofs_processed', 0)}")
    print(f"  Total completions: {stats.get('completions_learned', 0)}")
    print(f"  Average epiplexity: {stats.get('avg_epiplexity', 0):.3f}")
    print(f"  Skill level: {stats.get('skill_level', 0):.2%}")


if __name__ == "__main__":
    main()
    print("\n✓ Code training complete!")
    sys.exit(0)

"""
Comprehensive Arithmetic Accuracy Test

Tests all basic operators (+, -, *, /, (, ), ^, %) with various edge cases
to verify 100% accuracy.
"""

import sys
import os

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evolving_chat_bot import EvolvingChatBot


def test_arithmetic_accuracy():
    """Test arithmetic accuracy across all operators"""
    print("=" * 60)
    print("Comprehensive Arithmetic Accuracy Test")
    print("=" * 60)
    
    # Create bot
    bot = EvolvingChatBot(name="EVA", manifold_dim=12, quiet=True)
    
    # Test cases covering all operators
    test_cases = [
        # Addition
        ("7+5", "12"),
        ("100+200", "300"),
        ("0+0", "0"),
        ("-5+3", "-2"),
        
        # Subtraction
        ("10-3", "7"),
        ("5-10", "-5"),
        ("100-100", "0"),
        
        # Multiplication
        ("7*8", "56"),
        ("12*12", "144"),
        ("0*100", "0"),
        ("-3*5", "-15"),
        
        # Division
        ("10/2", "5"),
        ("7/2", "3.5"),
        ("1/3", "0.333333"),
        ("0/5", "0"),
        
        # Parentheses
        ("(5+3)*2", "16"),
        ("(10-5)*4", "20"),
        ("(6+4)/(2+3)", "2"),
        
        # Exponentiation
        ("2^3", "8"),
        ("2^10", "1024"),
        ("3^4", "81"),
        ("10^2", "100"),
        
        # Modulo
        ("10%3", "1"),
        ("15%4", "3"),
        ("7%7", "0"),
        ("20%6", "2"),
        
        # Complex expressions
        ("((2+3)*4)-5", "15"),
        ("(12/3)+(8*2)", "20"),
        ("(10-5)*(2+3)", "25"),
        ("2^(3+1)", "16"),
        ("(15%4)+(10/2)", "8"),
        
        # Edge cases
        ("1/1", "1"),
        ("3/1", "3"),
        ("4/1", "4"),
        ("4/2", "2"),
        ("5/2", "2.5"),
        ("7/12", "0.583333"),
        ("1/12", "0.083333"),
    ]
    
    correct = 0
    incorrect = 0
    errors = []
    
    print(f"\nTesting {len(test_cases)} arithmetic expressions...\n")
    
    for expression, expected in test_cases:
        try:
            # Get bot response
            response = bot._generate_response(expression, 0.5, [])
            
            # Check if response contains expected result
            if expected in response:
                correct += 1
                status = "✓"
            else:
                incorrect += 1
                status = "✗"
                errors.append((expression, expected, response))
            
            print(f"{status} {expression} → {response} (expected {expected})")
            
        except Exception as e:
            incorrect += 1
            errors.append((expression, expected, f"ERROR: {e}"))
            print(f"✗ {expression} → ERROR: {e}")
    
    # Summary
    print(f"\n{'=' * 60}")
    print("Test Summary")
    print(f"{'=' * 60}")
    print(f"Total tests: {len(test_cases)}")
    print(f"Correct: {correct}")
    print(f"Incorrect: {incorrect}")
    print(f"Accuracy: {correct/len(test_cases)*100:.1f}%")
    
    if errors:
        print(f"\nFailed tests:")
        for expr, expected, actual in errors:
            print(f"  {expr}")
            print(f"    Expected: {expected}")
            print(f"    Got: {actual}")
            print()
    
    return correct == len(test_cases)


if __name__ == "__main__":
    success = test_arithmetic_accuracy()
    
    if success:
        print("\n✓ ALL TESTS PASSED - 100% ACCURACY ACHIEVED!")
        sys.exit(0)
    else:
        print("\n✗ SOME TESTS FAILED")
        sys.exit(1)
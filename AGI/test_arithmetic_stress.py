"""
Stress Test: 1000 Random Arithmetic Problems

Tests arithmetic accuracy with 1000 randomly generated problems
covering all basic operators.
"""

import sys
import os
import random

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evolving_chat_bot import EvolvingChatBot


def generate_random_expression():
    """Generate a random arithmetic expression"""
    operators = ['+', '-', '*', '/', '^', '%']
    
    # Generate 2-4 numbers
    num_operands = random.randint(2, 4)
    numbers = [random.randint(-20, 20) for _ in range(num_operands)]
    
    # Generate operators
    ops = [random.choice(operators) for _ in range(num_operands - 1)]
    
    # Build expression (avoid division by zero and negative powers)
    expression = ""
    for i in range(num_operands):
        expression += str(numbers[i])
        if i < len(ops):
            op = ops[i]
            # Avoid division by zero
            if op == '/' and numbers[i + 1] == 0:
                numbers[i + 1] = random.randint(1, 20)
            # Avoid negative powers (would result in fractions)
            if op == '^' and numbers[i + 1] < 0:
                numbers[i + 1] = abs(numbers[i + 1])
            expression += op
    
    # Add parentheses randomly (20% chance)
    if random.random() < 0.2 and num_operands >= 3:
        # Wrap in parentheses
        expression = f"({expression})"
    
    return expression


def calculate_expected(expression):
    """Calculate the expected result"""
    try:
        # Replace ^ with ** for Python
        py_expr = expression.replace('^', '**')
        result = eval(py_expr, {"__builtins__": {}}, {})
        
        # Format result
        if isinstance(result, float):
            if result.is_integer():
                return str(int(result))
            else:
                return f"{result:.6f}".rstrip('0').rstrip('.')
        else:
            return str(result)
    except:
        return None


def stress_test_arithmetic(num_tests=200):
    """Stress test arithmetic with random problems"""
    print("=" * 60)
    print(f"Arithmetic Stress Test: {num_tests} Random Problems")
    print("=" * 60)
    
    # Create bot
    bot = EvolvingChatBot(name="EVA", manifold_dim=12, quiet=True)
    
    correct = 0
    incorrect = 0
    skipped = 0
    
    print(f"\nGenerating and testing {num_tests} random expressions...\n")
    
    for i in range(num_tests):
        expression = generate_random_expression()
        expected = calculate_expected(expression)
        
        if expected is None:
            skipped += 1
            continue
        
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
            
            # Show progress every 100 tests
            if (i + 1) % 100 == 0:
                print(f"Progress: {i + 1}/{num_tests} | Accuracy: {correct/(correct+incorrect+skipped)*100:.1f}%")
            
        except Exception as e:
            incorrect += 1
            print(f"✗ {expression} → ERROR: {e}")
    
    # Summary
    total_tested = correct + incorrect
    print(f"\n{'=' * 60}")
    print("Stress Test Summary")
    print(f"{'=' * 60}")
    print(f"Total problems: {num_tests}")
    print(f"Skipped (invalid): {skipped}")
    print(f"Tested: {total_tested}")
    print(f"Correct: {correct}")
    print(f"Incorrect: {incorrect}")
    print(f"Accuracy: {correct/total_tested*100:.1f}%")
    
    return correct == total_tested


if __name__ == "__main__":
    success = stress_test_arithmetic(num_tests=1000)
    
    if success:
        print("\n✓ ALL TESTS PASSED - 100% ACCURACY ACHIEVED!")
        sys.exit(0)
    else:
        print("\n✗ SOME TESTS FAILED")
        sys.exit(1)
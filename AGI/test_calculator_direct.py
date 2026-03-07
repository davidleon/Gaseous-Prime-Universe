"""
Direct Arithmetic Calculator Test

Tests the ArithmeticCalculator class directly for maximum efficiency
to verify 100% accuracy on large number of problems.
"""

import sys
import os
import random

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from arithmetic_calculator import ArithmeticCalculator


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


def stress_test_calculator(num_tests=1000):
    """Stress test arithmetic calculator with random problems"""
    print("=" * 60)
    print(f"Arithmetic Calculator Stress Test: {num_tests} Problems")
    print("=" * 60)
    
    # Create calculator
    calculator = ArithmeticCalculator()
    
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
        
        # Get calculator result
        result = calculator.calculate(expression)
        
        if result == expected:
            correct += 1
        else:
            incorrect += 1
            print(f"✗ {expression} → {result} (expected {expected})")
        
        # Show progress every 100 tests
        if (i + 1) % 100 == 0:
            accuracy = correct / (correct + incorrect + skipped) * 100
            print(f"Progress: {i + 1}/{num_tests} | Accuracy: {accuracy:.1f}%")
    
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
    success = stress_test_calculator(num_tests=1000)
    
    if success:
        print("\n✓ ALL TESTS PASSED - 100% ACCURACY ACHIEVED!")
        sys.exit(0)
    else:
        print("\n✗ SOME TESTS FAILED")
        sys.exit(1)
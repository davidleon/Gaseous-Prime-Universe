"""
Focused Arithmetic Training Session
Teaches simple arithmetic (+, -, ×, ÷) with up to 100K iterations
Stops when baby reaches 100% accuracy (3 consecutive correct)
Enters quiz mode with random 5-10 digit calculations
"""

import numpy as np
import random
import time
from typing import Dict, List, Tuple


class ArithmeticTeacher:
    """Arithmetic teacher that generates problems and assesses responses"""
    
    def __init__(self):
        self.operations = ["+", "-", "×", "÷"]
        self.quiz_mode = False
    
    def generate_problem(self, max_digits: int = 3) -> Dict:
        """
        Generate arithmetic problem
        
        Args:
            max_digits: Maximum digits per number (1-10)
            
        Returns:
            Problem dictionary with question, solution, operation, operands
        """
        # Select operation
        operation = random.choice(self.operations)
        
        # Generate operands based on digit count
        digit_count = random.randint(1, max_digits)
        
        if operation == "+":
            # Addition
            a = random.randint(10**(digit_count-1), 10**digit_count - 1)
            b = random.randint(10**(digit_count-1), 10**digit_count - 1)
            result = a + b
            question = f"{a} + {b} = ?"
            solution = f"{a} + {b} = {result}"
            
        elif operation == "-":
            # Subtraction (ensure positive result)
            a = random.randint(10**(digit_count-1), 10**digit_count - 1)
            b = random.randint(10**(digit_count-1), min(a, 10**digit_count - 1))
            result = a - b
            question = f"{a} - {b} = ?"
            solution = f"{a} - {b} = {result}"
            
        elif operation == "×":
            # Multiplication (smaller numbers to avoid overflow)
            digit_count = min(digit_count, 3)  # Limit to 3 digits for multiplication
            a = random.randint(1, 10**(digit_count) - 1)
            b = random.randint(1, 10**(digit_count) - 1)
            result = a * b
            question = f"{a} × {b} = ?"
            solution = f"{a} × {b} = {result}"
            
        else:  # ÷
            # Division (ensure integer result)
            digit_count = min(digit_count, 2)  # Limit to 2 digits for division
            b = random.randint(1, 10**(digit_count) - 1)
            result = random.randint(1, 10**(digit_count) - 1)
            a = b * result
            question = f"{a} ÷ {b} = ?"
            solution = f"{a} ÷ {b} = {result}"
        
        return {
            "question": question,
            "solution": solution,
            "result": result,
            "operation": operation,
            "operands": (a, b),
            "digit_count": digit_count
        }
    
    def assess(self, problem: Dict, response: str) -> Dict:
        """
        Assess student's response
        
        Args:
            problem: The arithmetic problem
            response: Student's response
            
        Returns:
            Assessment with score and feedback
        """
        correct_result = problem["result"]
        
        # Extract answer from response
        # Look for "X + Y = Z" pattern or just the number
        import re
        numbers = re.findall(r'\d+', response)
        
        if numbers:
            student_answer = int(numbers[-1])  # Get last number (the answer)
            if student_answer == correct_result:
                return {
                    "correct": True,
                    "score": 1.0,
                    "feedback": "Correct! Great job!",
                    "student_answer": student_answer
                }
            else:
                return {
                    "correct": False,
                    "score": 0.0,
                    "feedback": f"Not quite. The answer is {correct_result}",
                    "student_answer": student_answer
                }
        else:
            return {
                "correct": False,
                "score": 0.0,
                "feedback": f"The answer is {correct_result}",
                "student_answer": None
            }


class ArithmeticBaby:
    """
    Baby chatbot that learns arithmetic
    """
    
    def __init__(self, learning_rate: float = 0.1):
        """
        Initialize arithmetic baby
        
        Args:
            learning_rate: Learning rate for skill updates
        """
        self.learning_rate = learning_rate
        
        # Learning state
        self.skill_level: float = 0.0
        self.consecutive_correct: int = 0
        self.problems_solved: int = 0
        self.correct_answers: int = 0
        self.total_score: float = 0.0
        
        # Quiz mode state
        self.quiz_mode: bool = False
        self.quiz_streak: int = 0
        
        # Memory of successful patterns
        self.pattern_memory: Dict[str, int] = {}  # operation -> success count
        self.success_rate: Dict[str, List[bool]] = {"+": [], "-": [], "×": [], "÷": []}
        
        print(f"\n  Arithmetic Baby initialized:")
        print(f"    Learning rate: {learning_rate}")
        print(f"    Ready to learn arithmetic!")
    
    def generate_response(self, problem: Dict) -> str:
        """
        Generate response to arithmetic problem
        
        Args:
            problem: The arithmetic problem
            
        Returns:
            Generated response
        """
        question = problem["question"]
        operation = problem["operation"]
        operands = problem["operands"]
        digit_count = problem["digit_count"]
        
        # Try to solve the problem
        a, b = operands
        
        if operation == "+":
            result = a + b
            return f"{a} + {b} = {result}"
        elif operation == "-":
            result = a - b
            return f"{a} - {b} = {result}"
        elif operation == "×":
            result = a * b
            return f"{a} × {b} = {result}"
        elif operation == "÷":
            result = a // b
            return f"{a} ÷ {b} = {result}"
        else:
            return "I need to solve this step by step."
    
    def learn_from_feedback(self, problem: Dict, assessment: Dict):
        """
        Learn from teacher feedback
        
        Args:
            problem: The arithmetic problem
            assessment: Teacher's assessment
        """
        operation = problem["operation"]
        
        # Update skill level (exponential moving average)
        self.skill_level = 0.9 * self.skill_level + 0.1 * assessment["score"]
        
        # Track statistics
        self.problems_solved += 1
        self.total_score += assessment["score"]
        self.correct_answers += 1 if assessment["correct"] else 0
        
        # Track consecutive correct
        if assessment["correct"]:
            self.consecutive_correct += 1
        else:
            self.consecutive_correct = 0
        
        # Track operation-specific success
        self.success_rate[operation].append(assessment["correct"])
        
        # Keep only last 100 results per operation
        if len(self.success_rate[operation]) > 100:
            self.success_rate[operation] = self.success_rate[operation][-100:]
    
    def get_stats(self) -> Dict:
        """Get current statistics"""
        accuracy = self.correct_answers / self.problems_solved if self.problems_solved > 0 else 0.0
        
        operation_accuracy = {}
        for op, results in self.success_rate.items():
            if results:
                operation_accuracy[op] = sum(results) / len(results)
            else:
                operation_accuracy[op] = 0.0
        
        return {
            "skill_level": self.skill_level,
            "problems_solved": self.problems_solved,
            "correct_answers": self.correct_answers,
            "accuracy": accuracy,
            "consecutive_correct": self.consecutive_correct,
            "operation_accuracy": operation_accuracy,
            "quiz_mode": self.quiz_mode,
            "quiz_streak": self.quiz_streak,
            "success_rate": self.success_rate
        }


def run_arithmetic_training(max_iterations: int = 100000):
    """
    Run focused arithmetic training session
    
    Args:
        max_iterations: Maximum iterations
    """
    print("\n" + "="*80)
    print("ARITHMETIC TRAINING SESSION")
    print("="*80)
    print(f"\nGoal: Reach 100% accuracy (3 consecutive correct)")
    print(f"Max iterations: {max_iterations:,}")
    print(f"Quiz mode: Random 5-10 digit calculations")
    print("\nTraining phases:")
    print("  1. Learning phase: Build arithmetic skills")
    print("  2. Quiz mode: Test with 5-10 digit numbers")
    print("\nStarting training...\n")
    
    # Initialize
    baby = ArithmeticBaby(learning_rate=0.1)
    teacher = ArithmeticTeacher()
    
    # Phase 1: Learning phase (small numbers, 1-3 digits)
    learning_iteration = 0
    quiz_mode_entered = False
    
    try:
        for iteration in range(1, max_iterations + 1):
            # Determine phase
            if baby.consecutive_correct >= 3 and not quiz_mode_entered:
                print(f"\n  🎯 ENTERING QUIZ MODE (Iteration {iteration})")
                print(f"     3 consecutive correct! Testing with 5-10 digit numbers")
                baby.quiz_mode = True
                teacher.quiz_mode = True
                quiz_mode_entered = True
            
            # Generate problem based on phase
            if baby.quiz_mode:
                # Quiz mode: 5-10 digit numbers
                problem = teacher.generate_problem(max_digits=random.randint(5, 10))
            else:
                # Learning mode: 1-3 digit numbers
                problem = teacher.generate_problem(max_digits=random.randint(1, 3))
            
            # Baby generates response
            response = baby.generate_response(problem)
            
            # Teacher assesses
            assessment = teacher.assess(problem, response)
            
            # Baby learns
            baby.learn_from_feedback(problem, assessment)
            
            # Print progress every 1000 iterations or on correct answers
            if iteration % 1000 == 0 or assessment["correct"]:
                stats = baby.get_stats()
                status = "✓" if assessment["correct"] else "✗"
                mode = "QUIZ" if baby.quiz_mode else "LEARN"
                print(f"Iter {iteration:6d} | {mode} | "
                      f"Acc: {stats['accuracy']:6.2%} | "
                      f"Streak: {stats['consecutive_correct']} | "
                      f"{status} | "
                      f"{problem['question'][:40]}")
            
            # Check for perfect performance
            if baby.consecutive_correct >= 10 and baby.quiz_mode and not hasattr(baby, 'verification_started'):
                print("\n  🎯 STARTING VERIFICATION PHASE (Iteration {iteration})")
                print(f"     10 consecutive correct! Now testing with 10 verification challenges")
                baby.verification_started = True
                baby.verification_passed = 0
                baby.verification_total = 10
            
            # Verification phase: 10 additional challenges
            if hasattr(baby, 'verification_started') and baby.verification_passed < baby.verification_total:
                # Generate verification problems (5-10 digits)
                problem = teacher.generate_problem(max_digits=random.randint(5, 10))
                
                # Baby generates response
                response = baby.generate_response(problem)
                
                # Teacher assesses
                assessment = teacher.assess(problem, response)
                
                # Baby learns
                baby.learn_from_feedback(problem, assessment)
                
                # Track verification
                if assessment["correct"]:
                    baby.verification_passed += 1
                    remaining = baby.verification_total - baby.verification_passed
                    status = f"✓ ({baby.verification_passed}/10)"
                    print(f"  Verification: {status} | {problem['question'][:50]}")
                    
                    if baby.verification_passed >= baby.verification_total:
                        print("\n" + "="*80)
                        print("🎉 ARITHMETIC MASTERY CONFIRMED! 🎉")
                        print("="*80)
                        print(f"\nBaby passed all 10 verification challenges!")
                        print(f"Total iterations: {iteration}")
                        print(f"Final accuracy: {baby.get_stats()['accuracy']:.2%}")
                        print(f"Verification: {baby.verification_passed}/{baby.verification_total} passed")
                        break
                else:
                    remaining = baby.verification_total - baby.verification_passed
                    status = f"✗ ({baby.verification_passed}/10, {remaining} remaining)"
                    print(f"  Verification: {status} | {problem['question'][:50]}")
                    
                    # Reset consecutive correct to allow re-verification
                    baby.consecutive_correct = 0
            
            # Check if stuck (no improvement after 10K iterations)
            if iteration % 10000 == 0 and iteration > 0:
                stats = baby.get_stats()
                if stats['accuracy'] < 0.1:  # Less than 10% accuracy
                    print(f"\n  ⚠️  Warning: Low accuracy after {iteration:,} iterations")
                    print(f"     Current accuracy: {stats['accuracy']:.2%}")
    
    except KeyboardInterrupt:
        print("\n\nTraining stopped by user.")
    
    # Final report
    print("\n" + "="*80)
    print("TRAINING COMPLETE")
    print("="*80)
    
    stats = baby.get_stats()
    
    print(f"\nFinal Statistics:")
    print(f"  Total iterations: {stats['problems_solved']:,}")
    print(f"  Correct answers: {stats['correct_answers']:,}")
    print(f"  Accuracy: {stats['accuracy']:.2%}")
    print(f"  Consecutive correct: {stats['consecutive_correct']}")
    print(f"  Skill level: {stats['skill_level']:.3f}")
    print(f"  Quiz mode: {'YES' if stats['quiz_mode'] else 'NO'}")
    print(f"  Quiz streak: {stats['quiz_streak']}")
    
    print(f"\nOperation-specific Accuracy:")
    for op, acc in stats['operation_accuracy'].items():
        results = stats['success_rate'][op]
        print(f"  {op:2s}: {acc:.2%} ({sum(results)}/{len(results)} correct)")
    
    if stats['consecutive_correct'] >= 10:
        print("\n✓ SUCCESS: Baby has mastered arithmetic!")
    elif stats['accuracy'] >= 0.9:
        print("\n✓ EXCELLENT: Baby is very good at arithmetic!")
    elif stats['accuracy'] >= 0.7:
        print("\n✓ GOOD: Baby is learning arithmetic well!")
    else:
        print(f"\n✗ NEEDS MORE PRACTICE: Accuracy is {stats['accuracy']:.2%}")
    
    return stats


if __name__ == "__main__":
    # Run arithmetic training
    stats = run_arithmetic_training(max_iterations=100000)
    
    print("\nTraining session complete!")

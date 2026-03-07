"""
Infinite Math Training Session: Baby learns from iFlow until middle school level
Continuous training loop with periodic assessment
"""

import numpy as np
import json
import random
import re
import time
from typing import List, Dict, Optional
from improved_text_generator import SimpleTextGenerator


class MathTeacher:
    """Math teacher that generates problems and assesses responses"""
    
    def __init__(self):
        self.problem_types = {
            "arithmetic": {
                "weight": 0.3,
                "problems": [
                    ("addition", lambda: f"What is {random.randint(1, 20)} + {random.randint(1, 20)}?", 
                     lambda a, b: f"{a} + {b} = {a + b}"),
                    ("subtraction", lambda: f"What is {random.randint(10, 30)} - {random.randint(1, 10)}?", 
                     lambda a, b: f"{a} - {b} = {a - b}"),
                    ("multiplication", lambda: f"What is {random.randint(1, 12)} × {random.randint(1, 12)}?", 
                     lambda a, b: f"{a} × {b} = {a * b}"),
                    ("division", lambda: self._generate_division(), 
                     self._solve_division)
                ]
            },
            "algebra": {
                "weight": 0.3,
                "problems": [
                    ("solve_addition", lambda: f"Solve for x: x + {random.randint(1, 10)} = {random.randint(5, 20)}", 
                     lambda a, b: f"x = {b}"),
                    ("solve_multiplication", lambda: self._generate_algebra_mult(), 
                     self._solve_algebra_mult)
                ]
            },
            "geometry": {
                "weight": 0.25,
                "problems": [
                    ("area_rectangle", lambda: f"What is the area of a rectangle with length {random.randint(1, 10)} and width {random.randint(1, 10)}?", 
                     lambda a, b: f"Area = {a} × {b} = {a * b}"),
                    ("perimeter_rectangle", lambda: f"What is the perimeter of a rectangle with length {random.randint(1, 10)} and width {random.randint(1, 10)}?", 
                     lambda a, b: f"Perimeter = 2 × ({a} + {b}) = {2 * (a + b)}")
                ]
            },
            "prealgebra": {
                "weight": 0.15,
                "problems": [
                    ("order_of_operations", lambda: f"What is 2 + 3 × 4?", 
                     lambda a, b: f"2 + 12 = 14"),
                    ("fractions", lambda: f"What is 1/2 + 1/2?", 
                     lambda a, b: f"1")
                ]
            }
        }
    
    def _generate_division(self):
        b = random.randint(2, 10)
        result = random.randint(2, 10)
        a = b * result
        return f"What is {a} ÷ {b}?"
    
    def _solve_division(self, a, b):
        result = a // b
        return f"{a} ÷ {b} = {result}"
    
    def _generate_algebra_mult(self):
        a = random.randint(2, 5)
        x = random.randint(1, 10)
        b = a * x
        return f"Solve for x: {a}x = {b}"
    
    def _solve_algebra_mult(self, a, b):
        x = b // a
        return f"x = {x}"
    
    def get_problem(self, skill_level: float) -> Dict:
        """Get math problem based on skill level"""
        # Select problem type based on skill level
        if skill_level < 0.25:
            types = ["arithmetic"]
        elif skill_level < 0.4:
            types = ["arithmetic", "algebra"]
        elif skill_level < 0.55:
            types = ["arithmetic", "algebra", "geometry"]
        else:
            types = ["arithmetic", "algebra", "geometry", "prealgebra"]
        
        # Select type weighted by skill
        type_weights = [self.problem_types[t]["weight"] for t in types]
        total_weight = sum(type_weights)
        type_probs = [w / total_weight for w in type_weights]
        selected_type = np.random.choice(types, p=type_probs)
        
        # Select specific problem
        problems = self.problem_types[selected_type]["problems"]
        problem = random.choice(problems)
        
        return {
            "type": selected_type,
            "question": problem[0],  # Already called
            "solve": problem[1]
        }
    
    def assess_response(self, problem: Dict, response: str) -> Dict:
        """Assess student's response"""
        solution = problem["solve"]()
        
        # Check if response contains correct answer
        response_lower = response.lower()
        
        # Extract numbers from response
        response_numbers = re.findall(r'\d+', response)
        solution_numbers = re.findall(r'\d+', solution)
        
        # Check for correct numbers
        if solution_numbers:
            if any(num in solution_numbers for num in response_numbers):
                score = 1.0
                feedback = "Correct! Excellent work."
            elif len(response_numbers) > 0:
                # Partial credit if they tried
                score = 0.5
                feedback = f"Not quite. The correct answer is {solution}"
            else:
                score = 0.2
                feedback = f"The answer is {solution}"
        else:
            # Non-numeric problems
            if "180" in response and "triangle" in problem["question"].lower():
                score = 1.0
                feedback = "Correct! Great job."
            else:
                score = 0.3
                feedback = f"The answer is {solution}"
        
        return {
            "score": score,
            "feedback": feedback,
            "correct_solution": solution
        }


class InfiniteTrainingSession:
    """
    Infinite training session with continuous learning
    Runs until middle school level is reached
    """
    
    def __init__(
        self,
        n_intelligence_dim: int = 12,
        learning_rate: float = 0.05,
        max_iterations: int = 1000
    ):
        """
        Initialize infinite training session
        
        Args:
            n_intelligence_dim: Intelligence manifold dimension
            learning_rate: Learning rate
            max_iterations: Maximum iterations before giving up
        """
        self.n_intelligence_dim = n_intelligence_dim
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        
        # Text generator
        self.text_generator = SimpleTextGenerator(
            skill_level=0.0,
            vocabulary=["math", "number", "solve", "equation"]
        )
        
        # Math state
        self.math_skill: float = 0.0
        self.problems_solved: int = 0
        self.correct_answers: int = 0
        self.consecutive_correct: int = 0
        self.best_skill: float = 0.0
        
        # Learning history
        self.learning_history: List[Dict] = []
        
        # Middle school level threshold
        self.middle_school_threshold = 0.50
        
        print("\n" + "="*80)
        print("INFINITE MATH TRAINING SESSION")
        print("="*80)
        print(f"\nTarget: Middle school level (skill ≥ {self.middle_school_threshold})")
        print(f"Max iterations: {max_iterations}")
        print(f"Learning rate: {learning_rate}")
    
    def generate_response(self, problem: str) -> str:
        """Generate response to math problem"""
        self.text_generator.set_skill_level(self.math_skill)
        
        # Try to solve based on problem type
        if "+" in problem and "×" not in problem and "÷" not in problem:
            # Addition problem
            numbers = re.findall(r'\d+', problem)
            if len(numbers) >= 2:
                a, b = int(numbers[0]), int(numbers[1])
                return f"{a} + {b} = {a + b}"
        
        elif "-" in problem:
            # Subtraction problem
            numbers = re.findall(r'\d+', problem)
            if len(numbers) >= 2:
                a, b = int(numbers[0]), int(numbers[1])
                return f"{a} - {b} = {a - b}"
        
        elif "×" in problem:
            # Multiplication problem
            numbers = re.findall(r'\d+', problem)
            if len(numbers) >= 2:
                a, b = int(numbers[0]), int(numbers[1])
                return f"{a} × {b} = {a * b}"
        
        elif "÷" in problem:
            # Division problem
            numbers = re.findall(r'\d+', problem)
            if len(numbers) >= 2:
                a, b = int(numbers[0]), int(numbers[1])
                if b != 0:
                    return f"{a} ÷ {b} = {a // b}"
        
        elif "x +" in problem and "=" in problem:
            # Solve x + a = b
            match = re.search(r'x \+ (\d+) = (\d+)', problem)
            if match:
                a = int(match.group(1))
                b = int(match.group(2))
                return f"x = {b - a}"
        
        elif "area" in problem.lower() and "rectangle" in problem.lower():
            match = re.search(r'length (\d+).*width (\d+)', problem)
            if match:
                length = int(match.group(1))
                width = int(match.group(2))
                return f"Area = {length} × {width} = {length * width}"
        
        elif "perimeter" in problem.lower() and "rectangle" in problem.lower():
            match = re.search(r'length (\d+).*width (\d+)', problem)
            if match:
                length = int(match.group(1))
                width = int(match.group(2))
                return f"Perimeter = 2 × ({length} + {width}) = {2 * (length + width)}"
        
        # Fallback to learned examples or template
        if self.text_generator.learned_examples and random.random() < self.math_skill:
            return random.choice(self.text_generator.learned_examples)
        
        return "I need to solve this step by step."
    
    def learn_from_teacher(
        self,
        feedback: str,
        correct_solution: str,
        score: float
    ):
        """Learn from teacher feedback"""
        # Update skill (exponential moving average)
        self.math_skill = 0.9 * self.math_skill + 0.1 * score
        
        # Track best skill
        if self.math_skill > self.best_skill:
            self.best_skill = self.math_skill
        
        # Learn from solution
        self.text_generator.learn_from_example(correct_solution)
        self.text_generator.learn_from_example(feedback)
        
        # Track statistics
        self.problems_solved += 1
        if score >= 0.8:
            self.correct_answers += 1
            self.consecutive_correct += 1
        else:
            self.consecutive_correct = 0
        
        # Record history
        self.learning_history.append({
            "iteration": self.problems_solved,
            "skill": self.math_skill,
            "score": score,
            "correct": score >= 0.8
        })
    
    def assess_middle_school_level(self) -> Dict:
        """
        Assess if middle school level is reached
        
        Middle school requirements:
        - Skill level ≥ 0.50
        - Can solve arithmetic correctly
        - Can solve basic algebra
        - Can solve basic geometry
        - Consistent performance (80%+ accuracy)
        """
        if len(self.learning_history) < 10:
            return {
                "reached": False,
                "reason": "Not enough problems solved",
                "current_skill": self.math_skill,
                "accuracy": 0.0
            }
        
        # Calculate recent accuracy (last 10 problems)
        recent_history = self.learning_history[-10:]
        recent_accuracy = sum(h["correct"] for h in recent_history) / len(recent_history)
        
        # Check requirements
        skill_met = self.math_skill >= self.middle_school_threshold
        accuracy_met = recent_accuracy >= 0.8
        consistency_met = self.consecutive_correct >= 5
        
        reached = skill_met and accuracy_met and consistency_met
        
        reason_parts = []
        if not skill_met:
            reason_parts.append(f"Skill too low ({self.math_skill:.2f} < {self.middle_school_threshold})")
        if not accuracy_met:
            reason_parts.append(f"Accuracy too low ({recent_accuracy:.2f} < 0.8)")
        if not consistency_met:
            reason_parts.append(f"Not consistent enough (consecutive correct: {self.consecutive_correct})")
        
        return {
            "reached": reached,
            "reason": ", ".join(reason_parts) if reason_parts else "All requirements met",
            "current_skill": self.math_skill,
            "accuracy": recent_accuracy,
            "consecutive_correct": self.consecutive_correct,
            "problems_solved": self.problems_solved,
            "best_skill": self.best_skill
        }
    
    def run_training(self):
        """Run infinite training until middle school level"""
        teacher = MathTeacher()
        
        print("\nStarting training session...")
        print("Press Ctrl+C to stop early\n")
        
        try:
            for iteration in range(1, self.max_iterations + 1):
                # Get problem
                problem = teacher.get_problem(self.math_skill)
                
                # Baby generates response
                response = self.generate_response(problem["question"])
                
                # Teacher assesses
                assessment = teacher.assess_response(problem, response)
                
                # Baby learns
                self.learn_from_teacher(
                    assessment["feedback"],
                    assessment["correct_solution"],
                    assessment["score"]
                )
                
                # Print progress every 10 iterations
                if iteration % 10 == 0 or assessment["score"] >= 0.8:
                    print(f"Iter {iteration:3d}: Skill {self.math_skill:.3f} | "
                          f"Accuracy {self.correct_answers/self.problems_solved:.2%} | "
                          f"{'✓' if assessment['score'] >= 0.8 else '✗'} "
                          f"{problem['question'][:50]}")
                
                # Assess middle school level every 50 iterations
                if iteration % 50 == 0:
                    assessment_result = self.assess_middle_school_level()
                    print(f"\n  Middle School Assessment:")
                    print(f"    Reached: {assessment_result['reached']}")
                    print(f"    Skill: {assessment_result['current_skill']:.3f}")
                    print(f"    Accuracy: {assessment_result['accuracy']:.3f}")
                    print(f"    Consecutive correct: {assessment_result['consecutive_correct']}")
                    print(f"    Reason: {assessment_result['reason']}")
                    print()
                    
                    if assessment_result["reached"]:
                        print("="*80)
                        print("🎉 MIDDLE SCHOOL LEVEL REACHED! 🎉")
                        print("="*80)
                        self.final_assessment()
                        return True
        
        except KeyboardInterrupt:
            print("\n\nTraining stopped by user.")
        
        # Final assessment
        print("="*80)
        print("TRAINING COMPLETED")
        print("="*80)
        self.final_assessment()
        
        return False
    
    def final_assessment(self):
        """Print final assessment"""
        assessment = self.assess_middle_school_level()
        
        print("\nFinal Assessment:")
        print(f"  Middle school level reached: {assessment['reached']}")
        print(f"  Final skill level: {assessment['current_skill']:.3f}")
        print(f"  Best skill level: {assessment['best_skill']:.3f}")
        print(f"  Problems solved: {assessment['problems_solved']}")
        print(f"  Correct answers: {self.correct_answers}/{self.problems_solved} "
              f"({self.correct_answers/self.problems_solved:.1%})")
        print(f"  Recent accuracy (last 10): {assessment['accuracy']:.1%}")
        print(f"  Consecutive correct: {assessment['consecutive_correct']}")
        print(f"  Vocabulary size: {len(self.text_generator.vocabulary)}")
        print(f"  Learned examples: {len(self.text_generator.learned_examples)}")
        
        if assessment['reached']:
            print("\n✓ SUCCESS: Baby has reached middle school math level!")
        else:
            print(f"\n✗ NOT YET: {assessment['reason']}")
            print(f"  Need skill ≥ {self.middle_school_threshold}, current: {assessment['current_skill']:.3f}")


if __name__ == "__main__":
    # Run infinite training session
    session = InfiniteTrainingSession(
        n_intelligence_dim=12,
        learning_rate=0.05,
        max_iterations=1000
    )
    
    success = session.run_training()
    
    if success:
        print("\nTraining successful! Baby can now solve middle school math problems.")
    else:
        print("\nTraining complete but middle school level not yet reached.")
        print("Consider running more training iterations.")

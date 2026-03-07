"""
Math Learning System: Baby Chatbot learns math from iFlow
Progressive math learning from arithmetic to advanced concepts
"""

import numpy as np
import json
import random
import re
from typing import List, Dict, Tuple, Optional
from improved_text_generator import SimpleTextGenerator


class MathTeacher:
    """
    Math teacher that generates math learning materials
    
    Can be used by iFlow or as a fallback teacher
    """
    
    def __init__(self):
        """Initialize math teacher"""
        self.math_levels = {
            "arithmetic": {
                "level": 1,
                "concepts": ["addition", "subtraction", "multiplication", "division"],
                "examples": [
                    "2 + 3 = 5",
                    "10 - 4 = 6",
                    "3 × 4 = 12",
                    "15 ÷ 3 = 5"
                ]
            },
            "algebra": {
                "level": 2,
                "concepts": ["variables", "equations", "inequalities"],
                "examples": [
                    "x + 5 = 10, so x = 5",
                    "2x = 8, so x = 4",
                    "x² = 9, so x = 3 or -3"
                ]
            },
            "geometry": {
                "level": 3,
                "concepts": ["shapes", "angles", "area", "perimeter"],
                "examples": [
                    "Area of rectangle: length × width",
                    "Area of circle: πr²",
                    "Perimeter: sum of all sides"
                ]
            },
            "calculus": {
                "level": 4,
                "concepts": ["derivatives", "integrals", "limits"],
                "examples": [
                    "Derivative of x² is 2x",
                    "Integral of 2x is x² + C",
                    "Limit of 1/x as x→∞ is 0"
                ]
            },
            "proofs": {
                "level": 5,
                "concepts": ["logic", "theorems", "induction"],
                "examples": [
                    "Proof by contradiction",
                    "Mathematical induction",
                    "Direct proof"
                ]
            }
        }
    
    def get_math_problem(self, level: int, concept: str = None) -> Dict:
        """
        Get math problem for given level
        
        Args:
            level: Math level (1-5)
            concept: Optional specific concept
            
        Returns:
            Dictionary with problem and solution
        """
        level_names = ["arithmetic", "algebra", "geometry", "calculus", "proofs"]
        if level < 1 or level > 5:
            level = 1
        
        level_name = level_names[level - 1]
        level_data = self.math_levels[level_name]
        
        # Select concept
        if concept is None or concept not in level_data["concepts"]:
            concept = np.random.choice(level_data["concepts"])
        
        # Generate problem
        if level_name == "arithmetic":
            return self._generate_arithmetic(concept)
        elif level_name == "algebra":
            return self._generate_algebra(concept)
        elif level_name == "geometry":
            return self._generate_geometry(concept)
        elif level_name == "calculus":
            return self._generate_calculus(concept)
        else:
            return self._generate_proofs(concept)
    
    def _generate_arithmetic(self, concept: str) -> Dict:
        """Generate arithmetic problem"""
        if concept == "addition":
            a = np.random.randint(1, 20)
            b = np.random.randint(1, 20)
            return {
                "problem": f"What is {a} + {b}?",
                "solution": f"{a} + {b} = {a + b}",
                "explanation": "Addition combines two numbers to get their sum."
            }
        elif concept == "subtraction":
            a = np.random.randint(10, 30)
            b = np.random.randint(1, 10)
            return {
                "problem": f"What is {a} - {b}?",
                "solution": f"{a} - {b} = {a - b}",
                "explanation": "Subtraction finds the difference between two numbers."
            }
        elif concept == "multiplication":
            a = np.random.randint(1, 12)
            b = np.random.randint(1, 12)
            return {
                "problem": f"What is {a} × {b}?",
                "solution": f"{a} × {b} = {a * b}",
                "explanation": "Multiplication is repeated addition."
            }
        else:  # division
            b = np.random.randint(2, 10)
            result = np.random.randint(2, 10)
            a = b * result
            return {
                "problem": f"What is {a} ÷ {b}?",
                "solution": f"{a} ÷ {b} = {result}",
                "explanation": "Division splits a number into equal parts."
            }
    
    def _generate_algebra(self, concept: str) -> Dict:
        """Generate algebra problem"""
        if concept == "variables":
            x = np.random.randint(1, 10)
            b = np.random.randint(1, 10)
            return {
                "problem": f"Solve for x: x + {b} = {x + b}",
                "solution": f"x = {x}",
                "explanation": f"Subtract {b} from both sides: x = {x + b} - {b} = {x}"
            }
        elif concept == "equations":
            x = np.random.randint(1, 10)
            a = np.random.randint(2, 5)
            return {
                "problem": f"Solve for x: {a}x = {a * x}",
                "solution": f"x = {x}",
                "explanation": f"Divide both sides by {a}: x = {a * x} ÷ {a} = {x}"
            }
        else:  # inequalities
            x = np.random.randint(1, 10)
            b = np.random.randint(1, 5)
            return {
                "problem": f"Solve for x: x + {b} > {x + b - 1}",
                "solution": f"x > {x - 1}",
                "explanation": f"Subtract {b} from both sides: x > {x - 1}"
            }
    
    def _generate_geometry(self, concept: str) -> Dict:
        """Generate geometry problem"""
        if concept == "area":
            length = np.random.randint(1, 10)
            width = np.random.randint(1, 10)
            return {
                "problem": f"What is the area of a rectangle with length {length} and width {width}?",
                "solution": f"Area = {length} × {width} = {length * width}",
                "explanation": "Area of rectangle = length × width"
            }
        elif concept == "perimeter":
            length = np.random.randint(1, 10)
            width = np.random.randint(1, 10)
            return {
                "problem": f"What is the perimeter of a rectangle with length {length} and width {width}?",
                "solution": f"Perimeter = 2 × ({length} + {width}) = {2 * (length + width)}",
                "explanation": "Perimeter = 2 × (length + width)"
            }
        else:  # angles
            return {
                "problem": "What is the sum of angles in a triangle?",
                "solution": "180 degrees",
                "explanation": "The sum of interior angles in any triangle is always 180 degrees"
            }
    
    def _generate_calculus(self, concept: str) -> Dict:
        """Generate calculus problem"""
        if concept == "derivatives":
            n = np.random.randint(1, 4)
            return {
                "problem": f"What is the derivative of x^{n}?",
                "solution": f"{n}x^{n-1}",
                "explanation": f"Using power rule: d/dx(x^{n}) = {n}x^{n-1}"
            }
        elif concept == "integrals":
            n = np.random.randint(1, 4)
            return {
                "problem": f"What is the integral of x^{n}?",
                "solution": f"x^{n+1}/({n+1}) + C",
                "explanation": f"Using power rule: ∫x^{n}dx = x^{n+1}/({n+1}) + C"
            }
        else:  # limits
            return {
                "problem": "What is the limit of 1/x as x approaches infinity?",
                "solution": "0",
                "explanation": "As x gets very large, 1/x gets very small, approaching 0"
            }
    
    def _generate_proofs(self, concept: str) -> Dict:
        """Generate proof problem"""
        return {
            "problem": "Prove that the square root of 2 is irrational",
            "solution": "Proof by contradiction: Assume √2 is rational (p/q in lowest terms). Then p² = 2q², so p² is even, thus p is even. Write p = 2k. Then (2k)² = 2q² → 4k² = 2q² → 2k² = q², so q² is even, thus q is even. But p and q both even contradicts them being coprime. Therefore √2 is irrational.",
            "explanation": "This is a classic proof by contradiction"
        }
    
    def assess_response(self, problem: Dict, response: str) -> Dict:
        """
        Assess student's response to math problem
        
        Args:
            problem: The math problem
            response: Student's response
            
        Returns:
            Assessment with score and feedback
        """
        solution = problem["solution"]
        
        # Simple check: does response contain key parts of solution?
        response_lower = response.lower()
        solution_lower = solution.lower()
        
        # Extract numbers from both
        import re
        response_numbers = re.findall(r'\d+', response)
        solution_numbers = re.findall(r'\d+', solution)
        
        # Check if correct numbers are in response
        if solution_numbers:
            if any(num in solution_numbers for num in response_numbers):
                score = 1.0
                feedback = "Correct! Great job."
            else:
                score = 0.3
                feedback = f"Not quite. The answer is {solution}"
        else:
            # For non-numeric problems, check key phrases
            key_words = ["proof", "contradiction", "irrational", "rational"]
            if any(word in response_lower for word in key_words):
                score = 0.7
                feedback = "Good effort! " + problem["explanation"]
            else:
                score = 0.2
                feedback = f"Keep trying. {solution}"
        
        return {
            "score": score,
            "feedback": feedback,
            "correct_solution": solution,
            "explanation": problem["explanation"]
        }


class MathLearningBaby:
    """
    Baby chatbot that learns math from iFlow
    
    Progresses through math levels:
    1. Arithmetic
    2. Algebra
    3. Geometry
    4. Calculus
    5. Proofs
    """
    
    def __init__(
        self,
        n_intelligence_dim: int = 12,
        learning_rate: float = 0.05
    ):
        """
        Initialize math learning baby
        
        Args:
            n_intelligence_dim: Intelligence manifold dimension
            learning_rate: Learning rate
        """
        self.n_intelligence_dim = n_intelligence_dim
        self.learning_rate = learning_rate
        
        # Intelligence manifold
        self.intelligence_manifold = np.random.randn(n_intelligence_dim)
        self.intelligence_manifold = self.intelligence_manifold / np.linalg.norm(self.intelligence_manifold)
        
        # Math text generator
        self.text_generator = SimpleTextGenerator(
            skill_level=0.0,
            vocabulary=["math", "number", "solve", "equation"]
        )
        
        # Math-specific learning state
        self.math_level = 1  # Start with arithmetic
        self.math_skill: float = 0.0
        self.problems_solved = 0
        self.concepts_learned: List[str] = []
        
        # Math teacher (fallback)
        self.math_teacher = MathTeacher()
        
        # Learning history
        self.learning_history: List[Dict] = []
        
        print(f"\n  Math Learning Baby initialized:")
        print(f"    Math level: {self.math_level} (arithmetic)")
        print(f"    Math skill: {self.math_skill:.2f}")
        print(f"    Vocabulary: {len(self.text_generator.vocabulary)} words")
    
    def generate_response(self, math_problem: str) -> str:
        """
        Generate response to math problem
        
        Args:
            math_problem: Math problem prompt
            
        Returns:
            Generated response
        """
        # Update generator skill level
        self.text_generator.set_skill_level(self.math_skill)
        
        # Generate response using math-specific templates
        if self.math_level == 1:
            # Arithmetic: simple calculations
            return self._generate_arithmetic_response(math_problem)
        elif self.math_level == 2:
            # Algebra: solve for variables
            return self._generate_algebra_response(math_problem)
        elif self.math_level == 3:
            # Geometry: shapes and areas
            return self._generate_geometry_response(math_problem)
        elif self.math_level == 4:
            # Calculus: derivatives and integrals
            return self._generate_calculus_response(math_problem)
        else:
            # Proofs: logical reasoning
            return self._generate_proof_response(math_problem)
    
    def _generate_arithmetic_response(self, problem: str) -> str:
        """Generate arithmetic response"""
        # Extract numbers from problem
        numbers = re.findall(r'\d+', problem)
        
        if len(numbers) >= 2 and "+" in problem:
            a, b = int(numbers[0]), int(numbers[1])
            return f"{a} + {b} = {a + b}"
        elif len(numbers) >= 2 and "-" in problem:
            a, b = int(numbers[0]), int(numbers[1])
            return f"{a} - {b} = {a - b}"
        elif len(numbers) >= 2 and "×" in problem:
            a, b = int(numbers[0]), int(numbers[1])
            return f"{a} × {b} = {a * b}"
        elif len(numbers) >= 2 and "÷" in problem:
            a, b = int(numbers[0]), int(numbers[1])
            return f"{a} ÷ {b} = {a // b}"
        else:
            # Use learned examples
            if self.text_generator.learned_examples and random.random() < self.math_skill:
                return random.choice(self.text_generator.learned_examples)
            return "Let me solve this step by step."
    
    def _generate_algebra_response(self, problem: str) -> str:
        """Generate algebra response"""
        # Simple pattern matching
        if "x + " in problem and " = " in problem:
            # Extract equation: x + a = b
            match = re.search(r'x \+ (\d+) = (\d+)', problem)
            if match:
                a = int(match.group(1))
                b = int(match.group(2))
                return f"x = {b - a}"
        
        # Use learned examples
        if self.text_generator.learned_examples and random.random() < self.math_skill:
            return random.choice(self.text_generator.learned_examples)
        
        return "I need to solve for x."
    
    def _generate_geometry_response(self, problem: str) -> str:
        """Generate geometry response"""
        if "area" in problem.lower() and "rectangle" in problem.lower():
            match = re.search(r'length (\d+).*width (\d+)', problem)
            if match:
                length = int(match.group(1))
                width = int(match.group(2))
                return f"Area = {length} × {width} = {length * width}"
        
        if self.text_generator.learned_examples and random.random() < self.math_skill:
            return random.choice(self.text_generator.learned_examples)
        
        return "I need to calculate the area."
    
    def _generate_calculus_response(self, problem: str) -> str:
        """Generate calculus response"""
        if "derivative" in problem.lower() and "x^" in problem:
            match = re.search(r'x\^(\d+)', problem)
            if match:
                n = int(match.group(1))
                return f"{n}x^{n-1}"
        
        if self.text_generator.learned_examples and random.random() < self.math_skill:
            return random.choice(self.text_generator.learned_examples)
        
        return "I need to find the derivative."
    
    def _generate_proof_response(self, problem: str) -> str:
        """Generate proof response"""
        if "sqrt" in problem.lower() and "irrational" in problem.lower():
            return "This can be proven by contradiction. Assume √2 is rational..."
        
        if self.text_generator.learned_examples and random.random() < self.math_skill:
            return random.choice(self.text_generator.learned_examples)
        
        return "I need to construct a proof."
    
    def learn_from_teacher(
        self,
        teacher_feedback: str,
        correct_solution: str,
        explanation: str,
        skill_score: float
    ):
        """
        Learn from teacher's feedback
        
        Args:
            teacher_feedback: Teacher's feedback
            correct_solution: Correct solution
            explanation: Explanation of solution
            skill_score: New skill score
        """
        # Update math skill
        self.math_skill = skill_score
        
        # Learn from solution and explanation
        self.text_generator.learn_from_example(correct_solution)
        self.text_generator.learn_from_example(explanation)
        self.text_generator.learn_from_example(teacher_feedback)
        
        # Update intelligence manifold
        teacher_embedding = self._extract_embedding(teacher_feedback + " " + explanation)
        adaptive_lr = self.learning_rate * (1 - self.math_skill * 0.5)
        self.intelligence_manifold = (
            (1 - adaptive_lr) * self.intelligence_manifold +
            adaptive_lr * teacher_embedding[:self.n_intelligence_dim]
        )
        self.intelligence_manifold = self.intelligence_manifold / np.linalg.norm(self.intelligence_manifold)
        
        # Check for level progression
        if self.math_skill >= 0.2 and self.math_level == 1:
            self.math_level = 2
            print(f"    Level up! Now learning algebra")
        elif self.math_skill >= 0.4 and self.math_level == 2:
            self.math_level = 3
            print(f"    Level up! Now learning geometry")
        elif self.math_skill >= 0.6 and self.math_level == 3:
            self.math_level = 4
            print(f"    Level up! Now learning calculus")
        elif self.math_skill >= 0.8 and self.math_level == 4:
            self.math_level = 5
            print(f"    Level up! Now learning proofs")
        
        self.problems_solved += 1
        
        print(f"    Math skill: {self.math_skill:.2f}")
        print(f"    Math level: {self.math_level}/5")
        print(f"    Problems solved: {self.problems_solved}")
    
    def _extract_embedding(self, text: str) -> np.ndarray:
        """Extract simple embedding from text"""
        words = text.split()
        embedding = np.zeros(12)
        
        for i, word in enumerate(words):
            word_hash = hash(word)
            idx = abs(word_hash) % 12
            embedding[idx] += 1.0
        
        return embedding / (np.linalg.norm(embedding) + 1e-10)
    
    def get_math_status(self) -> Dict:
        """Get current math learning status"""
        level_names = ["arithmetic", "algebra", "geometry", "calculus", "proofs"]
        return {
            "math_level": self.math_level,
            "level_name": level_names[self.math_level - 1],
            "math_skill": self.math_skill,
            "problems_solved": self.problems_solved,
            "vocabulary_size": len(self.text_generator.vocabulary),
            "learned_examples": len(self.text_generator.learned_examples)
        }


def demo_math_learning():
    """Demonstrate math learning with iFlow as teacher"""
    print("\n" + "="*80)
    print("MATH LEARNING DEMO: Baby learns math from iFlow")
    print("="*80)
    print("\nThis demo shows progressive math learning:")
    print("  1. Arithmetic (level 1)")
    print("  2. Algebra (level 2)")
    print("  3. Geometry (level 3)")
    print("  4. Calculus (level 4)")
    print("  5. Proofs (level 5)")
    
    # Create math learning baby
    baby = MathLearningBaby(n_intelligence_dim=12, learning_rate=0.05)
    
    # Create math teacher
    teacher = MathTeacher()
    
    # Simulate learning iterations
    print("\nStarting math learning with iFlow as teacher...\n")
    
    for i in range(20):
        # Get math problem based on current level
        problem = teacher.get_math_problem(baby.math_level)
        
        # Baby generates response
        print(f"Problem {i+1}: {problem['problem']}")
        response = baby.generate_response(problem['problem'])
        print(f"  Baby: {response}")
        
        # Teacher assesses
        assessment = teacher.assess_response(problem, response)
        print(f"  iFlow: {assessment['feedback']}")
        
        # Baby learns
        baby.learn_from_teacher(
            assessment['feedback'],
            assessment['correct_solution'],
            assessment['explanation'],
            min(1.0, 0.05 + i * 0.05)  # Progressive skill
        )
        print()
    
    # Final status
    print("="*80)
    print("LEARNING COMPLETE")
    print("="*80)
    
    status = baby.get_math_status()
    print(f"\nFinal math level: {status['level_name']} (level {status['math_level']}/5)")
    print(f"Math skill: {status['math_skill']:.2f}")
    print(f"Problems solved: {status['problems_solved']}")
    print(f"Vocabulary: {status['vocabulary_size']} words")
    
    # Test final math skills
    print("\nTesting final math skills:")
    test_problems = [
        teacher.get_math_problem(1),  # Arithmetic
        teacher.get_math_problem(2),  # Algebra
        teacher.get_math_problem(3),  # Geometry
        teacher.get_math_problem(4),  # Calculus
        teacher.get_math_problem(5)   # Proofs
    ]
    
    for test_problem in test_problems:
        print(f"\n  {test_problem['problem']}")
        response = baby.generate_response(test_problem['problem'])
        print(f"  Baby: {response}")
        print(f"  Solution: {test_problem['solution']}")


if __name__ == "__main__":
    demo_math_learning()

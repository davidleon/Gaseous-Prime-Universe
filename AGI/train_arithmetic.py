"""
Arithmetic Training for Evolving Chat Bot

Trains the bot on basic arithmetic operations:
- Addition (+)
- Subtraction (-)
- Multiplication (*)
- Division (/)
- Parentheses ()
- Exponentiation (^)
- Modulo (%)

This helps the bot learn to perform and understand arithmetic calculations.
"""

import random
import sys
import os

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evolving_chat_bot import EvolvingChatBot
from manifold.semantic_text_generator import SemanticTextGenerator


def generate_arithmetic_problem(difficulty=1):
    """
    Generate an arithmetic problem based on difficulty
    
    Args:
        difficulty: 1 (easy), 2 (medium), 3 (hard)
    
    Returns:
        Tuple of (problem_str, answer_str)
    """
    operators = ['+', '-', '*', '/', '^', '%']
    
    if difficulty == 1:
        # Easy: single operation with small numbers
        op = random.choice(['+', '-', '*'])
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        
        if op == '/':
            b = random.randint(1, 10)
            a = b * random.randint(1, 10)  # Ensure clean division
        
        problem = f"{a}{op}{b}"
        answer = str(eval(problem))
        
    elif difficulty == 2:
        # Medium: two operations with parentheses
        op1 = random.choice(['+', '-', '*', '/'])
        op2 = random.choice(['+', '-', '*', '/'])
        
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        c = random.randint(1, 20)
        
        if op1 == '/' or op2 == '/':
            # Ensure clean division
            b = random.randint(1, 10)
            c = random.randint(1, 10)
            if op1 == '/':
                a = b * random.randint(1, 5)
            if op2 == '/':
                if random.random() < 0.5:
                    b = c * random.randint(1, 5)
                else:
                    a = c * random.randint(1, 5)
        
        problem = f"({a}{op1}{b}){op2}{c}"
        answer = str(eval(problem))
        
    else:
        # Hard: three operations with mixed complexity
        ops = random.choices(['+', '-', '*', '/', '^', '%'], k=3)
        
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        c = random.randint(1, 10)
        d = random.randint(1, 10)
        
        # Adjust for special operations
        for i, op in enumerate(ops):
            if op == '/':
                if i == 0:
                    a = b * random.randint(1, 5)
                elif i == 1:
                    b = c * random.randint(1, 5)
                else:
                    c = d * random.randint(1, 5)
            elif op == '%':
                if i == 0:
                    b = random.randint(1, 5)
                elif i == 1:
                    c = random.randint(1, 5)
                else:
                    d = random.randint(1, 5)
            elif op == '^':
                if i == 0:
                    a = random.randint(1, 3)
                elif i == 1:
                    b = random.randint(1, 3)
                else:
                    c = random.randint(1, 3)
        
        problem = f"(({a}{ops[0]}{b}){ops[1]}{c}){ops[2]}{d}"
        try:
            answer = str(eval(problem))
        except:
            # Fallback to simpler problem if error
            return generate_arithmetic_problem(difficulty=2)
    
    return problem, answer


def train_arithmetic(bot, num_problems=500, save_path=None):
    """
    Train bot on arithmetic problems with focused training
    
    Args:
        bot: EvolvingChatBot instance
        num_problems: Number of problems to train on
        save_path: Path to save bot state after training
    """
    print("=" * 60)
    print("Arithmetic Training")
    print("=" * 60)
    print(f"\nTraining on {num_problems} arithmetic problems...")
    print("Operators: +, -, *, /, (, ), ^, %")
    
    # Clear previous training bias by reinitializing autoencoder decoder
    bot.autoencoder.decoder = SemanticTextGenerator(bot.manifold_dim)
    
    correct_count = 0
    incorrect_responses = []
    
    # Train in batches for better learning
    batch_size = 50
    
    for batch_start in range(0, num_problems, batch_size):
        batch_problems = []
        
        # Generate batch of problems
        for i in range(batch_start, min(batch_start + batch_size, num_problems)):
            # Vary difficulty
            if i < num_problems * 0.5:
                difficulty = 1
            elif i < num_problems * 0.8:
                difficulty = 2
            else:
                difficulty = 3
            
            # Generate problem
            problem, correct_answer = generate_arithmetic_problem(difficulty)
            batch_problems.append((problem, correct_answer))
        
        # Train on batch
        for problem, correct_answer in batch_problems:
            # Format as equation (main training format)
            input_text = f"{problem}={correct_answer}"
            
            # Train encoder heavily on arithmetic
            bot.trainer.train_with_adaptive_repetition(input_text)
            
            # Multiple repetitions for better learning
            for _ in range(3):
                bot.trainer.learner.train_on_proof(input_text)
            
            # Add to autoencoder decoder
            manifold = bot.trainer.learner.encode_text(input_text)
            bot.autoencoder.decoder.add_text(input_text, manifold)
            
            # Also train query format
            query_text = f"Calculate: {problem}"
            bot.trainer.train_with_adaptive_repetition(query_text)
            bot.trainer.learner.train_on_proof(query_text)
            
            # Add query to decoder
            query_manifold = bot.trainer.learner.encode_text(query_text)
            bot.autoencoder.decoder.add_text(query_text, query_manifold)
        
        # Test the batch
        batch_correct = 0
        for problem, correct_answer in batch_problems:
            query_text = f"Calculate: {problem}"
            response = bot.autoencoder.compose(query_text)
            
            if correct_answer in response:
                batch_correct += 1
                correct_count += 1
            else:
                incorrect_responses.append((problem, correct_answer, response))
        
        # Progress update
        progress = min(batch_start + batch_size, num_problems)
        accuracy = correct_count / progress
        print(f"  Progress: {progress}/{num_problems} | Accuracy: {accuracy:.1%} | Batch accuracy: {batch_correct/len(batch_problems):.1%}")
    
    # Final statistics
    final_accuracy = correct_count / num_problems
    print(f"\n{'=' * 60}")
    print("Training Complete!")
    print(f"{'=' * 60}")
    print(f"Problems trained: {num_problems}")
    print(f"Correct responses: {correct_count}")
    print(f"Accuracy: {final_accuracy:.1%}")
    
    if incorrect_responses:
        print(f"\nSample incorrect responses:")
        for problem, answer, response in incorrect_responses[:5]:
            print(f"  Problem: {problem}")
            print(f"  Correct: {answer}")
            print(f"  Response: {response[:100]}...")
            print()
    
    # Save if path provided
    if save_path:
        bot.save_state(save_path)
        print(f"✓ Bot state saved to: {save_path}")
    
    # Test on new problems
    print(f"\nTesting on new arithmetic problems:")
    test_problems = 10
    test_correct = 0
    
    for _ in range(test_problems):
        problem, answer = generate_arithmetic_problem(difficulty=2)
        input_text = f"Calculate: {problem}"
        response = bot.autoencoder.compose(input_text)
        
        if answer in response:
            test_correct += 1
            print(f"  ✓ {problem} → {answer} (correct)")
        else:
            print(f"  ✗ {problem} → {response[:50]}... (expected {answer})")
    
    test_accuracy = test_correct / test_problems
    print(f"\nTest accuracy: {test_accuracy:.1%}")
    
    return final_accuracy


def main():
    """Main training function"""
    # Create bot instance
    bot = EvolvingChatBot(
        name="EVA",
        manifold_dim=12,
        quiet=True,
        load_chinese_bitstream=True
    )
    
    # Train arithmetic
    save_path = "/home/davidl/Gaseous Prime Universe/AGI/learning_sessions/arithmetic_trained_bot.npz"
    train_arithmetic(bot, num_problems=500, save_path=save_path)


if __name__ == "__main__":
    main()
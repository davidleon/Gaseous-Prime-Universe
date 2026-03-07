"""
iFlow CLI Integration for Interactive Learning
Shows how to use iFlow as teacher for baby chatbot
"""

import subprocess
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interactive_learning import BabyChatbot, InteractiveLearningSystem


class iFlowTeacher:
    """
    Wrapper for using iFlow CLI as teacher
    
    Sends teaching prompts to iFlow and processes responses
    """
    
    def __init__(
        self,
        iflow_command: str = "iflow",
        timeout: int = 60
    ):
        """
        Initialize iFlow teacher
        
        Args:
            iflow_command: Command to invoke iFlow
            timeout: Timeout for iFlow response (seconds)
        """
        self.iflow_command = iflow_command
        self.timeout = timeout
        
        print(f"\n  iFlow Teacher initialized:")
        print(f"    Command: {iflow_command}")
        print(f"    Timeout: {timeout}s")
    
    def send_teaching_prompt(
        self,
        teaching_prompt: str
    ) -> str:
        """
        Send teaching prompt to iFlow and get response
        
        Args:
            teaching_prompt: Teaching prompt for iFlow
            
        Returns:
            iFlow's response
        """
        print(f"\n  Sending teaching prompt to iFlow...")
        print(f"  Prompt length: {len(teaching_prompt)} characters")
        
        try:
            # Execute iFlow command with prompt
            result = subprocess.run(
                [self.iflow_command],
                input=teaching_prompt,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if result.returncode == 0:
                response = result.stdout
                print(f"  iFlow response received: {len(response)} characters")
                return response
            else:
                print(f"  iFlow error: {result.stderr}")
                # Fallback response
                return json.dumps({
                    "assessment": "iFlow unavailable, using fallback",
                    "skill_score": 0.5,
                    "teaching_material": "Keep learning and practicing!",
                    "examples": ["Hello", "Learning", "Practice"],
                    "next_prompt": "Continue"
                })
                
        except subprocess.TimeoutExpired:
            print(f"  iFlow timeout after {self.timeout}s")
            # Fallback response
            return json.dumps({
                "assessment": "iFlow timeout, using fallback",
                "skill_score": 0.5,
                "teaching_material": "Keep learning and practicing!",
                "examples": ["Hello", "Learning", "Practice"],
                "next_prompt": "Continue"
            })
        except Exception as e:
            print(f"  iFlow error: {e}")
            # Fallback response
            return json.dumps({
                "assessment": f"iFlow error ({e}), using fallback",
                "skill_score": 0.5,
                "teaching_material": "Keep learning and practicing!",
                "examples": ["Hello", "Learning", "Practice"],
                "next_prompt": "Continue"
            })


def run_interactive_learning_with_iflow(
    n_iterations: int = 10,
    prompts: Optional[List[str]] = None
):
    """
    Run interactive learning with iFlow as teacher
    
    Args:
        n_iterations: Number of learning iterations
        prompts: List of prompts for baby (auto-generated if None)
    """
    print("\n" + "=" * 80)
    print("INTERACTIVE LEARNING WITH iFLOW")
    print("=" * 80)
    print("\nThis runs the baby chatbot learning system with iFlow as teacher.")
    print("iFlow will be prompted to assess the baby and provide teaching material.")
    
    # Create baby chatbot
    print("\n[1] Creating baby chatbot...")
    baby = BabyChatbot(
        n_intelligence_dim=12,
        n_text_dim=768,
        initial_vocabulary_size=100,
        learning_rate=0.05
    )
    
    # Create learning system
    print("[2] Creating learning system...")
    learning_system = InteractiveLearningSystem(
        baby=baby,
        teacher_name="iFlow",
        max_iterations=n_iterations
    )
    
    # Create iFlow teacher
    print("[3] Creating iFlow teacher...")
    iflow_teacher = iFlowTeacher(iflow_command="iflow", timeout=60)
    
    # Generate prompts if not provided
    if prompts is None:
        prompts = [
            "Hello!",
            "What is machine learning?",
            "Tell me about neural networks",
            "Explain deep learning",
            "What is natural language processing?",
            "How do computers learn?",
            "What is artificial intelligence?",
            "Explain computer vision",
            "What is reinforcement learning?",
            "Tell me about transformers"
        ]
    
    # Run learning iterations
    print(f"\n[4] Starting interactive learning ({n_iterations} iterations)...\n")
    
    for i in range(min(n_iterations, len(prompts))):
        prompt = prompts[i]
        
        # Step 1: Baby generates response
        baby_response = baby.generate_response(prompt)
        print(f"\nIteration {i+1}/{n_iterations}")
        print(f"  Prompt: '{prompt}'")
        print(f"  Baby: '{baby_response}'")
        
        # Step 2: Create teaching prompt for iFlow
        skill = baby.get_skill_level()
        teaching_prompt = learning_system.create_teaching_prompt(
            baby_response,
            skill['skill_level'],
            i + 1
        )
        
        # Step 3: Send to iFlow
        print(f"  Asking iFlow to assess and teach...")
        iflow_response = iflow_teacher.send_teaching_prompt(teaching_prompt)
        
        # Step 4: Process iFlow response
        teacher_data = learning_system.process_teacher_response(iflow_response)
        print(f"  iFlow assessment: {teacher_data['assessment'][:50]}...")
        print(f"  Skill score: {teacher_data['skill_score']:.2f}")
        
        # Step 5: Baby learns
        baby.learn_from_teacher(
            teacher_data['teaching_material'],
            teacher_data['assessment'],
            teacher_data['skill_score']
        )
        
        # Step 6: Store in history
        learning_system.dialogue_history.append({
            "iteration": i + 1,
            "baby_prompt": prompt,
            "baby_response": baby_response,
            "teacher_response": iflow_response,
            "teacher_data": teacher_data,
            "skill_before": skill['skill_level'],
            "skill_after": baby.get_skill_level()['skill_level']
        })
        
        # Step 7: Get next prompt
        next_prompt = teacher_data.get('next_prompt', prompts[i+1] if i+1 < len(prompts) else "Continue")
    
    # Save session
    print("\n[5] Saving learning session...")
    learning_system.save_session()
    
    # Final assessment
    final_skill = baby.get_skill_level()
    print("\n" + "=" * 80)
    print("LEARNING COMPLETE")
    print("=" * 80)
    print(f"\nFinal skill level: {final_skill['skill_level']:.2f}")
    print(f"Learning iterations: {final_skill['learning_iterations']}")
    print(f"Vocabulary size: {final_skill['vocabulary_size']}")
    print(f"Max sequence: {final_skill['max_sequence_length']} words")
    
    # Test final response
    print("\n[6] Testing final response...")
    test_prompt = "What have you learned today?"
    final_response = baby.generate_response(test_prompt)
    print(f"  Prompt: '{test_prompt}'")
    print(f"  Response: '{final_response}'")
    
    return learning_system


def manual_learning_session():
    """
    Manual learning session where user acts as teacher
    
    Useful for testing without iFlow integration
    """
    print("\n" + "=" * 80)
    print("MANUAL LEARNING SESSION (User as Teacher)")
    print("=" * 80)
    print("\nYou will act as the teacher. iFlow will not be called.")
    print("For each iteration, provide your assessment and teaching material.")
    
    # Create baby chatbot
    baby = BabyChatbot()
    learning_system = InteractiveLearningSystem(baby, teacher_name="You", max_iterations=5)
    
    prompts = [
        "Hello!",
        "What is AI?",
        "Tell me about learning",
        "Explain neural networks",
        "What have you learned?"
    ]
    
    for i, prompt in enumerate(prompts):
        print(f"\n{'=' * 80}")
        print(f"ITERATION {i+1}")
        print(f"{'=' * 80}")
        
        # Baby generates response
        baby_response = baby.generate_response(prompt)
        print(f"\nBaby: '{baby_response}'")
        
        # User provides teaching
        print("\nPlease provide your assessment and teaching (JSON format):")
        print("Example:")
        print(json.dumps({
            "assessment": "Baby is doing well!",
            "skill_score": 0.3,
            "teaching_material": "AI is the study of intelligent machines.",
            "examples": ["AI learns", "Machines think"],
            "next_prompt": "Continue"
        }, indent=2))
        
        teacher_input = input("\nYour response (JSON): ")
        
        # Process and learn
        try:
            result = learning_system.learning_iteration(prompt, teacher_input)
            print(f"\n  Baby's skill increased to: {result['skill_level']:.2f}")
        except Exception as e:
            print(f"\n  Error: {e}")
            print("  Using fallback...")
            fallback_response = json.dumps({
                "assessment": "Good effort!",
                "skill_score": 0.2 + i * 0.1,
                "teaching_material": "Keep learning!",
                "examples": ["Hello", "Learn"],
                "next_prompt": prompts[i+1] if i+1 < len(prompts) else "Continue"
            })
            result = learning_system.learning_iteration(prompt, fallback_response)
    
    # Save session
    learning_system.save_session("learning_sessions/manual_session.json")
    
    print("\n" + "=" * 80)
    print("MANUAL SESSION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    print("\nChoose mode:")
    print("  1. Manual learning (you as teacher)")
    print("  2. iFlow integration (iflow as teacher)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        manual_learning_session()
    elif choice == "2":
        run_interactive_learning_with_iflow(n_iterations=5)
    else:
        print("\nInvalid choice. Running manual session...")
        manual_learning_session()
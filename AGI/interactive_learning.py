"""
Interactive Learning System: Baby Chatbot learns from iFlow
Lifelong communication-based learning instead of immediate distillation
"""

import numpy as np
import json
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from manifold.text_decoder_manifold import TextDecoderManifold
from manifold.text_generation_bridge import TextGenerationBridge


class BabyChatbot:
    """
    Baby chatbot that learns through interaction with iFlow
    
    Starts with minimal knowledge and learns through dialogue
    """
    
    def __init__(
        self,
        n_intelligence_dim: int = 12,
        n_text_dim: int = 768,
        initial_vocabulary_size: int = 100,  # Start small
        learning_rate: float = 0.01
    ):
        """
        Initialize baby chatbot
        
        Args:
            n_intelligence_dim: Intelligence manifold dimension
            n_text_dim: Text embedding dimension
            initial_vocabulary_size: Starting vocabulary size (small)
            learning_rate: Learning rate for updates
        """
        self.n_intelligence_dim = n_intelligence_dim
        self.n_text_dim = n_text_dim
        self.learning_rate = learning_rate
        
        # Intelligence manifold (starts random, like a baby's mind)
        self.intelligence_manifold = np.random.randn(n_intelligence_dim)
        self.intelligence_manifold = self.intelligence_manifold / np.linalg.norm(self.intelligence_manifold)
        
        # Text decoder (starts with minimal vocabulary)
        self.text_decoder = TextDecoderManifold(
            n_intelligence_dim=n_intelligence_dim,
            n_text_dim=n_text_dim,
            n_clusters=100,  # Start with small clusters
            vocab_size=initial_vocabulary_size,
            max_sequence_length=50,  # Start with short sequences
            temperature=0.9  # High temperature = more exploratory
        )
        
        # Learning history
        self.dialogue_history: List[Dict] = []
        self.skill_level: float = 0.0  # 0.0 = newborn, 1.0 = expert
        self.learning_iterations: int = 0
        
        print(f"\n  Baby Chatbot initialized:")
        print(f"    Skill level: {self.skill_level:.2f} (newborn)")
        print(f"    Vocabulary size: {initial_vocabulary_size} words")
        print(f"    Max sequence: 50 words")
        print(f"    Temperature: 0.9 (exploratory)")
    
    def generate_response(self, prompt: str) -> str:
        """
        Generate response to prompt (like a baby trying to respond)
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated response
        """
        if not self.text_decoder.trained:
            # Baby can't speak yet, make random sounds
            return self._make_baby_sounds()
        
        # Use text decoder to generate
        # Map prompt to intelligence manifold
        prompt_manifold = self._prompt_to_manifold(prompt)
        
        # Combine with current intelligence
        combined_manifold = 0.7 * self.intelligence_manifold + 0.3 * prompt_manifold
        combined_manifold = combined_manifold / np.linalg.norm(combined_manifold)
        
        # Generate response
        response = self.text_decoder.decode(
            combined_manifold,
            max_length=int(50 + self.skill_level * 100)  # Grow with skill
        )
        
        return response
    
    def _make_baby_sounds(self) -> str:
        """Make random baby-like sounds when untrained"""
        sounds = ["ba", "da", "ma", "pa", "ga", "na", "ta", "ka"]
        n_sounds = np.random.randint(1, 4)
        return " ".join(np.random.choice(sounds, n_sounds))
    
    def _prompt_to_manifold(self, prompt: str) -> np.ndarray:
        """Map prompt to manifold (simple hash-based for now)"""
        # Use prompt hash to create deterministic manifold
        prompt_hash = hash(prompt)
        manifold = np.array([
            (prompt_hash >> i) & 1 for i in range(self.n_intelligence_dim)
        ], dtype=float)
        manifold = manifold - 0.5  # Center around 0
        return manifold / np.linalg.norm(manifold)
    
    def learn_from_teacher(
        self,
        teacher_response: str,
        teacher_assessment: Optional[str] = None,
        skill_score: Optional[float] = None
    ):
        """
        Learn from teacher's response and assessment
        
        Args:
            teacher_response: Teacher's response (teaching material)
            teacher_assessment: Teacher's assessment of baby's skill
            skill_score: Numerical skill score (0-1)
        """
        print(f"\n  Baby learning from teacher...")
        
        # Update skill level
        if skill_score is not None:
            self.skill_level = skill_score
        
        # Add teacher's response to vocabulary
        self.text_decoder.initialize_vocabulary(
            [teacher_response],
            use_embeddings=False
        )
        
        # Extract text embedding from teacher response
        teacher_embedding = self._extract_text_embedding(teacher_response)
        
        # Update intelligence manifold (move towards teacher)
        # Learning rate decreases as skill increases (diminishing returns)
        adaptive_lr = self.learning_rate * (1 - self.skill_level * 0.5)
        self.intelligence_manifold = (
            (1 - adaptive_lr) * self.intelligence_manifold +
            adaptive_lr * teacher_embedding[:self.n_intelligence_dim]
        )
        self.intelligence_manifold = self.intelligence_manifold / np.linalg.norm(self.intelligence_manifold)
        
        # Grow vocabulary with skill
        new_vocab_size = int(100 + self.skill_level * 49000)  # 100 → 50000
        self.text_decoder.vocab_size = new_vocab_size
        
        # Grow max sequence length with skill
        new_max_length = int(50 + self.skill_level * 462)  # 50 → 512
        self.text_decoder.max_sequence_length = new_max_length
        
        # Adjust temperature (become more focused as skill increases)
        self.text_decoder.temperature = 0.9 - self.skill_level * 0.2  # 0.9 → 0.7
        
        self.learning_iterations += 1
        
        print(f"    Skill level: {self.skill_level:.2f}")
        print(f"    Vocabulary: {new_vocab_size} words")
        print(f"    Max sequence: {new_max_length} words")
        print(f"    Temperature: {self.text_decoder.temperature:.2f}")
    
    def _extract_text_embedding(self, text: str) -> np.ndarray:
        """Extract simple text embedding"""
        # Simple hash-based embedding (replace with sentence embeddings)
        words = text.split()
        embedding = np.zeros(self.n_text_dim)
        
        for i, word in enumerate(words):
            word_hash = hash(word)
            idx = abs(word_hash) % self.n_text_dim
            embedding[idx] += 1.0
        
        # Normalize
        embedding = embedding / (np.linalg.norm(embedding) + 1e-10)
        
        return embedding
    
    def get_skill_level(self) -> Dict:
        """Get current skill level"""
        return {
            "skill_level": self.skill_level,
            "learning_iterations": self.learning_iterations,
            "vocabulary_size": self.text_decoder.vocab_size,
            "max_sequence_length": self.text_decoder.max_sequence_length,
            "temperature": self.text_decoder.temperature
        }


class InteractiveLearningSystem:
    """
    Manages interactive learning between baby chatbot and iFlow teacher
    """
    
    def __init__(
        self,
        baby: BabyChatbot,
        teacher_name: str = "iFlow",
        max_iterations: int = 100
    ):
        """
        Initialize interactive learning system
        
        Args:
            baby: Baby chatbot instance
            teacher_name: Name of the teacher (iFlow)
            max_iterations: Maximum learning iterations
        """
        self.baby = baby
        self.teacher_name = teacher_name
        self.max_iterations = max_iterations
        
        # Learning session data
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.dialogue_history: List[Dict] = []
        self.iteration: int = 0
        
        print(f"\n  Interactive Learning System initialized:")
        print(f"    Teacher: {teacher_name}")
        print(f"    Max iterations: {max_iterations}")
        print(f"    Session ID: {self.session_id}")
    
    def create_teaching_prompt(
        self,
        baby_response: str,
        skill_level: float,
        iteration: int
    ) -> str:
        """
        Create prompt for iFlow teacher to assess and teach
        
        Args:
            baby_response: Baby's response
            skill_level: Baby's current skill level
            iteration: Current iteration number
            
        Returns:
            Teaching prompt for iFlow
        """
        prompt = f"""You are {self.teacher_name}, an AI teacher teaching a baby chatbot.

CURRENT SITUATION:
- Iteration: {iteration} / {self.max_iterations}
- Baby's skill level: {skill_level:.2f} (0.0 = newborn, 1.0 = expert)
- Baby's response: "{baby_response}"

YOUR TASK:
1. Assess the baby's response (is it meaningful? coherent? appropriate?)
2. Generate teaching material appropriate for this skill level
3. If baby's response is garbage, generate 10 simple daily language examples
4. If baby shows some skill, provide more complex examples
5. Always be encouraging and patient

RESPONSE FORMAT (JSON):
{{
    "assessment": "Your assessment of baby's response",
    "skill_score": 0.0 to 1.0,
    "teaching_material": "Your teaching text",
    "examples": ["example1", "example2", ...],
    "next_prompt": "Suggested next prompt for baby"
}}

Generate your response now:"""
        
        return prompt
    
    def process_teacher_response(
        self,
        teacher_response: str
    ) -> Dict:
        """
        Process teacher's response
        
        Args:
            teacher_response: Teacher's response (JSON format)
            
        Returns:
            Parsed teacher response
        """
        try:
            # Parse JSON response
            teacher_data = json.loads(teacher_response)
            
            return {
                "assessment": teacher_data.get("assessment", ""),
                "skill_score": teacher_data.get("skill_score", 0.0),
                "teaching_material": teacher_data.get("teaching_material", ""),
                "examples": teacher_data.get("examples", []),
                "next_prompt": teacher_data.get("next_prompt", "")
            }
        except json.JSONDecodeError:
            # Fallback: extract key information
            return {
                "assessment": "Could not parse teacher response",
                "skill_score": 0.0,
                "teaching_material": teacher_response,
                "examples": [],
                "next_prompt": "Continue learning"
            }
    
    def learning_iteration(
        self,
        baby_prompt: str,
        teacher_response: Optional[str] = None
    ) -> Dict:
        """
        Perform one learning iteration
        
        Args:
            baby_prompt: Prompt for baby
            teacher_response: Optional teacher response (if None, will be requested)
            
        Returns:
            Iteration results
        """
        print(f"\n{'=' * 80}")
        print(f"ITERATION {self.iteration + 1} / {self.max_iterations}")
        print(f"{'=' * 80}")
        
        # Step 1: Baby generates response
        print(f"\n[1] Baby generating response to: '{baby_prompt}'")
        baby_response = self.baby.generate_response(baby_prompt)
        print(f"  Baby says: \"{baby_response}\"")
        
        # Step 2: Create teaching prompt for iFlow
        skill = self.baby.get_skill_level()
        teaching_prompt = self.create_teaching_prompt(
            baby_response,
            skill['skill_level'],
            self.iteration + 1
        )
        
        # Step 3: Get teacher response (if not provided)
        if teacher_response is None:
            print(f"\n[2] Waiting for teacher ({self.teacher_name}) response...")
            print(f"  Teaching prompt prepared (see below)")
            print(f"\n{teaching_prompt}\n")
            print(f"  Please provide teacher's response:")
            teacher_response = input("  > ")
        
        # Step 4: Process teacher response
        print(f"\n[3] Processing teacher response...")
        teacher_data = self.process_teacher_response(teacher_response)
        
        print(f"  Assessment: {teacher_data['assessment']}")
        print(f"  Skill score: {teacher_data['skill_score']:.2f}")
        
        # Step 5: Baby learns from teacher
        print(f"\n[4] Baby learning from teacher...")
        self.baby.learn_from_teacher(
            teacher_data['teaching_material'],
            teacher_data['assessment'],
            teacher_data['skill_score']
        )
        
        # Step 6: Store dialogue history
        self.dialogue_history.append({
            "iteration": self.iteration + 1,
            "baby_prompt": baby_prompt,
            "baby_response": baby_response,
            "teacher_response": teacher_response,
            "teacher_data": teacher_data,
            "skill_before": skill['skill_level'],
            "skill_after": self.baby.get_skill_level()
        })
        
        # Step 7: Get next prompt
        next_prompt = teacher_data.get('next_prompt', 'Tell me something')
        
        self.iteration += 1
        
        return {
            "baby_response": baby_response,
            "teacher_data": teacher_data,
            "next_prompt": next_prompt,
            "skill_level": self.baby.get_skill_level()
        }
    
    def save_session(self, filepath: Optional[str] = None):
        """
        Save learning session
        
        Args:
            filepath: Path to save (auto-generated if None)
        """
        if filepath is None:
            filepath = f"learning_sessions/session_{self.session_id}.json"
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        session_data = {
            "session_id": self.session_id,
            "teacher_name": self.teacher_name,
            "max_iterations": self.max_iterations,
            "iteration": self.iteration,
            "dialogue_history": self.dialogue_history,
            "final_skill": self.baby.get_skill_level(),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"\n  Session saved to: {filepath}")
    
    def load_session(self, filepath: str):
        """
        Load learning session
        
        Args:
            filepath: Path to session file
        """
        with open(filepath, 'r') as f:
            session_data = json.load(f)
        
        self.session_id = session_data['session_id']
        self.dialogue_history = session_data['dialogue_history']
        self.iteration = session_data['iteration']
        
        print(f"\n  Session loaded from: {filepath}")
        print(f"  Resuming from iteration {self.iteration}")


def create_demo_learning_session():
    """Create and run demo learning session"""
    print("\n" + "=" * 80)
    print("INTERACTIVE LEARNING DEMO")
    print("=" * 80)
    print("\nThis demo shows a baby chatbot learning through interaction")
    print("with iFlow as teacher.")
    print("\nKey features:")
    print("  • Baby starts with minimal knowledge (like a newborn)")
    print("  • iFlow teaches through dialogue and examples")
    print("  • Baby's skill level increases over iterations")
    print("  • Vocabulary and complexity grow with skill")
    print("  • Natural lifelong learning process")
    
    # Create baby chatbot
    print("\nCreating baby chatbot...")
    baby = BabyChatbot(
        n_intelligence_dim=12,
        n_text_dim=768,
        initial_vocabulary_size=100,
        learning_rate=0.05
    )
    
    # Create learning system
    learning_system = InteractiveLearningSystem(
        baby=baby,
        teacher_name="iFlow",
        max_iterations=10  # Demo: 10 iterations
    )
    
    # Simulate learning iterations
    print("\nStarting interactive learning...\n")
    
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
    
    for i, prompt in enumerate(prompts[:learning_system.max_iterations]):
        # Simulate teacher response
        if i < 3:
            # Early stage: simple teaching
            teacher_response = json.dumps({
                "assessment": "Baby is making random sounds, needs basic vocabulary",
                "skill_score": 0.1 + i * 0.1,
                "teaching_material": f"Let's learn about {prompt.lower().replace('?', '')}. This is important in AI.",
                "examples": [
                    "Hello, how are you?",
                    "Machine learning teaches computers",
                    "Neural networks learn patterns",
                    "Deep learning has many layers",
                    "Language processing understands text"
                ],
                "next_prompt": prompts[i+1] if i+1 < len(prompts) else "What did you learn?"
            })
        else:
            # Later stage: more complex teaching
            teacher_response = json.dumps({
                "assessment": f"Baby is forming basic sentences, getting better",
                "skill_score": 0.4 + i * 0.05,
                "teaching_material": f"Good! {prompt} is a key concept. Let me explain it in more detail.",
                "examples": [
                    "Neural networks use interconnected layers",
                    "Deep learning extracts hierarchical features",
                    "Transformers use self-attention mechanisms",
                    "Reinforcement learning learns through rewards",
                    "Computer vision interprets visual data"
                ],
                "next_prompt": prompts[i+1] if i+1 < len(prompts) else "Summarize what you learned"
            })
        
        # Perform iteration
        result = learning_system.learning_iteration(prompt, teacher_response)
        
        print(f"\n  Next prompt: {result['next_prompt']}")
    
    # Save session
    learning_system.save_session()
    
    # Final assessment
    final_skill = baby.get_skill_level()
    print("\n" + "=" * 80)
    print("LEARNING SESSION COMPLETE")
    print("=" * 80)
    print(f"\nFinal skill level: {final_skill['skill_level']:.2f}")
    print(f"Learning iterations: {final_skill['learning_iterations']}")
    print(f"Vocabulary size: {final_skill['vocabulary_size']}")
    print(f"Max sequence: {final_skill['max_sequence_length']} words")
    
    # Test final response
    print("\nTesting final response...")
    test_prompt = "What have you learned?"
    final_response = baby.generate_response(test_prompt)
    print(f"  Prompt: '{test_prompt}'")
    print(f"  Response: '{final_response}'")
    
    return learning_system


if __name__ == "__main__":
    # Run demo learning session
    learning_system = create_demo_learning_session()
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)
    print("\nTo use this interactively with iFlow:")
    print("  1. Create baby: baby = BabyChatbot()")
    print("  2. Create system: system = InteractiveLearningSystem(baby)")
    print("  3. Run iteration: result = system.learning_iteration(prompt)")
    print("  4. iFlow will be prompted to assess and teach")
    print("  5. Baby learns incrementally through dialogue")
    print("=" * 80)
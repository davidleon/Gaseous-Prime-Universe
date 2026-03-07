# Simplified Text Generator - WORKING VERSION
# Simple template-based generation for immediate functionality

import numpy as np
from typing import List, Dict, Tuple, Optional
import random
import json


class SimpleTextGenerator:
    """
    Simple text generator using template-based approach
    Works immediately without complex training
    """
    
    def __init__(
        self,
        skill_level: float = 0.0,
        vocabulary: List[str] = None
    ):
        """
        Initialize simple text generator
        
        Args:
            skill_level: Current skill level (0.0 - 1.0)
            vocabulary: List of vocabulary words
        """
        self.skill_level = skill_level
        self.vocabulary = vocabulary or []
        
        # Template system
        self.templates = {
            "greeting": [
                "Hello!",
                "Hi there!",
                "Good day!"
            ],
            "definition": [
                "{term} is a concept in AI.",
                "{term} refers to {term} techniques.",
                "{term} is important in machine learning."
            ],
            "explanation": [
                "This involves processing data to learn patterns.",
                "The system learns from examples.",
                "It uses neural networks for understanding."
            ]
        }
        
        # Learn examples from teacher
        self.learned_examples: List[str] = []
        
        # Keywords for template selection
        self.keywords = {
            "hello": "greeting",
            "hi": "greeting",
            "what is": "definition",
            "explain": "explanation",
            "tell me": "explanation"
        }
    
    def generate(
        self,
        prompt: str,
        max_length: int = 50
    ) -> str:
        """
        Generate response to prompt
        
        Args:
            prompt: Input prompt
            max_length: Maximum response length
            
        Returns:
            Generated response
        """
        # Select template based on prompt
        template_type = self._select_template(prompt)
        
        if template_type == "greeting":
            templates = self.templates["greeting"]
            if self.learned_examples:
                # Use learned examples with probability based on skill
                if random.random() < self.skill_level:
                    return random.choice(self.learned_examples)
            return random.choice(templates)
        
        elif template_type == "definition":
            templates = self.templates["definition"]
            template = random.choice(templates)
            # Extract term from prompt
            term = self._extract_term(prompt)
            return template.format(term=term)
        
        elif template_type == "explanation":
            templates = self.templates["explanation"]
            if self.learned_examples and random.random() < self.skill_level:
                return random.choice(self.learned_examples)
            return random.choice(templates)
        
        else:
            # Fallback: use learned examples or simple response
            if self.learned_examples and random.random() < self.skill_level * 0.5:
                return random.choice(self.learned_examples)
            return "I am learning to respond."
    
    def _select_template(self, prompt: str) -> str:
        """Select template type based on prompt keywords"""
        prompt_lower = prompt.lower()
        
        for keyword, template_type in self.keywords.items():
            if keyword in prompt_lower:
                return template_type
        
        return "explanation"  # Default
    
    def _extract_term(self, prompt: str) -> str:
        """Extract term from prompt for definition template"""
        # Simple extraction: find words after "what is"
        prompt_lower = prompt.lower()
        if "what is" in prompt_lower:
            idx = prompt_lower.find("what is")
            term = prompt[idx + 7:].strip()
            # Remove question mark
            term = term.replace("?", "")
            return term[:20]  # Limit length
        
        return "this concept"
    
    def learn_from_example(self, example: str):
        """
        Learn from teacher example
        
        Args:
            example: Example text to learn
        """
        # Add to learned examples
        self.learned_examples.append(example)
        
        # Extract vocabulary
        words = example.split()
        for word in words:
            if word not in self.vocabulary:
                self.vocabulary.append(word)
        
        # Limit vocabulary size
        if len(self.vocabulary) > 1000:
            self.vocabulary = self.vocabulary[-1000:]
        
        # Limit learned examples
        if len(self.learned_examples) > 50:
            self.learned_examples = self.learned_examples[-50:]
    
    def set_skill_level(self, skill_level: float):
        """Update skill level"""
        self.skill_level = skill_level


class ImprovedBabyChatbot:
    """
    Improved baby chatbot with working text generation
    """
    
    def __init__(
        self,
        n_intelligence_dim: int = 12,
        learning_rate: float = 0.05
    ):
        """
        Initialize improved baby chatbot
        
        Args:
            n_intelligence_dim: Intelligence manifold dimension
            learning_rate: Learning rate
        """
        self.n_intelligence_dim = n_intelligence_dim
        self.learning_rate = learning_rate
        
        # Intelligence manifold
        self.intelligence_manifold = np.random.randn(n_intelligence_dim)
        self.intelligence_manifold = self.intelligence_manifold / np.linalg.norm(self.intelligence_manifold)
        
        # Simple text generator (actually works!)
        self.text_generator = SimpleTextGenerator(
            skill_level=0.0,
            vocabulary=["hello", "learning", "ai", "machine"]
        )
        
        # Learning state
        self.skill_level: float = 0.0
        self.learning_iterations: int = 0
        self.dialogue_history: List[Dict] = []
        
        print(f"\n  Improved Baby Chatbot initialized:")
        print(f"    Skill level: {self.skill_level:.2f}")
        print(f"    Vocabulary: {len(self.text_generator.vocabulary)} words")
    
    def generate_response(self, prompt: str) -> str:
        """
        Generate response to prompt
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated response
        """
        # Update generator skill level
        self.text_generator.set_skill_level(self.skill_level)
        
        # Generate response
        response = self.text_generator.generate(prompt)
        
        # Adjust based on skill level
        if self.skill_level < 0.3:
            # Early stage: simple responses
            if len(response) > 20:
                response = " ".join(response.split()[:5])
        
        return response
    
    def learn_from_teacher(
        self,
        teacher_response: str,
        teacher_examples: List[str],
        skill_score: float
    ):
        """
        Learn from teacher
        
        Args:
            teacher_response: Teacher's response
            teacher_examples: List of examples from teacher
            skill_score: New skill score
        """
        # Update skill level
        self.skill_level = skill_score
        
        # Learn from examples
        for example in teacher_examples:
            self.text_generator.learn_from_example(example)
        
        # Learn from teacher response
        self.text_generator.learn_from_example(teacher_response)
        
        # Update intelligence manifold
        teacher_embedding = self._extract_embedding(teacher_response)
        adaptive_lr = self.learning_rate * (1 - self.skill_level * 0.5)
        self.intelligence_manifold = (
            (1 - adaptive_lr) * self.intelligence_manifold +
            adaptive_lr * teacher_embedding[:self.n_intelligence_dim]
        )
        self.intelligence_manifold = self.intelligence_manifold / np.linalg.norm(self.intelligence_manifold)
        
        self.learning_iterations += 1
        
        print(f"    Skill level: {self.skill_level:.2f}")
        print(f"    Vocabulary: {len(self.text_generator.vocabulary)} words")
        print(f"    Learned examples: {len(self.text_generator.learned_examples)}")
    
    def _extract_embedding(self, text: str) -> np.ndarray:
        """Extract simple embedding from text"""
        words = text.split()
        embedding = np.zeros(12)  # Match intelligence manifold dimension
        
        for i, word in enumerate(words):
            word_hash = hash(word)
            idx = abs(word_hash) % 12
            embedding[idx] += 1.0
        
        return embedding / (np.linalg.norm(embedding) + 1e-10)
    
    def get_skill_level(self) -> Dict:
        """Get current skill level"""
        return {
            "skill_level": self.skill_level,
            "learning_iterations": self.learning_iterations,
            "vocabulary_size": len(self.text_generator.vocabulary),
            "learned_examples": len(self.text_generator.learned_examples)
        }


def demo_improved_learning():
    """Demonstrate improved learning"""
    print("\n" + "="*80)
    print("IMPROVED INTERACTIVE LEARNING DEMO")
    print("="*80)
    print("\nThis demo shows improved baby chatbot with working text generation.")
    
    # Create improved baby
    baby = ImprovedBabyChatbot(n_intelligence_dim=12, learning_rate=0.05)
    
    # Simulate learning
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
    
    print("\nStarting learning iterations...\n")
    
    for i, prompt in enumerate(prompts):
        print(f"Iteration {i+1}/10")
        print(f"  Prompt: '{prompt}'")
        
        # Baby generates response
        response = baby.generate_response(prompt)
        print(f"  Baby: '{response}'")
        
        # Simulated teacher response
        if i < 3:
            skill_score = 0.1 + i * 0.1
            examples = ["Hello, how are you?", "Machine learning teaches computers", "Neural networks learn patterns"]
        else:
            skill_score = 0.4 + i * 0.05
            examples = ["Neural networks use layers", "Deep learning extracts features", "Transformers use attention"]
        
        teacher_response = f"Great question! Let me teach you about {prompt.lower().replace('?', '')}."
        
        # Baby learns
        baby.learn_from_teacher(teacher_response, examples, skill_score)
        print()
    
    # Final test
    print("="*80)
    print("LEARNING COMPLETE")
    print("="*80)
    
    final_skill = baby.get_skill_level()
    print(f"\nFinal skill level: {final_skill['skill_level']:.2f}")
    print(f"Vocabulary: {final_skill['vocabulary_size']} words")
    print(f"Learned examples: {final_skill['learned_examples']}")
    
    print("\nTesting final responses:")
    test_prompts = [
        "Hello!",
        "What is AI?",
        "What have you learned?"
    ]
    
    for prompt in test_prompts:
        response = baby.generate_response(prompt)
        print(f"  '{prompt}' → '{response}'")


if __name__ == "__main__":
    demo_improved_learning()
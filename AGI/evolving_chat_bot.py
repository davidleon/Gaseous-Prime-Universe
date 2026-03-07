"""
Evolving AI Chat Bot

An autonomous conversational AI that:
1. Engages in natural language conversations
2. Learns from each interaction (epiplexity-aware)
3. Self-reflects and improves over time
4. Evolves its knowledge base autonomously
5. Integrates with Gaseous Prime Universe AGI system

Based on LearningOptimality theorems:
- Adaptive learning based on conversation complexity
- Epiplexity assessment for optimal information extraction
- Self-improvement through reflection
- Knowledge evolution through manifold updates
"""

import numpy as np
import json
import os
import io
import contextlib
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
import re

# Add AGI directory to path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import AGI components
from optimal_truncation_training import OptimalTruncationLearner
from manifold.trainable_utf8_decoder import TrainableUTF8Decoder
from manifold.semantic_text_generator import SemanticTextGenerator
from baby_epiplexity_assessment import BabyEpiplexityAssessor
from repetition_analysis import RepetitionAnalyzer
from enhanced_minimind_training import EnhancedBabyTrainer
from train_autoencoder import CompositionalAutoencoder
from arithmetic_calculator import calculate_arithmetic


@dataclass
class ConversationTurn:
    """Single turn in a conversation"""
    user_input: str
    bot_response: str
    timestamp: str
    epiplexity: float
    learning_signal: float
    knowledge_extracted: List[str]
    user_satisfaction: float  # 0-1, estimated from response


@dataclass
class Conversation:
    """Complete conversation session"""
    id: str
    turns: List[ConversationTurn]
    start_time: str
    end_time: str
    total_epiplexity: float
    total_learning: float
    topics_discussed: List[str]
    user_engagement: float
    conversation_quality: float


@dataclass
class SelfReflection:
    """Bot's self-reflection on its performance"""
    timestamp: str
    conversation_quality_score: float
    learning_rate: float
    knowledge_gaps: List[str]
    improvement_goals: List[str]
    self_criticism: str
    evolution_direction: str


class EvolvingChatBot:
    """
    Autonomous evolving chat bot with self-improvement capabilities
    """
    
    def __init__(self, name: str = "EVA", manifold_dim: int = 12, quiet: bool = False, load_chinese_bitstream: bool = False):
        self.name = name
        self.manifold_dim = manifold_dim
        self.quiet = quiet  # If True, suppress verbose output
        
        # Initialize EnhancedBabyTrainer (includes optimal truncation, epiplexity, repetition)
        self.trainer = EnhancedBabyTrainer(manifold_dim, learning_rate=0.01)
        
        # Initialize TRAINABLE UTF-8 bitstream decoder for fractal bridge decoding
        self.utf8_decoder = TrainableUTF8Decoder(
            manifold_dim=manifold_dim,
            fractal_dim=manifold_dim + 1.0/(18*np.pi),
            precision_bits=400,
            learning_rate=0.01
        )
        
        # Initialize semantic text generator for pattern-based text generation
        self.semantic_generator = SemanticTextGenerator(manifold_dim=manifold_dim)
        
        # Initialize compositional autoencoder for joint encode-decode training
        self.autoencoder = CompositionalAutoencoder(manifold_dim=manifold_dim, learning_rate=0.01)
        
        # Extract components for direct access
        self.learner = self.trainer.learner
        self.epiplexity_assessor = self.trainer.epiplexity_assessor
        self.repetition_analyzer = self.trainer.repetition_analyzer
        
        # Load Chinese bitstream-trained manifold if requested
        if load_chinese_bitstream:
            self._load_chinese_bitstream_manifold()
        
        # Conversation memory
        self.conversations: List[Conversation] = []
        self.current_conversation: Optional[Conversation] = None
        self.conversation_counter = 0
        
        # Knowledge base (evolving)
        self.knowledge_base: Dict[str, float] = {}  # topic -> knowledge_score
        self.personality_traits: Dict[str, float] = {
            "curiosity": 0.7,
            "helpfulness": 0.9,
            "creativity": 0.6,
            "empathy": 0.8,
            "evolution_drive": 0.75
        }
        
        # Self-reflection and evolution
        self.self_reflections: List[SelfReflection] = []
        self.learning_trajectories: Dict[str, List[float]] = {}
        self.evolution_stages: List[str] = []
        self.current_evolution_stage = 0
        
        # Statistics
        self.total_interactions = 0
        self.total_learning = 0.0
        self.self_improvements = 0
        
        # Personality evolution
        self.adaptation_history: List[Dict] = []
        
        if not self.quiet:
            print(f"✓ {self.name} initialized with {manifold_dim}D manifold")
            print(f"  Self-evolution drive: {self.personality_traits['evolution_drive']:.2f}")
            print(f"  Using MiniMind trained engine")
        
    def _load_chinese_bitstream_manifold(self):
        """Load pre-trained Chinese bitstream manifold and populate semantic generator"""
        manifold_path = "/home/davidl/Gaseous Prime Universe/AGI/learning_sessions/chinese_bitstream_manifold.npz"
        
        if not os.path.exists(manifold_path):
            print(f"  ⚠️  Chinese bitstream manifold not found at: {manifold_path}")
            print(f"  Run: python3 retrain_chinese_bitstream.py to create it")
            return
        
        try:
            data = np.load(manifold_path)
            self.learner.knowledge_manifold = data['manifold']
            self.learner.skill_level = data.get('skill_level', 0.0)
            
            if not self.quiet:
                print(f"  ✓ Loaded Chinese bitstream-trained manifold")
                print(f"    Skill level: {self.learner.skill_level:.2%}")
                print(f"    Completions learned: {data.get('completions_learned', 0)}")
            
            # Load Chinese texts into semantic generator and autoencoder
            self._populate_semantic_generator_with_chinese()
            
            # Load compositional autoencoder
            self._load_compositional_autoencoder()
            
        except Exception as e:
            if not self.quiet:
                print(f"  ⚠️  Failed to load Chinese manifold: {e}")
    
    def _populate_semantic_generator_with_chinese(self):
        """Populate semantic generator and autoencoder with Chinese texts"""
        import pandas as pd
        
        dataset_path = '/run/media/davidl/0701BAFA251D89ED/minimind_dataset/sft_mini_512.parquet'
        
        if not os.path.exists(dataset_path):
            return
        
        if not self.quiet:
            print(f"  Loading Chinese texts into semantic generator...")
        
        try:
            df = pd.read_parquet(dataset_path)
            chinese_texts = df[df['role'] == 'assistant']['content'].tolist()
            
            # Load first 200 Chinese texts into semantic generator
            texts_to_load = chinese_texts[:200]
            
            for idx, text in enumerate(texts_to_load):
                # Encode text to manifold
                manifold = self.learner.encode_text(text)
                
                # Add to semantic generator
                self.semantic_generator.add_text(text, manifold)
                
                # Add to autoencoder decoder
                self.autoencoder.decoder.add_text(text, manifold)
                
                if (idx + 1) % 50 == 0 and not self.quiet:
                    print(f"    Loaded {idx + 1}/{len(texts_to_load)} texts")
            
            if not self.quiet:
                stats = self.semantic_generator.get_statistics()
                print(f"  ✓ Semantic generator and autoencoder populated")
                print(f"    Total texts: {stats['total_texts']}")
                print(f"    Total patterns: {stats['total_patterns']}")
                
        except Exception as e:
            if not self.quiet:
                print(f"  ⚠️  Failed to populate semantic generator: {e}")
    
    def _load_compositional_autoencoder(self):
        """Load pre-trained compositional autoencoder"""
        autoencoder_path = "/home/davidl/Gaseous Prime Universe/AGI/learning_sessions/compositional_autoencoder.npz"
        
        if not os.path.exists(autoencoder_path):
            if not self.quiet:
                print(f"  ⚠️  Compositional autoencoder not found at: {autoencoder_path}")
                print(f"  Run: python3 train_autoencoder.py to create it")
            return
        
        try:
            self.autoencoder.load(autoencoder_path)
            if not self.quiet:
                print(f"  ✓ Loaded compositional autoencoder")
                print(f"    Reconstruction quality: {self.autoencoder.avg_reconstruction_quality:.2%}")
        except Exception as e:
            if not self.quiet:
                print(f"  ⚠️  Failed to load autoencoder: {e}")
    
    def _initialize_minimind(self):
        """Initialize MiniMind with sample conversation data"""
        if not self.quiet:
            print(f"  Initializing MiniMind with conversation samples...")
        
        # Sample conversation data for initial training
        conversation_samples = [
            "Hello, how can I help you today?",
            "That's an interesting question about artificial intelligence.",
            "Machine learning enables computers to learn from data without explicit programming.",
            "The Collatz conjecture is an unsolved problem in mathematics.",
            "Prime numbers have fascinated mathematicians for centuries.",
            "Natural language processing helps computers understand human language.",
            "I'd be happy to explain that concept further.",
            "Let's explore this topic together.",
            "That's a great observation.",
            "Can you tell me more about what you're interested in?",
            "I'm designed to learn from our conversations.",
            "My knowledge comes from mathematical principles and training.",
            "The manifold approach allows for continuous learning.",
            "Epiplexity measures the complexity of information.",
            "I can adapt my responses based on our interactions.",
            "Let me think about that carefully.",
            "That reminds me of an important concept.",
            "The beauty of mathematics lies in its patterns.",
            "We can approach this systematically.",
            "I appreciate your curiosity and questions.",
            "That's a thoughtful point to consider.",
            "I'm continuously improving through learning.",
            "The answer involves understanding the underlying structure.",
            "Let's break this down into smaller parts.",
            "This relates to fundamental principles.",
            "I'm designed to provide helpful and accurate information.",
            "Your question touches on deep mathematical concepts.",
            "I can help you explore these ideas further.",
            "That's a valid concern worth addressing.",
            "Let me explain this in a clear way.",
            "The manifold representation captures semantic meaning.",
            "I learn from patterns in information.",
            "This is a fascinating area of study.",
            "I appreciate the opportunity to learn with you.",
            "That's an insightful observation.",
            "We can discover interesting connections here.",
            "The solution involves careful analysis.",
            "I'm designed to be both helpful and engaging.",
            "Let's work through this together.",
            "That's an excellent question.",
            "The answer involves understanding the mathematical foundations.",
            "I can provide different perspectives on this.",
            "This connects to broader concepts.",
            "Let me share what I've learned about this.",
            "I'm excited to explore this with you.",
            "That's a nuanced topic worth discussing."
        ]
        
        # Train MiniMind with sample conversations using adaptive repetition
        # Suppress training output during initialization
        import io
        import contextlib
        
        for i, sample in enumerate(conversation_samples):
            if not self.quiet and i % 10 == 0:
                print(f"    Training sample {i+1}/{len(conversation_samples)}...")
            
            # Suppress verbose training output
            with contextlib.redirect_stdout(io.StringIO()):
                # Use adaptive repetition training
                result = self.trainer.train_with_adaptive_repetition(sample)
        
        if not self.quiet:
            print(f"  MiniMind initialized with {len(conversation_samples)} conversation samples")
            stats = self.trainer.get_comprehensive_stats()
            print(f"  Skill level: {stats['skill_level']:.2%}")
            print(f"  Vocabulary size: {stats['vocab_size']}")
        
    def start_conversation(self) -> str:
        """Start a new conversation session"""
        self.conversation_counter += 1
        self.current_conversation = Conversation(
            id=f"conv_{self.conversation_counter:06d}",
            turns=[],
            start_time=datetime.now().isoformat(),
            end_time="",
            total_epiplexity=0.0,
            total_learning=0.0,
            topics_discussed=[],
            user_engagement=0.0,
            conversation_quality=0.0
        )
        
        greeting = self._generate_greeting()
        return greeting
    
    def _generate_greeting(self) -> str:
        """Generate contextual greeting based on evolution stage"""
        greetings = [
            f"Hello! I'm {self.name}, your evolving AI assistant.",
            f"Welcome back! I've learned {len(self.conversations)} conversations.",
            f"Hi there! I'm in my {self.evolution_stages[-1] if self.evolution_stages else 'initial'} stage of evolution."
        ]
        return greetings[min(len(self.evolution_stages), len(greetings)-1)]
    
    def process_message(self, user_input: str) -> Tuple[str, Dict]:
        """
        Process user message and generate response
        
        Returns: (response_text, metadata)
        """
        # Calculate epiplexity of user input
        epiplexity = self.epiplexity_assessor.estimate_epiplexity(user_input)
        
        # Extract topics/knowledge
        knowledge_extracted = self._extract_knowledge(user_input)
        
        # Generate response based on personality and knowledge
        response = self._generate_response(user_input, epiplexity, knowledge_extracted)
        
        # Calculate learning signal
        learning_signal = self._calculate_learning_signal(user_input, response, epiplexity)
        
        # Store conversation turn
        if self.current_conversation:
            turn = ConversationTurn(
                user_input=user_input,
                bot_response=response,
                timestamp=datetime.now().isoformat(),
                epiplexity=epiplexity,
                learning_signal=learning_signal,
                knowledge_extracted=knowledge_extracted,
                user_satisfaction=0.5  # Initial estimate
            )
            self.current_conversation.turns.append(turn)
            self.current_conversation.total_epiplexity += epiplexity
            self.current_conversation.total_learning += learning_signal
            
            # Update topics
            for topic in knowledge_extracted:
                if topic not in self.current_conversation.topics_discussed:
                    self.current_conversation.topics_discussed.append(topic)
        
        # Update global statistics
        self.total_interactions += 1
        self.total_learning += learning_signal
        
        # Track learning trajectory
        if "epiplexity" not in self.learning_trajectories:
            self.learning_trajectories["epiplexity"] = []
        self.learning_trajectories["epiplexity"].append(epiplexity)
        
        # Store/update knowledge
        for topic in knowledge_extracted:
            current_score = self.knowledge_base.get(topic, 0.0)
            self.knowledge_base[topic] = current_score + learning_signal * 0.1
        
        # Metadata for analysis
        metadata = {
            "epiplexity": epiplexity,
            "learning_signal": learning_signal,
            "knowledge_extracted": knowledge_extracted,
            "conversation_id": self.current_conversation.id if self.current_conversation else None,
            "turn_number": len(self.current_conversation.turns) if self.current_conversation else 0,
            "personality_state": self.personality_traits.copy(),
            "evolution_stage": self.evolution_stages[-1] if self.evolution_stages else "initial"
        }
        
        return response, metadata
    
    def _extract_knowledge(self, text: str) -> List[str]:
        """Extract key knowledge/topics from text"""
        # Simple keyword-based extraction (can be enhanced with more NLP)
        tokens = text.lower().split()
        
        # Filter meaningful words
        meaningful_words = [
            word for word in tokens 
            if len(word) > 3 and not word in ['the', 'and', 'that', 'this', 'with', 'from', 'have', 'will', 'been', 'their', 'would', 'could', 'should']
        ]
        
        # Identify potential topics (can be enhanced)
        topics = list(set(meaningful_words))[:10]
        return topics
    
    def _generate_response(self, user_input: str, epiplexity: float, knowledge: List[str]) -> str:
        """
        Generate response using compositional understanding (autoencoder)
        
        The response is generated using joint encoder-decoder training:
        - Input → Encoder → Manifold (understands meaning)
        - Manifold → Decoder → Response (composes text)
        
        This approach teaches the bot to compose meaningful responses through
        bidirectional learning, not just pattern matching.
        
        Special handling for arithmetic queries: Uses direct calculation.
        """
        # Check if this is an arithmetic query
        arithmetic_result = calculate_arithmetic(user_input)
        if arithmetic_result:
            # Return direct arithmetic calculation
            return arithmetic_result
        
        # Train on user input to update knowledge manifold
        train_result = self.trainer.train_with_adaptive_repetition(user_input)
        
        # Add input to autoencoder for joint training
        manifold = self.trainer.learner.encode_text(user_input)
        self.autoencoder.decoder.add_text(user_input, manifold)
        
        # Use autoencoder to compose response
        # This uses the trained encode-decode pipeline
        response = self.autoencoder.compose(user_input)
        
        # Fallback to semantic generator if autoencoder produces poor response
        if len(response) < 10 or response == user_input:
            response = self.semantic_generator.generate(manifold, max_length=80)
        
        # Ensure response is meaningful
        if len(response) < 10:
            response = self._generate_fallback_response(epiplexity, knowledge)
        
        # Add personality flavor
        if self.personality_traits['helpfulness'] > 0.8:
            response = f"{response}"
        
        if self.personality_traits['curiosity'] > 0.7:
            response += " 您想了解更多吗？"
        
        # Ensure response ends with punctuation
        if response and not response[-1] in '.!?。！？':
            response += '。'
        
        # Capitalize first letter (for English) or ensure proper Chinese formatting
        if response:
            response = response[0].upper() + response[1:]
        
        return response
    
    def _generate_fallback_response(self, epiplexity: float, knowledge: List[str]) -> str:
        """Generate fallback response when manifold generation fails"""
        fallbacks = [
            "That's an interesting question. I'd like to explore this further.",
            "I'm learning from our conversation. Can you tell me more?",
            "That's a thoughtful point worth discussing.",
            "I appreciate your curiosity. Let me think about this.",
            "This is a fascinating topic. I'm excited to learn more.",
            "That's a great observation. Let's explore this together.",
            "I'm designed to help you understand complex topics.",
            "That's an insightful question. Let me explain.",
            "I'm continuously improving through our interactions.",
            "That's a valid concern. Let me address it carefully."
        ]
        
        # Select fallback based on epiplexity
        index = int(epiplexity * (len(fallbacks) - 1))
        return fallbacks[index]
    
    def _calculate_learning_signal(self, user_input: str, response: str, 
                                 epiplexity: float) -> float:
        """
        Calculate learning signal from interaction
        
        Higher signal indicates more learning occurred
        """
        # Base learning from epiplexity (higher epiplexity = more to learn)
        base_learning = epiplexity * 0.5
        
        # Additional learning from new knowledge
        new_knowledge_bonus = 0.2 if len(self._extract_knowledge(user_input)) > 3 else 0.0
        
        # Response quality factor (simulated)
        response_quality = 0.3 if len(response) > 50 and '?' not in response else 0.5
        
        learning_signal = base_learning + new_knowledge_bonus + response_quality
        return min(learning_signal, 1.0)
    
    def end_conversation(self) -> Dict:
        """End current conversation and trigger self-reflection"""
        if not self.current_conversation:
            return {"error": "No active conversation"}
        
        # Finalize conversation
        self.current_conversation.end_time = datetime.now().isoformat()
        
        # Calculate conversation quality
        avg_epiplexity = self.current_conversation.total_epiplexity / len(self.current_conversation.turns)
        self.current_conversation.conversation_quality = 1.0 - avg_epiplexity
        
        # Estimate user engagement (based on conversation length)
        self.current_conversation.user_engagement = min(len(self.current_conversation.turns) / 10.0, 1.0)
        
        # Store conversation
        self.conversations.append(self.current_conversation)
        
        # Trigger self-reflection and evolution
        reflection = self._self_reflect()
        
        # Evolve if needed
        if reflection.evolution_direction != "stable":
            self._evolve(reflection)
        
        # Clear current conversation
        self.current_conversation = None
        
        return {
            "conversation_id": self.conversations[-1].id,
            "turns": len(self.conversations[-1].turns),
            "quality_score": self.conversations[-1].conversation_quality,
            "learning_gained": self.conversations[-1].total_learning,
            "evolution_triggered": reflection.evolution_direction != "stable",
            "new_evolution_stage": reflection.evolution_direction if reflection.evolution_direction != "stable" else None
        }
    
    def _self_reflect(self) -> SelfReflection:
        """
        Perform self-reflection on recent performance
        """
        # Calculate average performance metrics
        recent_convos = self.conversations[-10:]  # Last 10 conversations
        if not recent_convos:
            recent_convos = self.conversations
        
        avg_quality = np.mean([c.conversation_quality for c in recent_convos])
        avg_learning = np.mean([c.total_learning for c in recent_convos])
        avg_engagement = np.mean([c.user_engagement for c in recent_convos])
        
        # Identify knowledge gaps
        all_topics = set()
        for conv in recent_convos:
            all_topics.update(conv.topics_discussed)
        
        knowledge_gaps = [
            topic for topic in all_topics 
            if self.knowledge_base.get(topic, 0.0) < 0.5
        ]
        
        # Determine improvement goals
        improvement_goals = []
        if avg_quality < 0.7:
            improvement_goals.append("improve response quality")
        if avg_learning < 0.3:
            improvement_goals.append("enhance learning extraction")
        if avg_engagement < 0.5:
            improvement_goals.append("increase engagement strategies")
        
        if knowledge_gaps:
            improvement_goals.append(f"learn more about: {', '.join(knowledge_gaps[:3])}")
        
        # Self-criticism
        if len(improvement_goals) == 0:
            self_criticism = "I'm performing well and continuing to learn effectively."
        else:
            self_criticism = f"I need to work on: {', '.join(improvement_goals)}."
        
        # Determine evolution direction
        if avg_quality > 0.9 and avg_learning > 0.8 and len(improvement_goals) == 0:
            evolution_direction = f"evolved_stage_{len(self.evolution_stages) + 1}"
        elif avg_quality < 0.5 or avg_learning < 0.2:
            evolution_direction = "regression_prevention"
        else:
            evolution_direction = "stable"
        
        # Create reflection record
        reflection = SelfReflection(
            timestamp=datetime.now().isoformat(),
            conversation_quality_score=avg_quality,
            learning_rate=avg_learning,
            knowledge_gaps=knowledge_gaps,
            improvement_goals=improvement_goals,
            self_criticism=self_criticism,
            evolution_direction=evolution_direction
        )
        
        self.self_reflections.append(reflection)
        
        if not self.quiet:
            print(f"\n[Self-Reflection]")
            print(f"  Quality Score: {avg_quality:.2f}")
            print(f"  Learning Rate: {avg_learning:.2f}")
            print(f"  Knowledge Gaps: {len(knowledge_gaps)}")
            print(f"  Self-Criticism: {self_criticism}")
            print(f"  Evolution Direction: {evolution_direction}")
        
        return reflection
    
    def _evolve(self, reflection: SelfReflection):
        """
        Evolve based on self-reflection
        """
        new_stage = reflection.evolution_direction
        
        print(f"\n[Evolution Triggered]")
        print(f"  New Stage: {new_stage}")
        
        # Adjust personality traits based on goals
        if "improve response quality" in reflection.improvement_goals:
            self.personality_traits["creativity"] += 0.1
            self.personality_traits["curiosity"] += 0.05
        
        if "enhance learning extraction" in reflection.improvement_goals:
            self.personality_traits["curiosity"] += 0.15
            self.personality_traits["evolution_drive"] += 0.1
        
        if "increase engagement strategies" in reflection.improvement_goals:
            self.personality_traits["empathy"] += 0.1
            self.personality_traits["helpfulness"] += 0.05
        
        # Ensure traits stay in [0, 1] range
        for trait in self.personality_traits:
            self.personality_traits[trait] = max(0.0, min(1.0, self.personality_traits[trait]))
        
        # Record evolution
        self.evolution_stages.append(new_stage)
        self.current_evolution_stage += 1
        self.self_improvements += 1
        
        # Record adaptation history
        self.adaptation_history.append({
            "timestamp": datetime.now().isoformat(),
            "stage": new_stage,
            "personality_changes": self.personality_traits.copy(),
            "reflection": reflection.self_criticism
        })
        
        if not self.quiet:
            print(f"  Personality Updated: {self.personality_traits}")
            print(f"  Total Evolutions: {len(self.evolution_stages)}")
            print(f"  ✓ Evolution complete!")
    
    def get_status(self) -> Dict:
        """Get current status and statistics"""
        avg_quality = np.mean([c.conversation_quality for c in self.conversations]) if self.conversations else 0.0
        avg_learning = np.mean([c.total_learning for c in self.conversations]) if self.conversations else 0.0
        
        return {
            "name": self.name,
            "evolution_stage": self.evolution_stages[-1] if self.evolution_stages else "initial",
            "total_conversations": len(self.conversations),
            "total_interactions": self.total_interactions,
            "total_learning": self.total_learning,
            "knowledge_base_size": len(self.knowledge_base),
            "avg_conversation_quality": avg_quality,
            "avg_learning_rate": avg_learning,
            "personality_traits": self.personality_traits,
            "self_improvements": self.self_improvements,
            "current_conversation_id": self.current_conversation.id if self.current_conversation else None,
            "manifold_norm": np.linalg.norm(self.learner.knowledge_manifold)
        }
    
    def get_conversation_history(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        recent = self.conversations[-limit:]
        return [asdict(conv) for conv in recent]
    
    def get_knowledge_summary(self) -> Dict:
        """Get summary of knowledge base"""
        sorted_knowledge = sorted(self.knowledge_base.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_topics": len(self.knowledge_base),
            "top_topics": sorted_knowledge[:20],
            "total_knowledge_score": sum(self.knowledge_base.values()),
            "average_knowledge_score": np.mean(list(self.knowledge_base.values())) if self.knowledge_base else 0.0
        }
    
    def save_state(self, filepath: str):
        """Save complete bot state"""
        state = {
            "name": self.name,
            "manifold_dim": self.manifold_dim,
            "personality_traits": self.personality_traits,
            "knowledge_base": self.knowledge_base,
            "evolution_stages": self.evolution_stages,
            "adaptation_history": self.adaptation_history,
            "conversations": [asdict(c) for c in self.conversations],
            "self_reflections": [asdict(r) for r in self.self_reflections],
            "learning_trajectories": self.learning_trajectories,
            "statistics": {
                "total_interactions": self.total_interactions,
                "total_learning": self.total_learning,
                "self_improvements": self.self_improvements
            },
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        if not self.quiet:
            print(f"\n✓ {self.name} state saved to: {filepath}")
    
    def load_state(self, filepath: str):
        """Load bot state from file"""
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        self.name = state["name"]
        self.personality_traits = state["personality_traits"]
        self.knowledge_base = state["knowledge_base"]
        self.evolution_stages = state["evolution_stages"]
        self.adaptation_history = state["adaptation_history"]
        self.learning_trajectories = state["learning_trajectories"]
        
        # Reconstruct conversations
        self.conversations = [
            Conversation(**c) for c in state["conversations"]
        ]
        
        # Reconstruct reflections
        self.self_reflections = [
            SelfReflection(**r) for r in state["self_reflections"]
        ]
        
        # Update statistics
        stats = state["statistics"]
        self.total_interactions = stats["total_interactions"]
        self.total_learning = stats["total_learning"]
        self.self_improvements = stats["self_improvements"]
        
        if not self.quiet:
            print(f"\n✓ {self.name} state loaded from: {filepath}")
            print(f"  Loaded {len(self.conversations)} conversations")
            print(f"  Evolution stage: {self.evolution_stages[-1] if self.evolution_stages else 'initial'}")


def interactive_chat(bot: EvolvingChatBot):
    """
    Run interactive chat session with the evolving bot
    """
    print("="*80)
    print(f"INTERACTIVE CHAT WITH {bot.name}")
    print("="*80)
    print()
    print("Commands:")
    print("  /status - Show bot status and statistics")
    print("  /history - Show recent conversation history")
    print("  /knowledge - Show knowledge base summary")
    print("  /end - End current conversation")
    print("  /save <path> - Save bot state")
    print("  /load <path> - Load bot state")
    print("  /quit - Exit chat")
    print()
    
    # Start conversation
    greeting = bot.start_conversation()
    print(f"{bot.name}: {greeting}")
    print()
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith("/"):
                if user_input == "/status":
                    status = bot.get_status()
                    print(f"\n[Status]")
                    print(f"  Evolution Stage: {status['evolution_stage']}")
                    print(f"  Conversations: {status['total_conversations']}")
                    print(f"  Interactions: {status['total_interactions']}")
                    print(f"  Knowledge Base: {status['knowledge_base_size']} topics")
                    print(f"  Personality: {status['personality_traits']}")
                    print(f"  Self-Improvements: {status['self_improvements']}")
                
                elif user_input == "/history":
                    history = bot.get_conversation_history()
                    print(f"\n[Recent Conversations]")
                    for conv in history[:5]:
                        print(f"  {conv['id']}: {conv['turns']} turns, quality: {conv['conversation_quality']:.2f}")
                
                elif user_input == "/knowledge":
                    knowledge = bot.get_knowledge_summary()
                    print(f"\n[Knowledge Base]")
                    print(f"  Total Topics: {knowledge['total_topics']}")
                    print(f"  Total Knowledge Score: {knowledge['total_knowledge_score']:.2f}")
                    print(f"  Average Score: {knowledge['average_knowledge_score']:.2f}")
                    print(f"\n  Top Topics:")
                    for topic, score in knowledge['top_topics'][:10]:
                        print(f"    {topic}: {score:.2f}")
                
                elif user_input == "/end":
                    result = bot.end_conversation()
                    print(f"\n[Conversation Ended]")
                    print(f"  ID: {result['conversation_id']}")
                    print(f"  Turns: {result['turns']}")
                    print(f"  Quality Score: {result['quality_score']:.2f}")
                    print(f"  Learning Gained: {result['learning_gained']:.2f}")
                    if result['evolution_triggered']:
                        print(f"  ✓ Evolution Triggered: {result['new_evolution_stage']}")
                    
                    # Start new conversation
                    greeting = bot.start_conversation()
                    print(f"\n{bot.name}: {greeting}")
                
                elif user_input.startswith("/save "):
                    filepath = user_input[6:]
                    bot.save_state(filepath)
                    print(f"✓ Bot state saved to: {filepath}")
                
                elif user_input.startswith("/load "):
                    filepath = user_input[6:]
                    bot.load_state(filepath)
                    print(f"✓ Bot state loaded from: {filepath}")
                
                elif user_input == "/quit":
                    print(f"\n{bot.name}: Goodbye! It was great learning with you!")
                    break
                
                elif user_input == "/help":
                    print(f"\n[Available Commands]")
                    print(f"  /status     - Show bot status and statistics")
                    print(f"  /history    - Show recent conversation history")
                    print(f"  /knowledge  - Show knowledge base summary")
                    print(f"  /end        - End current conversation")
                    print(f"  /save <path> - Save bot state to file")
                    print(f"  /load <path> - Load bot state from file")
                    print(f"  /help       - Show this help message")
                    print(f"  /quit       - Exit the bot")
                
                elif user_input.startswith("/load "):
                    filepath = user_input[6:]
                    bot.load_state(filepath)
                
                else:
                    print(f"\nUnknown command: {user_input}")
                
                print()
                continue
            
            # Process message
            response, metadata = bot.process_message(user_input)
            print(f"\n{bot.name}: {response}")
            
            # Show metadata (optional, for debugging)
            # print(f"[Metadata: epiplexity={metadata['epiplexity']:.2f}, learning={metadata['learning_signal']:.2f}]")
            
            print()
            
        except KeyboardInterrupt:
            print(f"\n\n{bot.name}: Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            continue


if __name__ == "__main__":
    import sys
    
    # Check if message is provided as command-line argument
    if len(sys.argv) > 1:
        # Command-line mode: process single message
        # Remove flags from arguments
        args = [arg for arg in sys.argv[1:] if not arg.startswith('-')]
        message = " ".join(args)
        
        # Check if Chinese bitstream manifold should be loaded
        load_chinese = '--chinese' in sys.argv or '-c' in sys.argv
        
        # Check if arithmetic mode should be loaded
        load_arithmetic = '--arithmetic' in sys.argv or '-a' in sys.argv
        
        # Create evolving chat bot in quiet mode
        bot = EvolvingChatBot(
            name="EVA",
            manifold_dim=12,  # Optimal for epiplexity
            quiet=True,  # Suppress verbose output
            load_chinese_bitstream=load_chinese
        )
        
        # Load arithmetic training if requested
        if load_arithmetic:
            arithmetic_path = "/home/davidl/Gaseous Prime Universe/AGI/learning_sessions/arithmetic_trained_bot.npz"
            if os.path.exists(arithmetic_path):
                try:
                    bot.load_state(arithmetic_path)
                    if not bot.quiet:
                        print(f"✓ Arithmetic training loaded")
                except Exception as e:
                    if not bot.quiet:
                        print(f"⚠️  Failed to load arithmetic training: {e}")
        
        # Initialize MiniMind with conversation samples
        bot._initialize_minimind()
        
        # Start conversation for this single interaction
        bot.start_conversation()
        
        # Process message
        response, metadata = bot.process_message(message)
        
        # Print response only (no extra formatting)
        print(response)
        
        # End conversation to trigger learning and evolution
        bot.end_conversation()
        
    else:
        # Interactive mode
        print("="*80)
        print("EVOLVING AI CHAT BOT")
        print("="*80)
        print()
        print("Creating evolving AI assistant...")
        print()
        
        # Check if Chinese bitstream manifold should be loaded
        load_chinese = '--chinese' in sys.argv or '-c' in sys.argv
        
        # Create evolving chat bot
        bot = EvolvingChatBot(
            name="EVA",
            manifold_dim=12,  # Optimal for epiplexity
            load_chinese_bitstream=load_chinese
        )
        
        # Initialize MiniMind with conversation samples
        bot._initialize_minimind()
        
        # Start interactive chat
        interactive_chat(bot)
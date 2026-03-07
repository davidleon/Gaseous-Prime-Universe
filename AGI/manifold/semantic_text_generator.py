"""
Semantic Text Generator

Generates text based on manifold semantic meaning using pattern matching
from the training corpus. This approach uses the manifold to understand
the semantic content and then generates text by finding similar patterns.
"""

import numpy as np
import re
from typing import List, Dict, Tuple, Optional
from collections import defaultdict, Counter


class SemanticTextGenerator:
    """
    Generate text based on manifold semantic meaning
    
    Uses manifold to find semantically similar texts from the training corpus
    and generates responses by combining patterns.
    """
    
    def __init__(self, manifold_dim: int = 12):
        """
        Initialize semantic text generator
        
        Args:
            manifold_dim: Dimension of the manifold
        """
        self.manifold_dim = manifold_dim
        
        # Store training texts and their manifold representations
        self.texts: List[str] = []
        self.manifolds: List[np.ndarray] = []
        
        # Build pattern database
        self.patterns: Dict[str, List[str]] = defaultdict(list)
        
        # Common response patterns
        self.response_templates = [
            "这是一个很好的问题。",
            "让我来解释一下。",
            "这个话题很有趣。",
            "我理解你的意思。",
            "这是一个重要的观点。",
            "我们可以从多个角度来看待这个问题。",
            "这涉及到复杂的因素。",
            "让我详细说明一下。",
            "这个问题很有深度。",
            "我很乐意帮助您理解。"
        ]
    
    def add_text(self, text: str, manifold: np.ndarray):
        """
        Add a text and its manifold representation to the database
        
        Args:
            text: Text string
            manifold: Manifold representation
        """
        self.texts.append(text)
        self.manifolds.append(manifold)
        
        # Extract patterns
        self._extract_patterns(text)
    
    def _extract_patterns(self, text: str):
        """
        Extract patterns from text
        
        Args:
            text: Text string
        """
        # Extract sentences
        sentences = re.split(r'[。！？.!?]', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 3:
                # Store sentence as a pattern
                self.patterns['sentences'].append(sentence)
                
                # Extract key phrases (n-grams)
                for n in range(2, 5):
                    words = sentence.split()
                    for i in range(len(words) - n + 1):
                        phrase = ' '.join(words[i:i+n])
                        self.patterns['phrases'].append(phrase)
    
    def find_similar_texts(self, query_manifold: np.ndarray, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Find texts with similar manifold representation
        
        Args:
            query_manifold: Query manifold
            top_k: Number of similar texts to return
            
        Returns:
            List of (text, similarity_score) tuples
        """
        if len(self.manifolds) == 0:
            return []
        
        # Calculate cosine similarity with all stored manifolds
        similarities = []
        for i, manifold in enumerate(self.manifolds):
            similarity = self._cosine_similarity(query_manifold, manifold)
            similarities.append((i, similarity))
        
        # Sort by similarity and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_similar = similarities[:top_k]
        
        return [(self.texts[i], score) for i, score in top_similar]
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)
    
    def generate(self, query_manifold: np.ndarray, max_length: int = 100) -> str:
        """
        Generate text based on manifold semantic meaning
        
        Args:
            query_manifold: Query manifold
            max_length: Maximum length of generated text
            
        Returns:
            Generated text
        """
        # Find similar texts
        similar_texts = self.find_similar_texts(query_manifold, top_k=3)
        
        if not similar_texts:
            # Fallback to random template
            return np.random.choice(self.response_templates)
        
        # Generate response by combining patterns from similar texts
        response_parts = []
        
        # Add a greeting/introduction
        if len(self.patterns['sentences']) > 0:
            intro = np.random.choice(self.patterns['sentences'][:10])
            if len(intro) < 30:
                response_parts.append(intro)
        
        # Add content from similar texts
        for text, similarity in similar_texts:
            if similarity > 0.1:  # Only use sufficiently similar texts
                # Extract a sentence from the text
                sentences = re.split(r'[。！？.!?]', text)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if len(sentence) > 5 and len(sentence) < 50:
                        response_parts.append(sentence)
                        break
        
        # Add a closing
        if len(self.patterns['sentences']) > 0:
            closing = np.random.choice(self.patterns['sentences'][-10:])
            if len(closing) < 30:
                response_parts.append(closing)
        
        # Combine parts
        response = ' '.join(response_parts)
        
        # Truncate to max length
        if len(response) > max_length:
            response = response[:max_length]
            response = response[:response.rfind(' ')] + '。'
        
        # Ensure response ends with punctuation
        if response and response[-1] not in '。！？.!?':
            response += '。'
        
        return response
    
    def generate_from_query(self, query_text: str, encoder) -> str:
        """
        Generate response from query text
        
        Args:
            query_text: Query text
            encoder: Encoder function (text → manifold)
            
        Returns:
            Generated response
        """
        # Encode query to manifold
        query_manifold = encoder(query_text)
        
        # Generate response
        return self.generate(query_manifold)
    
    def get_statistics(self) -> Dict:
        """Get generator statistics"""
        return {
            'total_texts': len(self.texts),
            'total_patterns': len(self.patterns.get('sentences', [])) + len(self.patterns.get('phrases', [])),
            'avg_text_length': np.mean([len(t) for t in self.texts]) if self.texts else 0
        }
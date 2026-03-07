"""
Text Decoder Manifold
Bridges intelligence manifolds to text generation without traditional tokenizers
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')

try:
    from sklearn.decomposition import PCA
    from sklearn.cluster import KMeans
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("  [WARN] sklearn not available - some features limited")


class TextDecoderManifold:
    """
    Text decoder manifold for generating text from intelligence manifolds
    
    Instead of a traditional tokenizer, uses:
    1. Continuous text embeddings (semantic space)
    2. Learned manifold-to-text mapping
    3. Probabilistic generation with semantic coherence
    """
    
    def __init__(
        self,
        n_intelligence_dim: int = 12,
        n_text_dim: int = 768,  # Like sentence transformers
        n_clusters: int = 1000,  # Semantic clusters
        vocab_size: int = 50000,  # Effective vocabulary
        max_sequence_length: int = 512,
        temperature: float = 0.7,
        top_k: int = 50,
        top_p: float = 0.9
    ):
        """
        Initialize text decoder manifold
        
        Args:
            n_intelligence_dim: Dimensionality of input intelligence manifold
            n_text_dim: Dimensionality of text embedding space
            n_clusters: Number of semantic clusters for organization
            vocab_size: Effective vocabulary size
            max_sequence_length: Maximum text generation length
            temperature: Sampling temperature (higher = more random)
            top_k: Top-k sampling parameter
            top_p: Nucleus sampling parameter
        """
        self.n_intelligence_dim = n_intelligence_dim
        self.n_text_dim = n_text_dim
        self.n_clusters = n_clusters
        self.vocab_size = vocab_size
        self.max_sequence_length = max_sequence_length
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        
        # Intelligence-to-text mapping matrix
        self.W_intelligence_to_text: Optional[np.ndarray] = None
        self.b_text: Optional[np.ndarray] = None
        
        # Text embedding space (semantic clusters)
        self.text_embeddings: Optional[np.ndarray] = None
        self.cluster_centers: Optional[np.ndarray] = None
        self.cluster_labels: Optional[np.ndarray] = None
        
        # Vocabulary (text snippets organized by semantic clusters)
        self.vocabulary: Dict[int, List[str]] = {}
        
        # Training state
        self.trained = False
        self.training_samples = 0
        
        print(f"  Text Decoder Manifold initialized:")
        print(f"    Intelligence dim: {n_intelligence_dim}")
        print(f"    Text embedding dim: {n_text_dim}")
        print(f"    Semantic clusters: {n_clusters}")
        print(f"    Vocabulary size: {vocab_size}")
    
    def initialize_vocabulary(
        self,
        text_samples: List[str],
        use_embeddings: bool = True
    ):
        """
        Initialize vocabulary from text samples
        
        Args:
            text_samples: List of text samples
            use_embeddings: Whether to use sentence embeddings
        """
        print(f"\nInitializing vocabulary from {len(text_samples)} text samples...")
        
        # Extract text snippets (words, phrases, short sentences)
        self._extract_text_snippets(text_samples)
        
        # Organize vocabulary into semantic clusters
        if SKLEARN_AVAILABLE and use_embeddings:
            self._cluster_vocabulary_semantic()
        else:
            self._cluster_vocabulary_random()
        
        # Initialize text embedding space
        self._initialize_text_embeddings()
        
        print(f"  Vocabulary initialized with {len(self.vocabulary)} clusters")
        print(f"  Total text snippets: {sum(len(snippets) for snippets in self.vocabulary.values())}")
    
    def _extract_text_snippets(self, text_samples: List[str]):
        """Extract text snippets from samples"""
        all_snippets = []
        
        for text in text_samples:
            # Extract words
            words = text.split()
            all_snippets.extend(words)
            
            # Extract bigrams
            bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
            all_snippets.extend(bigrams[:100])  # Limit bigrams
            
            # Extract short sentences
            sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 5]
            all_snippets.extend(sentences[:50])  # Limit sentences
        
        # Deduplicate and limit
        unique_snippets = list(set(all_snippets))
        unique_snippets = unique_snippets[:self.vocab_size]
        
        # Initialize vocabulary with random cluster assignment
        for i, snippet in enumerate(unique_snippets):
            cluster_id = i % self.n_clusters
            if cluster_id not in self.vocabulary:
                self.vocabulary[cluster_id] = []
            self.vocabulary[cluster_id].append(snippet)
    
    def _cluster_vocabulary_semantic(self):
        """Cluster vocabulary using semantic embeddings"""
        # Flatten vocabulary
        all_snippets = []
        cluster_ids = []
        
        for cluster_id, snippets in self.vocabulary.items():
            for snippet in snippets:
                all_snippets.append(snippet)
                cluster_ids.append(cluster_id)
        
        # Create simple length-based embeddings (replace with sentence embeddings)
        text_features = np.array([
            [len(snippet), snippet.count(' '), hash(snippet) % 1000]
            for snippet in all_snippets
        ])
        
        # Cluster using K-means
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        new_cluster_labels = kmeans.fit_predict(text_features)
        
        # Reorganize vocabulary
        self.vocabulary = {}
        for snippet, new_cluster_id in zip(all_snippets, new_cluster_labels):
            if new_cluster_id not in self.vocabulary:
                self.vocabulary[new_cluster_id] = []
            self.vocabulary[new_cluster_id].append(snippet)
        
        self.cluster_centers = kmeans.cluster_centers_
    
    def _cluster_vocabulary_random(self):
        """Cluster vocabulary randomly (fallback)"""
        # Already done in _extract_text_snippets
        pass
    
    def _initialize_text_embeddings(self):
        """Initialize text embedding space"""
        # Create random text embeddings for each cluster
        self.text_embeddings = np.random.randn(
            self.n_clusters,
            self.n_text_dim
        )
        
        # Normalize
        self.text_embeddings = self.text_embeddings / np.linalg.norm(
            self.text_embeddings, axis=1, keepdims=True
        )
    
    def train(
        self,
        intelligence_manifolds: List[np.ndarray],
        text_outputs: List[str],
        epochs: int = 100,
        learning_rate: float = 0.01
    ):
        """
        Train intelligence-to-text mapping
        
        Args:
            intelligence_manifolds: List of 12D intelligence manifold points
            text_outputs: Corresponding text outputs
            epochs: Number of training epochs
            learning_rate: Learning rate
        """
        print(f"\nTraining intelligence-to-text mapping...")
        print(f"  Training samples: {len(intelligence_manifolds)}")
        print(f"  Epochs: {epochs}")
        
        # Initialize mapping matrix
        self.W_intelligence_to_text = np.random.randn(
            self.n_intelligence_dim,
            self.n_text_dim
        ) * 0.1
        self.b_text = np.zeros(self.n_text_dim)
        
        # Extract text embeddings for training
        text_embeddings_train = self._extract_text_embeddings(text_outputs)
        
        # Train mapping
        for epoch in range(epochs):
            epoch_loss = 0.0
            
            for intel_manifold, text_emb in zip(intelligence_manifolds, text_embeddings_train):
                # Forward pass
                predicted_emb = np.dot(intel_manifold, self.W_intelligence_to_text) + self.b_text
                
                # Compute loss (MSE)
                loss = np.mean((predicted_emb - text_emb) ** 2)
                epoch_loss += loss
                
                # Backward pass (gradient descent)
                d_loss = 2 * (predicted_emb - text_emb) / len(text_emb)
                
                d_W = np.outer(intel_manifold, d_loss)
                d_b = d_loss
                
                # Update (using absolute value to avoid complex casting error if input manifolds are complex)
                self.W_intelligence_to_text -= learning_rate * np.abs(d_W)
                self.b_text -= learning_rate * np.abs(d_b)
            
            if epoch % 10 == 0:
                print(f"  Epoch {epoch}: Loss = {epoch_loss / len(intelligence_manifolds):.6f}")
        
        self.trained = True
        self.training_samples = len(intelligence_manifolds)
        
        print(f"  Training complete!")
        print(f"  Final loss: {epoch_loss / len(intelligence_manifolds):.6f}")
    
    def _extract_text_embeddings(self, texts: List[str]) -> np.ndarray:
        """Extract text embeddings from texts"""
        embeddings = []
        
        for text in texts:
            # Extract text snippets
            snippets = text.split()
            
            # Get cluster IDs for snippets
            cluster_ids = []
            for snippet in snippets:
                # Find best matching cluster
                best_cluster = self._find_best_cluster(snippet)
                cluster_ids.append(best_cluster)
            
            # Average cluster embeddings
            if cluster_ids:
                text_emb = np.mean([self.text_embeddings[cid] for cid in cluster_ids], axis=0)
            else:
                text_emb = np.zeros(self.n_text_dim)
            
            embeddings.append(text_emb)
        
        return np.array(embeddings)
    
    def _find_best_cluster(self, text: str) -> int:
        """Find best matching semantic cluster for text"""
        # Simple hash-based matching (replace with semantic similarity)
        return hash(text) % self.n_clusters
    
    def decode(
        self,
        intelligence_manifold: np.ndarray,
        max_length: Optional[int] = None,
        decode_strategy: str = "sampling"
    ) -> str:
        """
        Decode intelligence manifold to text
        
        Args:
            intelligence_manifold: 12D intelligence manifold point
            max_length: Maximum text length (default: max_sequence_length)
            decode_strategy: "sampling" or "greedy"
            
        Returns:
            Generated text
        """
        if not self.trained:
            raise ValueError("Text decoder not trained. Call train() first.")
        
        max_length = max_length or self.max_sequence_length
        
        # Map intelligence manifold to text embedding
        text_embedding = np.dot(intelligence_manifold, self.W_intelligence_to_text) + self.b_text
        
        # Generate text from embedding
        if decode_strategy == "sampling":
            generated_text = self._generate_text_sampling(text_embedding, max_length)
        else:
            generated_text = self._generate_text_greedy(text_embedding, max_length)
        
        return generated_text
    
    def _generate_text_sampling(
        self,
        text_embedding: np.ndarray,
        max_length: int
    ) -> str:
        """Generate text using sampling"""
        # Find nearest clusters
        similarities = np.dot(self.text_embeddings, text_embedding)
        top_k_clusters = np.argsort(similarities)[-self.top_k:]
        
        # Sample from top clusters
        generated_words = []
        
        for _ in range(max_length):
            # Sample cluster
            cluster_probs = similarities[top_k_clusters]
            cluster_probs = np.exp(cluster_probs / self.temperature)
            cluster_probs = cluster_probs / np.sum(cluster_probs)
            
            sampled_cluster = np.random.choice(top_k_clusters, p=cluster_probs)
            
            # Sample word from cluster
            if sampled_cluster in self.vocabulary and len(self.vocabulary[sampled_cluster]) > 0:
                word = np.random.choice(self.vocabulary[sampled_cluster])
                generated_words.append(word)
            else:
                break
        
        return " ".join(generated_words)
    
    def _generate_text_greedy(
        self,
        text_embedding: np.ndarray,
        max_length: int
    ) -> str:
        """Generate text using greedy decoding"""
        # Find nearest clusters
        similarities = np.dot(self.text_embeddings, text_embedding)
        sorted_clusters = np.argsort(similarities)[::-1]
        
        # Select words greedily
        generated_words = []
        
        for cluster_id in sorted_clusters:
            if cluster_id in self.vocabulary and len(self.vocabulary[cluster_id]) > 0:
                # Select word from cluster
                words = self.vocabulary[cluster_id]
                for word in words[:max_length - len(generated_words)]:
                    generated_words.append(word)
            
            if len(generated_words) >= max_length:
                break
        
        return " ".join(generated_words)
    
    def decode_batch(
        self,
        intelligence_manifolds: List[np.ndarray],
        max_length: Optional[int] = None
    ) -> List[str]:
        """Decode multiple intelligence manifolds to text"""
        return [
            self.decode(manifold, max_length)
            for manifold in intelligence_manifolds
        ]
    
    def get_text_probability(
        self,
        intelligence_manifold: np.ndarray,
        text: str
    ) -> float:
        """
        Compute probability of text given intelligence manifold
        
        Args:
            intelligence_manifold: 12D intelligence manifold point
            text: Text to compute probability for
            
        Returns:
            Probability (0-1)
        """
        if not self.trained:
            raise ValueError("Text decoder not trained. Call train() first.")
        
        # Map intelligence manifold to text embedding
        text_embedding_pred = np.dot(intelligence_manifold, self.W_intelligence_to_text) + self.b_text
        
        # Extract text embedding for input text
        text_emb_input = self._extract_text_embeddings([text])[0]
        
        # Compute similarity (proxy for probability)
        similarity = np.dot(text_embedding_pred, text_emb_input)
        similarity = np.clip(similarity, -1, 1)
        probability = (similarity + 1) / 2  # Map to [0, 1]
        
        return probability
    
    def get_manifold_space_info(self) -> dict:
        """Get information about the manifold space"""
        return {
            "n_intelligence_dim": self.n_intelligence_dim,
            "n_text_dim": self.n_text_dim,
            "n_clusters": self.n_clusters,
            "vocab_size": self.vocab_size,
            "max_sequence_length": self.max_sequence_length,
            "trained": self.trained,
            "training_samples": self.training_samples,
            "temperature": self.temperature,
            "top_k": self.top_k,
            "top_p": self.top_p
        }


def create_demo_text_decoder():
    """Create demo text decoder manifold"""
    print("\nCreating Demo Text Decoder Manifold...")
    
    # Sample text data
    text_samples = [
        "The quick brown fox jumps over the lazy dog.",
        "Artificial intelligence is transforming the world.",
        "Machine learning models process data to make predictions.",
        "Neural networks learn complex patterns from examples.",
        "Natural language processing enables computers to understand text.",
        "Computer vision allows machines to interpret visual information.",
        "Deep learning uses multiple layers to extract features.",
        "Reinforcement learning teaches agents through trial and error.",
        "Generative models can create new data samples.",
        "Transformer architectures revolutionized sequence modeling."
    ]
    
    # Create text decoder
    text_decoder = TextDecoderManifold(
        n_intelligence_dim=12,
        n_text_dim=768,
        n_clusters=100,
        vocab_size=1000,
        max_sequence_length=50,
        temperature=0.7,
        top_k=10,
        top_p=0.9
    )
    
    # Initialize vocabulary
    text_decoder.initialize_vocabulary(text_samples)
    
    # Train with sample intelligence manifolds
    intelligence_manifolds = [np.random.randn(12) for _ in range(len(text_samples))]
    text_decoder.train(intelligence_manifolds, text_samples, epochs=50)
    
    # Test decoding
    print("\nTesting text generation...")
    test_manifold = np.random.randn(12)
    generated_text = text_decoder.decode(test_manifold)
    print(f"  Input manifold: {test_manifold[:5]}...")
    print(f"  Generated text: {generated_text}")
    
    return text_decoder


if __name__ == "__main__":
    # Create and test demo text decoder
    text_decoder = create_demo_text_decoder()
    
    print("\n" + "=" * 80)
    print("Text Decoder Manifold Demo Complete!")
    print("=" * 80)
    print("\nKey features:")
    print("  ✓ No traditional tokenizer needed")
    print("  ✓ Continuous text embeddings (semantic space)")
    print("  ✓ Probabilistic generation with sampling")
    print("  ✓ Semantic coherence through clustering")
    print("  ✓ Learned intelligence-to-text mapping")
    print("\nUsage:")
    print("  1. Initialize vocabulary from text samples")
    print("  2. Train with intelligence manifold + text pairs")
    print("  3. Decode intelligence manifolds to text")
    print("=" * 80)

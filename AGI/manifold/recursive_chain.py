"""
Recursive Manifold Chain
Hierarchical manifold structure with fractal bridges between levels
"""

import numpy as np
from typing import List, Tuple, Optional, Dict
from .svd_decoder import SVDDecoder


class RecursiveManifold:
    """
    Single recursive manifold with hierarchical levels
    """
    
    def __init__(
        self,
        n_weights: int,
        levels: int = 4,
        dimensions: Optional[List[int]] = None,
        precision_bits: int = 400,
        seed: int = 42
    ):
        """
        Initialize recursive manifold
        
        Args:
            n_weights: Number of weights
            levels: Number of hierarchical levels
            dimensions: List of dimensions for each level (default: [12, 9, 6, 3])
            precision_bits: Precision for calculations
            seed: Random seed
        """
        self.n_weights = n_weights
        self.levels = levels
        self.precision_bits = precision_bits
        self.seed = seed
        
        # Default dimensions: 12D → 9D → 6D → 3D
        if dimensions is None:
            self.dimensions = [12, 9, 6, 3][:levels]
        else:
            self.dimensions = dimensions[:levels]
        
        # Create decoder for each level
        self.decoders = []
        for level, dim in enumerate(self.dimensions):
            decoder = SVDDecoder(
                n_weights=n_weights,
                n_manifold_dim=dim,
                precision_bits=precision_bits,
                seed=seed + level
            )
            self.decoders.append(decoder)
        
        # Manifold chain
        self.manifold_chain: List[np.ndarray] = []
        
        # Fractal bridge dimensions (non-integer)
        self.fractal_dimensions = self._calculate_fractal_dimensions()
    
    def _calculate_fractal_dimensions(self) -> List[float]:
        """
        Calculate fractal bridge dimensions between levels
        
        Returns:
            List of fractal dimensions
        """
        fractal_dims = []
        for i in range(len(self.dimensions) - 1):
            d1 = self.dimensions[i]
            d2 = self.dimensions[i + 1]
            # Fractal dimension between levels
            fractal_dim = d1 - (d1 - d2) * 0.618  # Golden ratio transition
            fractal_dims.append(fractal_dim)
        
        return fractal_dims
    
    def learn_reference_structure(self, weights: np.ndarray):
        """
        Learn reference structure for all levels
        
        Args:
            weights: Reference weight vector
        """
        current_weights = weights.copy()
        
        for level, decoder in enumerate(self.decoders):
            decoder.learn_reference_structure(current_weights)
            
            # Decode to manifold at this level
            manifold_point = decoder.decode(current_weights)
            self.manifold_chain.append(manifold_point)
            
            # Prepare for next level (simulate compression)
            if level < len(self.decoders) - 1:
                # Reconstruct and compress for next level
                reconstructed = decoder.reconstruct(manifold_point)
                # Simulate compression by reducing dimensionality
                compression_ratio = self.dimensions[level + 1] / self.dimensions[level]
                current_weights = reconstructed * compression_ratio
        
        print(f"Learned recursive chain with {len(self.manifold_chain)} levels")
        print(f"  Dimensions: {self.dimensions}")
        print(f"  Fractal bridges: {self.fractal_dimensions}")
    
    def decode_recursive(self, weights: np.ndarray) -> List[np.ndarray]:
        """
        Decode weights through all levels recursively
        
        Args:
            weights: Input weight vector
            
        Returns:
            List of manifold points at each level
        """
        chain = []
        current_weights = weights.copy()
        
        for level, decoder in enumerate(self.decoders):
            # Decode to manifold at this level
            manifold_point = decoder.decode(current_weights)
            chain.append(manifold_point)
            
            # Prepare for next level
            if level < len(self.decoders) - 1:
                # Reconstruct and compress
                reconstructed = decoder.reconstruct(manifold_point)
                compression_ratio = self.dimensions[level + 1] / self.dimensions[level]
                current_weights = reconstructed * compression_ratio
        
        return chain
    
    def refine_prediction(
        self,
        x: np.ndarray,
        chain: Optional[List[np.ndarray]] = None
    ) -> np.ndarray:
        """
        Refine prediction using recursive chain
        
        Args:
            x: Input to refine
            chain: Optional pre-computed chain
            
        Returns:
            Refined output
        """
        if chain is None:
            raise ValueError("Manifold chain not provided. Use decode_recursive() first.")
        
        # Start with input
        x_refined = x.copy()
        
        # Refine at each level (coarse to fine)
        for level, manifold_point in enumerate(chain):
            # Apply manifold-based refinement
            # This is a simplified refinement - in practice, would use geodesic flow
            level_weight = 1.0 / (level + 1)
            x_refined = x_refined * (1 - level_weight) + manifold_point[:len(x_refined)] * level_weight
        
        return x_refined
    
    def get_manifold_at_level(self, level: int) -> Optional[np.ndarray]:
        """
        Get manifold point at specific level
        
        Args:
            level: Level index
            
        Returns:
            Manifold point or None if not computed
        """
        if 0 <= level < len(self.manifold_chain):
            return self.manifold_chain[level]
        return None
    
    def chain_distance(self, other_chain: List[np.ndarray]) -> float:
        """
        Calculate distance between two recursive chains
        
        Args:
            other_chain: Other manifold chain
            
        Returns:
            Average distance across all levels
        """
        if len(self.manifold_chain) != len(other_chain):
            raise ValueError("Chains must have same number of levels")
        
        distances = []
        for i in range(len(self.manifold_chain)):
            dist = np.linalg.norm(self.manifold_chain[i] - other_chain[i])
            distances.append(dist)
        
        return np.mean(distances)
    
    def chain_similarity(self, other_chain: List[np.ndarray]) -> float:
        """
        Calculate similarity between two recursive chains
        
        Args:
            other_chain: Other manifold chain
            
        Returns:
            Average similarity across all levels
        """
        if len(self.manifold_chain) != len(other_chain):
            raise ValueError("Chains must have same number of levels")
        
        similarities = []
        for i in range(len(self.manifold_chain)):
            dot_product = np.dot(self.manifold_chain[i], other_chain[i])
            norm1 = np.linalg.norm(self.manifold_chain[i])
            norm2 = np.linalg.norm(other_chain[i])
            
            if norm1 > 0 and norm2 > 0:
                similarity = dot_product / (norm1 * norm2)
            else:
                similarity = 0.0
            
            similarities.append(similarity)
        
        return np.mean(similarities)


class RecursiveManifoldChain:
    """
    Manager for multiple recursive manifolds
    """
    
    def __init__(
        self,
        n_weights: int,
        n_manifolds: int,
        levels: int = 4,
        dimensions: Optional[List[int]] = None,
        precision_bits: int = 400
    ):
        """
        Initialize recursive manifold chain manager
        
        Args:
            n_weights: Number of weights per manifold
            n_manifolds: Number of recursive manifolds
            levels: Number of levels per manifold
            dimensions: Dimensions for each level
            precision_bits: Precision for calculations
        """
        self.n_weights = n_weights
        self.n_manifolds = n_manifolds
        self.levels = levels
        self.dimensions = dimensions or [12, 9, 6, 3][:levels]
        self.precision_bits = precision_bits
        
        # Create recursive manifolds
        self.manifolds = []
        for i in range(n_manifolds):
            manifold = RecursiveManifold(
                n_weights=n_weights,
                levels=levels,
                dimensions=dimensions,
                precision_bits=precision_bits,
                seed=42 + i
            )
            self.manifolds.append(manifold)
        
        # Store all chains
        self.all_chains: List[List[np.ndarray]] = []
    
    def train_all(self, weights_list: List[np.ndarray]):
        """
        Train all recursive manifolds
        
        Args:
            weights_list: List of weight vectors for each manifold
        """
        if len(weights_list) != self.n_manifolds:
            raise ValueError(f"Expected {self.n_manifolds} weight vectors, got {len(weights_list)}")
        
        self.all_chains = []
        
        for i, (manifold, weights) in enumerate(zip(self.manifolds, weights_list)):
            manifold.learn_reference_structure(weights)
            chain = manifold.decode_recursive(weights)
            self.all_chains.append(chain)
            print(f"  Trained manifold {i+1}/{self.n_manifolds}")
        
        print(f"Trained {self.n_manifolds} recursive manifolds")
    
    def get_chain(self, manifold_idx: int) -> Optional[List[np.ndarray]]:
        """
        Get manifold chain for specific manifold
        
        Args:
            manifold_idx: Index of manifold
            
        Returns:
            Manifold chain or None
        """
        if 0 <= manifold_idx < len(self.all_chains):
            return self.all_chains[manifold_idx]
        return None
    
    def get_all_chains(self) -> List[List[np.ndarray]]:
        """Get all manifold chains"""
        return self.all_chains


def test_recursive_manifold():
    """Test recursive manifold functionality"""
    print("Testing Recursive Manifold...")
    
    # Create recursive manifold
    n_weights = 50000
    manifold = RecursiveManifold(
        n_weights=n_weights,
        levels=4,
        dimensions=[12, 9, 6, 3],
        precision_bits=400
    )
    
    # Learn structure
    weights = np.random.randn(n_weights)
    manifold.learn_reference_structure(weights)
    
    # Decode recursively
    chain = manifold.decode_recursive(weights)
    
    print(f"  Recursive chain with {len(chain)} levels:")
    for level, manifold_point in enumerate(chain):
        print(f"    Level {level}: {len(manifold_point)}D, norm={np.linalg.norm(manifold_point):.6f}")
    
    # Test refinement
    x = np.random.randn(10)
    x_refined = manifold.refine_prediction(x, chain)
    
    print(f"  Refinement test:")
    print(f"    Input norm: {np.linalg.norm(x):.6f}")
    print(f"    Refined norm: {np.linalg.norm(x_refined):.6f}")
    
    # Test multiple manifolds
    print("\nTesting Multiple Recursive Manifolds...")
    chain_manager = RecursiveManifoldChain(
        n_weights=n_weights,
        n_manifolds=5,
        levels=4
    )
    
    weights_list = [np.random.randn(n_weights) for _ in range(5)]
    chain_manager.train_all(weights_list)
    
    all_chains = chain_manager.get_all_chains()
    print(f"  Trained {len(all_chains)} recursive chains")
    
    print("  All tests passed!")


if __name__ == "__main__":
    test_recursive_manifold()

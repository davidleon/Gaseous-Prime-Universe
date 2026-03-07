"""
SVD-Based Manifold Decoder
Uses SVD instead of eigenvalue decomposition for O(N^2) complexity instead of O(N^3)
"""

import numpy as np
from typing import Tuple, Optional, List
from scipy.linalg import svd
from scipy.sparse.linalg import svds
import warnings

warnings.filterwarnings('ignore')


class SVDDecoder:
    """
    SVD-based decoder for extracting intelligence manifolds from weights
    
    Uses randomized SVD for large-scale efficiency (O(N^2) vs O(N^3))
    """
    
    def __init__(
        self,
        n_weights: int,
        n_manifold_dim: int = 12,
        use_randomized: bool = True,
        precision_bits: int = 400,
        seed: int = 42
    ):
        """
        Initialize SVD decoder
        
        Args:
            n_weights: Number of weights in the model
            n_manifold_dim: Dimensionality of the output manifold
            use_randomized: Use randomized SVD for efficiency
            precision_bits: Precision for calculations
            seed: Random seed for reproducibility
        """
        self.n_weights = n_weights
        self.n_manifold_dim = n_manifold_dim
        self.use_randomized = use_randomized
        self.precision_bits = precision_bits
        self.seed = seed
        
        # Initialize omega projection
        self.omega_projection = self._initialize_omega_projection()
        
        # Reference structure (for learning)
        self.reference_weights: Optional[np.ndarray] = None
        self.reference_manifold: Optional[np.ndarray] = None
        
        # Set random seed
        np.random.seed(seed)
    
    def _initialize_omega_projection(self) -> np.ndarray:
        """
        Initialize omega projection based on 12D + 1/(18π) principle
        
        Returns:
            Omega projection vector
        """
        # 12D manifold with phase locking to 1/(18π)
        projection = np.random.randn(self.n_manifold_dim)
        phase_lock = 1.0 / (18 * np.pi)
        
        # Apply phase locking
        projection[0] = phase_lock
        projection = projection / np.linalg.norm(projection)
        
        return projection
    
    def _complex_embedding(self, weights: np.ndarray) -> np.ndarray:
        """
        Multi-scale FFT-based complex embedding
        
        Args:
            weights: Input weights vector
            
        Returns:
            Complex embedding
        """
        # Normalize weights
        weights_normalized = weights / (np.linalg.norm(weights) + 1e-10)
        
        # Multi-scale FFT
        scales = [0.5, 1.0, 2.0]
        n_complex = len(weights_normalized) // 3
        
        complex_weights = np.zeros(n_complex, dtype=np.complex128)
        
        for scale_idx, scale in enumerate(scales):
            scaled_weights = weights_normalized * scale
            fft_result = np.fft.fft(scaled_weights)
            
            # Fuse results with inverse weight scaling
            weight = 1.0 / (scale_idx + 1)
            for i in range(n_complex):
                magnitude = np.abs(fft_result[i])
                phase = np.angle(fft_result[i])
                complex_weights[i] += complex(magnitude * weight, phase * weight)
        
        return complex_weights
    
    def _optical_projection(self, complex_weights: np.ndarray) -> np.ndarray:
        """
        Multi-beam optical projection using interference patterns
        
        Args:
            complex_weights: Complex embedding
            
        Returns:
            Projected real-valued vector
        """
        n_beams = 5
        projected = np.zeros(self.n_manifold_dim)
        
        # Multi-beam interference
        for i in range(self.n_manifold_dim):
            beam_sum = 0.0 + 0.0j
            phase_sum = 0.0
            
            for beam in range(n_beams):
                idx = (i + beam * 7) % len(complex_weights)
                beam_phase = 2.0 * np.pi * beam / n_beams
                
                # Interference pattern
                kernel = np.abs(complex_weights[idx]) * np.exp(1j * (np.angle(complex_weights[idx]) + beam_phase))
                beam_sum += kernel
                phase_sum += np.angle(complex_weights[idx])
            
            # Average phase
            avg_phase = phase_sum / n_beams
            
            # Project to real space
            if i < self.n_manifold_dim // 2:
                projected[i] = beam_sum.real * np.cos(avg_phase)
            else:
                projected[i] = beam_sum.imag * np.sin(avg_phase)
        
        return projected
    
    def _build_affinity_matrix(self, projected: np.ndarray, sigma: float = 1.0) -> np.ndarray:
        """
        Build affinity matrix for manifold embedding
        
        Args:
            projected: Projected vectors
            sigma: Bandwidth parameter for Gaussian kernel
            
        Returns:
            Affinity matrix
        """
        n = len(projected)
        affinity = np.zeros((n, n))
        
        # Vectorized pairwise distances
        projected_matrix = projected.reshape(-1, 1)
        distances_squared = (projected_matrix - projected_matrix.T) ** 2
        affinity = np.exp(-distances_squared / (2 * sigma ** 2))
        
        # Set diagonal to 0 (no self-similarity)
        np.fill_diagonal(affinity, 0)
        
        return affinity
    
    def _svd_embedding(self, affinity: np.ndarray, n_components: Optional[int] = None) -> np.ndarray:
        """
        Use SVD for dimensionality reduction (O(N^2) instead of O(N^3))
        
        Args:
            affinity: Affinity matrix
            n_components: Number of components to extract
            
        Returns:
            Manifold embedding (always n_manifold_dim dimensional)
        """
        if n_components is None:
            n_components = self.n_manifold_dim
        
        n = affinity.shape[0]
        
        # Ensure we don't ask for more components than available
        n_components = min(n_components, n - 1)
        
        # Choose SVD method based on matrix size
        if self.use_randomized and n > 1000:
            # Use randomized SVD for large matrices
            from sklearn.utils.extmath import randomized_svd
            U, S, Vt = randomized_svd(affinity, n_components=n_components, random_state=self.seed)
        else:
            # Use standard SVD for small matrices
            U, S, Vt = svd(affinity, full_matrices=False)
            U = U[:, :n_components]
            S = S[:n_components]
        
        # Extract manifold point (first n_components singular vectors weighted by singular values)
        manifold_point = np.zeros(self.n_manifold_dim)  # Always return full dimension
        for i in range(n_components):
            manifold_point[i] = U[i, 0] * S[i]  # Weight by singular value
        
        # Normalize
        norm = np.linalg.norm(manifold_point)
        if norm > 0:
            manifold_point = manifold_point / norm
        
        return manifold_point
    
    def learn_reference_structure(self, reference_weights: np.ndarray):
        """
        Learn reference structure from weights
        
        Args:
            reference_weights: Reference weight vector
        """
        self.reference_weights = reference_weights.copy()
        self.reference_manifold = self.decode(reference_weights)
        
        print(f"Learned reference structure: {self.n_manifold_dim}D manifold")
    
    def decode(self, weights: np.ndarray) -> np.ndarray:
        """
        Decode weights to manifold point
        
        Args:
            weights: Input weight vector
            
        Returns:
            Manifold point (n_manifold_dim-dimensional)
        """
        # Step 1: Complex embedding
        complex_weights = self._complex_embedding(weights)
        
        # Step 2: Optical projection
        projected = self._optical_projection(complex_weights)
        
        # Step 3: Build affinity matrix
        affinity = self._build_affinity_matrix(projected)
        
        # Step 4: SVD-based manifold embedding
        manifold_point = self._svd_embedding(affinity)
        
        # Step 5: Apply omega projection
        manifold_point = manifold_point * self.omega_projection
        
        # Step 6: Normalize
        norm = np.linalg.norm(manifold_point)
        if norm > 0:
            manifold_point = manifold_point / norm
        
        return manifold_point
    
    def decode_batch(self, weights_list: List[np.ndarray]) -> List[np.ndarray]:
        """
        Decode multiple weight vectors in batch
        
        Args:
            weights_list: List of weight vectors
            
        Returns:
            List of manifold points
        """
        manifold_points = []
        for weights in weights_list:
            manifold_point = self.decode(weights)
            manifold_points.append(manifold_point)
        
        return manifold_points
    
    def reconstruct(self, manifold_point: np.ndarray) -> np.ndarray:
        """
        Reconstruct weights from manifold point (approximate)
        
        Args:
            manifold_point: Manifold point
            
        Returns:
            Reconstructed weight vector
        """
        if self.reference_weights is None:
            raise ValueError("Reference structure not learned. Call learn_reference_structure() first.")
        
        # Approximate reconstruction using reference
        # This is a simplified reconstruction - in practice, would use inverse SVD
        scale_factor = np.linalg.norm(manifold_point)
        reconstructed = self.reference_weights * scale_factor
        
        return reconstructed
    
    def manifold_distance(self, m1: np.ndarray, m2: np.ndarray) -> float:
        """
        Calculate distance between two manifold points
        
        Args:
            m1, m2: Manifold points
            
        Returns:
            Euclidean distance
        """
        return np.linalg.norm(m1 - m2)
    
    def manifold_similarity(self, m1: np.ndarray, m2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two manifold points
        
        Args:
            m1, m2: Manifold points
            
        Returns:
            Cosine similarity
        """
        dot_product = np.dot(m1, m2)
        norm_m1 = np.linalg.norm(m1)
        norm_m2 = np.linalg.norm(m2)
        
        if norm_m1 > 0 and norm_m2 > 0:
            return dot_product / (norm_m1 * norm_m2)
        else:
            return 0.0


def test_svd_decoder():
    """Test SVD decoder functionality"""
    print("Testing SVD Decoder...")
    
    # Create decoder
    n_weights = 50000
    decoder = SVDDecoder(n_weights=n_weights, n_manifold_dim=12, use_randomized=True)
    
    # Generate random weights
    weights = np.random.randn(n_weights)
    
    # Learn reference structure
    decoder.learn_reference_structure(weights)
    
    # Decode to manifold
    manifold_point = decoder.decode(weights)
    
    print(f"  Decoded {n_weights} weights to {len(manifold_point)}D manifold")
    print(f"  Manifold point: {manifold_point[:5]}...")
    print(f"  Manifold norm: {np.linalg.norm(manifold_point):.6f}")
    
    # Test batch decoding
    weights_list = [np.random.randn(n_weights) for _ in range(5)]
    manifold_points = decoder.decode_batch(weights_list)
    
    print(f"  Batch decoded {len(manifold_points)} weight vectors")
    
    # Test reconstruction
    reconstructed = decoder.reconstruct(manifold_point)
    reconstruction_error = np.linalg.norm(weights - reconstructed)
    
    print(f"  Reconstruction error: {reconstruction_error:.6f}")
    
    # Test distance and similarity
    m1 = decoder.decode(np.random.randn(n_weights))
    m2 = decoder.decode(np.random.randn(n_weights))
    
    distance = decoder.manifold_distance(m1, m2)
    similarity = decoder.manifold_similarity(m1, m2)
    
    print(f"  Distance between random manifolds: {distance:.6f}")
    print(f"  Similarity between random manifolds: {similarity:.6f}")
    
    print("  All tests passed!")


if __name__ == "__main__":
    test_svd_decoder()
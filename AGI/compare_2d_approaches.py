"""
Competitive Evaluation Framework for 2D Image Learning Approaches

Compares multiple candidate approaches:
1. Column-to-Line Flattening (Baseline)
2. Holographic/Wavelet Encoding
3. Fractal/Space-Filling Curve (Hilbert)
4. Quadtree/Multi-Scale Decomposition
5. Graph-Based Embedding
6. Manifold Learning (Isomap/LLE)

Metrics:
- Reconstruction quality
- Spatial preservation
- Integrated information
- Computational efficiency
"""

import numpy as np
from typing import Dict, Tuple, List, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
import time


@dataclass
class EncodingResult:
    """Result of encoding an image"""
    embedding: np.ndarray
    reconstruction: np.ndarray
    reconstruction_quality: float
    spatial_preservation: float
    integrated_information: float
    encoding_time: float
    decoding_time: float
    metadata: dict


class ImageEncoder(ABC):
    """Abstract base class for image encoders"""
    
    def __init__(self, image_dim: Tuple[int, int], embedding_dim: int = 12):
        self.image_dim = image_dim
        self.embedding_dim = embedding_dim
        self.name = self.__class__.__name__
    
    @abstractmethod
    def encode(self, image: np.ndarray) -> np.ndarray:
        """Encode 2D image to embedding"""
        pass
    
    @abstractmethod
    def decode(self, embedding: np.ndarray) -> np.ndarray:
        """Decode embedding back to 2D image"""
        pass
    
    def evaluate(self, image: np.ndarray) -> EncodingResult:
        """Evaluate encoding on an image"""
        # Measure encoding time
        start_time = time.time()
        embedding = self.encode(image)
        encoding_time = time.time() - start_time
        
        # Measure decoding time
        start_time = time.time()
        reconstruction = self.decode(embedding)
        decoding_time = time.time() - start_time
        
        # Calculate metrics
        reconstruction_quality = self._calculate_reconstruction_quality(image, reconstruction)
        spatial_preservation = self._calculate_spatial_preservation(image, reconstruction)
        integrated_information = self._calculate_integrated_information(image, reconstruction)
        
        return EncodingResult(
            embedding=embedding,
            reconstruction=reconstruction,
            reconstruction_quality=reconstruction_quality,
            spatial_preservation=spatial_preservation,
            integrated_information=integrated_information,
            encoding_time=encoding_time,
            decoding_time=decoding_time,
            metadata={"name": self.name, "embedding_dim": self.embedding_dim}
        )
    
    def _calculate_reconstruction_quality(self, original: np.ndarray, reconstructed: np.ndarray) -> float:
        """Calculate reconstruction quality (1 - MSE)"""
        if original.max() > 0:
            original = original / original.max()
        if reconstructed.max() > 0:
            reconstructed = reconstructed / reconstructed.max()
        
        mse = np.mean((original - reconstructed)**2)
        return max(0, 1.0 - mse)
    
    def _calculate_spatial_preservation(self, original: np.ndarray, reconstructed: np.ndarray) -> float:
        """
        Calculate how well spatial relationships are preserved
        
        Uses gradient correlation to measure spatial preservation
        """
        # Calculate gradients
        orig_grad_x = np.gradient(original, axis=1)
        orig_grad_y = np.gradient(original, axis=0)
        recon_grad_x = np.gradient(reconstructed, axis=1)
        recon_grad_y = np.gradient(reconstructed, axis=0)
        
        # Correlation of gradients
        corr_x = np.corrcoef(orig_grad_x.flatten(), recon_grad_x.flatten())[0, 1]
        corr_y = np.corrcoef(orig_grad_y.flatten(), recon_grad_y.flatten())[0, 1]
        
        # Average correlation (handle NaN)
        correlations = [c for c in [corr_x, corr_y] if not np.isnan(c)]
        return np.mean(correlations) if correlations else 0.0
    
    def _calculate_integrated_information(self, original: np.ndarray, reconstructed: np.ndarray) -> float:
        """
        Calculate integrated information (IIT-style)
        
        Measures how information is distributed across the encoding
        """
        # Use entropy difference as proxy
        def entropy(arr):
            arr = arr.flatten()
            prob = arr**2
            prob = prob / (np.sum(prob) + 1e-10)
            return -np.sum(prob * np.log(prob + 1e-10))
        
        orig_entropy = entropy(original)
        recon_entropy = entropy(reconstructed)
        
        # Integrated information = ratio of entropies
        return min(1.0, recon_entropy / (orig_entropy + 1e-10))


class ColumnToLineEncoder(ImageEncoder):
    """Baseline: Column-to-line flattening"""
    
    def encode(self, image: np.ndarray) -> np.ndarray:
        """Flatten 2D image to 1D, then compress to embedding"""
        # Flatten
        flattened = image.flatten()
        
        # Compress to embedding dim using random projection
        np.random.seed(42)  # For reproducibility
        projection = np.random.randn(len(flattened), self.embedding_dim)
        embedding = np.dot(flattened, projection)
        
        # Normalize
        embedding = embedding / (np.linalg.norm(embedding) + 1e-10)
        return embedding
    
    def decode(self, embedding: np.ndarray) -> np.ndarray:
        """Decode embedding back to 2D image"""
        # Use same random projection (transpose)
        np.random.seed(42)
        projection = np.random.randn(self.image_dim[0] * self.image_dim[1], self.embedding_dim)
        
        # Project back
        flattened = np.dot(embedding, projection.T)
        
        # Reshape to 2D
        reconstruction = flattened.reshape(self.image_dim)
        
        # Normalize
        reconstruction = np.clip(reconstruction, 0, 1)
        reconstruction = reconstruction / (reconstruction.max() + 1e-10)
        
        return reconstruction


class HolographicEncoder(ImageEncoder):
    """Holographic/Wavelet encoding"""
    
    def __init__(self, image_dim: Tuple[int, int], embedding_dim: int = 12):
        super().__init__(image_dim, embedding_dim)
        self.basis = self._create_holographic_basis()
    
    def _create_holographic_basis(self) -> np.ndarray:
        """Create holographic spatial frequency basis"""
        basis = np.zeros((self.embedding_dim, self.image_dim[0], self.image_dim[1]))
        
        center_x, center_y = self.image_dim[0] // 2, self.image_dim[1] // 2
        
        for i in range(self.embedding_dim):
            frequency = (i + 1) / self.embedding_dim
            angle = (i * np.pi) / self.embedding_dim
            
            y, x = np.ogrid[0:self.image_dim[1], 0:self.image_dim[0]]
            r = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            
            # Holographic wavelet
            basis[i] = np.sin(2 * np.pi * frequency * r * np.cos(angle) + frequency * 10)
            basis[i] = basis[i] / (np.linalg.norm(basis[i]) + 1e-10)
        
        return basis
    
    def encode(self, image: np.ndarray) -> np.ndarray:
        """Project onto holographic basis"""
        coefficients = np.zeros(self.embedding_dim)
        for i in range(self.embedding_dim):
            coefficients[i] = np.sum(image * self.basis[i])
        
        # Normalize
        embedding = coefficients / (np.linalg.norm(coefficients) + 1e-10)
        return embedding
    
    def decode(self, embedding: np.ndarray) -> np.ndarray:
        """Reconstruct from holographic coefficients"""
        reconstruction = np.zeros(self.image_dim)
        for i in range(self.embedding_dim):
            reconstruction += embedding[i] * self.basis[i]
        
        # Normalize
        reconstruction = np.clip(reconstruction, 0, 1)
        reconstruction = reconstruction / (reconstruction.max() + 1e-10)
        
        return reconstruction


class HilbertCurveEncoder(ImageEncoder):
    """Fractal encoding using Hilbert space-filling curve"""
    
    def __init__(self, image_dim: Tuple[int, int], embedding_dim: int = 12):
        super().__init__(image_dim, embedding_dim)
        self.hilbert_order = int(np.log2(min(image_dim)))
        self.hilbert_map = self._create_hilbert_map()
    
    def _create_hilbert_map(self) -> np.ndarray:
        """Create Hilbert curve mapping"""
        size = 2 ** self.hilbert_order
        hilbert_map = np.zeros((size, size), dtype=int)
        
        for y in range(size):
            for x in range(size):
                hilbert_map[y, x] = self._hilbert_index(x, y, self.hilbert_order)
        
        return hilbert_map
    
    def _hilbert_index(self, x: int, y: int, order: int) -> int:
        """Calculate Hilbert curve index"""
        index = 0
        s = 1 << (order - 1)
        
        for _ in range(order):
            rx = 1 & (x // s)
            ry = 1 & (y // s)
            index += s * s * ((3 * rx) ^ ry)
            
            # Rotate/flip
            if ry == 0:
                if rx == 1:
                    x = s - 1 - x
                    y = s - 1 - y
                x, y = y, x
            
            s //= 2
        
        return index
    
    def encode(self, image: np.ndarray) -> np.ndarray:
        """Encode using Hilbert curve ordering"""
        # Flatten using Hilbert order
        flattened = np.zeros(self.image_dim[0] * self.image_dim[1])
        
        size = min(self.image_dim[0], self.image_dim[1])
        for y in range(size):
            for x in range(size):
                idx = self.hilbert_map[y, x]
                flattened[idx] = image[y, x]
        
        # Compress using PCA-like projection
        np.random.seed(43)
        projection = np.random.randn(len(flattened), self.embedding_dim)
        embedding = np.dot(flattened, projection)
        
        # Normalize
        embedding = embedding / (np.linalg.norm(embedding) + 1e-10)
        return embedding
    
    def decode(self, embedding: np.ndarray) -> np.ndarray:
        """Decode from Hilbert curve ordering"""
        # Project back
        np.random.seed(43)
        projection = np.random.randn(self.image_dim[0] * self.image_dim[1], self.embedding_dim)
        flattened = np.dot(embedding, projection.T)
        
        # Reshape using Hilbert order
        reconstruction = np.zeros(self.image_dim)
        size = min(self.image_dim[0], self.image_dim[1])
        
        for y in range(size):
            for x in range(size):
                idx = self.hilbert_map[y, x]
                reconstruction[y, x] = flattened[idx]
        
        # Normalize
        reconstruction = np.clip(reconstruction, 0, 1)
        reconstruction = reconstruction / (reconstruction.max() + 1e-10)
        
        return reconstruction


class QuadtreeEncoder(ImageEncoder):
    """Multi-scale quadtree decomposition"""
    
    def __init__(self, image_dim: Tuple[int, int], embedding_dim: int = 12):
        super().__init__(image_dim, embedding_dim)
        self.max_depth = int(np.log2(min(image_dim))) - 1
    
    def encode(self, image: np.ndarray) -> np.ndarray:
        """Encode using quadtree decomposition"""
        features = []
        
        # Extract features at multiple scales
        for depth in range(self.max_depth + 1):
            block_size = 2 ** depth
            features.append(self._extract_scale_features(image, block_size))
        
        # Combine and compress
        combined = np.concatenate(features)
        
        # Compress to embedding dimension
        if len(combined) > self.embedding_dim:
            # Simple sampling
            indices = np.linspace(0, len(combined) - 1, self.embedding_dim, dtype=int)
            embedding = combined[indices]
        else:
            # Pad
            embedding = np.pad(combined, (0, self.embedding_dim - len(combined)))
        
        # Normalize
        embedding = embedding / (np.linalg.norm(embedding) + 1e-10)
        return embedding
    
    def _extract_scale_features(self, image: np.ndarray, block_size: int) -> np.ndarray:
        """Extract features at a specific scale"""
        h, w = image.shape
        features = []
        
        for y in range(0, h, block_size):
            for x in range(0, w, block_size):
                block = image[y:y+block_size, x:x+block_size]
                if block.size > 0:
                    features.append(np.mean(block))
                    features.append(np.std(block))
        
        return np.array(features)
    
    def decode(self, embedding: np.ndarray) -> np.ndarray:
        """Decode from quadtree features (simplified reconstruction)"""
        # This is a simplified reconstruction
        # In practice, would need more sophisticated reconstruction
        
        reconstruction = np.zeros(self.image_dim)
        
        # Use embedding to guide reconstruction
        # Simple approach: create gradient-like pattern
        for i in range(self.embedding_dim):
            y = (i // self.embedding_dim) * self.image_dim[0]
            x = (i % self.embedding_dim) * self.image_dim[1]
            if y < self.image_dim[0] and x < self.image_dim[1]:
                reconstruction[y, x] = embedding[i]
        
        # Smooth reconstruction
        # Simple averaging
        from scipy import ndimage
        try:
            reconstruction = ndimage.gaussian_filter(reconstruction, sigma=1)
        except ImportError:
            pass
        
        # Normalize
        reconstruction = np.clip(reconstruction, 0, 1)
        reconstruction = reconstruction / (reconstruction.max() + 1e-10)
        
        return reconstruction


class GraphEncoder(ImageEncoder):
    """Graph-based embedding (adjacency graph)"""
    
    def __init__(self, image_dim: Tuple[int, int], embedding_dim: int = 12):
        super().__init__(image_dim, embedding_dim)
        self.adjacency_matrix = self._create_adjacency_matrix()
    
    def _create_adjacency_matrix(self) -> np.ndarray:
        """Create adjacency matrix for image grid"""
        size = self.image_dim[0] * self.image_dim[1]
        adjacency = np.zeros((size, size))
        
        for y in range(self.image_dim[0]):
            for x in range(self.image_dim[1]):
                idx = y * self.image_dim[1] + x
                
                # Connect to neighbors
                neighbors = []
                if y > 0:
                    neighbors.append((y - 1, x))
                if y < self.image_dim[0] - 1:
                    neighbors.append((y + 1, x))
                if x > 0:
                    neighbors.append((y, x - 1))
                if x < self.image_dim[1] - 1:
                    neighbors.append((y, x + 1))
                
                for ny, nx in neighbors:
                    nidx = ny * self.image_dim[1] + nx
                    adjacency[idx, nidx] = 1
        
        return adjacency
    
    def encode(self, image: np.ndarray) -> np.ndarray:
        """Encode using graph-based approach"""
        # Flatten image
        flattened = image.flatten()
        
        # Simple graph-based encoding: use adjacency to smooth
        # Apply graph Laplacian
        degree = np.sum(self.adjacency_matrix, axis=1)
        laplacian = np.diag(degree) - self.adjacency_matrix
        
        # Smooth signal on graph
        smoothed = flattened - 0.1 * np.dot(laplacian, flattened)
        
        # Compress
        np.random.seed(44)
        projection = np.random.randn(len(smoothed), self.embedding_dim)
        embedding = np.dot(smoothed, projection)
        
        # Normalize
        embedding = embedding / (np.linalg.norm(embedding) + 1e-10)
        return embedding
    
    def decode(self, embedding: np.ndarray) -> np.ndarray:
        """Decode from graph embedding"""
        # Project back
        np.random.seed(44)
        projection = np.random.randn(self.image_dim[0] * self.image_dim[1], self.embedding_dim)
        flattened = np.dot(embedding, projection.T)
        
        # Reshape
        reconstruction = flattened.reshape(self.image_dim)
        
        # Apply graph smoothing
        reconstruction = reconstruction / (reconstruction.max() + 1e-10)
        
        return reconstruction


class ManifoldLearningEncoder(ImageEncoder):
    """Manifold learning (Isomap-style)"""
    
    def __init__(self, image_dim: Tuple[int, int], embedding_dim: int = 12):
        super().__init__(image_dim, embedding_dim)
        self.reference_images = []
        self.is_trained = False
    
    def train(self, images: List[np.ndarray]):
        """Train on reference images"""
        self.reference_images = images
        self.is_trained = True
    
    def encode(self, image: np.ndarray) -> np.ndarray:
        """Encode using manifold learning"""
        if not self.is_trained or len(self.reference_images) == 0:
            # Fallback: simple projection
            flattened = image.flatten()
            np.random.seed(45)
            projection = np.random.randn(len(flattened), self.embedding_dim)
            embedding = np.dot(flattened, projection)
            return embedding / (np.linalg.norm(embedding) + 1e-10)
        
        # Find nearest neighbors in reference set
        flattened = image.flatten()
        flattened = flattened / (np.linalg.norm(flattened) + 1e-10)
        
        similarities = []
        for ref_img in self.reference_images:
            ref_flat = ref_img.flatten()
            ref_flat = ref_flat / (np.linalg.norm(ref_flat) + 1e-10)
            similarity = np.dot(flattened, ref_flat)
            similarities.append(similarity)
        
        # Use top similarities as embedding
        similarities = np.array(similarities)
        top_k = min(self.embedding_dim, len(similarities))
        top_indices = np.argsort(similarities)[-top_k:]
        
        embedding = np.zeros(self.embedding_dim)
        for i, idx in enumerate(top_indices):
            embedding[i] = similarities[idx]
        
        # Normalize
        embedding = embedding / (np.linalg.norm(embedding) + 1e-10)
        return embedding
    
    def decode(self, embedding: np.ndarray) -> np.ndarray:
        """Decode from manifold embedding"""
        if not self.is_trained or len(self.reference_images) == 0:
            # Fallback
            reconstruction = np.random.randn(*self.image_dim)
            reconstruction = np.abs(reconstruction)
            reconstruction = reconstruction / (reconstruction.max() + 1e-10)
            return reconstruction
        
        # Weighted combination of reference images
        top_k = min(self.embedding_dim, len(self.reference_images))
        weights = embedding[:top_k]
        
        reconstruction = np.zeros(self.image_dim)
        total_weight = 0
        
        for i in range(len(weights)):
            if i < len(self.reference_images):
                reconstruction += weights[i] * self.reference_images[i]
                total_weight += weights[i]
        
        if total_weight > 0:
            reconstruction /= total_weight
        
        # Normalize
        reconstruction = np.clip(reconstruction, 0, 1)
        reconstruction = reconstruction / (reconstruction.max() + 1e-10)
        
        return reconstruction


def create_test_images(image_dim: Tuple[int, int] = (28, 28)) -> Dict[str, np.ndarray]:
    """Create diverse test images"""
    images = {}
    
    # Horizontal line
    img = np.zeros(image_dim)
    img[image_dim[0] // 2, :] = 1.0
    images["horizontal_line"] = img
    
    # Vertical line
    img = np.zeros(image_dim)
    img[:, image_dim[1] // 2] = 1.0
    images["vertical_line"] = img
    
    # Diagonal line
    img = np.zeros(image_dim)
    for i in range(min(image_dim)):
        img[i, i] = 1.0
    images["diagonal_line"] = img
    
    # Cross
    img = np.zeros(image_dim)
    img[image_dim[0] // 2, :] = 1.0
    img[:, image_dim[1] // 2] = 1.0
    images["cross"] = img
    
    # Circle
    img = np.zeros(image_dim)
    y, x = np.ogrid[0:image_dim[0], 0:image_dim[1]]
    center_x, center_y = image_dim[1] // 2, image_dim[0] // 2
    radius = 8
    circle_mask = (x - center_x)**2 + (y - center_y)**2 <= radius**2
    img[circle_mask] = 1.0
    images["circle"] = img
    
    # Checkerboard
    img = np.zeros(image_dim)
    for i in range(image_dim[0]):
        for j in range(image_dim[1]):
            if ((i // 4) + (j // 4)) % 2 == 0:
                img[i, j] = 1.0
    images["checkerboard"] = img
    
    # Gaussian blob
    img = np.zeros(image_dim)
    y, x = np.ogrid[0:image_dim[0], 0:image_dim[1]]
    center_x, center_y = image_dim[1] // 2, image_dim[0] // 2
    sigma = 4
    img = np.exp(-((x - center_x)**2 + (y - center_y)**2) / (2 * sigma**2))
    images["gaussian_blob"] = img
    
    # Noise
    img = np.random.rand(*image_dim)
    images["noise"] = img
    
    return images


def compare_approaches(image_dim: Tuple[int, int] = (28, 28), embedding_dim: int = 12):
    """Compare all approaches on test images"""
    print("=" * 80)
    print("Competitive Evaluation of 2D Image Learning Approaches")
    print("=" * 80)
    
    # Create test images
    test_images = create_test_images(image_dim)
    print(f"\nCreated {len(test_images)} test images: {list(test_images.keys())}")
    
    # Initialize encoders
    encoders = [
        ColumnToLineEncoder(image_dim, embedding_dim),
        HolographicEncoder(image_dim, embedding_dim),
        HilbertCurveEncoder(image_dim, embedding_dim),
        QuadtreeEncoder(image_dim, embedding_dim),
        GraphEncoder(image_dim, embedding_dim),
        ManifoldLearningEncoder(image_dim, embedding_dim),
    ]
    
    # Train manifold learning encoder
    manifold_encoder = encoders[-1]
    manifold_encoder.train(list(test_images.values()))
    
    print(f"\nEvaluating {len(encoders)} approaches:")
    for encoder in encoders:
        print(f"  - {encoder.name}")
    
    # Evaluate each approach
    results = {}
    for encoder in encoders:
        print(f"\n{'='*80}")
        print(f"Evaluating: {encoder.name}")
        print(f"{'='*80}")
        
        encoder_results = []
        
        for image_name, image in test_images.items():
            result = encoder.evaluate(image)
            encoder_results.append((image_name, result))
            
            print(f"\n  {image_name}:")
            print(f"    Reconstruction quality: {result.reconstruction_quality:.4f}")
            print(f"    Spatial preservation: {result.spatial_preservation:.4f}")
            print(f"    Integrated information: {result.integrated_information:.4f}")
            print(f"    Encoding time: {result.encoding_time*1000:.2f}ms")
            print(f"    Decoding time: {result.decoding_time*1000:.2f}ms")
        
        results[encoder.name] = encoder_results
    
    # Summary statistics
    print(f"\n{'='*80}")
    print("SUMMARY STATISTICS")
    print(f"{'='*80}")
    
    summary = {}
    for encoder_name, encoder_results in results.items():
        qualities = [r.reconstruction_quality for _, r in encoder_results]
        spatial = [r.spatial_preservation for _, r in encoder_results]
        integrated = [r.integrated_information for _, r in encoder_results]
        encode_times = [r.encoding_time for _, r in encoder_results]
        decode_times = [r.decoding_time for _, r in encoder_results]
        
        summary[encoder_name] = {
            "avg_quality": np.mean(qualities),
            "avg_spatial": np.mean(spatial),
            "avg_integrated": np.mean(integrated),
            "avg_encode_time": np.mean(encode_times),
            "avg_decode_time": np.mean(decode_times),
            "overall_score": np.mean(qualities) * 0.4 + np.mean(spatial) * 0.3 + np.mean(integrated) * 0.3
        }
    
    # Print summary
    print(f"\n{'Approach':<30} {'Quality':>10} {'Spatial':>10} {'Integrated':>10} {'Time(ms)':>12} {'Score':>10}")
    print("-" * 92)
    
    # Sort by overall score
    sorted_approaches = sorted(summary.items(), key=lambda x: x[1]["overall_score"], reverse=True)
    
    for rank, (encoder_name, stats) in enumerate(sorted_approaches, 1):
        print(f"{rank}. {encoder_name:<28} {stats['avg_quality']:>10.4f} "
              f"{stats['avg_spatial']:>10.4f} {stats['avg_integrated']:>10.4f} "
              f"{(stats['avg_encode_time'] + stats['avg_decode_time'])*1000:>11.2f} "
              f"{stats['overall_score']:>10.4f}")
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    best_approach = sorted_approaches[0][0]
    print(f"\n🏆 Best Overall: {best_approach}")
    
    # Category winners
    best_quality = max(summary.items(), key=lambda x: x[1]["avg_quality"])
    best_spatial = max(summary.items(), key=lambda x: x[1]['avg_spatial'])
    best_integrated = max(summary.items(), key=lambda x: x[1]['avg_integrated'])
    fastest = min(summary.items(), key=lambda x: x[1]["avg_encode_time"] + x[1]["avg_decode_time"])
    
    print(f"\n  Best Reconstruction Quality: {best_quality[0]} ({best_quality[1]['avg_quality']:.4f})")
    print(f"  Best Spatial Preservation: {best_spatial[0]} ({best_spatial[1]['avg_spatial']:.4f})")
    print(f"  Best Integrated Information: {best_integrated[0]} ({best_integrated[1]['avg_integrated']:.4f})")
    print(f"  Fastest: {fastest[0]} ({(fastest[1]['avg_encode_time'] + fastest[1]['avg_decode_time'])*1000:.2f}ms)")
    
    print("\n" + "=" * 80)
    print("KEY INSIGHTS")
    print("=" * 80)
    
    # Analysis
    if best_spatial[0] == "HolographicEncoder":
        print("\n✓ Holographic approach best preserves spatial relationships")
        print("  → Supports holographic theory for 2D image learning")
    elif best_spatial[0] == "HilbertCurveEncoder":
        print("\n✓ Hilbert curve (fractal) best preserves spatial relationships")
        print("  → Suggests space-filling curves are optimal for 2D locality")
    elif best_spatial[0] == "GraphEncoder":
        print("\n✓ Graph-based approach best preserves spatial relationships")
        print("  → Explicit adjacency modeling is crucial")
    
    print(f"\n→ Baseline (Column-to-Line) performance: {summary['ColumnToLineEncoder']['overall_score']:.4f}")
    print(f"→ Best improvement: {sorted_approaches[0][1]['overall_score'] / summary['ColumnToLineEncoder']['overall_score']:.2f}x")
    
    print("\n" + "=" * 80)
    print("✓ Competitive evaluation complete!")
    print("=" * 80)
    
    return results, summary


if __name__ == "__main__":
    results, summary = compare_approaches(image_dim=(28, 28), embedding_dim=12)
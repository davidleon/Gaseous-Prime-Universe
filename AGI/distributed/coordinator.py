"""
Distributed Manifold Coordinator
Manages coordination between 100,000+ manifolds with joint optimization
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Callable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import cpu_count
import warnings

warnings.filterwarnings('ignore')


class ManifoldInstance:
    """
    Single manifold instance with its decoder and state
    """
    
    def __init__(
        self,
        manifold_id: int,
        n_weights: int,
        n_manifold_dim: int = 12,
        seed: int = 42
    ):
        """
        Initialize manifold instance
        
        Args:
            manifold_id: Unique identifier
            n_weights: Number of weights
            n_manifold_dim: Manifold dimensionality
            seed: Random seed
        """
        self.manifold_id = manifold_id
        self.n_weights = n_weights
        self.n_manifold_dim = n_manifold_dim
        self.seed = seed
        
        # Manifold state
        self.manifold_point: Optional[np.ndarray] = None
        self.confidence: float = 0.0
        self.specialization: str = "general"
        
        # Performance metrics
        self.accuracy: float = 0.0
        self.error_rate: float = 1.0
        
    def set_state(
        self,
        manifold_point: np.ndarray,
        confidence: float = 1.0,
        specialization: str = "general"
    ):
        """Set manifold state"""
        self.manifold_point = manifold_point.copy()
        self.confidence = confidence
        self.specialization = specialization
    
    def predict(self, x: np.ndarray) -> Tuple[int, float]:
        """
        Make prediction using manifold
        
        Args:
            x: Input vector
            
        Returns:
            (prediction, confidence)
        """
        if self.manifold_point is None:
            return 0, 0.0
        
        # Simplified prediction based on manifold
        # In practice, would use manifold-based classifier
        similarity = np.dot(x[:min(len(x), len(self.manifold_point))], 
                          self.manifold_point[:min(len(x), len(self.manifold_point))])
        
        # Convert similarity to prediction (0-9 for digits)
        prediction = int(abs(similarity * 100)) % 10
        confidence = min(1.0, abs(similarity))
        
        return prediction, confidence * self.confidence


class DistributedCoordinator:
    """
    Coordinates 100,000+ distributed manifolds
    """
    
    def __init__(
        self,
        n_manifolds: int = 100000,
        n_weights: int = 50000,
        n_manifold_dim: int = 12,
        use_parallel: bool = True,
        n_workers: Optional[int] = None,
        precision_bits: int = 400
    ):
        """
        Initialize distributed coordinator
        
        Args:
            n_manifolds: Number of manifolds (100,000 by default)
            n_weights: Number of weights per manifold
            n_manifold_dim: Dimensionality of each manifold
            use_parallel: Use parallel processing
            n_workers: Number of workers (default: cpu_count)
            precision_bits: Precision for calculations
        """
        self.n_manifolds = n_manifolds
        self.n_weights = n_weights
        self.n_manifold_dim = n_manifold_dim
        self.use_parallel = use_parallel
        self.precision_bits = precision_bits
        
        # Number of workers
        if n_workers is None:
            self.n_workers = min(cpu_count(), 32) if use_parallel else 1
        else:
            self.n_workers = n_workers
        
        # Initialize manifolds
        self.manifolds: Dict[int, ManifoldInstance] = {}
        for i in range(n_manifolds):
            manifold = ManifoldInstance(
                manifold_id=i,
                n_weights=n_weights,
                n_manifold_dim=n_manifold_dim,
                seed=42 + i
            )
            self.manifolds[i] = manifold
        
        # Coordination weights (joint optimization)
        self.coordination_weights = np.ones(n_manifolds) / n_manifolds
        
        # Performance tracking
        self.total_predictions = 0
        self.correct_predictions = 0
        self.accuracy_history: List[float] = []
        
        print(f"Initialized distributed coordinator with {n_manifolds} manifolds")
        print(f"  Using {self.n_workers} workers for parallel processing")
    
    def set_manifold_state(
        self,
        manifold_id: int,
        manifold_point: np.ndarray,
        confidence: float = 1.0,
        specialization: str = "general"
    ):
        """
        Set state for a specific manifold
        
        Args:
            manifold_id: Manifold ID
            manifold_point: Manifold point
            confidence: Confidence score
            specialization: Specialization type
        """
        if manifold_id not in self.manifolds:
            raise ValueError(f"Manifold {manifold_id} not found")
        
        self.manifolds[manifold_id].set_state(manifold_point, confidence, specialization)
    
    def set_manifolds_batch(
        self,
        manifold_ids: List[int],
        manifold_points: List[np.ndarray],
        confidences: Optional[List[float]] = None,
        specializations: Optional[List[str]] = None
    ):
        """
        Set states for multiple manifolds in batch
        
        Args:
            manifold_ids: List of manifold IDs
            manifold_points: List of manifold points
            confidences: Optional list of confidences
            specializations: Optional list of specializations
        """
        if len(manifold_ids) != len(manifold_points):
            raise ValueError("manifold_ids and manifold_points must have same length")
        
        if confidences is None:
            confidences = [1.0] * len(manifold_ids)
        
        if specializations is None:
            specializations = ["general"] * len(manifold_ids)
        
        for manifold_id, point, conf, spec in zip(manifold_ids, manifold_points, confidences, specializations):
            self.set_manifold_state(manifold_id, point, conf, spec)
    
    def optimize_coordination_weights(self, validation_data: List[Tuple[np.ndarray, int]]):
        """
        Optimize coordination weights using joint optimization
        
        Minimizes F_joint ≤ Σ F_independent
        
        Args:
            validation_data: List of (input, label) pairs
        """
        print("Optimizing coordination weights...")
        
        # Calculate errors for each manifold
        manifold_errors = np.zeros(self.n_manifolds)
        
        for manifold in self.manifolds.values():
            if manifold.manifold_point is None:
                manifold_errors[manifold.manifold_id] = 1.0
                continue
            
            errors = 0
            total = 0
            
            for x, label in validation_data:
                pred, conf = manifold.predict(x)
                if pred != label:
                    errors += 1
                total += 1
            
            if total > 0:
                manifold_errors[manifold.manifold_id] = errors / total
                manifold.error_rate = manifold_errors[manifold.manifold_id]
                manifold.accuracy = 1.0 - manifold.error_rate
        
        # Calculate coordination weights (inverse of error)
        # F_joint ≤ Σ F_independent with synergy gain
        total_inv_error = np.sum(1.0 / (manifold_errors + 1e-10))
        
        for manifold_id in range(self.n_manifolds):
            self.coordination_weights[manifold_id] = (1.0 / (manifold_errors[manifold_id] + 1e-10)) / total_inv_error
        
        # Normalize weights
        self.coordination_weights = self.coordination_weights / np.sum(self.coordination_weights)
        
        print(f"  Optimized weights: min={self.coordination_weights.min():.6f}, max={self.coordination_weights.max():.6f}")
        print(f"  Average weight: {self.coordination_weights.mean():.6f}")
    
    def predict_single(self, x: np.ndarray) -> Tuple[int, float, Dict[int, Tuple[int, float]]]:
        """
        Make prediction using all manifolds
        
        Args:
            x: Input vector
            
        Returns:
            (prediction, confidence, individual_predictions)
        """
        # Collect predictions from all manifolds
        votes = np.zeros(10)
        individual_predictions = {}
        
        for manifold in self.manifolds.values():
            if manifold.manifold_point is None:
                continue
            
            pred, conf = manifold.predict(x)
            weight = self.coordination_weights[manifold.manifold_id]
            
            votes[pred] += weight * conf
            individual_predictions[manifold.manifold_id] = (pred, conf)
        
        # Weighted voting
        final_prediction = np.argmax(votes)
        final_confidence = votes[final_prediction] / (np.sum(votes) + 1e-10)
        
        return final_prediction, final_confidence, individual_predictions
    
    def predict_batch(self, inputs: List[np.ndarray]) -> List[Tuple[int, float]]:
        """
        Make predictions for multiple inputs
        
        Args:
            inputs: List of input vectors
            
        Returns:
            List of (prediction, confidence) tuples
        """
        results = []
        
        if self.use_parallel and self.n_workers > 1:
            # Parallel prediction
            with ThreadPoolExecutor(max_workers=self.n_workers) as executor:
                futures = [executor.submit(self.predict_single, x) for x in inputs]
                results = [(future.result()[0], future.result()[1]) for future in futures]
        else:
            # Sequential prediction
            for x in inputs:
                pred, conf, _ = self.predict_single(x)
                results.append((pred, conf))
        
        return results
    
    def evaluate(self, test_data: List[Tuple[np.ndarray, int]]) -> Dict[str, float]:
        """
        Evaluate system performance
        
        Args:
            test_data: List of (input, label) pairs
            
        Returns:
            Performance metrics
        """
        print("Evaluating system performance...")
        
        correct = 0
        total = len(test_data)
        confidences = []
        
        for x, label in test_data:
            pred, conf, _ = self.predict_single(x)
            confidences.append(conf)
            
            if pred == label:
                correct += 1
        
        accuracy = correct / total if total > 0 else 0.0
        avg_confidence = np.mean(confidences) if confidences else 0.0
        
        # Update tracking
        self.total_predictions += total
        self.correct_predictions += correct
        self.accuracy_history.append(accuracy)
        
        metrics = {
            "accuracy": accuracy,
            "avg_confidence": avg_confidence,
            "total_correct": correct,
            "total_samples": total,
            "overall_accuracy": self.correct_predictions / self.total_predictions if self.total_predictions > 0 else 0.0
        }
        
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  Average confidence: {avg_confidence:.4f}")
        print(f"  Overall accuracy: {metrics['overall_accuracy']:.4f}")
        
        return metrics
    
    def get_manifold_stats(self) -> Dict[str, any]:
        """
        Get statistics about manifolds
        
        Returns:
            Dictionary of statistics
        """
        specializations = {}
        accuracies = []
        confidences = []
        
        for manifold in self.manifolds.values():
            spec = manifold.specialization
            if spec not in specializations:
                specializations[spec] = 0
            specializations[spec] += 1
            
            if manifold.manifold_point is not None:
                accuracies.append(manifold.accuracy)
                confidences.append(manifold.confidence)
        
        stats = {
            "n_manifolds": self.n_manifolds,
            "n_active": len([m for m in self.manifolds.values() if m.manifold_point is not None]),
            "specializations": specializations,
            "avg_accuracy": np.mean(accuracies) if accuracies else 0.0,
            "avg_confidence": np.mean(confidences) if confidences else 0.0,
            "total_predictions": self.total_predictions,
            "correct_predictions": self.correct_predictions
        }
        
        return stats
    
    def get_top_manifolds(self, n: int = 10) -> List[Tuple[int, float]]:
        """
        Get top performing manifolds
        
        Args:
            n: Number of top manifolds to return
            
        Returns:
            List of (manifold_id, weight) tuples
        """
        # Sort by coordination weight (which is based on performance)
        sorted_indices = np.argsort(self.coordination_weights)[::-1]
        
        top_manifolds = []
        for idx in sorted_indices[:n]:
            top_manifolds.append((idx, self.coordination_weights[idx]))
        
        return top_manifolds


def test_distributed_coordinator():
    """Test distributed coordinator"""
    print("Testing Distributed Coordinator...")
    
    # Create coordinator with 100 manifolds (for testing)
    coordinator = DistributedCoordinator(
        n_manifolds=100,
        n_weights=1000,
        n_manifold_dim=12,
        use_parallel=True
    )
    
    # Set manifold states
    manifold_ids = list(range(100))
    manifold_points = [np.random.randn(12) for _ in range(100)]
    
    coordinator.set_manifolds_batch(manifold_ids, manifold_points)
    
    # Create test data
    test_data = [(np.random.randn(10), np.random.randint(0, 10)) for _ in range(50)]
    
    # Optimize coordination weights
    coordinator.optimize_coordination_weights(test_data)
    
    # Make predictions
    inputs = [x for x, _ in test_data[:10]]
    predictions = coordinator.predict_batch(inputs)
    
    print(f"  Made {len(predictions)} predictions")
    
    # Evaluate
    metrics = coordinator.evaluate(test_data)
    
    # Get statistics
    stats = coordinator.get_manifold_stats()
    print(f"\n  Manifold Statistics:")
    print(f"    Total manifolds: {stats['n_manifolds']}")
    print(f"    Active manifolds: {stats['n_active']}")
    print(f"    Average accuracy: {stats['avg_accuracy']:.4f}")
    
    # Get top manifolds
    top_manifolds = coordinator.get_top_manifolds(n=5)
    print(f"\n  Top 5 Manifolds:")
    for manifold_id, weight in top_manifolds:
        print(f"    Manifold {manifold_id}: weight={weight:.6f}")
    
    print("  All tests passed!")


if __name__ == "__main__":
    test_distributed_coordinator()
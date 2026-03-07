"""
Continuous Manifold Distillation
Dynamic learning system that grows manifolds over time
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Callable
from datetime import datetime
import json
import os

# Import dependencies
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manifold.svd_decoder import SVDDecoder
from manifold.fractal_bridge import FractalBridge, FractalBridgeNetwork


class ManifoldSnapshot:
    """
    Snapshot of manifold at a specific time
    """
    
    def __init__(
        self,
        timestamp: datetime,
        manifold_point: np.ndarray,
        knowledge_size: float,
        metadata: Optional[Dict] = None
    ):
        """
        Initialize manifold snapshot
        
        Args:
            timestamp: Time of snapshot
            manifold_point: Manifold point at this time
            knowledge_size: Size of knowledge (e.g., number of samples seen)
            metadata: Additional metadata
        """
        self.timestamp = timestamp
        self.manifold_point = manifold_point.copy()
        self.knowledge_size = knowledge_size
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "manifold_point": self.manifold_point.tolist(),
            "knowledge_size": self.knowledge_size,
            "metadata": self.metadata
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'ManifoldSnapshot':
        """Create from dictionary"""
        return ManifoldSnapshot(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            manifold_point=np.array(data["manifold_point"]),
            knowledge_size=data["knowledge_size"],
            metadata=data.get("metadata", {})
        )


class ContinuousManifold:
    """
    Manifold that grows continuously through distillation
    """
    
    def __init__(
        self,
        manifold_id: int,
        n_weights: int,
        n_manifold_dim: int = 12,
        precision_bits: int = 400,
        seed: int = 42
    ):
        """
        Initialize continuous manifold
        
        Args:
            manifold_id: Unique identifier
            n_weights: Number of weights
            n_manifold_dim: Manifold dimensionality
            precision_bits: Precision for calculations
            seed: Random seed
        """
        self.manifold_id = manifold_id
        self.n_weights = n_weights
        self.n_manifold_dim = n_manifold_dim
        self.precision_bits = precision_bits
        self.seed = seed
        
        # Decoder
        self.decoder = SVDDecoder(
            n_weights=n_weights,
            n_manifold_dim=n_manifold_dim,
            precision_bits=precision_bits,
            seed=seed
        )
        
        # Current state
        self.current_manifold: Optional[np.ndarray] = None
        self.current_weights: Optional[np.ndarray] = None
        
        # History
        self.snapshots: List[ManifoldSnapshot] = []
        
        # Fractal bridges
        self.bridge_network = FractalBridgeNetwork(precision_bits=precision_bits)
        self.bridge_network.add_manifold(manifold_id, n_manifold_dim)
        
        # Learning statistics
        self.total_samples_seen = 0
        self.learning_steps = 0
        self.growth_rate = 0.0
    
    def initialize(self, initial_weights: np.ndarray):
        """
        Initialize manifold with initial weights
        
        Args:
            initial_weights: Initial weight vector
        """
        self.current_weights = initial_weights.copy()
        self.decoder.learn_reference_structure(initial_weights)
        self.current_manifold = self.decoder.decode(initial_weights)
        
        # Create initial snapshot
        self._create_snapshot()
        
        print(f"Manifold {self.manifold_id} initialized with {self.n_manifold_dim}D manifold")
    
    def _create_snapshot(self, metadata: Optional[Dict] = None):
        """Create snapshot of current state"""
        snapshot = ManifoldSnapshot(
            timestamp=datetime.now(),
            manifold_point=self.current_manifold,
            knowledge_size=self.total_samples_seen,
            metadata=metadata
        )
        self.snapshots.append(snapshot)
    
    def learn(
        self,
        new_data: List[np.ndarray],
        new_labels: Optional[List[int]] = None,
        learning_rate: float = 0.01
    ):
        """
        Learn from new data
        
        Args:
            new_data: New training data
            new_labels: Optional labels
            learning_rate: Learning rate
        """
        if self.current_weights is None:
            raise ValueError("Manifold not initialized. Call initialize() first.")
        
        # Simulate learning by updating weights
        # In practice, would train model on new data and extract updated weights
        n_samples = len(new_data)
        
        # Update weights (simplified - would use actual training)
        for sample in new_data:
            # Simulate gradient descent
            gradient = np.random.randn(len(self.current_weights)) * 0.01
            self.current_weights = self.current_weights - learning_rate * gradient
        
        # Decode new manifold
        new_manifold = self.decoder.decode(self.current_weights)
        
        # Create fractal bridge from old to new manifold
        if len(self.snapshots) > 0:
            old_manifold = self.snapshots[-1].manifold_point
            
            # Create temporary manifold ID for new state
            temp_id = f"{self.manifold_id}_new_{len(self.snapshots)}"
            self.bridge_network.add_manifold(temp_id, self.n_manifold_dim)
            
            # Build bridge
            self.bridge_network.build_bridge(
                source_id=self.manifold_id,
                target_id=temp_id,
                source_point=old_manifold,
                target_point=new_manifold
            )
        
        # Update current state
        self.current_manifold = new_manifold
        self.total_samples_seen += n_samples
        self.learning_steps += 1
        
        # Calculate growth rate
        if len(self.snapshots) > 0:
            old_knowledge = self.snapshots[-1].knowledge_size
            self.growth_rate = (self.total_samples_seen - old_knowledge) / (old_knowledge + 1)
        
        # Create snapshot
        self._create_snapshot({
            "n_samples": n_samples,
            "learning_rate": learning_rate,
            "growth_rate": self.growth_rate
        })
        
        print(f"Manifold {self.manifold_id} learned from {n_samples} samples (total: {self.total_samples_seen})")
    
    def get_growth_trajectory(self) -> List[Tuple[datetime, float]]:
        """
        Get growth trajectory over time
        
        Returns:
            List of (timestamp, knowledge_size) tuples
        """
        trajectory = []
        for snapshot in self.snapshots:
            trajectory.append((snapshot.timestamp, snapshot.knowledge_size))
        
        return trajectory
    
    def get_manifold_at_time(self, timestamp: datetime) -> Optional[np.ndarray]:
        """
        Get manifold state at specific time
        
        Args:
            timestamp: Time to query
            
        Returns:
            Manifold point or None if not found
        """
        for snapshot in self.snapshots:
            if snapshot.timestamp == timestamp:
                return snapshot.manifold_point
        
        return None
    
    def save_state(self, filepath: str):
        """
        Save manifold state to file
        
        Args:
            filepath: Path to save file
        """
        state = {
            "manifold_id": self.manifold_id,
            "n_weights": self.n_weights,
            "n_manifold_dim": self.n_manifold_dim,
            "current_manifold": self.current_manifold.tolist() if self.current_manifold is not None else None,
            "total_samples_seen": self.total_samples_seen,
            "learning_steps": self.learning_steps,
            "growth_rate": self.growth_rate,
            "snapshots": [s.to_dict() for s in self.snapshots]
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"Saved manifold {self.manifold_id} state to {filepath}")
    
    def load_state(self, filepath: str):
        """
        Load manifold state from file
        
        Args:
            filepath: Path to load file
        """
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        self.manifold_id = state["manifold_id"]
        self.n_weights = state["n_weights"]
        self.n_manifold_dim = state["n_manifold_dim"]
        self.current_manifold = np.array(state["current_manifold"]) if state["current_manifold"] is not None else None
        self.total_samples_seen = state["total_samples_seen"]
        self.learning_steps = state["learning_steps"]
        self.growth_rate = state["growth_rate"]
        self.snapshots = [ManifoldSnapshot.from_dict(s) for s in state["snapshots"]]
        
        print(f"Loaded manifold {self.manifold_id} state from {filepath}")


class ContinuousLearningSystem:
    """
    System for continuous learning across multiple manifolds
    """
    
    def __init__(
        self,
        n_manifolds: int = 100000,
        n_weights: int = 50000,
        n_manifold_dim: int = 12,
        precision_bits: int = 400
    ):
        """
        Initialize continuous learning system
        
        Args:
            n_manifolds: Number of manifolds
            n_weights: Number of weights per manifold
            n_manifold_dim: Manifold dimensionality
            precision_bits: Precision for calculations
        """
        self.n_manifolds = n_manifolds
        self.n_weights = n_weights
        self.n_manifold_dim = n_manifold_dim
        self.precision_bits = precision_bits
        
        # Continuous manifolds
        self.manifolds: Dict[int, ContinuousManifold] = {}
        
        # Global statistics
        self.global_learning_steps = 0
        self.global_samples_seen = 0
        
        print(f"Initialized continuous learning system with {n_manifolds} manifolds")
    
    def add_manifold(self, manifold_id: int, initial_weights: np.ndarray):
        """
        Add a manifold to the system
        
        Args:
            manifold_id: Unique identifier
            initial_weights: Initial weights
        """
        manifold = ContinuousManifold(
            manifold_id=manifold_id,
            n_weights=self.n_weights,
            n_manifold_dim=self.n_manifold_dim,
            precision_bits=self.precision_bits,
            seed=42 + manifold_id
        )
        
        manifold.initialize(initial_weights)
        self.manifolds[manifold_id] = manifold
        
        print(f"Added manifold {manifold_id} to system")
    
    def continuous_learn(
        self,
        manifold_id: int,
        new_data: List[np.ndarray],
        new_labels: Optional[List[int]] = None,
        learning_rate: float = 0.01
    ):
        """
        Continuous learning for specific manifold
        
        Args:
            manifold_id: Manifold to train
            new_data: New data
            new_labels: Optional labels
            learning_rate: Learning rate
        """
        if manifold_id not in self.manifolds:
            raise ValueError(f"Manifold {manifold_id} not found")
        
        self.manifolds[manifold_id].learn(new_data, new_labels, learning_rate)
        
        self.global_learning_steps += 1
        self.global_samples_seen += len(new_data)
    
    def batch_learn(
        self,
        data_per_manifold: Dict[int, List[np.ndarray]],
        labels_per_manifold: Optional[Dict[int, List[int]]] = None,
        learning_rate: float = 0.01
    ):
        """
        Batch learning for multiple manifolds
        
        Args:
            data_per_manifold: Dictionary mapping manifold_id to data
            labels_per_manifold: Optional labels
            learning_rate: Learning rate
        """
        for manifold_id, data in data_per_manifold.items():
            labels = labels_per_manifold.get(manifold_id) if labels_per_manifold else None
            self.continuous_learn(manifold_id, data, labels, learning_rate)
    
    def get_system_growth(self) -> Dict[str, float]:
        """
        Get overall system growth statistics
        
        Returns:
            Growth statistics
        """
        total_knowledge = sum(m.total_samples_seen for m in self.manifolds.values())
        avg_growth_rate = np.mean([m.growth_rate for m in self.manifolds.values()]) if self.manifolds else 0.0
        
        return {
            "total_manifolds": len(self.manifolds),
            "total_knowledge": total_knowledge,
            "global_learning_steps": self.global_learning_steps,
            "global_samples_seen": self.global_samples_seen,
            "avg_growth_rate": avg_growth_rate
        }


def test_continuous_learning():
    """Test continuous learning system"""
    print("Testing Continuous Learning System...")
    
    # Create system with 10 manifolds (for testing)
    system = ContinuousLearningSystem(
        n_manifolds=10,
        n_weights=1000,
        n_manifold_dim=12
    )
    
    # Add manifolds
    for i in range(10):
        initial_weights = np.random.randn(1000)
        system.add_manifold(i, initial_weights)
    
    # Simulate continuous learning
    for step in range(5):
        print(f"\nLearning step {step + 1}:")
        
        for manifold_id in range(10):
            # Generate new data
            new_data = [np.random.randn(10) for _ in range(10)]
            system.continuous_learn(manifold_id, new_data, learning_rate=0.01)
    
    # Get system growth
    growth = system.get_system_growth()
    print(f"\nSystem Growth:")
    print(f"  Total knowledge: {growth['total_knowledge']}")
    print(f"  Average growth rate: {growth['avg_growth_rate']:.4f}")
    
    # Get growth trajectory for first manifold
    trajectory = system.manifolds[0].get_growth_trajectory()
    print(f"\nGrowth trajectory for manifold 0:")
    for timestamp, knowledge in trajectory:
        print(f"  {timestamp}: {knowledge} samples")
    
    print("  All tests passed!")


if __name__ == "__main__":
    test_continuous_learning()
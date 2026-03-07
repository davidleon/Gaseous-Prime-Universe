"""
Fractal Bridge Construction
Creates non-integer dimensional connections between manifolds
"""

import numpy as np
from typing import List, Tuple, Optional, Dict
from scipy.spatial.distance import cdist
from scipy.interpolate import interp1d


class FractalBridge:
    """
    Fractal bridge between two manifolds
    Uses non-integer dimensions for smooth information transfer
    """
    
    def __init__(
        self,
        source_dim: int,
        target_dim: int,
        fractal_dim: Optional[float] = None,
        bridge_points: int = 100,
        precision_bits: int = 400
    ):
        """
        Initialize fractal bridge
        
        Args:
            source_dim: Source manifold dimension
            target_dim: Target manifold dimension
            fractal_dim: Fractal dimension (calculated if None)
            bridge_points: Number of intermediate points
            precision_bits: Precision for calculations
        """
        self.source_dim = source_dim
        self.target_dim = target_dim
        self.bridge_points = bridge_points
        self.precision_bits = precision_bits
        
        # Calculate fractal dimension if not provided
        if fractal_dim is None:
            # Golden ratio transition
            self.fractal_dim = source_dim - (source_dim - target_dim) * 0.618
        else:
            self.fractal_dim = fractal_dim
        
        # Bridge parameters
        self.source_point: Optional[np.ndarray] = None
        self.target_point: Optional[np.ndarray] = None
        self.bridge_path: Optional[np.ndarray] = None
        
        # Transfer matrix
        self.transfer_matrix: Optional[np.ndarray] = None
    
    def build_bridge(
        self,
        source_point: np.ndarray,
        target_point: np.ndarray
    ) -> np.ndarray:
        """
        Build fractal bridge between two manifold points
        
        Args:
            source_point: Source manifold point
            target_point: Target manifold point
            
        Returns:
            Bridge path (intermediate points)
        """
        self.source_point = source_point.copy()
        self.target_point = target_point.copy()
        
        # Create fractal interpolation
        bridge_path = np.zeros((self.bridge_points, max(self.source_dim, self.target_dim)))
        
        for i in range(self.bridge_points):
            t = i / (self.bridge_points - 1)
            
            # Fractal interpolation using fractional power
            fractal_t = t ** (self.fractal_dim / self.source_dim)
            
            # Interpolate dimensions
            for dim in range(max(self.source_dim, self.target_dim)):
                if dim < self.source_dim and dim < self.target_dim:
                    # Both have this dimension
                    bridge_path[i, dim] = (1 - fractal_t) * source_point[dim] + fractal_t * target_point[dim]
                elif dim < self.source_dim:
                    # Only source has this dimension
                    bridge_path[i, dim] = source_point[dim] * (1 - fractal_t)
                else:
                    # Only target has this dimension
                    bridge_path[i, dim] = target_point[dim] * fractal_t
        
        self.bridge_path = bridge_path
        
        # Build transfer matrix
        self._build_transfer_matrix()
        
        return bridge_path
    
    def _build_transfer_matrix(self):
        """Build transfer matrix for information flow"""
        if self.source_point is None or self.target_point is None:
            return
        
        # Create transfer matrix based on fractal dimension
        self.transfer_matrix = np.zeros((self.target_dim, self.source_dim))
        
        for i in range(self.target_dim):
            for j in range(self.source_dim):
                # Fractal scaling factor
                scale = (self.fractal_dim / self.source_dim) ** ((i + 1) / (j + 1))
                self.transfer_matrix[i, j] = scale
        
        # Normalize
        self.transfer_matrix = self.transfer_matrix / (np.sum(np.abs(self.transfer_matrix)) + 1e-10)
    
    def transfer(self, source_point: np.ndarray) -> np.ndarray:
        """
        Transfer information across fractal bridge
        
        Args:
            source_point: Source manifold point
            
        Returns:
            Transformed point in target manifold space
        """
        if self.transfer_matrix is None:
            raise ValueError("Bridge not built. Call build_bridge() first.")
        
        # Apply transfer matrix
        transformed = np.dot(self.transfer_matrix, source_point)
        
        # Adjust dimensionality
        if len(transformed) < self.target_dim:
            # Pad with zeros
            transformed = np.pad(transformed, (0, self.target_dim - len(transformed)))
        elif len(transformed) > self.target_dim:
            # Truncate
            transformed = transformed[:self.target_dim]
        
        return transformed
    
    def bridge_capacity(self) -> float:
        """
        Calculate information capacity of fractal bridge
        
        Returns:
            Capacity (based on fractal dimension)
        """
        # Capacity scales with fractal dimension
        capacity = 2 ** (self.fractal_dim / 3)
        return capacity
    
    def bridge_efficiency(self) -> float:
        """
        Calculate transfer efficiency
        
        Returns:
            Efficiency (0 to 1)
        """
        if self.bridge_path is None:
            return 0.0
        
        # Calculate path smoothness
        differences = np.diff(self.bridge_path, axis=0)
        smoothness = np.mean(np.linalg.norm(differences, axis=1))
        
        # Normalize efficiency
        max_smoothness = np.linalg.norm(self.source_point - self.target_point)
        efficiency = 1.0 - (smoothness / (max_smoothness + 1e-10))
        
        return max(0.0, min(1.0, efficiency))


class FractalBridgeNetwork:
    """
    Network of fractal bridges connecting multiple manifolds
    """
    
    def __init__(self, precision_bits: int = 400):
        """
        Initialize fractal bridge network
        
        Args:
            precision_bits: Precision for calculations
        """
        self.precision_bits = precision_bits
        self.bridges: Dict[Tuple[int, int], FractalBridge] = {}
        self.manifold_dims: Dict[int, int] = {}
    
    def add_manifold(self, manifold_id: int, dimension: int):
        """
        Add a manifold to the network
        
        Args:
            manifold_id: Unique identifier for manifold
            dimension: Dimensionality of manifold
        """
        self.manifold_dims[manifold_id] = dimension
    
    def build_bridge(
        self,
        source_id: int,
        target_id: int,
        source_point: np.ndarray,
        target_point: np.ndarray,
        fractal_dim: Optional[float] = None
    ):
        """
        Build a fractal bridge between two manifolds
        
        Args:
            source_id: Source manifold ID
            target_id: Target manifold ID
            source_point: Source manifold point
            target_point: Target manifold point
            fractal_dim: Optional fractal dimension
        """
        if source_id not in self.manifold_dims:
            raise ValueError(f"Source manifold {source_id} not found")
        if target_id not in self.manifold_dims:
            raise ValueError(f"Target manifold {target_id} not found")
        
        source_dim = self.manifold_dims[source_id]
        target_dim = self.manifold_dims[target_id]
        
        bridge = FractalBridge(
            source_dim=source_dim,
            target_dim=target_dim,
            fractal_dim=fractal_dim,
            precision_bits=self.precision_bits
        )
        
        bridge_path = bridge.build_bridge(source_point, target_point)
        
        self.bridges[(source_id, target_id)] = bridge
        self.bridges[(target_id, source_id)] = bridge  # Bidirectional
        
        print(f"Built bridge {source_id} ↔ {target_id}: {source_dim}D → {target_dim}D (fractal: {bridge.fractal_dim:.3f})")
    
    def transfer(
        self,
        source_id: int,
        target_id: int,
        source_point: np.ndarray
    ) -> np.ndarray:
        """
        Transfer information across bridge
        
        Args:
            source_id: Source manifold ID
            target_id: Target manifold ID
            source_point: Source manifold point
            
        Returns:
            Transformed point in target manifold
        """
        bridge_key = (source_id, target_id)
        if bridge_key not in self.bridges:
            raise ValueError(f"No bridge from {source_id} to {target_id}")
        
        bridge = self.bridges[bridge_key]
        return bridge.transfer(source_point)
    
    def get_bridge_capacity(self, source_id: int, target_id: int) -> float:
        """
        Get capacity of a specific bridge
        
        Args:
            source_id: Source manifold ID
            target_id: Target manifold ID
            
        Returns:
            Bridge capacity
        """
        bridge_key = (source_id, target_id)
        if bridge_key not in self.bridges:
            return 0.0
        
        return self.bridges[bridge_key].bridge_capacity()
    
    def get_network_capacity(self) -> float:
        """
        Calculate total network capacity
        
        Returns:
            Total capacity
        """
        total_capacity = 0.0
        for bridge in self.bridges.values():
            total_capacity += bridge.bridge_capacity()
        
        # Divide by 2 because bridges are bidirectional
        return total_capacity / 2
    
    def visualize_network(self) -> str:
        """
        Generate network visualization string
        
        Returns:
            Network structure as string
        """
        lines = ["Fractal Bridge Network:"]
        lines.append(f"  Manifolds: {len(self.manifold_dims)}")
        
        for manifold_id, dim in self.manifold_dims.items():
            lines.append(f"    Manifold {manifold_id}: {dim}D")
        
        lines.append(f"  Bridges: {len(self.bridges) // 2}")
        
        for (source_id, target_id), bridge in self.bridges.items():
            if source_id < target_id:  # Avoid duplicates
                capacity = bridge.bridge_capacity()
                efficiency = bridge.bridge_efficiency()
                lines.append(f"    {source_id} ↔ {target_id}: capacity={capacity:.2f}, efficiency={efficiency:.3f}")
        
        total_capacity = self.get_network_capacity()
        lines.append(f"  Total Network Capacity: {total_capacity:.2f}")
        
        return "\n".join(lines)


def test_fractal_bridge():
    """Test fractal bridge functionality"""
    print("Testing Fractal Bridge...")
    
    # Create bridge
    bridge = FractalBridge(
        source_dim=12,
        target_dim=9,
        bridge_points=100
    )
    
    # Build bridge
    source_point = np.random.randn(12)
    target_point = np.random.randn(9)
    
    bridge_path = bridge.build_bridge(source_point, target_point)
    
    print(f"  Built bridge: 12D → 9D (fractal: {bridge.fractal_dim:.3f})")
    print(f"  Bridge path shape: {bridge_path.shape}")
    print(f"  Bridge capacity: {bridge.bridge_capacity():.4f}")
    print(f"  Bridge efficiency: {bridge.bridge_efficiency():.4f}")
    
    # Test transfer
    transferred = bridge.transfer(source_point)
    print(f"  Transfer test:")
    print(f"    Source shape: {source_point.shape}")
    print(f"    Transferred shape: {transferred.shape}")
    
    # Test network
    print("\nTesting Fractal Bridge Network...")
    network = FractalBridgeNetwork()
    
    # Add manifolds
    network.add_manifold(0, 12)
    network.add_manifold(1, 9)
    network.add_manifold(2, 6)
    network.add_manifold(3, 3)
    
    # Build bridges
    network.build_bridge(0, 1, np.random.randn(12), np.random.randn(9))
    network.build_bridge(1, 2, np.random.randn(9), np.random.randn(6))
    network.build_bridge(2, 3, np.random.randn(6), np.random.randn(3))
    
    # Test transfer
    transferred_0_1 = network.transfer(0, 1, np.random.randn(12))
    transferred_1_2 = network.transfer(1, 2, np.random.randn(9))
    
    print(f"  Network transfer test:")
    print(f"    0→1: {transferred_0_1.shape}")
    print(f"    1→2: {transferred_1_2.shape}")
    
    # Visualize network
    print("\n" + network.visualize_network())
    
    print("  All tests passed!")


if __name__ == "__main__":
    test_fractal_bridge()
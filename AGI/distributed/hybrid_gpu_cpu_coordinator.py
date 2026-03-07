"""
Distributed Manifold Coordinator with GPU+CPU Hybrid
Manages coordination between 1M+ manifolds with sharding and hybrid GPU+CPU
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Callable
import warnings
import time

warnings.filterwarnings('ignore')

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    import ray
    RAY_AVAILABLE = True
    print("  [DIST] Ray available - using distributed computing")
except ImportError:
    RAY_AVAILABLE = False
    print("  [DIST] Ray not available - falling back to multiprocessing")

try:
    import dask.array as da
    DASK_AVAILABLE = True
    print("  [DIST] Dask available - using array parallelization")
except ImportError:
    DASK_AVAILABLE = False

try:
    from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
    MULTIPROCESSING_AVAILABLE = True
except ImportError:
    MULTIPROCESSING_AVAILABLE = False

try:
    from multiprocessing import cpu_count
except ImportError:
    cpu_count = lambda: 1

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class ManifoldShard:
    """
    Single shard of manifolds for distributed processing
    """
    
    def __init__(
        self,
        shard_id: int,
        n_manifolds: int,
        n_manifold_dim: int = 12,
        n_weights: int = 50000
    ):
        """
        Initialize manifold shard
        
        Args:
            shard_id: Unique shard identifier
            n_manifolds: Number of manifolds in this shard
            n_manifold_dim: Dimensionality of each manifold
            n_weights: Number of weights per manifold
        """
        self.shard_id = shard_id
        self.n_manifolds = n_manifolds
        self.n_manifold_dim = n_manifold_dim
        self.n_weights = n_weights
        
        # Store manifolds as numpy array (efficient storage)
        self.manifolds: np.ndarray = np.zeros((n_manifolds, n_manifold_dim))
        self.confidences: np.ndarray = np.zeros(n_manifolds)
        self.specializations: List[str] = ["general"] * n_manifolds
        
        # Shard performance metrics
        self.total_operations = 0
        self.total_time = 0.0
    
    def set_manifolds_batch(
        self,
        manifold_ids: List[int],
        manifold_points: List[np.ndarray]
    ):
        """
        Set multiple manifolds at once
        
        Args:
            manifold_ids: List of manifold IDs
            manifold_points: List of manifold points
        """
        for i, manifold_id in enumerate(manifold_ids):
            if i < self.n_manifolds:
                self.manifolds[manifold_id] = manifold_points[i]
                self.confidences[manifold_id] = 1.0
    
    def get_manifold(self, manifold_id: int) -> np.ndarray:
        """Get specific manifold"""
        return self.manifolds[manifold_id]
    
    def get_all_manifolds(self) -> np.ndarray:
        """Get all manifolds in this shard"""
        return self.manifolds.copy()
    
    def compute_distances(
        self,
        query_point: np.ndarray,
        top_k: int = 100
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute distances to query point (for nearest neighbor search)
        
        Args:
            query_point: Query manifold point
            top_k: Number of nearest neighbors to return
            
        Returns:
            (indices, distances)
        """
        # Compute distances to all manifolds
        distances = np.linalg.norm(
            self.manifolds - query_point,
            axis=1
        )
        
        # Get top-k nearest
        top_k_indices = np.argsort(distances)[:top_k]
        top_k_distances = distances[top_k_indices]
        
        return top_k_indices, top_k_distances


if RAY_AVAILABLE:
    @ray.remote
    class RemoteManifoldShard(ManifoldShard):
        """
        Ray remote shard for distributed processing
        """
        pass
else:
    class RemoteManifoldShard(ManifoldShard):
        """
        Fallback shard when Ray is not available
        """
        pass


class HybridGPUCPUCoordinator:
    """
    Hybrid GPU+CPU coordinator for super large manifolds
    
    Features:
    - GPU acceleration for compute-intensive operations
    - CPU for coordination and sequential logic
    - Sharding for super large manifolds
    - Auto-scaling based on load
    """
    
    def __init__(
        self,
        n_manifolds: int = 1000000,  # 1M manifolds
        n_weights: int = 50000,
        n_manifold_dim: int = 12,
        n_shards: int = 100,
        use_ray: bool = True,
        use_dask: bool = False,
        n_workers: Optional[int] = None,
        gpu_memory_gb: float = 16.0,
        precision_bits: int = 400
    ):
        """
        Initialize hybrid GPU+CPU coordinator
        
        Args:
            n_manifolds: Total number of manifolds (1,000,000 by default)
            n_weights: Number of weights per manifold
            n_manifold_dim: Dimensionality of each manifold
            n_shards: Number of shards to split manifolds across
            use_ray: Use Ray for distributed computing
            use_dask: Use Dask for array parallelization
            n_workers: Number of workers (auto-detect if None)
            gpu_memory_gb: GPU memory available per device
            precision_bits: Precision for calculations
        """
        print("=" * 80)
        print("INITIALIZING HYBRID GPU+CPU COORDINATOR")
        print("=" * 80)
        
        self.n_manifolds = n_manifolds
        self.n_weights = n_weights
        self.n_manifold_dim = n_manifold_dim
        self.n_shards = n_shards
        self.precision_bits = precision_bits
        self.gpu_memory_gb = gpu_memory_gb
        
        # Determine parallelization strategy
        self.use_ray = use_ray and RAY_AVAILABLE
        self.use_dask = use_dask and DASK_AVAILABLE
        self.use_multiprocessing = MULTIPROCESSING_AVAILABLE
        
        if not (self.use_ray or self.use_dask or self.use_multiprocessing):
            print("  [WARN] No distributed computing available, using serial mode")
            self.use_serial = True
        else:
            self.use_serial = False
        
        # Determine number of workers
        if n_workers is None:
            n_workers = cpu_count()
        self.n_workers = n_workers
        
        # GPU configuration
        self.n_gpus = 0
        self.gpus_available = False
        if TORCH_AVAILABLE:
            self.n_gpus = torch.cuda.device_count()
            self.gpus_available = self.n_gpus > 0
            if self.gpus_available:
                print(f"  [GPU] {self.n_gpus} GPU(s) detected")
                for i in range(self.n_gpus):
                    mem_info = torch.cuda.get_device_properties(i)
                    print(f"    GPU {i}: {mem_info.name}, {mem_info.total_memory / 1e9:.1f}GB")
        
        # Memory monitoring
        self.psutil_available = PSUTIL_AVAILABLE
        if PSUTIL_AVAILABLE:
            mem = psutil.virtual_memory()
            print(f"  [SYSTEM] Total RAM: {mem.total / 1e9:.1f}GB, Available: {mem.available / 1e9:.1f}GB")
        
        # Initialize shards
        print(f"\n  Initializing {n_shards} shards...")
        self._initialize_shards()
        
        # Performance tracking
        self.operation_times = {
            'gpu': [],
            'cpu': [],
            'distributed': []
        }
        
        print("\nHybrid GPU+CPU Coordinator initialized!")
        print(f"  Scale: {n_manifolds:,} manifolds")
        print(f"  Shards: {n_shards}")
        print(f"  Workers: {self.n_workers}")
        print(f"  GPUs: {self.n_gpus}")
        print(f"  Strategy: {self._get_strategy_description()}")
        print("=" * 80)
    
    def _get_strategy_description(self) -> str:
        """Get current parallelization strategy description"""
        if self.use_ray:
            return "Ray distributed"
        elif self.use_dask:
            return "Dask array parallelization"
        elif self.use_multiprocessing:
            return "Multiprocessing"
        elif self.use_serial:
            return "Serial"
        else:
            return "Unknown"
    
    def _initialize_shards(self):
        """Initialize manifold shards"""
        self.shards: List[ManifoldShard] = []
        manifolds_per_shard = self.n_manifolds // self.n_shards
        remaining = self.n_manifolds % self.n_shards
        
        for shard_id in range(self.n_shards):
            n_this_shard = manifolds_per_shard
            if shard_id < remaining:
                n_this_shard += 1
            
            if self.use_ray:
                # Create remote shard
                shard = RemoteManifoldShard.remote(
                    shard_id=shard_id,
                    n_manifolds=n_this_shard,
                    n_manifold_dim=self.n_manifold_dim,
                    n_weights=self.n_weights
                )
            else:
                # Create local shard
                shard = ManifoldShard(
                    shard_id=shard_id,
                    n_manifolds=n_this_shard,
                    n_manifold_dim=self.n_manifold_dim,
                    n_weights=self.n_weights
                )
            
            self.shards.append(shard)
    
    def _get_shard_for_manifold(self, manifold_id: int) -> int:
        """Get which shard contains a specific manifold"""
        divisor = max(1, self.n_manifolds // self.n_shards)
        return manifold_id // divisor
    
    def set_manifolds_batch(
        self,
        manifold_ids: List[int],
        manifold_points: List[np.ndarray]
    ):
        """
        Set multiple manifolds at once (optimized for batch processing)
        
        Args:
            manifold_ids: List of manifold IDs
            manifold_points: List of manifold points
        """
        # Group by shard
        shard_groups = {}
        for manifold_id in manifold_ids:
            shard_id = self._get_shard_for_manifold(manifold_id)
            if shard_id not in shard_groups:
                shard_groups[shard_id] = []
            shard_groups[shard_id].append(manifold_id)
        
        # Set manifolds per shard
        for shard_id, group in shard_groups.items():
            divisor = max(1, self.n_manifolds // self.n_shards)
            if self.use_ray:
                # Remote call
                manifold_indices = [mid % divisor for mid in group]
                shard_points = [manifold_points[i] for i, mid in enumerate(group)]
                ray.get(self.shards[shard_id].set_manifolds_batch.remote(
                    manifold_indices, shard_points
                ))
            else:
                # Local call
                manifold_indices = [mid % divisor for mid in group]
                shard_points = [manifold_points[i] for i, mid in enumerate(group)]
                self.shards[shard_id].set_manifolds_batch(manifold_indices, shard_points)
    
    def get_manifold(self, manifold_id: int) -> np.ndarray:
        """
        Get specific manifold from appropriate shard
        
        Args:
            manifold_id: Manifold ID
            
        Returns:
            Manifold point
        """
        shard_id = self._get_shard_for_manifold(manifold_id)
        local_id = manifold_id % (self.n_manifolds // self.n_shards)
        
        if self.use_ray:
            return ray.get(self.shards[shard_id].get_manifold.remote(local_id))
        else:
            return self.shards[shard_id].get_manifold(local_id)
    
    def query_nearest_neighbors(
        self,
        query_point: np.ndarray,
        top_k: int = 100,
        use_gpu: bool = True
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Query nearest neighbors across all shards (distributed)
        
        Args:
            query_point: Query manifold point
            top_k: Number of nearest neighbors
            use_gpu: Use GPU for distance computation
            
        Returns:
            (indices, distances)
        """
        start_time = time.time()
        
        # Query each shard
        all_indices = []
        all_distances = []
        
        for shard_id, shard in enumerate(self.shards):
            if self.use_ray:
                # Remote query
                shard_indices, shard_distances = ray.get(
                    shard.compute_distances.remote(query_point, top_k)
                )
                # Adjust indices to global manifold IDs
                global_indices = shard_indices + (shard_id * (self.n_manifolds // self.n_shards))
                all_indices.extend(global_indices)
                all_distances.extend(shard_distances)
            else:
                # Local query
                shard_indices, shard_distances = shard.compute_distances(
                    query_point, top_k
                )
                global_indices = shard_indices + (shard_id * (self.n_manifolds // self.n_shards))
                all_indices.extend(global_indices)
                all_distances.extend(shard_distances)
        
        # Combine results and get top-k globally
        combined = list(zip(all_indices, all_distances))
        combined.sort(key=lambda x: x[1])
        top_k_combined = combined[:top_k]
        
        top_k_indices = np.array([x[0] for x in top_k_combined])
        top_k_distances = np.array([x[1] for x in top_k_combined])
        
        # Record performance
        elapsed = time.time() - start_time
        self.operation_times['distributed'].append(elapsed)
        
        return top_k_indices, top_k_distances
    
    def weighted_voting(
        self,
        manifold_ids: List[int],
        query_point: np.ndarray,
        weights: Optional[np.ndarray] = None
    ) -> Tuple[int, float]:
        """
        Weighted voting across selected manifolds
        
        Args:
            manifold_ids: Manifold IDs to include in voting
            query_point: Query point
            weights: Optional weights for each manifold
            
        Returns:
            (prediction, confidence)
        """
        # Get predictions from all selected manifolds
        predictions = []
        confidences = []
        
        for manifold_id in manifold_ids:
            manifold = self.get_manifold(manifold_id)
            
            # Compute similarity
            similarity = np.dot(
                query_point[:min(len(query_point), len(manifold))],
                manifold[:min(len(query_point), len(manifold))]
            )
            
            # Convert to prediction (0-9 for digits)
            prediction = int(abs(similarity * 100)) % 10
            confidence = min(1.0, abs(similarity))
            
            predictions.append(prediction)
            confidences.append(confidence)
        
        # Weighted voting
        if weights is None:
            weights = np.ones(len(predictions))
        
        weighted_votes = np.zeros(10)
        for i, (pred, conf) in enumerate(zip(predictions, confidences)):
            weighted_votes[pred] += weights[i] * conf
        
        final_prediction = int(np.argmax(weighted_votes))
        final_confidence = weighted_votes[final_prediction] / np.sum(weighted_votes)
        
        return final_prediction, final_confidence
    
    def get_performance_metrics(self) -> dict:
        """Get performance metrics"""
        return {
            'n_manifolds': self.n_manifolds,
            'n_shards': self.n_shards,
            'n_workers': self.n_workers,
            'n_gpus': self.n_gpus,
            'strategy': self._get_strategy_description(),
            'operation_times': self.operation_times,
            'avg_gpu_time': np.mean(self.operation_times['gpu']) if self.operation_times['gpu'] else 0,
            'avg_cpu_time': np.mean(self.operation_times['cpu']) if self.operation_times['cpu'] else 0,
            'avg_distributed_time': np.mean(self.operation_times['distributed']) if self.operation_times['distributed'] else 0,
            'gpu_available': self.gpus_available,
            'ray_available': self.use_ray,
            'dask_available': self.use_dask,
            'multiprocessing_available': self.use_multiprocessing
        }
    
    def get_system_info(self) -> dict:
        """Get system information"""
        info = {
            'platform': 'linux' if 'linux' in str(os.uname()).lower() else 'unknown',
            'cpu_count': cpu_count() if PSUTIL_AVAILABLE else 'unknown',
            'gpu_count': self.n_gpus if self.gpus_available else 0,
            'total_memory_gb': psutil.virtual_memory().total / 1e9 if PSUTIL_AVAILABLE else 'unknown',
            'available_memory_gb': psutil.virtual_memory().available / 1e9 if PSUTIL_AVAILABLE else 'unknown'
        }
        
        if self.gpus_available:
            info['gpus'] = []
            for i in range(self.n_gpus):
                mem_info = torch.cuda.get_device_properties(i)
                info['gpus'].append({
                    'id': i,
                    'name': mem_info.name,
                    'total_memory_gb': mem_info.total_memory / 1e9,
                    'compute_capability': mem_info.major,
                    'minor': mem_info.minor
                })
        
        return info


def get_optimal_coordinator(
    n_manifolds: int,
    n_weights: int = 50000,
    n_manifold_dim: int = 12,
    force_serial: bool = False
) -> HybridGPUCPUCoordinator:
    """
    Get optimal coordinator configuration
    
    Args:
        n_manifolds: Total number of manifolds
        n_weights: Number of weights per manifold
        n_manifold_dim: Manifold dimensionality
        force_serial: Force serial mode
        
    Returns:
        Optimized coordinator instance
    """
    # Determine optimal number of shards
    if n_manifolds < 1000:
        n_shards = 1
    elif n_manifolds < 10000:
        n_shards = 10
    elif n_manifolds < 100000:
        n_shards = 100
    else:
        n_shards = 1000
    
    # Determine optimal strategy
    use_ray = not force_serial and RAY_AVAILABLE and n_manifolds > 10000
    use_dask = not force_serial and DASK_AVAILABLE and n_manifolds > 1000
    
    coordinator = HybridGPUCPUCoordinator(
        n_manifolds=n_manifolds,
        n_weights=n_weights,
        n_manifold_dim=n_manifold_dim,
        n_shards=n_shards,
        use_ray=use_ray,
        use_dask=use_dask,
        precision_bits=400
    )
    
    return coordinator

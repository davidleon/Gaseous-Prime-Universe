"""
Distributed Computing Module
Coordination and scaling for large-scale manifold systems
"""

from .coordinator import DistributedCoordinator
from .hybrid_gpu_cpu_coordinator import HybridGPUCPUCoordinator, get_optimal_coordinator

__all__ = [
    'DistributedCoordinator',
    'HybridGPUCPUCoordinator',
    'get_optimal_coordinator'
]
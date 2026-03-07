"""
Manifold Learning Module
Intelligence manifold extraction and analysis
"""

from .svd_decoder import SVDDecoder
from .gpu_svd_decoder import GPUSVDDecoder, get_optimal_decoder
from .recursive_chain import RecursiveManifold, RecursiveManifoldChain
from .fractal_bridge import FractalBridge, FractalBridgeNetwork
from .text_decoder_manifold import TextDecoderManifold
from .text_generation_bridge import TextGenerationBridge

__all__ = [
    'SVDDecoder',
    'GPUSVDDecoder',
    'get_optimal_decoder',
    'RecursiveManifold',
    'RecursiveManifoldChain',
    'FractalBridge',
    'FractalBridgeNetwork',
    'TextDecoderManifold',
    'TextGenerationBridge'
]
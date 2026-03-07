"""
Practical Guide: Model Extraction, Injection, and Storage
Comprehensive examples for working with AGI manifolds
"""

import numpy as np
import pickle
import json
import sys
import os
from typing import List, Dict, Tuple, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from manifold.gpu_svd_decoder import GPUSVDDecoder
from manifold.text_generation_bridge import TextGenerationBridge
from distributed.hybrid_gpu_cpu_coordinator import HybridGPUCPUCoordinator


# ============================================================================
# PART 1: Extract Model Weights to 12D Manifolds
# ============================================================================

def extract_model_weights_to_manifold(
    model_weights: np.ndarray,
    decoder: Optional[GPUSVDDecoder] = None
) -> np.ndarray:
    """
    Extract model weights to 12D intelligence manifold
    
    Args:
        model_weights: Flattened model weights (1D array)
        decoder: SVD decoder (creates new if None)
    
    Returns:
        12D manifold point
    
    Example:
        >>> # Simulated model weights (e.g., from PyTorch model)
        >>> import torch
        >>> model = torch.nn.Linear(1000, 100)
        >>> weights = torch.cat([p.flatten() for p in model.parameters()]).numpy()
        >>> manifold = extract_model_weights_to_manifold(weights)
        >>> print(f"Manifold shape: {manifold.shape}")  # (12,)
    """
    # Create decoder if not provided
    if decoder is None:
        decoder = GPUSVDDecoder(
            n_weights=len(model_weights),
            n_manifold_dim=12,
            use_gpu=True
        )
    
    # Learn reference structure (optional, improves decoding)
    if decoder.reference_weights is None:
        decoder.learn_reference_structure(model_weights)
    
    # Decode weights to 12D manifold
    manifold = decoder.decode(model_weights)
    
    return manifold


def extract_multiple_models_to_manifolds(
    models_list: List[Dict[str, np.ndarray]],
    decoder: Optional[GPUSVDDecoder] = None
) -> List[np.ndarray]:
    """
    Extract multiple models to 12D manifolds
    
    Args:
        models_list: List of model weight dictionaries
        decoder: SVD decoder (creates new if None)
    
    Returns:
        List of 12D manifold points
    
    Example:
        >>> models = [
        ...     {'weights': np.random.randn(50000), 'name': 'model1'},
        ...     {'weights': np.random.randn(50000), 'name': 'model2'}
        ... ]
        >>> manifolds = extract_multiple_models_to_manifolds(models)
        >>> print(f"Extracted {len(manifolds)} manifolds")
    """
    manifolds = []
    
    for model_data in models_list:
        weights = model_data['weights']
        name = model_data.get('name', 'unknown')
        
        # Flatten weights to 1D
        if weights.ndim > 1:
            weights = weights.flatten()
        
        # Extract manifold
        manifold = extract_model_weights_to_manifold(weights, decoder)
        manifolds.append(manifold)
        
        print(f"  Extracted '{name}': {weights.shape} → {manifold.shape}")
    
    return manifolds


# ============================================================================
# PART 2: Inject Different Manifolds into Intelligence Manifold
# ============================================================================

def inject_manifold_into_intelligence(
    base_manifold: np.ndarray,
    injected_manifold: np.ndarray,
    injection_strength: float = 0.5,
    method: str = "linear"
) -> np.ndarray:
    """
    Inject one manifold into another intelligence manifold
    
    Args:
        base_manifold: Base intelligence manifold (12D)
        injected_manifold: Manifold to inject (12D)
        injection_strength: How much to inject (0-1)
        method: "linear", "fractal", or "phase_lock"
    
    Returns:
        Modified intelligence manifold
    
    Example:
        >>> base = np.random.randn(12)
        >>> vision_manifold = extract_vision_model_to_manifold(...)
        >>> text_manifold = extract_text_model_to_manifold(...)
        >>> # Inject vision into text (50% mix)
        >>> mixed = inject_manifold_into_intelligence(text_manifold, vision_manifold, 0.5)
    """
    if method == "linear":
        # Simple linear interpolation
        result = (1 - injection_strength) * base_manifold + injection_strength * injected_manifold
    
    elif method == "fractal":
        # Fractal injection with golden ratio
        golden_ratio = 0.618
        fractal_weight = golden_ratio * injection_strength
        result = base_manifold + fractal_weight * injected_manifold
        result = result / np.linalg.norm(result)  # Normalize
    
    elif method == "phase_lock":
        # Phase-lock injection (18π periodicity)
        phase_shift = 18 * np.pi / 12
        result = base_manifold * np.cos(phase_shift) + injection_strength * injected_manifold
        result = result / np.linalg.norm(result)
    
    else:
        raise ValueError(f"Unknown injection method: {method}")
    
    return result


def combine_multiple_manifolds(
    manifolds: List[np.ndarray],
    weights: Optional[List[float]] = None,
    method: str = "weighted_average"
) -> np.ndarray:
    """
    Combine multiple manifolds into one intelligence manifold
    
    Args:
        manifolds: List of manifolds to combine (each 12D)
        weights: Optional weights for each manifold
        method: "weighted_average", "attention", or "phase_lock"
    
    Returns:
        Combined intelligence manifold
    
    Example:
        >>> vision_manifold = extract_vision_model_to_manifold(...)
        >>> text_manifold = extract_text_model_to_manifold(...)
        >>> audio_manifold = extract_audio_model_to_manifold(...)
        >>> # Combine with attention
        >>> combined = combine_multiple_manifolds(
        ...     [vision_manifold, text_manifold, audio_manifold],
        ...     method="attention"
        ... )
    """
    n_manifolds = len(manifolds)
    
    if weights is None:
        # Equal weights by default
        weights = [1.0 / n_manifolds] * n_manifolds
    else:
        # Normalize weights
        total = sum(weights)
        weights = [w / total for w in weights]
    
    if method == "weighted_average":
        # Simple weighted average
        result = sum(w * m for w, m in zip(weights, manifolds))
    
    elif method == "attention":
        # Attention-based combination
        # Compute pairwise similarities
        similarities = np.zeros((n_manifolds, n_manifolds))
        for i in range(n_manifolds):
            for j in range(n_manifolds):
                similarities[i, j] = np.dot(manifolds[i], manifolds[j])
        
        # Attention weights
        attention = np.exp(similarities) / np.sum(np.exp(similarities), axis=1, keepdims=True)
        
        # Combine with attention
        result = np.zeros(12)
        for i in range(n_manifolds):
            result += np.sum(attention[i, j] * manifolds[j] for j in range(n_manifolds))
        result /= n_manifolds
    
    elif method == "phase_lock":
        # Phase-lock combination with 18π
        phase_shift = 18 * np.pi / 12
        result = np.zeros(12)
        for i, manifold in enumerate(manifolds):
            rotated = manifold * np.cos(phase_shift * i)
            result += weights[i] * rotated
    
    else:
        raise ValueError(f"Unknown combination method: {method}")
    
    # Normalize
    result = result / np.linalg.norm(result)
    
    return result


# ============================================================================
# PART 3: Store and Load Models/Manifolds
# ============================================================================

def store_manifold(
    manifold: np.ndarray,
    filepath: str,
    metadata: Optional[Dict] = None
):
    """
    Store a manifold to disk
    
    Args:
        manifold: 12D manifold point
        filepath: Path to save file (.npz recommended)
        metadata: Optional metadata dictionary
    
    Example:
        >>> manifold = extract_model_weights_to_manifold(weights)
        >>> store_manifold(
        ...     manifold,
        ...     "models/vision_model.npz",
        ...     metadata={
        ...         "name": "vision_model",
        ...         "date": datetime.now().isoformat(),
        ...         "source": "DINOv2-giant"
        ...     }
        ... )
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save with metadata
    data = {
        "manifold": manifold,
        "shape": manifold.shape,
        "dtype": str(manifold.dtype),
        "timestamp": datetime.now().isoformat()
    }
    
    if metadata:
        data["metadata"] = metadata
    
    np.savez_compressed(filepath, **data)
    print(f"Stored manifold to {filepath}")


def load_manifold(filepath: str) -> Tuple[np.ndarray, Dict]:
    """
    Load a manifold from disk
    
    Args:
        filepath: Path to manifold file
    
    Returns:
        (manifold, metadata)
    
    Example:
        >>> manifold, metadata = load_manifold("models/vision_model.npz")
        >>> print(f"Loaded {metadata['name']}")
    """
    data = np.load(filepath, allow_pickle=True)
    
    manifold = data["manifold"]
    metadata = {
        "shape": data["shape"],
        "dtype": data["dtype"],
        "timestamp": data["timestamp"]
    }
    
    if "metadata" in data:
        metadata.update(data["metadata"].item())
    
    print(f"Loaded manifold from {filepath}")
    
    return manifold, metadata


def store_manifold_collection(
    manifolds: List[np.ndarray],
    filepath: str,
    labels: Optional[List[str]] = None,
    metadata: Optional[Dict] = None
):
    """
    Store a collection of manifolds
    
    Args:
        manifolds: List of 12D manifold points
        filepath: Path to save file (.npz recommended)
        labels: Optional labels for each manifold
        metadata: Optional metadata dictionary
    
    Example:
        >>> manifolds = [extract_model_to_manifold(w) for w in model_weights]
        >>> store_manifold_collection(
        ...     manifolds,
        ...     "models/manifold_collection.npz",
        ...     labels=["vision", "text", "audio"],
        ...     metadata={"version": "1.0"}
        ... )
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    data = {
        "manifolds": np.array(manifolds),
        "count": len(manifolds),
        "shape": manifolds[0].shape,
        "timestamp": datetime.now().isoformat()
    }
    
    if labels:
        data["labels"] = labels
    
    if metadata:
        data["metadata"] = metadata
    
    np.savez_compressed(filepath, **data)
    print(f"Stored {len(manifolds)} manifolds to {filepath}")


def load_manifold_collection(filepath: str) -> Tuple[np.ndarray, Dict]:
    """
    Load a collection of manifolds
    
    Args:
        filepath: Path to manifold collection file
    
    Returns:
        (manifolds_array, metadata)
    
    Example:
        >>> manifolds, metadata = load_manifold_collection("models/manifold_collection.npz")
        >>> print(f"Loaded {metadata['count']} manifolds")
    """
    data = np.load(filepath, allow_pickle=True)
    
    manifolds = data["manifolds"]
    metadata = {
        "count": int(data["count"]),
        "shape": data["shape"],
        "timestamp": data["timestamp"]
    }
    
    if "labels" in data:
        metadata["labels"] = data["labels"]
    
    if "metadata" in data:
        metadata.update(data["metadata"].item())
    
    print(f"Loaded {len(manifolds)} manifolds from {filepath}")
    
    return manifolds, metadata


def store_complete_model_state(
    decoder: GPUSVDDecoder,
    manifolds: List[np.ndarray],
    text_bridge: Optional[TextGenerationBridge] = None,
    filepath: str = "models/complete_agi_state.pkl"
):
    """
    Store complete AGI model state (decoder, manifolds, text bridge)
    
    Args:
        decoder: SVD decoder
        manifolds: List of manifolds
        text_bridge: Optional text generation bridge
        filepath: Path to save file
    
    Example:
        >>> store_complete_model_state(
        ...     decoder=decoder,
        ...     manifolds=manifold_list,
        ...     text_bridge=text_bridge,
        ...     filepath="models/agi_state_v1.pkl"
        ... )
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    state = {
        "decoder": {
            "n_weights": decoder.n_weights,
            "n_manifold_dim": decoder.n_manifold_dim,
            "omega_projection": decoder.omega_projection,
            "reference_weights": decoder.reference_weights,
            "reference_manifold": decoder.reference_manifold,
            "gpu_speedup": decoder.gpu_speedup
        },
        "manifolds": manifolds,
        "n_manifolds": len(manifolds),
        "timestamp": datetime.now().isoformat()
    }
    
    if text_bridge and text_bridge.built:
        state["text_bridge"] = {
            "built": text_bridge.built,
            "bridge_points": text_bridge.bridge_points,
            "text_decoder_trained": text_bridge.text_decoder.trained if text_bridge.text_decoder else False
        }
    
    with open(filepath, 'wb') as f:
        pickle.dump(state, f)
    
    print(f"Stored complete AGI state to {filepath}")


def load_complete_model_state(
    filepath: str = "models/complete_agi_state.pkl"
) -> Dict:
    """
    Load complete AGI model state
    
    Args:
        filepath: Path to state file
    
    Returns:
        Complete state dictionary
    
    Example:
        >>> state = load_complete_model_state("models/agi_state_v1.pkl")
        >>> manifolds = state["manifolds"]
        >>> print(f"Loaded {state['n_manifolds']} manifolds")
    """
    with open(filepath, 'rb') as f:
        state = pickle.load(f)
    
    print(f"Loaded complete AGI state from {filepath}")
    print(f"  Manifolds: {state['n_manifolds']}")
    print(f"  Timestamp: {state['timestamp']}")
    
    return state


# ============================================================================
# PART 4: Verification Tests
# ============================================================================

def verify_extraction():
    """Verify model extraction to manifold"""
    print("\n" + "=" * 80)
    print("VERIFICATION 1: Model Extraction")
    print("=" * 80)
    
    # Simulate model weights
    weights = np.random.randn(50000)
    
    # Extract to manifold
    manifold = extract_model_weights_to_manifold(weights)
    
    print(f"\n✓ Model extraction successful")
    print(f"  Input: {weights.shape} (model weights)")
    print(f"  Output: {manifold.shape} (12D manifold)")
    print(f"  Manifold norm: {np.linalg.norm(manifold):.4f}")
    print(f"  Manifold range: [{manifold.min():.4f}, {manifold.max():.4f}]")
    
    return manifold


def verify_injection():
    """Verify manifold injection"""
    print("\n" + "=" * 80)
    print("VERIFICATION 2: Manifold Injection")
    print("=" * 80)
    
    # Create two manifolds
    manifold1 = np.random.randn(12)
    manifold2 = np.random.randn(12)
    
    # Normalize
    manifold1 = manifold1 / np.linalg.norm(manifold1)
    manifold2 = manifold2 / np.linalg.norm(manifold2)
    
    # Test different injection methods
    methods = ["linear", "fractal", "phase_lock"]
    
    for method in methods:
        result = inject_manifold_into_intelligence(
            manifold1, manifold2, 0.5, method
        )
        print(f"\n✓ {method} injection:")
        print(f"  Result norm: {np.linalg.norm(result):.4f}")
        print(f"  Result range: [{result.min():.4f}, {result.max():.4f}]")
        similarity = np.dot(manifold1, result)
        print(f"  Similarity to base: {similarity:.4f}")
    
    return True


def verify_storage():
    """Verify manifold storage and loading"""
    print("\n" + "=" * 80)
    print("VERIFICATION 3: Storage and Loading")
    print("=" * 80)
    
    # Create test manifold
    manifold = np.random.randn(12)
    manifold = manifold / np.linalg.norm(manifold)
    
    # Test single manifold storage
    filepath = "test_data/test_manifold.npz"
    store_manifold(
        manifold,
        filepath,
        metadata={"name": "test", "version": "1.0"}
    )
    
    # Load and verify
    loaded_manifold, metadata = load_manifold(filepath)
    
    print(f"\n✓ Single manifold storage successful")
    print(f"  Original norm: {np.linalg.norm(manifold):.4f}")
    print(f"  Loaded norm: {np.linalg.norm(loaded_manifold):.4f}")
    print(f"  Difference: {np.linalg.norm(manifold - loaded_manifold):.6f}")
    print(f"  Metadata: {metadata}")
    
    # Test collection storage
    manifolds = [np.random.randn(12) for _ in range(10)]
    filepath_collection = "test_data/test_collection.npz"
    store_manifold_collection(
        manifolds,
        filepath_collection,
        labels=[f"manifold_{i}" for i in range(10)]
    )
    
    loaded_manifolds, metadata = load_manifold_collection(filepath_collection)
    
    print(f"\n✓ Collection storage successful")
    print(f"  Original count: {len(manifolds)}")
    print(f"  Loaded count: {len(loaded_manifolds)}")
    print(f"  Metadata: {metadata}")
    
    return True


def verify_text_generation():
    """Verify text generation from manifolds"""
    print("\n" + "=" * 80)
    print("VERIFICATION 4: Text Generation")
    print("=" * 80)
    
    # Create sample data
    intelligence_manifolds = [np.random.randn(12) for _ in range(20)]
    text_outputs = [
        "The neural network learns patterns from data.",
        "Machine learning algorithms make predictions.",
        "Deep learning uses multiple layers for features.",
        "Natural language processing understands language.",
        "Computer vision interprets visual information."
    ] * 4  # Repeat to match 20
    
    # Build text bridge
    text_bridge = TextGenerationBridge(
        n_intelligence_dim=12,
        n_text_dim=768
    )
    
    text_bridge.build_bridge(intelligence_manifolds, text_outputs)
    
    # Generate text
    test_manifold = np.random.randn(12)
    generated_text = text_bridge.generate_text(
        test_manifold,
        use_fractal_smoothing=True,
        temperature=0.7,
        max_length=50
    )
    
    print(f"\n✓ Text generation successful")
    print(f"  Input manifold: {test_manifold[:5]}...")
    print(f"  Generated text: {generated_text}")
    print(f"  Text length: {len(generated_text)} characters")
    
    # Test probability
    test_text = "machine learning"
    probability = text_bridge.get_text_probability(test_manifold, test_text)
    print(f"  Probability of '{test_text}': {probability:.4f}")
    
    return True


def run_all_verifications():
    """Run all verification tests"""
    print("\n" + "=" * 80)
    print("AGI SYSTEM VERIFICATION SUITE")
    print("=" * 80)
    
    results = {}
    
    try:
        results['extraction'] = verify_extraction()
        print("\n✓ Extraction verification PASSED")
    except Exception as e:
        results['extraction'] = False
        print(f"\n✗ Extraction verification FAILED: {e}")
    
    try:
        results['injection'] = verify_injection()
        print("\n✓ Injection verification PASSED")
    except Exception as e:
        results['injection'] = False
        print(f"\n✗ Injection verification FAILED: {e}")
    
    try:
        results['storage'] = verify_storage()
        print("\n✓ Storage verification PASSED")
    except Exception as e:
        results['storage'] = False
        print(f"\n✗ Storage verification FAILED: {e}")
    
    try:
        results['text_generation'] = verify_text_generation()
        print("\n✓ Text generation verification PASSED")
    except Exception as e:
        results['text_generation'] = False
        print(f"\n✗ Text generation verification FAILED: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {test_name}: {status}")
    
    return all(results.values())


# ============================================================================
# PART 5: Practical Examples
# ============================================================================

def example_complete_workflow():
    """Complete workflow example"""
    print("\n" + "=" * 80)
    print("COMPLETE WORKFLOW EXAMPLE")
    print("=" * 80)
    
    # Step 1: Extract models to manifolds
    print("\n[Step 1] Extract models to manifolds")
    vision_weights = np.random.randn(50000)
    text_weights = np.random.randn(50000)
    
    vision_manifold = extract_model_weights_to_manifold(vision_weights)
    text_manifold = extract_model_weights_to_manifold(text_weights)
    
    print(f"  Vision: {vision_weights.shape} → {vision_manifold.shape}")
    print(f"  Text: {text_weights.shape} → {text_manifold.shape}")
    
    # Step 2: Inject manifolds
    print("\n[Step 2] Inject manifolds")
    combined_manifold = inject_manifold_into_intelligence(
        text_manifold,
        vision_manifold,
        injection_strength=0.3,
        method="fractal"
    )
    print(f"  Combined: {combined_manifold.shape}")
    
    # Step 3: Store manifolds
    print("\n[Step 3] Store manifolds")
    store_manifold(
        combined_manifold,
        "models/combined_multimodal.npz",
        metadata={
            "name": "multimodal",
            "components": ["vision", "text"],
            "injection_strength": 0.3
        }
    )
    
    # Step 4: Load manifold
    print("\n[Step 4] Load manifold")
    loaded_manifold, metadata = load_manifold("models/combined_multimodal.npz")
    print(f"  Loaded: {loaded_manifold.shape}")
    print(f"  Metadata: {metadata}")
    
    print("\n✓ Complete workflow successful!")


if __name__ == "__main__":
    # Run all verifications
    success = run_all_verifications()
    
    # Run complete workflow example
    if success:
        example_complete_workflow()
    
    print("\n" + "=" * 80)
    print("VERIFICATION COMPLETE")
    print("=" * 80)

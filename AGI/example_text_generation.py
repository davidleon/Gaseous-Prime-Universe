"""
Example: Integrating Text Generation with AGI System
Demonstrates how to make AGI emit proper text
"""

import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agi_system import AGISystem
from manifold.text_generation_bridge import TextGenerationBridge


def create_training_data():
    """Create sample training data for text generation"""
    print("\nCreating training data...")
    
    # Sample intelligence manifolds (12D)
    n_samples = 100
    intelligence_manifolds = [
        np.random.randn(12) for _ in range(n_samples)
    ]
    
    # Sample text outputs
    text_outputs = [
        "The neural network learns complex patterns from large datasets.",
        "Machine learning algorithms make predictions based on training examples.",
        "Deep learning uses multiple layers to extract hierarchical features.",
        "Natural language processing enables computers to understand human language.",
        "Computer vision allows machines to interpret and analyze visual information.",
        "Reinforcement learning teaches agents through trial and error interactions.",
        "Generative models can create new data samples similar to training data.",
        "Transformer architectures use self-attention to process sequential data.",
        "Artificial intelligence is transforming many industries and applications.",
        "Data preprocessing is crucial for machine learning model performance.",
        "Supervised learning requires labeled training data for training.",
        "Unsupervised learning discovers hidden patterns in unlabeled data.",
        "Convolutional neural networks are effective for image recognition tasks.",
        "Recurrent neural networks process sequential data with internal memory.",
        "Gradient descent optimizes neural network parameters during training.",
        "Backpropagation efficiently computes gradients for multi-layer networks.",
        "Regularization techniques prevent overfitting in machine learning models.",
        "Transfer learning leverages pre-trained models for new tasks.",
        "Ensemble methods combine multiple models for improved performance.",
        "Feature engineering transforms raw data into useful representations."
    ] * 5  # Repeat to get 100 samples
    
    print(f"  Created {len(intelligence_manifolds)} manifold-text pairs")
    
    return intelligence_manifolds, text_outputs


def create_agi_with_text_generation():
    """Create AGI system with text generation capability"""
    print("\n" + "=" * 80)
    print("AGI SYSTEM WITH TEXT GENERATION")
    print("=" * 80)
    
    # Create AGI system (small scale for demo)
    print("\n1. Creating AGI system...")
    agi = AGISystem(
        n_manifolds=1000,      # Small scale for demo
        n_weights=5000,        # Small weights for demo
        n_manifold_dim=12,
        n_levels=4,
        precision_bits=400,
        use_parallel=False,    # Disable for local demo
        use_gpu=False          # Disable for local demo
    )
    
    # Initialize AGI
    print("2. Initializing AGI system...")
    agi.initialize(n_initialize=100)
    
    # Get intelligence manifolds from AGI
    print("3. Extracting intelligence manifolds from AGI...")
    intelligence_manifolds = []
    for i in range(100):
        manifold = agi.coordinator.get_manifold(i)
        intelligence_manifolds.append(manifold)
    
    # Create text outputs (paired with manifolds)
    print("4. Creating paired text outputs...")
    text_outputs = [
        "The neural network learns complex patterns from data.",
        "Machine learning algorithms make predictions based on examples.",
        "Deep learning uses multiple layers to extract features.",
        "Natural language processing enables computers to understand language.",
        "Computer vision allows machines to interpret visual information.",
        "Reinforcement learning teaches agents through trial and error.",
        "Generative models can create new data samples.",
        "Transformer architectures use self-attention mechanisms.",
        "Artificial intelligence transforms industries and applications.",
        "Data preprocessing is crucial for model performance."
    ] * 10  # Repeat to match 100 manifolds
    
    # Build text generation bridge
    print("5. Building text generation fractal bridge...")
    text_bridge = TextGenerationBridge(
        n_intelligence_dim=12,
        n_text_dim=768,
        n_fractal_levels=4,
        golden_ratio=0.618,
        phase_lock_period=18 * np.pi
    )
    
    text_bridge.build_bridge(intelligence_manifolds, text_outputs)
    
    # Demonstrate text generation
    print("\n6. Demonstrating text generation...")
    
    # Generate text from random manifold
    test_manifold = np.random.randn(12)
    generated_text = text_bridge.generate_text(
        test_manifold,
        use_fractal_smoothing=True,
        temperature=0.7,
        max_length=50
    )
    
    print(f"\n  Input manifold: {test_manifold[:5]}...")
    print(f"  Generated text: {generated_text}")
    
    # Generate text from AGI prediction
    print("\n7. Generating text from AGI prediction...")
    test_input = np.random.randn(100)
    prediction, confidence, details = agi.predict(test_input)
    
    # Get manifold for prediction
    pred_manifold = agi.coordinator.get_manifold(prediction % 100)
    pred_text = text_bridge.generate_text(
        pred_manifold,
        use_fractal_smoothing=True,
        temperature=0.7,
        max_length=50
    )
    
    print(f"  AGI prediction: {prediction} (confidence: {confidence:.4f})")
    print(f"  Generated text: {pred_text}")
    
    # Batch generation
    print("\n8. Batch text generation...")
    test_manifolds = [np.random.randn(12) for _ in range(5)]
    generated_texts = text_bridge.generate_text_batch(
        test_manifolds,
        use_fractal_smoothing=True,
        temperature=0.7,
        max_length=30
    )
    
    for i, text in enumerate(generated_texts):
        print(f"  Manifold {i}: {text}")
    
    # Text probability
    print("\n9. Computing text probabilities...")
    test_text = "machine learning is powerful"
    probability = text_bridge.get_text_probability(test_manifold, test_text)
    print(f"  Text: '{test_text}'")
    print(f"  Probability: {probability:.4f}")
    
    # Get system info
    print("\n10. System information...")
    bridge_info = text_bridge.get_bridge_info()
    print(f"  Bridge built: {bridge_info['built']}")
    print(f"  Fractal levels: {bridge_info['n_fractal_levels']}")
    print(f"  Text decoder trained: {bridge_info['text_decoder_trained']}")
    print(f"  Bridge points: {bridge_info['n_bridge_points']}")
    
    return agi, text_bridge


def main():
    """Main demo function"""
    print("\n" + "=" * 80)
    print("TEXT GENERATION INTEGRATION DEMO")
    print("=" * 80)
    print("\nThis demo shows how to integrate text generation")
    print("with your AGI system using:")
    print("  • Text Decoder Manifold (no tokenizer needed)")
    print("  • Text Generation Fractal Bridge")
    print("  • Continuous text embeddings (768D)")
    print("  • Semantic clusters (1000 clusters)")
    print("  • Fractal smoothing for coherence")
    
    try:
        # Create AGI with text generation
        agi, text_bridge = create_agi_with_text_generation()
        
        # Summary
        print("\n" + "=" * 80)
        print("DEMO COMPLETE!")
        print("=" * 80)
        print("\nKey achievements:")
        print("  ✓ AGI system created and initialized")
        print("  ✓ Text generation bridge built")
        print("  ✓ Intelligence manifolds extracted from AGI")
        print("  ✓ Text generated from manifolds")
        print("  ✓ Batch generation demonstrated")
        print("  ✓ Text probabilities computed")
        print("\nBenefits:")
        print("  ✓ No traditional tokenizer needed")
        print("  ✓ Continuous semantic space")
        print("  ✓ Smooth fractal transitions")
        print("  ✓ Works naturally with 12D manifolds")
        print("  ✓ High semantic coherence")
        print("\nNext steps:")
        print("  1. Collect more training data (10K+ pairs)")
        print("  2. Train on real AGI manifold-text pairs")
        print("  3. Tune hyperparameters (temperature, top-k, etc.)")
        print("  4. Evaluate text quality metrics")
        print("  5. Integrate into production AGI system")
        
    except Exception as e:
        print(f"\n[ERROR] Demo failed: {e}")
        import traceback
        traceback.print_exc()
        print("\nTroubleshooting:")
        print("  1. Ensure all dependencies are installed")
        print("  2. Check AGI system initialization")
        print("  3. Verify manifold-text pair alignment")
        print("  4. Review error messages above")


if __name__ == "__main__":
    main()
"""
Test Interactive Session Message Ingestion

Verifies that the interactive session ingests messages correctly with:
1. Epiplexity assessment
2. Optimal truncation with even spacing
3. Adaptive repetition based on epiplexity
"""

import sys
import os

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evolving_chat_bot import EvolvingChatBot


def test_message_ingestion():
    """Test message ingestion with epiplexity and optimal truncation"""
    print("=" * 60)
    print("Interactive Session Message Ingestion Test")
    print("=" * 60)
    
    # Create bot
    bot = EvolvingChatBot(name="EVA", manifold_dim=12, quiet=True)
    
    # Test messages of varying complexity
    test_messages = [
        ("Hello", "Simple greeting (low epiplexity)"),
        ("What is the Collatz conjecture?", "Medium complexity question"),
        ("Explain the relationship between prime distribution and the Riemann zeta function zeros in the context of the Gaseous Prime Universe theory.", "Complex question (high epiplexity)"),
        ("7+5=12", "Arithmetic (handled separately)"),
    ]
    
    print("\nTesting message ingestion...\n")
    
    for message, description in test_messages:
        print(f"Message: {message}")
        print(f"Description: {description}")
        
        # Process message
        response, metadata = bot.process_message(message)
        
        # Show metadata
        print(f"Epiplexity: {metadata['epiplexity']:.4f}")
        print(f"Learning signal: {metadata['learning_signal']:.4f}")
        print(f"Knowledge extracted: {len(metadata['knowledge_extracted'])} topics")
        
        # Check trainer statistics
        stats = bot.trainer.get_comprehensive_stats()
        print(f"Total texts processed: {stats.get('proofs_processed', 0)}")
        print(f"Total truncations: {stats['truncations_applied']}")
        print(f"Average epiplexity: {stats['avg_epiplexity']:.4f}")
        
        # Get optimal truncation points for this message
        n_tokens = len(message.split())
        optimal_points = bot.trainer.learner.optimal_truncation_points(n_tokens)
        
        print(f"Text length: {n_tokens} tokens")
        print(f"Optimal truncation points: {optimal_points}")
        
        # Verify even spacing
        if len(optimal_points) > 1:
            # Calculate spacing between consecutive points
            spacings = [optimal_points[i+1] - optimal_points[i] for i in range(len(optimal_points)-1)]
            print(f"Spacings: {spacings}")
            
            # Check if spacings are approximately equal
            if len(spacings) > 1:
                avg_spacing = sum(spacings) / len(spacings)
                max_deviation = max(abs(s - avg_spacing) for s in spacings)
                print(f"Average spacing: {avg_spacing:.2f}")
                print(f"Max deviation: {max_deviation:.2f}")
                
                # Check if spacing is even (deviation < 1.5 for uniform spacing)
                if max_deviation < 1.5:
                    print("✓ EVEN SPACING VERIFIED")
                else:
                    print("✗ Spacing is not even!")
        
        print(f"\nBot response: {response}")
        print(f"\n{'-' * 60}\n")
    
    # Final statistics
    final_stats = bot.trainer.get_comprehensive_stats()
    print("=" * 60)
    print("Final Statistics")
    print("=" * 60)
    print(f"Total texts processed: {final_stats.get('proofs_processed', 0)}")
    print(f"Total truncations: {final_stats['truncations_applied']}")
    print(f"Total completions: {final_stats['completions_learned']}")
    print(f"Average epiplexity: {final_stats['avg_epiplexity']:.4f}")
    print(f"Max epiplexity: {final_stats.get('max_epiplexity_value', 0.0):.4f}")
    
    if 'avg_adaptive_reps' in final_stats:
        print(f"Average adaptive repetitions: {final_stats['avg_adaptive_reps']:.2f}")
    
    if 'uniform_efficiency' in final_stats:
        print(f"Average uniform efficiency: {final_stats['uniform_efficiency']:.4f}")
        print(f"Average adaptive efficiency: {final_stats['adaptive_efficiency']:.4f}")
    
    return True


if __name__ == "__main__":
    test_message_ingestion()
    print("\n✓ Message ingestion test complete!")
    sys.exit(0)
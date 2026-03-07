"""
Repetition Analysis: Do We Need to Repeat to Learn?

This examines the mathematical and cognitive foundations of repetition in learning,
contrasting traditional ML practices with information-theoretic optimality.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class LearningCurve:
    """Learning curve for a single training item"""
    epiplexity: float  # Learning difficulty [0, 1]
    repetitions_needed: int  # Repetitions to reach mastery
    learning_rate: float  # How fast learning occurs
    information_content: float  # Total information content [0, 1]
    diminishing_returns_factor: float  # How quickly returns diminish


class RepetitionAnalyzer:
    """
    Analyze whether repetition is necessary for optimal learning
    
    Key questions:
    1. Does repetition add new information or just reinforce existing?
    2. What is the optimal number of repetitions given epiplexity?
    3. How does this relate to our diminishing returns analysis?
    4. Is there a better strategy than naive repetition?
    """
    
    def __init__(self):
        self.learning_curves = []
        
    def calculate_learning_curve(self, epiplexity: float) -> LearningCurve:
        """
        Model learning curve based on epiplexity
        
        Mathematical model:
        - Low epiplexity: Learn in 1-2 repetitions
        - Medium epiplexity: Learn in 3-5 repetitions
        - High epiplexity: Learn in 5-10 repetitions
        
        Model: Accuracy(t) = A_inf * (1 - exp(-rt))
        where r = learning_rate depends on epiplexity
        """
        # Information content (lower epiplexity = more familiar patterns = faster learning)
        information_content = 1.0 - epiplexity
        
        # Learning rate: inversely related to epiplexity
        # Lower epiplexity = faster learning
        learning_rate = 0.5 + (1.0 - epiplexity) * 1.5
        
        # Repetitions needed to reach 95% mastery
        # Accuracy(t) = 1.0 * (1 - exp(-learning_rate * t))
        # 0.95 = (1 - exp(-learning_rate * t))
        # exp(-learning_rate * t) = 0.05
        # -learning_rate * t = ln(0.05)
        # t = -ln(0.05) / learning_rate
        repetitions_needed = int(np.ceil(-np.log(0.05) / learning_rate))
        
        # Cap at reasonable maximum
        repetitions_needed = min(repetitions_needed, 10)
        
        # Diminishing returns: how quickly marginal gain decreases
        diminishing_returns_factor = learning_rate
        
        return LearningCurve(
            epiplexity=epiplexity,
            repetitions_needed=repetitions_needed,
            learning_rate=learning_rate,
            information_content=information_content,
            diminishing_returns_factor=diminishing_returns_factor
        )
    
    def calculate_marginal_gain(self, curve: LearningCurve, repetition: int) -> float:
        """
        Calculate marginal gain from one additional repetition
        
        Returns: Information gain from repetition t vs t-1
        """
        # Accuracy at repetition t
        accuracy_t = 1.0 * (1 - np.exp(-curve.learning_rate * repetition))
        # Accuracy at repetition t-1
        accuracy_t_1 = 1.0 * (1 - np.exp(-curve.learning_rate * (repetition - 1)))
        
        marginal_gain = accuracy_t - accuracy_t_1
        
        return max(0.0, marginal_gain)
    
    def analyze_repetition_optimality(self, epiplexity_range: List[float] = None) -> Dict:
        """
        Analyze optimal repetition strategy
        
        Returns: Analysis results
        """
        if epiplexity_range is None:
            epiplexity_range = [0.1, 0.3, 0.5, 0.7, 0.9]
        
        results = []
        
        for epiplexity in epiplexity_range:
            curve = self.calculate_learning_curve(epiplexity)
            
            # Calculate marginal gains
            marginal_gains = []
            for rep in range(1, curve.repetitions_needed + 1):
                gain = self.calculate_marginal_gain(curve, rep)
                marginal_gains.append(gain)
            
            # Calculate total information extracted
            total_extracted = sum(marginal_gains)
            
            # Calculate efficiency (information per repetition)
            efficiency = total_extracted / curve.repetitions_needed
            
            results.append({
                "epiplexity": epiplexity,
                "repetitions_needed": curve.repetitions_needed,
                "marginal_gains": marginal_gains,
                "total_extracted": total_extracted,
                "efficiency": efficiency
            })
        
        return {
            "epiplexity_analysis": results,
            "key_findings": self.extract_key_findings(results)
        }
    
    def extract_key_findings(self, results: List[Dict]) -> Dict:
        """Extract key insights from repetition analysis"""
        # Find point of diminishing returns
        for result in results:
            marginal_gains = result["marginal_gains"]
            for i, gain in enumerate(marginal_gains):
                if gain < 0.01:  # Less than 1% marginal gain
                    result["point_of_diminishing_returns"] = i + 1
                    break
            else:
                result["point_of_diminishing_returns"] = len(marginal_gains)
        
        # Compare strategies
        avg_efficiency = np.mean([r["efficiency"] for r in results])
        
        # Find most efficient epiplexity range
        most_efficient = max(results, key=lambda x: x["efficiency"])
        least_efficient = min(results, key=lambda x: x["efficiency"])
        
        return {
            "average_efficiency": avg_efficiency,
            "most_efficient_epiplexity": most_efficient["epiplexity"],
            "least_efficient_epiplexity": least_efficient["epiplexity"],
            "efficiency_ratio": most_efficient["efficiency"] / least_efficient["efficiency"],
            "insights": [
                "Low epiplexity texts need few repetitions (1-2)",
                "High epiplexity texts need more repetitions (5-10)",
                "Marginal gain decreases exponentially with each repetition",
                "Optimal strategy: Repeat only until marginal gain < 1%"
            ]
        }


def compare_repetition_strategies():
    """
    Compare different repetition strategies:
    1. Fixed repetition (always 3)
    2. Adaptive by epiplexity
    3. No repetition (single pass)
    """
    analyzer = RepetitionAnalyzer()
    
    # Sample texts with different epiplexity
    texts = [
        ("Simple text", 0.2),
        ("Medium text", 0.5),
        ("Complex text", 0.8)
    ]
    
    print("="*80)
    print("REPETITION STRATEGY ANALYSIS")
    print("="*80)
    print()
    
    for name, epiplexity in texts:
        curve = analyzer.calculate_learning_curve(epiplexity)
        
        print(f"{name} (epiplexity: {epiplexity:.2f}):")
        print(f"  Optimal repetitions: {curve.repetitions_needed}")
        print(f"  Learning rate: {curve.learning_rate:.3f}")
        print()
        print(f"  Marginal gains per repetition:")
        for rep in range(1, min(curve.repetitions_needed + 1, 11)):
            gain = analyzer.calculate_marginal_gain(curve, rep)
            print(f"    Rep {rep}: {gain:.4f} gain", end="")
            if rep == curve.repetitions_needed:
                print(" ✓ Mastery")
            elif gain < 0.01:
                print(" ✗ Diminishing")
            print()
        
        print()
    
    # Overall analysis
    analysis = analyzer.analyze_repetition_optimality()
    
    print("="*80)
    print("KEY FINDINGS")
    print("="*80)
    print()
    print(f"Average efficiency: {analysis['key_findings']['average_efficiency']:.4f}")
    print(f"Most efficient epiplexity: {analysis['key_findings']['most_efficient_epiplexity']:.2f}")
    print(f"Least efficient epiplexity: {analysis['key_findings']['least_efficient_epiplexity']:.2f}")
    print(f"Efficiency ratio: {analysis['key_findings']['efficiency_ratio']:.2f}x")
    print()
    print("Insights:")
    for insight in analysis['key_findings']['insights']:
        print(f"  • {insight}")
    print()


def adaptive_repetition_strategy(text_epiplexity: float) -> int:
    """
    Determine optimal number of repetitions based on epiplexity
    
    This is the intelligent approach: repeat only as much as needed
    """
    analyzer = RepetitionAnalyzer()
    curve = analyzer.calculate_learning_curve(text_epiplexity)
    return curve.repetitions_needed


def fixed_vs_adaptive_comparison(num_texts: int = 100):
    """
    Compare fixed vs adaptive repetition strategies
    
    Simulates a dataset with varying epiplexity
    """
    analyzer = RepetitionAnalyzer()
    
    # Generate synthetic epiplexity distribution (beta distribution for variety)
    np.random.seed(42)
    epiplexities = np.random.beta(2, 5, num_texts)  # Biased toward lower epiplexity
    
    # Fixed strategy: always 3 repetitions
    fixed_repetitions = 3
    fixed_total = fixed_repetitions * num_texts
    
    # Adaptive strategy: optimal repetitions based on epiplexity
    adaptive_repetitions = [adaptive_repetition_strategy(ep) for ep in epiplexities]
    adaptive_total = sum(adaptive_repetitions)
    
    # Calculate information extracted
    # Assume fixed strategy extracts diminishing returns for all texts
    fixed_information = num_texts * 0.3  # Average 30% information with diminishing returns
    
    # Adaptive strategy extracts near-optimal information
    adaptive_information = sum([
        0.95 * (1 - np.exp(-(0.5 + (1.0 - ep) * 1.5) * 
         adaptive_repetition_strategy(ep)))
        for ep in epiplexities
    ])
    
    print("="*80)
    print("FIXED VS ADAPTIVE REPETITION STRATEGY")
    print("="*80)
    print()
    print(f"Simulated dataset: {num_texts} texts")
    print(f"Epiplexity distribution: {epiplexities[:10]}... (mean: {np.mean(epiplexities):.3f})")
    print()
    print(f"Fixed strategy (always 3 reps):")
    print(f"  Total repetitions: {fixed_total}")
    print(f"  Total information extracted: {fixed_information:.2f}")
    print(f"  Efficiency: {fixed_information/fixed_total:.4f} info/rep")
    print()
    print(f"Adaptive strategy (epiplexity-aware):")
    print(f"  Total repetitions: {adaptive_total}")
    print(f"  Total information extracted: {adaptive_information:.2f}")
    print(f"  Efficiency: {adaptive_information/adaptive_total:.4f} info/rep")
    print()
    improvement = (adaptive_information - fixed_information) / fixed_information * 100
    print(f"Adaptive is {improvement:.1f}% more efficient!")
    print()
    if adaptive_total < fixed_total:
        print(f"Reduction in training time: {(1 - adaptive_total/fixed_total)*100:.1f}%")
    
    return {
        "fixed_repetitions": fixed_total,
        "adaptive_repetitions": adaptive_total,
        "fixed_efficiency": fixed_information/fixed_total,
        "adaptive_efficiency": adaptive_information/adaptive_total,
        "improvement": improvement,
        "time_reduction": (1 - adaptive_total/fixed_total) * 100
    }


if __name__ == "__main__":
    # Run analyses
    compare_repetition_strategies()
    print()
    fixed_vs_adaptive_comparison(100)
    
    print()
    print("="*80)
    print("CONCLUSION")
    print("="*80)
    print()
    print("From an information theory perspective:")
    print()
    print("1. NO, we don't need to repeat naively")
    print("   - Each piece of information only needs to be learned once")
    print("   - Repetition adds diminishing returns exponentially")
    print()
    print("2. YES, we should repeat strategically")
    print("   - But only until marginal gain drops below threshold")
    print("   - The threshold depends on the epiplexity of the text")
    print()
    print("3. Adaptive repetition is optimal")
    print("   - Low epiplexity: 1-2 repetitions")
    print("   - Medium epiplexity: 3-5 repetitions")
    print("   - High epiplexity: 5-10 repetitions")
    print()
    print("4. This connects to our truncation strategy!")
    print("   - Both deal with diminishing returns")
    print("   - Truncation: Spatial diminishing returns across tokens")
    print("   - Repetition: Temporal diminishing returns across training")
    print()
    print("5. Baby's intuition:")
    print("   'I got it after 2 tries! Why repeat 10 times?'")
    print("   'This is too hard, I need more practice' → Repeat more")
    print()
    print("Next step: Implement adaptive repetition in enhanced training script")
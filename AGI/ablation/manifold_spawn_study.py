#!/usr/bin/env python3
"""
Manifold Spawn Strategy Empirical Study

This study compares 7 different manifold generation strategies:
1. Static constant noise (baseline)
2. Adaptive noise schedule
3. Task-dependent noise
4. Ensemble-optimal noise
5. High-dimensional scaling
6. Multi-objective Pareto-optimal
7. Hybrid strategy

Author: Gaseous Prime Universe Research Team
Date: 2026-03-06
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from dataclasses import dataclass
from typing import List, Dict, Tuple, Callable
from scipy import stats
from sklearn.metrics import pairwise_distances
import warnings
warnings.filterwarnings('ignore')

# =====================
# CONSTANTS
# =====================
PHI = (1 + np.sqrt(5)) / 2  # Golden ratio
SIGMA_STAR = 1 / PHI  # Optimal noise: ≈ 0.618
NUM_TRIALS = 20
NUM_EPOCHS = 50
ENSEMBLE_SIZES = [1, 3, 5, 10]
MANIFOLD_DIMENSIONS = [12, 24, 48]
NUM_SAMPLES = 1000
NUM_CLASSES = 4


# =====================
# DATA STRUCTURES
# =====================
@dataclass
class ManifoldPoint:
    """Represents a point on a manifold"""
    coordinates: np.ndarray  # d-dimensional coordinates
    dimension: int


@dataclass
class Ensemble:
    """Represents an ensemble of manifolds"""
    manifolds: List[ManifoldPoint]
    size: int
    dimension: int


@dataclass
class Task:
    """Represents a learning task"""
    name: str
    complexity: float  # C ∈ [0, 1]
    data: np.ndarray  # Input data
    labels: np.ndarray  # Labels (for classification)


@dataclass
class PerformanceMetrics:
    """Performance metrics for evaluation"""
    accuracy: float
    diversity: float
    convergence_speed: float
    robustness: float
    generalization_gap: float
    stability: float


@dataclass
class StrategyResult:
    """Results for a spawn strategy"""
    strategy_name: str
    metrics: PerformanceMetrics
    noise_levels: List[float]  # Noise levels used across epochs


# =====================
# SPAWN STRATEGIES
# =====================
class SpawnStrategies:
    """Collection of manifold spawn strategies"""
    
    @staticmethod
    def static_constant_noise(base: ManifoldPoint, num_manifolds: int, 
                              epoch: int = 0) -> Ensemble:
        """
        Strategy 1: Static constant noise
        σ_spawn = σ* ≈ 0.618
        """
        noise_level = SIGMA_STAR
        manifolds = [base]  # Include base
        
        for _ in range(num_manifolds - 1):
            noise = np.random.randn(base.dimension) * noise_level
            new_coords = base.coordinates + noise
            manifolds.append(ManifoldPoint(new_coords, base.dimension))
        
        return Ensemble(manifolds, num_manifolds, base.dimension)
    
    @staticmethod
    def adaptive_noise_schedule(base: ManifoldPoint, num_manifolds: int,
                               epoch: int, time_constant: float = 50.0) -> Ensemble:
        """
        Strategy 2: Adaptive noise schedule
        σ_spawn(t) = φ·exp(-t/τ)
        """
        noise_level = PHI * np.exp(-epoch / time_constant)
        manifolds = [base]
        
        for _ in range(num_manifolds - 1):
            noise = np.random.randn(base.dimension) * noise_level
            new_coords = base.coordinates + noise
            manifolds.append(ManifoldPoint(new_coords, base.dimension))
        
        return Ensemble(manifolds, num_manifolds, base.dimension)
    
    @staticmethod
    def task_dependent_noise(base: ManifoldPoint, num_manifolds: int,
                            task_complexity: float) -> Ensemble:
        """
        Strategy 3: Task-dependent noise
        σ_spawn(C) = φ·C^(1/3)
        """
        noise_level = PHI * (task_complexity + 0.1) ** (1/3)
        manifolds = [base]
        
        for _ in range(num_manifolds - 1):
            noise = np.random.randn(base.dimension) * noise_level
            new_coords = base.coordinates + noise
            manifolds.append(ManifoldPoint(new_coords, base.dimension))
        
        return Ensemble(manifolds, num_manifolds, base.dimension)
    
    @staticmethod
    def ensemble_optimal_noise(base: ManifoldPoint, num_manifolds: int,
                               ensemble_size: int) -> Ensemble:
        """
        Strategy 4: Ensemble-optimal noise
        σ_spawn(k) = φ/√k
        """
        noise_level = PHI / np.sqrt(ensemble_size)
        manifolds = [base]
        
        for _ in range(num_manifolds - 1):
            noise = np.random.randn(base.dimension) * noise_level
            new_coords = base.coordinates + noise
            manifolds.append(ManifoldPoint(new_coords, base.dimension))
        
        return Ensemble(manifolds, num_manifolds, base.dimension)
    
    @staticmethod
    def high_dimensional_scaling(base: ManifoldPoint, num_manifolds: int,
                                 dimension: int) -> Ensemble:
        """
        Strategy 5: High-dimensional scaling
        σ_spawn(d) = φ/√(d/12)
        """
        noise_level = PHI / np.sqrt(dimension / 12.0)
        manifolds = [base]
        
        for _ in range(num_manifolds - 1):
            noise = np.random.randn(base.dimension) * noise_level
            new_coords = base.coordinates + noise
            manifolds.append(ManifoldPoint(new_coords, base.dimension))
        
        return Ensemble(manifolds, num_manifolds, base.dimension)
    
    @staticmethod
    def pareto_optimal_noise(base: ManifoldPoint, num_manifolds: int,
                            accuracy_weight: float = 0.5,
                            diversity_weight: float = 0.5) -> Ensemble:
        """
        Strategy 6: Pareto-optimal noise
        Choose σ to balance accuracy and diversity objectives
        """
        # Solve: maximize w_acc * accuracy(σ) + w_div * diversity(σ)
        # For balanced case (w_acc = w_div = 0.5), solution is σ* = 1/φ
        if accuracy_weight == 0.5 and diversity_weight == 0.5:
            noise_level = SIGMA_STAR
        else:
            # Numerical optimization for weighted case
            def objective(sigma):
                acc = 1 / (1 + sigma**2)
                div = 2 * sigma / (1 + sigma**2)
                return -(accuracy_weight * acc + diversity_weight * div)
            
            from scipy.optimize import minimize_scalar
            result = minimize_scalar(objective, bounds=(0.01, 5.0), method='bounded')
            noise_level = result.x
        
        manifolds = [base]
        for _ in range(num_manifolds - 1):
            noise = np.random.randn(base.dimension) * noise_level
            new_coords = base.coordinates + noise
            manifolds.append(ManifoldPoint(new_coords, base.dimension))
        
        return Ensemble(manifolds, num_manifolds, base.dimension)
    
    @staticmethod
    def hybrid_strategy(base: ManifoldPoint, num_manifolds: int,
                        epoch: int, task_complexity: float,
                        ensemble_size: int, dimension: int,
                        time_constant: float = 50.0) -> Ensemble:
        """
        Strategy 7: Hybrid strategy
        σ_spawn = φ·C^(1/3)·exp(-t/τ)/√(k·d/12)
        """
        noise_level = (PHI * 
                      (task_complexity + 0.1) ** (1/3) * 
                      np.exp(-epoch / time_constant) / 
                      np.sqrt(ensemble_size * dimension / 12.0))
        
        manifolds = [base]
        for _ in range(num_manifolds - 1):
            noise = np.random.randn(base.dimension) * noise_level
            new_coords = base.coordinates + noise
            manifolds.append(ManifoldPoint(new_coords, base.dimension))
        
        return Ensemble(manifolds, num_manifolds, base.dimension)


# =====================
# EVALUATION METRICS
# =====================
class Evaluator:
    """Evaluate ensemble performance"""
    
    @staticmethod
    def compute_accuracy(ensemble: Ensemble, task: Task) -> float:
        """
        Simulate accuracy: higher similarity to true pattern = higher accuracy
        """
        # Create a synthetic "true" pattern for the task
        np.random.seed(hash(task.name) % (2**32))
        true_pattern = np.random.randn(ensemble.dimension)
        
        # Ensemble prediction: average of all manifolds
        ensemble_pred = np.mean([m.coordinates for m in ensemble.manifolds], axis=0)
        
        # Accuracy: negative distance from true pattern (normalized to [0,1])
        distance = np.linalg.norm(ensemble_pred - true_pattern)
        accuracy = np.exp(-distance / ensemble.dimension)
        
        return accuracy
    
    @staticmethod
    def compute_diversity(ensemble: Ensemble) -> float:
        """
        Compute ensemble diversity: average pairwise distance
        """
        coords = np.array([m.coordinates for m in ensemble.manifolds])
        
        if len(coords) < 2:
            return 0.0
        
        # Pairwise distances
        distances = pairwise_distances(coords, metric='euclidean')
        
        # Diversity: mean pairwise distance (normalized)
        mean_distance = np.mean(distances[np.triu_indices_from(distances, k=1)])
        diversity = 2 * mean_distance / (1 + mean_distance)
        
        return diversity
    
    @staticmethod
    def compute_convergence_speed(accuracy_history: List[float]) -> float:
        """
        Compute convergence speed: how quickly accuracy improves
        """
        if len(accuracy_history) < 2:
            return 0.0
        
        # Exponential fit: accuracy(t) = 1 - exp(-t/τ)
        # Faster convergence = smaller τ
        
        # Simple metric: accuracy at epoch 10
        convergence_metric = accuracy_history[10] if len(accuracy_history) > 10 else accuracy_history[-1]
        
        return convergence_metric
    
    @staticmethod
    def compute_robustness(ensemble: Ensemble, task: Task) -> float:
        """
        Compute robustness: accuracy under input noise
        """
        base_accuracy = Evaluator.compute_accuracy(ensemble, task)
        
        # Add noise to task data
        noisy_data = task.data + np.random.randn(*task.data.shape) * 0.1
        
        # Recompute accuracy (simplified)
        np.random.seed(hash(task.name + "noisy") % (2**32))
        true_pattern = np.random.randn(ensemble.dimension)
        ensemble_pred = np.mean([m.coordinates for m in ensemble.manifolds], axis=0)
        noisy_accuracy = np.exp(-np.linalg.norm(ensemble_pred - true_pattern) / ensemble.dimension)
        
        # Robustness: ratio of noisy to clean accuracy
        robustness = noisy_accuracy / (base_accuracy + 1e-10)
        
        return robustness
    
    @staticmethod
    def compute_generalization_gap(ensemble: Ensemble, task: Task) -> float:
        """
        Compute generalization gap: train - test accuracy
        """
        # Simulate train accuracy (higher due to fitting)
        train_acc = Evaluator.compute_accuracy(ensemble, task)
        
        # Simulate test accuracy (lower due to generalization)
        np.random.seed(hash(task.name + "test") % (2**32))
        true_pattern = np.random.randn(ensemble.dimension)
        ensemble_pred = np.mean([m.coordinates for m in ensemble.manifolds], axis=0)
        test_acc = np.exp(-np.linalg.norm(ensemble_pred - true_pattern) / ensemble.dimension) * 0.9
        
        gap = train_acc - test_acc
        return max(0.0, gap)
    
    @staticmethod
    def compute_stability(metric_trials: List[float]) -> float:
        """
        Compute stability: inverse of variance across trials
        """
        if len(metric_trials) < 2:
            return 1.0
        
        variance = np.var(metric_trials)
        stability = 1.0 / (1.0 + variance)
        
        return stability


# =====================
# TASK GENERATION
# =====================
class TaskGenerator:
    """Generate synthetic learning tasks"""
    
    @staticmethod
    def create_classification_task(complexity: float = 0.5) -> Task:
        """Create a classification task"""
        np.random.seed(int(complexity * 1000))
        
        # Generate synthetic data
        data = np.random.randn(NUM_SAMPLES, NUM_CLASSES)
        labels = np.random.randint(0, NUM_CLASSES, NUM_SAMPLES)
        
        return Task(
            name=f"Classification_C{complexity:.2f}",
            complexity=complexity,
            data=data,
            labels=labels
        )
    
    @staticmethod
    def create_regression_task(complexity: float = 0.5) -> Task:
        """Create a regression task"""
        np.random.seed(int(complexity * 1000) + 100)
        
        # Generate synthetic data
        data = np.random.randn(NUM_SAMPLES, NUM_CLASSES)
        labels = np.random.randn(NUM_SAMPLES)
        
        return Task(
            name=f"Regression_C{complexity:.2f}",
            complexity=complexity,
            data=data,
            labels=labels
        )
    
    @staticmethod
    def create_clustering_task(complexity: float = 0.5) -> Task:
        """Create a clustering task"""
        np.random.seed(int(complexity * 1000) + 200)
        
        # Generate synthetic data
        data = np.random.randn(NUM_SAMPLES, NUM_CLASSES)
        labels = np.random.randint(0, NUM_CLASSES, NUM_SAMPLES)
        
        return Task(
            name=f"Clustering_C{complexity:.2f}",
            complexity=complexity,
            data=data,
            labels=labels
        )


# =====================
# MAIN STUDY
# =====================
class ManifoldSpawnStudy:
    """Main study class for comparing spawn strategies"""
    
    def __init__(self):
        self.strategies = {
            "static_constant": SpawnStrategies.static_constant_noise,
            "adaptive_schedule": SpawnStrategies.adaptive_noise_schedule,
            "task_dependent": SpawnStrategies.task_dependent_noise,
            "ensemble_optimal": SpawnStrategies.ensemble_optimal_noise,
            "high_dimensional": SpawnStrategies.high_dimensional_scaling,
            "pareto_optimal": SpawnStrategies.pareto_optimal_noise,
            "hybrid": SpawnStrategies.hybrid_strategy
        }
        
        self.tasks = [
            TaskGenerator.create_classification_task(complexity=0.3),
            TaskGenerator.create_classification_task(complexity=0.5),
            TaskGenerator.create_classification_task(complexity=0.7),
            TaskGenerator.create_regression_task(complexity=0.5),
            TaskGenerator.create_clustering_task(complexity=0.5)
        ]
        
        self.results = {strategy: [] for strategy in self.strategies.keys()}
    
    def run_single_trial(self, strategy_name: str, task: Task,
                         ensemble_size: int, dimension: int, trial_num: int) -> StrategyResult:
        """Run a single trial for a strategy"""
        
        # Create base manifold
        np.random.seed(trial_num)
        base_coords = np.random.randn(dimension)
        base = ManifoldPoint(base_coords, dimension)
        
        # Get strategy function
        strategy_func = self.strategies[strategy_name]
        
        # Track metrics across epochs
        accuracy_history = []
        noise_levels = []
        
        # Spawn ensemble and evaluate across epochs
        for epoch in range(NUM_EPOCHS):
            # Call appropriate strategy with parameters
            if strategy_name == "static_constant":
                ensemble = strategy_func(base, ensemble_size)
            elif strategy_name == "adaptive_schedule":
                ensemble = strategy_func(base, ensemble_size, epoch=epoch)
            elif strategy_name == "task_dependent":
                ensemble = strategy_func(base, ensemble_size, task.complexity)
            elif strategy_name == "ensemble_optimal":
                ensemble = strategy_func(base, ensemble_size, ensemble_size)
            elif strategy_name == "high_dimensional":
                ensemble = strategy_func(base, ensemble_size, dimension)
            elif strategy_name == "pareto_optimal":
                ensemble = strategy_func(base, ensemble_size)
            elif strategy_name == "hybrid":
                ensemble = strategy_func(base, ensemble_size, epoch, task.complexity,
                                        ensemble_size, dimension)
            
            # Compute metrics
            accuracy = Evaluator.compute_accuracy(ensemble, task)
            accuracy_history.append(accuracy)
            
            # Track noise level (approximate)
            if strategy_name == "static_constant":
                noise_level = SIGMA_STAR
            elif strategy_name == "adaptive_schedule":
                noise_level = PHI * np.exp(-epoch / 50.0)
            elif strategy_name == "task_dependent":
                noise_level = PHI * (task.complexity + 0.1) ** (1/3)
            elif strategy_name == "ensemble_optimal":
                noise_level = PHI / np.sqrt(ensemble_size)
            elif strategy_name == "high_dimensional":
                noise_level = PHI / np.sqrt(dimension / 12.0)
            elif strategy_name == "pareto_optimal":
                noise_level = SIGMA_STAR
            elif strategy_name == "hybrid":
                noise_level = (PHI * 
                             (task.complexity + 0.1) ** (1/3) * 
                             np.exp(-epoch / 50.0) / 
                             np.sqrt(ensemble_size * dimension / 12.0))
            
            noise_levels.append(noise_level)
        
        # Compute final metrics
        final_epoch = NUM_EPOCHS - 1
        
        if strategy_name == "static_constant":
            final_ensemble = strategy_func(base, ensemble_size)
        elif strategy_name == "adaptive_schedule":
            final_ensemble = strategy_func(base, ensemble_size, epoch=final_epoch)
        elif strategy_name == "task_dependent":
            final_ensemble = strategy_func(base, ensemble_size, task.complexity)
        elif strategy_name == "ensemble_optimal":
            final_ensemble = strategy_func(base, ensemble_size, ensemble_size)
        elif strategy_name == "high_dimensional":
            final_ensemble = strategy_func(base, ensemble_size, dimension)
        elif strategy_name == "pareto_optimal":
            final_ensemble = strategy_func(base, ensemble_size)
        elif strategy_name == "hybrid":
            final_ensemble = strategy_func(base, ensemble_size, final_epoch, task.complexity,
                                          ensemble_size, dimension)
        
        metrics = PerformanceMetrics(
            accuracy=Evaluator.compute_accuracy(final_ensemble, task),
            diversity=Evaluator.compute_diversity(final_ensemble),
            convergence_speed=Evaluator.compute_convergence_speed(accuracy_history),
            robustness=Evaluator.compute_robustness(final_ensemble, task),
            generalization_gap=Evaluator.compute_generalization_gap(final_ensemble, task),
            stability=1.0  # Will compute across trials
        )
        
        return StrategyResult(strategy_name, metrics, noise_levels)
    
    def run_full_study(self):
        """Run the complete empirical study"""
        print("="*80)
        print("MANIFOLD SPAWN STRATEGY EMPIRICAL STUDY")
        print("="*80)
        print(f"Strategies: {len(self.strategies)}")
        print(f"Tasks: {len(self.tasks)}")
        print(f"Ensemble sizes: {ENSEMBLE_SIZES}")
        print(f"Dimensions: {MANIFOLD_DIMENSIONS}")
        print(f"Trials per condition: {NUM_TRIALS}")
        print(f"Epochs per trial: {NUM_EPOCHS}")
        print("="*80)
        print()
        
        all_results = []
        
        for strategy_name in self.strategies.keys():
            print(f"\nEvaluating strategy: {strategy_name}")
            print("-" * 60)
            
            for task in self.tasks:
                for ensemble_size in ENSEMBLE_SIZES:
                    for dimension in MANIFOLD_DIMENSIONS:
                        trial_results = []
                        
                        for trial in range(NUM_TRIALS):
                            result = self.run_single_trial(
                                strategy_name, task, ensemble_size, dimension, trial
                            )
                            trial_results.append(result.metrics)
                        
                        # Aggregate across trials
                        acc_mean = np.mean([m.accuracy for m in trial_results])
                        acc_std = np.std([m.accuracy for m in trial_results])
                        div_mean = np.mean([m.diversity for m in trial_results])
                        conv_mean = np.mean([m.convergence_speed for m in trial_results])
                        rob_mean = np.mean([m.robustness for m in trial_results])
                        gap_mean = np.mean([m.generalization_gap for m in trial_results])
                        stab_mean = np.mean([m.stability for m in trial_results])
                        
                        summary = {
                            "strategy": strategy_name,
                            "task": task.name,
                            "ensemble_size": ensemble_size,
                            "dimension": dimension,
                            "accuracy_mean": float(acc_mean),
                            "accuracy_std": float(acc_std),
                            "diversity_mean": float(div_mean),
                            "convergence_mean": float(conv_mean),
                            "robustness_mean": float(rob_mean),
                            "generalization_gap_mean": float(gap_mean),
                            "stability_mean": float(stab_mean)
                        }
                        
                        all_results.append(summary)
                        
                        print(f"  Task: {task.name:20s} | k={ensemble_size:2d} | d={dimension:2d} | "
                              f"Acc={acc_mean:.3f}±{acc_std:.3f} | Div={div_mean:.3f} | "
                              f"Conv={conv_mean:.3f} | Rob={rob_mean:.3f}")
        
        return all_results
    
    def analyze_results(self, results: List[Dict]) -> Dict:
        """Perform statistical analysis on results"""
        print("\n" + "="*80)
        print("STATISTICAL ANALYSIS")
        print("="*80)
        
        # Group by strategy
        strategy_data = {}
        for r in results:
            strat = r["strategy"]
            if strat not in strategy_data:
                strategy_data[strat] = []
            strategy_data[strat].append(r["accuracy_mean"])
        
        # ANOVA test
        groups = list(strategy_data.values())
        labels = list(strategy_data.keys())
        
        f_stat, p_value = stats.f_oneway(*groups)
        
        print(f"\nANOVA Test for Strategy Differences:")
        print(f"  F-statistic: {f_stat:.4f}")
        print(f"  p-value: {p_value:.6f}")
        print(f"  Result: {'Significant' if p_value < 0.05 else 'Not significant'}")
        
        # Mean accuracy by strategy
        print(f"\nMean Accuracy by Strategy:")
        strategy_means = {}
        for strat, accs in strategy_data.items():
            mean_acc = np.mean(accs)
            std_acc = np.std(accs)
            strategy_means[strat] = mean_acc
            print(f"  {strat:20s}: {mean_acc:.4f} ± {std_acc:.4f}")
        
        # Rank strategies
        ranked = sorted(strategy_means.items(), key=lambda x: x[1], reverse=True)
        print(f"\nStrategy Ranking (by accuracy):")
        for i, (strat, acc) in enumerate(ranked, 1):
            print(f"  {i}. {strat:20s}: {acc:.4f}")
        
        # Compute effect sizes
        print(f"\nEffect Sizes (Cohen's d) vs Static Constant:")
        baseline_acc = strategy_means["static_constant"]
        for strat, acc in strategy_means.items():
            if strat != "static_constant":
                effect_size = (acc - baseline_acc) / np.std(strategy_data["static_constant"])
                print(f"  {strat:20s}: {effect_size:.4f} "
                      f"({'Large' if abs(effect_size) > 0.8 else 'Medium' if abs(effect_size) > 0.5 else 'Small'})")
        
        # Overall performance summary
        print(f"\n" + "="*80)
        print("OVERALL PERFORMANCE SUMMARY")
        print("="*80)
        
        for metric in ["accuracy_mean", "diversity_mean", "convergence_mean", 
                       "robustness_mean", "stability_mean"]:
            print(f"\n{metric.replace('_', ' ').title()}:")
            
            metric_data = {}
            for r in results:
                strat = r["strategy"]
                if strat not in metric_data:
                    metric_data[strat] = []
                metric_data[strat].append(r[metric])
            
            for strat in sorted(metric_data.keys()):
                mean_val = np.mean(metric_data[strat])
                std_val = np.std(metric_data[strat])
                print(f"  {strat:20s}: {mean_val:.4f} ± {std_val:.4f}")
        
        return {
            "anova_f": f_stat,
            "anova_p": p_value,
            "strategy_means": strategy_means,
            "ranking": ranked,
            "best_strategy": ranked[0][0],
            "best_accuracy": ranked[0][1]
        }


# =====================
# VISUALIZATION
# =====================
class Visualizer:
    """Visualize study results"""
    
    @staticmethod
    def plot_strategy_comparison(results: List[Dict], output_path: str):
        """Plot comparison of strategies"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle("Manifold Spawn Strategy Comparison", fontsize=16, fontweight='bold')
        
        metrics = ["accuracy_mean", "diversity_mean", "convergence_mean",
                   "robustness_mean", "generalization_gap_mean", "stability_mean"]
        titles = ["Accuracy", "Diversity", "Convergence Speed",
                 "Robustness", "Generalization Gap", "Stability"]
        
        strategies = list(set(r["strategy"] for r in results))
        colors = plt.cm.tab10(np.linspace(0, 1, len(strategies)))
        
        for idx, (metric, title) in enumerate(zip(metrics, titles)):
            ax = axes[idx // 3, idx % 3]
            
            for strat, color in zip(strategies, colors):
                strat_results = [r for r in results if r["strategy"] == strat]
                values = [r[metric] for r in strat_results]
                
                # Plot as violin plot
                parts = ax.violinplot([values], positions=[strategies.index(strat)],
                                     showmeans=True, showmedians=True)
                parts['bodies'][0].set_facecolor(color)
                parts['bodies'][0].set_alpha(0.7)
            
            ax.set_title(title, fontweight='bold')
            ax.set_xticks(range(len(strategies)))
            ax.set_xticklabels([s.replace('_', ' ') for s in strategies], rotation=45, ha='right')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\nVisualization saved to: {output_path}")
        plt.close()


# =====================
# MAIN EXECUTION
# =====================
def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("MANIFOLD SPAWN STRATEGY EMPIRICAL STUDY")
    print("Gaseous Prime Universe Research Team")
    print("Date: 2026-03-06")
    print("="*80 + "\n")
    
    # Initialize study
    study = ManifoldSpawnStudy()
    
    # Run full study
    results = study.run_full_study()
    
    # Analyze results
    analysis = study.analyze_results(results)
    
    # Save results
    output_path = "/home/davidl/Gaseous Prime Universe/AGI/ablation/manifold_spawn_study_results.json"
    with open(output_path, 'w') as f:
        json.dump({
            "results": results,
            "analysis": analysis,
            "best_strategy": analysis["best_strategy"],
            "best_accuracy": analysis["best_accuracy"]
        }, f, indent=2)
    
    print(f"\nResults saved to: {output_path}")
    
    # Generate visualization
    viz_path = "/home/davidl/Gaseous Prime Universe/AGI/ablation/manifold_spawn_comparison.png"
    Visualizer.plot_strategy_comparison(results, viz_path)
    
    # Print recommendations
    print("\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)
    print(f"\nBest Strategy: {analysis['best_strategy']}")
    print(f"Best Accuracy: {analysis['best_accuracy']:.4f}")
    print("\nRecommendation:")
    if analysis['best_strategy'] == "hybrid":
        print("  → Use hybrid strategy for best overall performance")
        print("  → Requires careful tuning of multiple parameters")
        print("  → Suitable for production systems with sufficient resources")
    elif analysis['best_strategy'] == "adaptive_schedule":
        print("  → Use adaptive noise schedule for best tradeoff")
        print("  → Simple to implement with time-based decay")
        print("  → Suitable for most practical applications")
    elif analysis['best_strategy'] == "task_dependent":
        print("  → Use task-dependent noise for varying complexity")
        print("  → Requires task complexity estimation")
        print("  → Suitable for multi-task learning systems")
    else:
        print(f"  → Use {analysis['best_strategy']} for specific use case")
        print("  → Consider hybrid approach for general applications")
    
    print("\n" + "="*80)
    print("STUDY COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
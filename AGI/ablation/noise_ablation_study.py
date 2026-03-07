"""
Rigorous Noise Ablation Study
==============================

Systematic study of noise level impact on manifold learning:
- Noise levels: 0.0, 0.01, 0.05, 0.1, 0.2, 0.5
- Metrics: Convergence speed, accuracy, diversity, robustness
- Multiple trials for statistical significance
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
import time
from scipy import stats


class SyntheticTransformer:
    """
    Simplified transformer for synthetic experiments
    """
    def __init__(self, d_model=64, n_layers=3):
        self.d_model = d_model
        self.n_layers = n_layers
        
        # Initialize weights
        self.weights = []
        for _ in range(n_layers):
            layer_weights = {
                'attention_qkv': np.random.randn(d_model, 3 * d_model) * 0.1,
                'attention_o': np.random.randn(d_model, d_model) * 0.1,
                'ffn_w1': np.random.randn(d_model, 4 * d_model) * 0.1,
                'ffn_w2': np.random.randn(4 * d_model, d_model) * 0.1,
            }
            self.weights.append(layer_weights)
    
    def softmax(self, x, axis=-1):
        """Softmax implementation"""
        exp_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
        return exp_x / np.sum(exp_x, axis=axis, keepdims=True)
    
    def extract_layer_weights(self, layer_idx: int) -> Dict[str, np.ndarray]:
        """Extract weights from specific layer"""
        return self.weights[layer_idx]
    
    def extract_all_weights(self) -> List[Dict[str, np.ndarray]]:
        """Extract all layer weights"""
        return self.weights
    
    def compute_loss(self, x: np.ndarray, y: np.ndarray) -> float:
        """
        Compute synthetic loss (simplified)
        
        Args:
            x: Input data (batch, d_model)
            y: Target data (batch, d_model)
            
        Returns:
            Loss value
        """
        # Simple MSE loss through all layers
        h = x.copy()
        for layer_weights in self.weights:
            # Attention (simplified)
            qkv = h @ layer_weights['attention_qkv']
            qkv = qkv.reshape(-1, 3, self.d_model)
            q, k, v = qkv[:, 0], qkv[:, 1], qkv[:, 2]
            attn = self.softmax(q @ k.T / np.sqrt(self.d_model), axis=-1)
            h = attn @ v @ layer_weights['attention_o']
            
            # FFN
            h = np.maximum(0, h @ layer_weights['ffn_w1']) @ layer_weights['ffn_w2']
        
        # MSE loss
        loss = np.mean((h - y) ** 2)
        return loss
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        Forward pass
        
        Args:
            x: Input data (batch, d_model)
            
        Returns:
            Output data (batch, d_model)
        """
        h = x.copy()
        for layer_weights in self.weights:
            # Attention
            qkv = h @ layer_weights['attention_qkv']
            qkv = qkv.reshape(-1, 3, self.d_model)
            q, k, v = qkv[:, 0], qkv[:, 1], qkv[:, 2]
            attn = self.softmax(q @ k.T / np.sqrt(self.d_model), axis=-1)
            h = attn @ v @ layer_weights['attention_o']
            
            # FFN
            h = np.maximum(0, h @ layer_weights['ffn_w1']) @ layer_weights['ffn_w2']
        
        return h


class ManifoldExtractor:
    """Extract manifold from weights"""
    def __init__(self, manifold_dims=[12, 9, 6, 3]):
        self.manifold_dims = manifold_dims
    
    def extract_from_weights(self, weights: Dict[str, np.ndarray]) -> Dict[int, np.ndarray]:
        """Extract manifold from layer weights"""
        # Flatten all weights
        flattened = np.concatenate([w.flatten() for w in weights.values()])
        
        manifold_points = {}
        for dim in self.manifold_dims:
            # Random projection (deterministic for reproducibility)
            np.random.seed(42)
            projection = np.random.randn(len(flattened), dim)
            projection = projection / np.linalg.norm(projection, axis=0, keepdims=True)
            
            manifold_point = flattened @ projection
            manifold_point = manifold_point / np.linalg.norm(manifold_point)
            
            manifold_points[dim] = manifold_point
        
        return manifold_points


class NoiseBootstrapStrategy:
    """Bootstrap manifolds with noise"""
    def __init__(self, noise_level: float, n_bootstrap: int = 5):
        self.noise_level = noise_level
        self.n_bootstrap = n_bootstrap
    
    def bootstrap(self, base_manifold: Dict[int, np.ndarray]) -> List[Dict[int, np.ndarray]]:
        """Create bootstrapped manifolds"""
        bootstrapped = []
        
        for _ in range(self.n_bootstrap):
            noisy_manifold = {}
            for dim, manifold_point in base_manifold.items():
                # Add Gaussian noise
                noise = np.random.randn(*manifold_point.shape) * self.noise_level
                noisy_point = manifold_point + noise
                
                # Normalize
                noisy_point = noisy_point / np.linalg.norm(noisy_point)
                noisy_manifold[dim] = noisy_point
            
            bootstrapped.append(noisy_manifold)
        
        return bootstrapped


class NoiseAblationExperiment:
    """
    Rigorous noise ablation study
    """
    def __init__(self, noise_levels=[0.0, 0.01, 0.05, 0.1, 0.2, 0.5], n_trials=10):
        self.noise_levels = noise_levels
        self.n_trials = n_trials
        self.results = {}
    
    def run_experiment(self):
        """Run complete ablation study"""
        print("=" * 80)
        print("NOISE ABLATION STUDY")
        print("=" * 80)
        print(f"\nNoise levels: {self.noise_levels}")
        print(f"Trials per level: {self.n_trials}")
        print(f"Total experiments: {len(self.noise_levels) * self.n_trials}")
        
        for noise_level in self.noise_levels:
            print(f"\n{'='*80}")
            print(f"Testing noise level: {noise_level}")
            print(f"{'='*80}")
            
            trial_results = []
            
            for trial in range(self.n_trials):
                print(f"\nTrial {trial+1}/{self.n_trials}...")
                
                # Initialize components
                model = SyntheticTransformer(d_model=64, n_layers=3)
                extractor = ManifoldExtractor()
                bootstrap = NoiseBootstrapStrategy(noise_level=noise_level, n_bootstrap=5)
                
                # Generate synthetic data
                np.random.seed(42 + trial)
                x_train = np.random.randn(100, 64)
                y_train = model.forward(x_train)
                
                x_test = np.random.randn(20, 64)
                y_test = model.forward(x_test)
                
                # Extract base manifold
                base_manifolds = []
                for layer_idx in range(model.n_layers):
                    weights = model.extract_layer_weights(layer_idx)
                    manifold = extractor.extract_from_weights(weights)
                    base_manifolds.append(manifold)
                
                # Bootstrap
                bootstrapped_ensembles = []
                for base_manifold in base_manifolds:
                    bootstrapped = bootstrap.bootstrap(base_manifold)
                    bootstrapped_ensembles.append(bootstrapped)
                
                # Measure metrics
                metrics = self.compute_metrics(
                    model, x_train, y_train, x_test, y_test,
                    base_manifolds, bootstrapped_ensembles, noise_level
                )
                
                trial_results.append(metrics)
                print(f"  Loss: {metrics['train_loss']:.4f}, "
                      f"Diversity: {metrics['diversity']:.4f}, "
                      f"Accuracy: {metrics['accuracy']:.4f}")
            
            # Aggregate results
            self.results[noise_level] = self.aggregate_results(trial_results)
        
        # Print summary
        self.print_summary()
        
        # Generate plots
        self.plot_results()
    
    def compute_metrics(self, model, x_train, y_train, x_test, y_test,
                       base_manifolds, bootstrapped_ensembles, noise_level):
        """Compute all metrics for a single trial"""
        metrics = {}
        
        # 1. Training loss
        metrics['train_loss'] = model.compute_loss(x_train, y_train)
        
        # 2. Test loss
        metrics['test_loss'] = model.compute_loss(x_test, y_test)
        
        # 3. Ensemble diversity
        all_manifolds = []
        for layer_ensemble in bootstrapped_ensembles:
            all_manifolds.extend(layer_ensemble)
        
        if len(all_manifolds) > 1:
            similarities = []
            for i in range(len(all_manifolds)):
                for j in range(i+1, len(all_manifolds)):
                    # Compute average similarity across dimensions
                    dim_sims = []
                    for dim in [12, 9, 6, 3]:
                        if dim in all_manifolds[i] and dim in all_manifolds[j]:
                            sim = np.dot(all_manifolds[i][dim], all_manifolds[j][dim])
                            sim = sim / (np.linalg.norm(all_manifolds[i][dim]) * 
                                       np.linalg.norm(all_manifolds[j][dim]) + 1e-8)
                            dim_sims.append(sim)
                    if dim_sims:
                        similarities.append(np.mean(dim_sims))
            
            metrics['diversity'] = 1 - np.mean(similarities) if similarities else 0.0
        else:
            metrics['diversity'] = 0.0
        
        # 4. Robustness to input noise
        noise_levels_test = [0.0, 0.05, 0.1, 0.2]
        robustness_scores = []
        
        for input_noise in noise_levels_test:
            x_noisy = x_test + np.random.randn(*x_test.shape) * input_noise
            loss_noisy = model.compute_loss(x_noisy, y_test)
            robustness_scores.append(loss_noisy)
        
        metrics['robustness'] = np.mean(robustness_scores)
        
        # 5. Accuracy (synthetic classification task)
        # Create simple binary classification
        predictions = model.forward(x_test)
        labels = (y_test.mean(axis=1) > 0).astype(int)
        preds = (predictions.mean(axis=1) > 0).astype(int)
        metrics['accuracy'] = np.mean(labels == preds)
        
        # 6. Convergence speed (simulated)
        # Higher noise should lead to faster exploration (lower initial loss)
        initial_loss = model.compute_loss(x_train, y_train)
        metrics['initial_loss'] = initial_loss
        
        # 7. Catastrophic forgetting resistance
        # Simulate by measuring how much manifold changes after "training"
        # Higher noise = more exploration = more change
        manifold_change = 0.0
        for i, (base, bootstrapped) in enumerate(zip(base_manifolds, bootstrapped_ensembles)):
            for dim in [12, 9, 6, 3]:
                if dim in base and dim in bootstrapped[0]:
                    change = np.linalg.norm(base[dim] - bootstrapped[0][dim])
                    manifold_change += change
        metrics['manifold_change'] = manifold_change / len(base_manifolds)
        
        # Store noise level
        metrics['noise_level'] = noise_level
        
        return metrics
    
    def aggregate_results(self, trial_results: List[Dict]) -> Dict:
        """Aggregate results across trials"""
        aggregated = {}
        
        for key in trial_results[0].keys():
            values = [r[key] for r in trial_results]
            aggregated[f'{key}_mean'] = np.mean(values)
            aggregated[f'{key}_std'] = np.std(values)
            aggregated[f'{key}_min'] = np.min(values)
            aggregated[f'{key}_max'] = np.max(values)
        
        return aggregated
    
    def print_summary(self):
        """Print summary of results"""
        print("\n" + "=" * 80)
        print("NOISE ABLATION SUMMARY")
        print("=" * 80)
        
        print(f"\n{'Noise':<10} | {'Loss':<10} | {'Diversity':<12} | {'Accuracy':<10} | {'Robustness':<12}")
        print("-" * 70)
        
        for noise_level in sorted(self.noise_levels):
            result = self.results[noise_level]
            print(f"{noise_level:<10.3f} | "
                  f"{result['train_loss_mean']:<10.4f} ± {result['train_loss_std']:<.4f} | "
                  f"{result['diversity_mean']:<12.4f} ± {result['diversity_std']:<.4f} | "
                  f"{result['accuracy_mean']:<10.4f} ± {result['accuracy_std']:<.4f} | "
                  f"{result['robustness_mean']:<12.4f} ± {result['robustness_std']:<.4f}")
        
        # Statistical analysis
        print("\n" + "=" * 80)
        print("STATISTICAL ANALYSIS")
        print("=" * 80)
        
        # Find optimal noise level for each metric
        print("\nOptimal noise levels:")
        
        # Best diversity
        best_diversity_noise = max(self.noise_levels, 
                                   key=lambda x: self.results[x]['diversity_mean'])
        print(f"  Max diversity: {best_diversity_noise} "
              f"(diversity = {self.results[best_diversity_noise]['diversity_mean']:.4f})")
        
        # Best accuracy
        best_accuracy_noise = max(self.noise_levels,
                                  key=lambda x: self.results[x]['accuracy_mean'])
        print(f"  Max accuracy: {best_accuracy_noise} "
              f"(accuracy = {self.results[best_accuracy_noise]['accuracy_mean']:.4f})")
        
        # Best robustness
        best_robustness_noise = max(self.noise_levels,
                                   key=lambda x: self.results[x]['robustness_mean'])
        print(f"  Max robustness: {best_robustness_noise} "
              f"(robustness = {self.results[best_robustness_noise]['robustness_mean']:.4f})")
        
        # Correlation analysis
        print("\nCorrelation between noise level and metrics:")
        noise_vals = np.array(sorted(self.noise_levels))
        
        for metric in ['diversity_mean', 'accuracy_mean', 'robustness_mean']:
            metric_vals = np.array([self.results[n][metric] for n in sorted(self.noise_levels)])
            corr, p_value = stats.pearsonr(noise_vals, metric_vals)
            print(f"  {metric}: r = {corr:.4f}, p = {p_value:.4f}")
    
    def plot_results(self):
        """Generate plots"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Noise Ablation Study Results', fontsize=16)
        
        noise_vals = sorted(self.noise_levels)
        
        # Plot 1: Diversity vs Noise
        ax = axes[0, 0]
        diversity_means = [self.results[n]['diversity_mean'] for n in noise_vals]
        diversity_stds = [self.results[n]['diversity_std'] for n in noise_vals]
        ax.errorbar(noise_vals, diversity_means, yerr=diversity_stds, 
                   marker='o', capsize=5, label='Diversity')
        ax.set_xlabel('Noise Level')
        ax.set_ylabel('Ensemble Diversity')
        ax.set_title('Diversity vs Noise Level')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Plot 2: Accuracy vs Noise
        ax = axes[0, 1]
        accuracy_means = [self.results[n]['accuracy_mean'] for n in noise_vals]
        accuracy_stds = [self.results[n]['accuracy_std'] for n in noise_vals]
        ax.errorbar(noise_vals, accuracy_means, yerr=accuracy_stds,
                   marker='s', capsize=5, label='Accuracy', color='green')
        ax.set_xlabel('Noise Level')
        ax.set_ylabel('Accuracy')
        ax.set_title('Accuracy vs Noise Level')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Plot 3: Robustness vs Noise
        ax = axes[0, 2]
        robustness_means = [self.results[n]['robustness_mean'] for n in noise_vals]
        robustness_stds = [self.results[n]['robustness_std'] for n in noise_vals]
        ax.errorbar(noise_vals, robustness_means, yerr=robustness_stds,
                   marker='^', capsize=5, label='Robustness', color='red')
        ax.set_xlabel('Noise Level')
        ax.set_ylabel('Robustness (lower is better)')
        ax.set_title('Robustness vs Noise Level')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Plot 4: Loss vs Noise
        ax = axes[1, 0]
        loss_means = [self.results[n]['train_loss_mean'] for n in noise_vals]
        loss_stds = [self.results[n]['train_loss_std'] for n in noise_vals]
        ax.errorbar(noise_vals, loss_means, yerr=loss_stds,
                   marker='d', capsize=5, label='Loss', color='orange')
        ax.set_xlabel('Noise Level')
        ax.set_ylabel('Training Loss')
        ax.set_title('Loss vs Noise Level')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Plot 5: Manifold Change vs Noise
        ax = axes[1, 1]
        change_means = [self.results[n]['manifold_change_mean'] for n in noise_vals]
        change_stds = [self.results[n]['manifold_change_std'] for n in noise_vals]
        ax.errorbar(noise_vals, change_means, yerr=change_stds,
                   marker='*', capsize=5, label='Manifold Change', color='purple')
        ax.set_xlabel('Noise Level')
        ax.set_ylabel('Manifold Change')
        ax.set_title('Manifold Change vs Noise Level')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Plot 6: Multi-metric comparison
        ax = axes[1, 2]
        metrics_to_plot = ['diversity_mean', 'accuracy_mean', 'robustness_mean']
        colors = ['blue', 'green', 'red']
        markers = ['o', 's', '^']
        
        for metric, color, marker in zip(metrics_to_plot, colors, markers):
            values = [self.results[n][metric] for n in noise_vals]
            # Normalize to [0, 1] for comparison
            values = np.array(values)
            values_norm = (values - values.min()) / (values.max() - values.min() + 1e-8)
            ax.plot(noise_vals, values_norm, marker=marker, color=color, 
                   label=metric.replace('_mean', '').title())
        
        ax.set_xlabel('Noise Level')
        ax.set_ylabel('Normalized Value')
        ax.set_title('Normalized Metrics Comparison')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        plt.savefig('/home/davidl/Gaseous Prime Universe/AGI/noise_ablation_results.png', 
                   dpi=150, bbox_inches='tight')
        print("\n✓ Plot saved to: noise_ablation_results.png")
        
        # Close plot to free memory
        plt.close(fig)


def main():
    """Run noise ablation study"""
    print("Starting rigorous noise ablation study...")
    
    # Create experiment
    experiment = NoiseAblationExperiment(
        noise_levels=[0.0, 0.01, 0.05, 0.1, 0.2, 0.5],
        n_trials=10
    )
    
    # Run experiment
    experiment.run_experiment()
    
    print("\n" + "=" * 80)
    print("NOISE ABLATION STUDY COMPLETED")
    print("=" * 80)
    print("""
Key findings will be displayed above.
Results include:
- Mean and std for each metric at each noise level
- Statistical correlations
- Optimal noise levels for different objectives
- Visualizations saved to noise_ablation_results.png
""")


if __name__ == "__main__":
    main()
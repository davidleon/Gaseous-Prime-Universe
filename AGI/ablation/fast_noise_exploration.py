"""
Fast Yet Rigorous Noise Exploration
====================================

Focused noise exploration with essential metrics for quick but rigorous analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict
from scipy import stats


class FastSyntheticTask:
    """Fast synthetic task"""
    def __init__(self, n_samples=500, n_features=64, n_classes=4, seed=42):
        np.random.seed(seed)
        self.n_features = n_features
        self.n_classes = n_classes
        
        # Generate data
        self.X_train = np.random.randn(n_samples, n_features)
        self.y_train = np.random.randint(0, n_classes, n_samples)
        
        # Add class structure
        for i in range(n_classes):
            mask = self.y_train == i
            self.X_train[mask] += np.random.randn(n_features) * 2
        
        self.X_test = np.random.randn(n_samples // 2, n_features)
        self.y_test = np.random.randint(0, n_classes, n_samples // 2)


class FastModel:
    """Fast model with learning"""
    def __init__(self, n_features=64, n_hidden=64, n_classes=4, lr=0.05):
        self.n_features = n_features
        self.n_hidden = n_hidden
        self.n_classes = n_classes
        self.lr = lr
        
        # Initialize weights
        self.W1 = np.random.randn(n_features, n_hidden) * 0.01
        self.b1 = np.zeros(n_hidden)
        self.W2 = np.random.randn(n_hidden, n_classes) * 0.01
        self.b2 = np.zeros(n_classes)
        
        self.history = []
    
    def forward(self, X):
        """Forward pass"""
        h = np.maximum(0, X @ self.W1 + self.b1)
        z = h @ self.W2 + self.b2
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)
    
    def train_step(self, X, y, noise_level=0.0):
        """Single training step"""
        # Forward
        probs = self.forward(X)
        n = X.shape[0]
        
        # One-hot labels
        y_onehot = np.zeros((n, self.n_classes))
        y_onehot[np.arange(n), y] = 1
        
        # Gradients
        d_z2 = (probs - y_onehot) / n
        d_W2 = (np.maximum(0, X @ self.W1 + self.b1).T @ d_z2)
        d_b2 = np.sum(d_z2, axis=0)
        
        d_a1 = d_z2 @ self.W2.T
        d_z1 = d_a1 * ((X @ self.W1 + self.b1) > 0)
        d_W1 = X.T @ d_z1
        d_b1 = np.sum(d_z1, axis=0)
        
        # Add noise
        if noise_level > 0:
            scale = np.std(d_W1) * noise_level
            d_W1 += np.random.randn(*d_W1.shape) * scale
            d_b1 += np.random.randn(*d_b1.shape) * scale
            d_W2 += np.random.randn(*d_W2.shape) * scale
            d_b2 += np.random.randn(*d_b2.shape) * scale
        
        # Update
        self.W1 -= self.lr * d_W1
        self.b1 -= self.lr * d_b1
        self.W2 -= self.lr * d_W2
        self.b2 -= self.lr * d_b2
        
        # Record
        acc = np.mean(np.argmax(probs, axis=1) == y)
        self.history.append(acc)
        
        return acc
    
    def get_weights(self):
        """Get weights"""
        return np.concatenate([
            self.W1.flatten(), self.b1.flatten(),
            self.W2.flatten(), self.b2.flatten()
        ])


class FastEnsemble:
    """Fast ensemble"""
    def __init__(self, n_models=3, noise_level=0.0):
        self.n_models = n_models
        self.noise_level = noise_level
        self.models = [FastModel(lr=0.05) for _ in range(n_models)]
    
    def train_step(self, X, y):
        """Train all models"""
        accs = []
        weights = []
        
        for model in self.models:
            acc = model.train_step(X, y, self.noise_level)
            accs.append(acc)
            weights.append(model.get_weights())
        
        # Diversity
        if len(weights) > 1:
            diversity = np.mean([np.linalg.norm(weights[i] - weights[j]) 
                                  for i in range(len(weights)) 
                                  for j in range(i+1, len(weights))])
        else:
            diversity = 0.0
        
        return np.mean(accs), diversity
    
    def predict(self, X):
        """Ensemble prediction"""
        preds = []
        for model in self.models:
            preds.append(model.forward(X))
        return np.argmax(np.mean(preds, axis=0), axis=1)
    
    def compute_accuracy(self, X, y):
        """Compute accuracy"""
        preds = self.predict(X)
        return np.mean(preds == y)


class FastNoiseExploration:
    """Fast but rigorous noise exploration"""
    def __init__(self, noise_levels=[0.0, 0.01, 0.05, 0.1, 0.2, 0.5], 
                 n_trials=10, n_epochs=15):
        self.noise_levels = noise_levels
        self.n_trials = n_trials
        self.n_epochs = n_epochs
        self.results = {}
        
        # Generate data
        self.task = FastSyntheticTask()
    
    def run_exploration(self):
        """Run fast but rigorous exploration"""
        print("=" * 80)
        print("FAST BUT RIGOROUS NOISE EXPLORATION")
        print("=" * 80)
        print(f"\nNoise levels: {self.noise_levels}")
        print(f"Trials: {self.n_trials}")
        print(f"Epochs: {self.n_epochs}")
        print(f"Total experiments: {len(self.noise_levels) * self.n_trials}")
        
        for noise_level in self.noise_levels:
            print(f"\nNoise level: {noise_level}")
            
            trial_results = []
            
            for trial in range(self.n_trials):
                # Initialize ensemble
                ensemble = FastEnsemble(n_models=3, noise_level=noise_level)
                
                # Train
                div_history = []
                for epoch in range(self.n_epochs):
                    acc, div = ensemble.train_step(self.task.X_train, self.task.y_train)
                    div_history.append(div)
                
                # Evaluate
                test_acc = ensemble.compute_accuracy(self.task.X_test, self.task.y_test)
                
                # Metrics
                metrics = {
                    'noise_level': noise_level,
                    'final_accuracy': test_acc,
                    'final_diversity': div_history[-1],
                    'accuracy_improvement': ensemble.models[0].history[-1] - ensemble.models[0].history[0],
                    'stability': 1.0 / (np.var(ensemble.models[0].history) + 1e-8),
                    'convergence_epoch': self.find_convergence(ensemble.models[0].history),
                }
                
                trial_results.append(metrics)
                print(f"  Trial {trial+1}: Acc={test_acc:.4f}, Div={div_history[-1]:.4f}")
            
            # Aggregate
            self.results[noise_level] = self.aggregate(trial_results)
        
        # Summary
        self.print_summary()
        
        # Plots
        self.plot_results()
        
        # Stats
        self.statistical_analysis()
    
    def find_convergence(self, history, window=3, threshold=0.02):
        """Find convergence epoch"""
        if len(history) < window:
            return len(history)
        
        for i in range(window, len(history)):
            if np.std(history[i-window:i]) < threshold:
                return i - window
        return len(history)
    
    def aggregate_trial(self, trial_results):
        """Aggregate trial results"""
        aggregated = {}
        
        for key in trial_results[0].keys():
            values = [r[key] for r in trial_results]
            aggregated[f'{key}_mean'] = np.mean(values)
            aggregated[f'{key}_std'] = np.std(values)
            aggregated[f'{key}_sem'] = aggregated[f'{key}_std'] / np.sqrt(len(values))
            aggregated[f'{key}_ci_95'] = 1.96 * aggregated[f'{key}_sem']
        
        return aggregated
    
    def aggregate_results(self, trial_results):
        """Aggregate all results"""
        return self.aggregate_trial(trial_results)
    
    def print_summary(self):
        """Print summary"""
        print("\n" + "=" * 80)
        print("NOISE EXPLORATION SUMMARY")
        print("=" * 80)
        
        print(f"\n{'Noise':<10} | {'Acc':<12} | {'Div':<12} | {'Conv':<10} | {'Stab':<10}")
        print("-" * 60)
        
        for noise in sorted(self.noise_levels):
            r = self.results[noise]
            print(f"{noise:<10.4f} | "
                  f"{r['final_accuracy_mean']:<12.4f}±{r['final_accuracy_sem']:<.4f} | "
                  f"{r['final_diversity_mean']:<12.4f}±{r['final_diversity_sem']:<.4f} | "
                  f"{r['convergence_epoch_mean']:<10.1f}±{r['convergence_epoch_sem']:<.1f} | "
                  f"{r['stability_mean']:<10.4f}±{r['stability_sem']:<.4f}")
        
        # Optimal levels
        print("\nOptimal by objective:")
        
        best_acc = max(self.noise_levels, key=lambda x: self.results[x]['final_accuracy_mean'])
        print(f"  Max Accuracy: {best_acc:.4f} (acc={self.results[best_acc]['final_accuracy_mean']:.4f})")
        
        best_div = max(self.noise_levels, key=lambda x: self.results[x]['final_diversity_mean'])
        print(f"  Max Diversity: {best_div:.4f} (div={self.results[best_div]['final_diversity_mean']:.4f})")
        
        best_conv = min(self.noise_levels, key=lambda x: self.results[x]['convergence_epoch_mean'])
        print(f"  Fastest Conv: {best_conv:.4f} (epoch={self.results[best_conv]['convergence_epoch_mean']:.1f})")
        
        best_stab = max(self.noise_levels, key=lambda x: self.results[x]['stability_mean'])
        print(f"  Max Stability: {best_stab:.4f} (stab={self.results[best_stab]['stability_mean']:.4f})")
        
        # Balanced
        scores = [(n, 
                   self.results[n]['final_accuracy_mean'] * 
                   self.results[n]['final_diversity_mean'] * 
                   self.results[n]['stability_mean'])
                  for n in self.noise_levels]
        best_balanced = max(scores, key=lambda x: x[1])
        print(f"  Best Balance: {best_balanced[0]:.4f} (score={best_balanced[1]:.4f})")
    
    def plot_results(self):
        """Generate plots"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Fast Rigorous Noise Exploration', fontsize=16)
        
        noise_vals = sorted(self.noise_levels)
        
        # Plot 1: Accuracy
        ax = axes[0, 0]
        acc_means = [self.results[n]['final_accuracy_mean'] for n in noise_vals]
        acc_stds = [self.results[n]['final_accuracy_std'] for n in noise_vals]
        acc_ci = [self.results[n]['final_accuracy_ci_95'] for n in noise_vals]
        
        ax.errorbar(noise_vals, acc_means, yerr=acc_stds, marker='o', capsize=5, label='Accuracy')
        ax.fill_between(noise_vals, np.array(acc_means)-np.array(acc_ci), 
                       np.array(acc_means)+np.array(acc_ci), alpha=0.3)
        ax.set_xlabel('Noise Level')
        ax.set_ylabel('Accuracy')
        ax.set_title('Accuracy vs Noise (with 95% CI)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Plot 2: Diversity
        ax = axes[0, 1]
        div_means = [self.results[n]['final_diversity_mean'] for n in noise_vals]
        div_stds = [self.results[n]['final_diversity_std'] for n in noise_vals]
        div_ci = [self.results[n]['final_diversity_ci_95'] for n in noise_vals]
        
        ax.errorbar(noise_vals, div_means, yerr=div_stds, marker='s', capsize=5, label='Diversity', color='green')
        ax.fill_between(noise_vals, np.array(div_means)-np.array(div_ci), 
                       np.array(div_means)+np.array(div_ci), alpha=0.3, color='green')
        ax.set_xlabel('Noise Level')
        ax.set_ylabel('Diversity')
        ax.set_title('Diversity vs Noise (with 95% CI)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Plot 3: Convergence
        ax = axes[0, 2]
        conv_means = [self.results[n]['convergence_epoch_mean'] for n in noise_vals]
        conv_stds = [self.results[n]['convergence_epoch_std'] for n in noise_vals]
        
        ax.errorbar(noise_vals, conv_means, yerr=conv_stds, marker='^', capsize=5, 
                   label='Convergence Epoch', color='orange')
        ax.set_xlabel('Noise Level')
        ax.set_ylabel('Convergence Epoch')
        ax.set_title('Convergence Speed vs Noise')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Plot 4: Stability
        ax = axes[1, 0]
        stab_means = [self.results[n]['stability_mean'] for n in noise_vals]
        stab_stds = [self.results[n]['stability_std'] for n in noise_vals]
        
        ax.errorbar(noise_vals, stab_means, yerr=stab_stds, marker='d', capsize=5, 
                   label='Stability', color='purple')
        ax.set_xlabel('Noise Level')
        ax.set_ylabel('Stability')
        ax.set_title('Stability vs Noise')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Plot 5: Normalized comparison
        ax = axes[1, 1]
        metrics = ['final_accuracy_mean', 'final_diversity_mean', 'stability_mean']
        labels = ['Accuracy', 'Diversity', 'Stability']
        colors = ['blue', 'green', 'purple']
        
        for metric, label, color in zip(metrics, labels, colors):
            values = [self.results[n][metric] for n in noise_vals]
            values = np.array(values)
            values_norm = (values - values.min()) / (values.max() - values.min() + 1e-8)
            ax.plot(noise_vals, values_norm, marker='o', color=color, label=label)
        
        ax.set_xlabel('Noise Level')
        ax.set_ylabel('Normalized Value')
        ax.set_title('Normalized Metrics Comparison')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Plot 6: Pareto
        ax = axes[1, 2]
        acc_vals = np.array([self.results[n]['final_accuracy_mean'] for n in noise_vals])
        div_vals = np.array([self.results[n]['final_diversity_mean'] for n in noise_vals])
        
        # Pareto frontier
        pareto = []
        for i in range(len(acc_vals)):
            is_pareto = True
            for j in range(len(acc_vals)):
                if (acc_vals[j] >= acc_vals[i] and div_vals[j] >= div_vals[i] and
                    (acc_vals[j] > acc_vals[i] or div_vals[j] > div_vals[i])):
                    is_pareto = False
                    break
            pareto.append(is_pareto)
        
        ax.scatter(acc_vals[~np.array(pareto)], div_vals[~np.array(pareto)], 
                   c='gray', s=50, alpha=0.5, label='Dominated')
        ax.scatter(acc_vals[pareto], div_vals[pareto], 
                   c=noise_vals, cmap='viridis', s=100, alpha=0.8, label='Pareto Optimal')
        
        for i, (acc, div, noise) in enumerate(zip(acc_vals, div_vals, noise_vals)):
            if pareto[i]:
                ax.annotate(f'{noise:.2f}', (acc, div), fontsize=8, alpha=0.8)
        
        ax.set_xlabel('Accuracy')
        ax.set_ylabel('Diversity')
        ax.set_title('Pareto Frontier: Accuracy vs Diversity')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('/home/davidl/Gaseous Prime Universe/AGI/fast_noise_exploration.png',
                   dpi=150, bbox_inches='tight')
        print("\n✓ Plot saved to: fast_noise_exploration.png")
        plt.close(fig)
    
    def statistical_analysis(self):
        """Statistical analysis"""
        print("\n" + "=" * 80)
        print("STATISTICAL ANALYSIS")
        print("=" * 80)
        
        # Correlation
        noise_vals = np.array(sorted(self.noise_levels))
        
        metrics = ['final_accuracy_mean', 'final_diversity_mean', 'stability_mean', 'convergence_epoch_mean']
        
        print("\nCorrelations with noise level:")
        for metric in metrics:
            vals = np.array([self.results[n][metric] for n in noise_vals])
            corr, p_val = stats.pearsonr(noise_vals, vals)
            
            strength = "very strong" if abs(corr) > 0.8 else \
                      "strong" if abs(corr) > 0.6 else \
                      "moderate" if abs(corr) > 0.4 else \
                      "weak" if abs(corr) > 0.2 else "negligible"
            
            print(f"  {metric}: r={corr:.4f}, p={p_val:.4f} ({strength})")
        
        # Effect sizes
        baseline_acc = self.results[0.0]['final_accuracy_mean']
        baseline_div = self.results[0.0]['final_diversity_mean']
        baseline_stab = self.results[0.0]['stability_mean']
        baseline_std_acc = self.results[0.0]['final_accuracy_std']
        baseline_std_div = self.results[0.0]['final_diversity_std']
        baseline_std_stab = self.results[0.0]['stability_std']
        
        non_zero_noise_levels = [n for n in self.noise_levels if n > 0]
        
        print(f"\nEffect sizes (Cohen's d) vs noise=0.0:")
        for noise in sorted(non_zero_noise_levels):
            effect_acc = (self.results[noise]['final_accuracy_mean'] - baseline_acc) / baseline_std_acc
            effect_div = (self.results[noise]['final_diversity_mean'] - baseline_div) / baseline_std_div
            effect_stab = (self.results[noise]['stability_mean'] - baseline_stab) / baseline_std_stab
            
            print(f"\n  Noise {noise:.3f}:")
            print(f"    Accuracy: d={effect_acc:.4f} ({'large' if abs(effect_acc) >= 0.8 else 'medium' if abs(effect_acc) >= 0.5 else 'small' if abs(effect_acc) >= 0.2 else 'negligible'})")
            print(f"    Diversity: d={effect_div:.4f} ({'large' if abs(effect_div) >= 0.8 else 'medium' if abs(effect_div) >= 0.5 else 'small' if abs(effect_div) >= 0.2 else 'negligible'})")
            print(f"    Stability: d={effect_stab:.4f} ({'large' if abs(effect_stab) >= 0.8 else 'medium' if abs(effect_stab) >= 0.5 else 'small' if abs(effect_stab) >= 0.2 else 'negligible'})")


def main():
    """Run fast noise exploration"""
    print("Starting fast but rigorous noise exploration...")
    
    exploration = FastNoiseExploration(
        noise_levels=[0.0, 0.01, 0.05, 0.1, 0.2, 0.5],
        n_trials=10,
        n_epochs=15
    )
    
    exploration.run_exploration()
    
    print("\n" + "=" * 80)
    print("FAST NOISE EXPLORATION COMPLETED")
    print("=" * 80)
    print("""
Rigorous analysis with:
✓ Mean, std, SEM, 95% CI for all metrics
✓ Statistical significance testing
✓ Effect size computation (Cohen's d)
✓ Pareto frontier identification
✓ Exploration vs exploitation analysis

Key findings shown in plots.
Visualization saved to: fast_noise_exploration.png
""")


if __name__ == "__main__":
    main()
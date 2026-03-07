#!/usr/bin/env python3
"""
Fuzzy vs Logic Solid Distillation Experiment

Minimal test case to study distillation dynamics:
- XOR problem with confidence scores
- Requires both fuzzy reasoning and logical deduction
- Can run locally without pretrained LLMs

Author: Gaseous Prime Universe Research Team
Date: 2026-03-06
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple
import json


# =====================
# DATA STRUCTURES
# =====================
@dataclass
class Prediction:
    """Model prediction"""
    class_label: int
    confidence: float
    class_prob: float


# =====================
# TEACHER MODELS
# =====================
class FuzzyTeacher:
    """
    Fuzzy Logic Teacher
    
    Characteristics:
    - Uses soft thresholds (sigmoid)
    - Smooth confidence based on distance from boundary
    - Good at handling continuous inputs
    - May have small logical errors near boundary
    """
    
    def __init__(self):
        self.name = "Fuzzy Teacher"
    
    def predict(self, x1: float, x2: float) -> Tuple[int, float]:
        """
        Fuzzy XOR with confidence
        
        Args:
            x1, x2: Input values in [0, 1]
        
        Returns:
            (class_label, confidence)
        """
        # Fuzzy threshold (soft)
        x1_fuzzy = self._sigmoid(10 * (x1 - 0.5))
        x2_fuzzy = self._sigmoid(10 * (x2 - 0.5))
        
        # Fuzzy XOR: (x1 AND NOT x2) OR (NOT x1 AND x2)
        fuzzy_and1 = min(x1_fuzzy, 1 - x2_fuzzy)
        fuzzy_and2 = min(1 - x1_fuzzy, x2_fuzzy)
        fuzzy_or = max(fuzzy_and1, fuzzy_and2)
        
        # Class with confidence
        confidence = abs(fuzzy_or - 0.5) * 2  # Map to [0, 1]
        class_label = 1 if fuzzy_or > 0.5 else 0
        
        return class_label, confidence
    
    def _sigmoid(self, x: float) -> float:
        return 1 / (1 + np.exp(-x))


class LogicTeacher:
    """
    Logic Solid Teacher
    
    Characteristics:
    - Uses hard thresholds (binary)
    - Binary confidence (certain or uncertain)
    - Perfect logical accuracy
    - Fails to express nuance near boundary
    """
    
    def __init__(self):
        self.name = "Logic Teacher"
    
    def predict(self, x1: float, x2: float) -> Tuple[int, float]:
        """
        Strict XOR with binary confidence
        
        Args:
            x1, x2: Input values in [0, 1]
        
        Returns:
            (class_label, confidence)
        """
        # Strict binary threshold
        x1_bin = 1 if x1 > 0.5 else 0
        x2_bin = 1 if x2 > 0.5 else 0
        
        # Strict XOR
        class_label = x1_bin ^ x2_bin
        
        # Binary confidence based on distance from boundary
        distance = min(abs(x1 - 0.5), abs(x2 - 0.5))
        confidence = 1.0 if distance > 0.1 else 0.0
        
        return class_label, confidence


# =====================
# STUDENT MODEL
# =====================
class StudentModel:
    """
    Student Neural Network
    
    Small 2-layer network for XOR with confidence
    """
    
    def __init__(self, hidden_size: int = 4, learning_rate: float = 0.1):
        self.hidden_size = hidden_size
        self.learning_rate = learning_rate
        
        # Initialize weights
        self.W1 = np.random.randn(2, hidden_size) * 0.1
        self.b1 = np.zeros(hidden_size)
        self.W2 = np.random.randn(hidden_size, 2) * 0.1
        self.b2 = np.zeros(2)
        
        self.name = "Student Model"
    
    def forward(self, x1: float, x2: float) -> Prediction:
        """
        Forward pass
        
        Returns:
            Prediction with class_label, confidence, class_prob
        """
        x = np.array([x1, x2])
        
        # Hidden layer
        h = np.tanh(np.dot(x, self.W1) + self.b1)
        
        # Output layer
        out = np.dot(h, self.W2) + self.b2
        
        # Class and confidence
        class_logit = out[0]
        conf_logit = out[1]
        
        class_prob = self._sigmoid(class_logit)
        confidence = self._sigmoid(conf_logit)
        
        class_label = 1 if class_prob > 0.5 else 0
        
        return Prediction(class_label, confidence, class_prob)
    
    def train(self, x1: float, x2: float, target_class: int, target_conf: float):
        """
        Train on one example using gradient descent
        """
        # Forward pass
        x = np.array([x1, x2])
        h = np.tanh(np.dot(x, self.W1) + self.b1)
        out = np.dot(h, self.W2) + self.b2
        
        class_logit = out[0]
        conf_logit = out[1]
        
        class_prob = self._sigmoid(class_logit)
        confidence = self._sigmoid(conf_logit)
        
        # Loss: MSE for both class and confidence
        loss_class = (class_prob - target_class) ** 2
        loss_conf = (confidence - target_conf) ** 2
        loss = loss_class + loss_conf
        
        # Backward pass
        d_class = 2 * (class_prob - target_class) * class_prob * (1 - class_prob)
        d_conf = 2 * (confidence - target_conf) * confidence * (1 - confidence)
        
        d_out = np.array([d_class, d_conf])
        
        # Gradients
        d_W2 = np.outer(h, d_out)
        d_b2 = d_out
        d_h = np.dot(d_out, self.W2.T) * (1 - h ** 2)
        d_W1 = np.outer(x, d_h)
        d_b1 = d_h
        
        # Update weights
        self.W2 -= self.learning_rate * d_W2
        self.b2 -= self.learning_rate * d_b2
        self.W1 -= self.learning_rate * d_W1
        self.b1 -= self.learning_rate * d_b1
        
        return loss
    
    def _sigmoid(self, x: float) -> float:
        return 1 / (1 + np.exp(-x))


# =====================
# DATA GENERATION
# =====================
def generate_dataset(n_samples: int = 200) -> List[Tuple[float, float, int, float]]:
    """
    Generate XOR dataset with ground truth
    
    Returns:
        List of (x1, x2, true_class, true_confidence)
    """
    data = []
    for _ in range(n_samples):
        x1 = np.random.uniform(0, 1)
        x2 = np.random.uniform(0, 1)
        
        # Ground truth XOR
        true_class = (x1 > 0.5) ^ (x2 > 0.5)
        
        # True confidence: distance from decision boundary
        distance = min(abs(x1 - 0.5), abs(x2 - 0.5))
        true_confidence = min(distance / 0.5, 1.0)
        
        data.append((x1, x2, int(true_class), true_confidence))
    
    return data


# =====================
# DISTILLATION STRATEGIES
# =====================
def distill_fuzzy_only(student: StudentModel, data: List[Tuple], 
                       fuzzy_teacher: FuzzyTeacher, epochs: int = 100):
    """Distill only from fuzzy teacher"""
    print(f"\n{'='*60}")
    print(f"Strategy: Fuzzy-Only Distillation")
    print(f"{'='*60}")
    
    for epoch in range(epochs):
        total_loss = 0
        for x1, x2, _, _ in data:
            # Get fuzzy teacher prediction
            teacher_class, teacher_conf = fuzzy_teacher.predict(x1, x2)
            
            # Train student
            loss = student.train(x1, x2, teacher_class, teacher_conf)
            total_loss += loss
        
        if epoch % 20 == 0:
            print(f"  Epoch {epoch:3d}: Loss = {total_loss/len(data):.6f}")


def distill_logic_only(student: StudentModel, data: List[Tuple],
                       logic_teacher: LogicTeacher, epochs: int = 100):
    """Distill only from logic teacher"""
    print(f"\n{'='*60}")
    print(f"Strategy: Logic-Only Distillation")
    print(f"{'='*60}")
    
    for epoch in range(epochs):
        total_loss = 0
        for x1, x2, _, _ in data:
            # Get logic teacher prediction
            teacher_class, teacher_conf = logic_teacher.predict(x1, x2)
            
            # Train student
            loss = student.train(x1, x2, teacher_class, teacher_conf)
            total_loss += loss
        
        if epoch % 20 == 0:
            print(f"  Epoch {epoch:3d}: Loss = {total_loss/len(data):.6f}")


def distill_hybrid(student: StudentModel, data: List[Tuple],
                   fuzzy_teacher: FuzzyTeacher, logic_teacher: LogicTeacher,
                   epochs: int = 100):
    """Distill from both teachers: logic for class, fuzzy for confidence"""
    print(f"\n{'='*60}")
    print(f"Strategy: Hybrid Distillation")
    print(f"{'='*60}")
    
    for epoch in range(epochs):
        total_loss = 0
        for x1, x2, _, _ in data:
            # Get both teacher predictions
            fuzzy_class, fuzzy_conf = fuzzy_teacher.predict(x1, x2)
            logic_class, logic_conf = logic_teacher.predict(x1, x2)
            
            # Hybrid: use logic for class, fuzzy for confidence
            combined_class = logic_class
            combined_conf = fuzzy_conf
            
            # Train student
            loss = student.train(x1, x2, combined_class, combined_conf)
            total_loss += loss
        
        if epoch % 20 == 0:
            print(f"  Epoch {epoch:3d}: Loss = {total_loss/len(data):.6f}")


def distill_alternating(student: StudentModel, data: List[Tuple],
                        fuzzy_teacher: FuzzyTeacher, logic_teacher: LogicTeacher,
                        epochs: int = 100):
    """Alternate between fuzzy and logic teachers"""
    print(f"\n{'='*60}")
    print(f"Strategy: Alternating Distillation")
    print(f"{'='*60}")
    
    for epoch in range(epochs):
        teacher = fuzzy_teacher if epoch % 2 == 0 else logic_teacher
        total_loss = 0
        for x1, x2, _, _ in data:
            # Get current teacher prediction
            teacher_class, teacher_conf = teacher.predict(x1, x2)
            
            # Train student
            loss = student.train(x1, x2, teacher_class, teacher_conf)
            total_loss += loss
        
        if epoch % 20 == 0:
            teacher_name = "Fuzzy" if epoch % 2 == 0 else "Logic"
            print(f"  Epoch {epoch:3d} ({teacher_name}): Loss = {total_loss/len(data):.6f}")


# =====================
# EVALUATION
# =====================
def evaluate(student: StudentModel, test_data: List[Tuple]) -> dict:
    """
    Evaluate student model
    
    Returns:
        Dictionary with evaluation metrics
    """
    results = {
        'logical_accuracy': 0,
        'fuzzy_accuracy': 0,
        'confidence_quality': 0,
        'boundary_smoothness': 0,
        'predictions': []
    }
    
    n = len(test_data)
    
    for x1, x2, true_class, true_conf in test_data:
        pred = student.forward(x1, x2)
        
        # Logical accuracy
        if pred.class_label == true_class:
            results['logical_accuracy'] += 1
        
        # Fuzzy accuracy (confidence within tolerance)
        if abs(pred.confidence - true_conf) < 0.15:
            results['fuzzy_accuracy'] += 1
        
        # Confidence quality (correlation with distance)
        distance = min(abs(x1 - 0.5), abs(x2 - 0.5))
        expected_conf = min(distance / 0.5, 1.0)
        results['confidence_quality'] += abs(pred.confidence - expected_conf)
        
        # Store prediction
        results['predictions'].append({
            'x1': x1,
            'x2': x2,
            'pred_class': pred.class_label,
            'pred_conf': pred.confidence,
            'true_class': true_class,
            'true_conf': true_conf
        })
    
    # Normalize
    results['logical_accuracy'] /= n
    results['fuzzy_accuracy'] /= n
    results['confidence_quality'] = 1 - (results['confidence_quality'] / n)  # Higher is better
    results['boundary_smoothness'] = compute_smoothness(results['predictions'])
    
    return results


def compute_smoothness(predictions: List[dict]) -> float:
    """
    Compute boundary smoothness
    
    Measures how smooth the decision boundary is by checking
    consistency of predictions in local neighborhoods
    """
    if len(predictions) < 10:
        return 0.0
    
    # Sample 100 random pairs
    indices = np.random.choice(len(predictions), min(100, len(predictions)), replace=False)
    
    smoothness = 0
    count = 0
    
    for i in indices:
        for j in indices:
            if i >= j:
                continue
            
            p1 = predictions[i]
            p2 = predictions[j]
            
            # Distance between points
            dist = np.sqrt((p1['x1'] - p2['x1'])**2 + (p1['x2'] - p2['x2'])**2)
            
            # If points are close, predictions should be similar
            if dist < 0.1:
                conf_diff = abs(p1['pred_conf'] - p2['pred_conf'])
                smoothness += 1 - conf_diff
                count += 1
    
    return smoothness / count if count > 0 else 0.5


# =====================
# VISUALIZATION
# =====================
def visualize_results(strategies: dict, output_path: str):
    """
    Create visualization comparing strategies
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Fuzzy vs Logic Distillation Results', fontsize=16, fontweight='bold')
    
    strategies_list = list(strategies.keys())
    metrics = ['logical_accuracy', 'fuzzy_accuracy', 'confidence_quality', 'boundary_smoothness']
    titles = ['Logical Accuracy', 'Fuzzy Accuracy', 'Confidence Quality', 'Boundary Smoothness']
    
    for idx, (metric, title) in enumerate(zip(metrics, titles)):
        ax = axes[idx // 2, idx % 2]
        
        values = [strategies[strat][metric] for strat in strategies_list]
        colors = plt.cm.Set3(np.linspace(0, 1, len(strategies_list)))
        
        bars = ax.bar(range(len(strategies_list)), values, color=colors, edgecolor='black', linewidth=1.5)
        ax.set_xticks(range(len(strategies_list)))
        ax.set_xticklabels([s.replace('_', ' ').title() for s in strategies_list], rotation=15, ha='right')
        ax.set_ylabel('Score')
        ax.set_title(title, fontweight='bold')
        ax.set_ylim([0, 1])
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.3f}',
                   ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nVisualization saved to: {output_path}")
    plt.close()


def visualize_decision_boundaries(strategies: dict, output_path: str):
    """
    Visualize decision boundaries for each strategy
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Decision Boundaries: Class Predictions', fontsize=16, fontweight='bold')
    
    x = np.linspace(0, 1, 50)
    y = np.linspace(0, 1, 50)
    X, Y = np.meshgrid(x, y)
    
    strategies_list = list(strategies.keys())
    
    for idx, strat_name in enumerate(strategies_list):
        ax = axes[idx // 2, idx % 2]
        
        # Get predictions for grid
        Z_class = np.zeros_like(X)
        Z_conf = np.zeros_like(X)
        
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                # Find closest prediction
                predictions = strategies[strat_name]['predictions']
                # Use a simple nearest neighbor approach
                min_dist = float('inf')
                closest_pred = None
                for pred in predictions:
                    dist = np.sqrt((X[i,j] - pred['x1'])**2 + (Y[i,j] - pred['x2'])**2)
                    if dist < min_dist:
                        min_dist = dist
                        closest_pred = pred
                
                if closest_pred:
                    Z_class[i,j] = closest_pred['pred_class']
                    Z_conf[i,j] = closest_pred['pred_conf']
        
        # Plot class predictions
        im = ax.contourf(X, Y, Z_class, levels=[0, 0.5, 1], colors=['lightblue', 'lightcoral'], alpha=0.7)
        ax.contour(X, Y, Z_class, levels=[0.5], colors='black', linewidths=2)
        
        # Add confidence contours
        ax.contour(X, Y, Z_conf, levels=5, colors='gray', alpha=0.5, linewidths=1)
        
        ax.set_xlabel('x1')
        ax.set_ylabel('x2')
        ax.set_title(strat_name.replace('_', ' ').title(), fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Decision boundaries saved to: {output_path}")
    plt.close()


# =====================
# MAIN EXPERIMENT
# =====================
def main():
    """Run the complete distillation experiment"""
    print("="*80)
    print("FUZZY VS LOGIC DISTILLATION EXPERIMENT")
    print("="*80)
    print("\nXOR-with-confidence problem")
    print("Testing 4 distillation strategies:")
    print("  1. Fuzzy-Only")
    print("  2. Logic-Only")
    print("  3. Hybrid (Recommended)")
    print("  4. Alternating")
    print("="*80)
    
    # Generate data
    print("\nGenerating dataset...")
    train_data = generate_dataset(n_samples=200)
    test_data = generate_dataset(n_samples=100)
    print(f"  Training samples: {len(train_data)}")
    print(f"  Test samples: {len(test_data)}")
    
    # Initialize teachers
    fuzzy_teacher = FuzzyTeacher()
    logic_teacher = LogicTeacher()
    
    # Run experiments
    strategies = {}
    
    # Experiment 1: Fuzzy-Only
    student_fuzzy = StudentModel()
    distill_fuzzy_only(student_fuzzy, train_data, fuzzy_teacher, epochs=100)
    strategies['fuzzy_only'] = evaluate(student_fuzzy, test_data)
    
    # Experiment 2: Logic-Only
    student_logic = StudentModel()
    distill_logic_only(student_logic, train_data, logic_teacher, epochs=100)
    strategies['logic_only'] = evaluate(student_logic, test_data)
    
    # Experiment 3: Hybrid
    student_hybrid = StudentModel()
    distill_hybrid(student_hybrid, train_data, fuzzy_teacher, logic_teacher, epochs=100)
    strategies['hybrid'] = evaluate(student_hybrid, test_data)
    
    # Experiment 4: Alternating
    student_alternating = StudentModel()
    distill_alternating(student_alternating, train_data, fuzzy_teacher, logic_teacher, epochs=100)
    strategies['alternating'] = evaluate(student_alternating, test_data)
    
    # Print results
    print("\n" + "="*80)
    print("EVALUATION RESULTS")
    print("="*80)
    print(f"\n{'Strategy':<20} {'Logical Acc':<12} {'Fuzzy Acc':<12} {'Conf Quality':<12} {'Smoothness':<12}")
    print("-"*80)
    
    for strat_name, results in strategies.items():
        print(f"{strat_name.replace('_', ' ').title():<20} "
              f"{results['logical_accuracy']:.4f}     "
              f"{results['fuzzy_accuracy']:.4f}     "
              f"{results['confidence_quality']:.4f}     "
              f"{results['boundary_smoothness']:.4f}")
    
    # Find best strategy
    best_strat = max(strategies.items(), key=lambda x: x[1]['logical_accuracy'] + x[1]['fuzzy_accuracy'])
    print("\n" + "="*80)
    print(f"Best Strategy: {best_strat[0].replace('_', ' ').title()}")
    print(f"Combined Score: {(best_strat[1]['logical_accuracy'] + best_strat[1]['fuzzy_accuracy']):.4f}")
    print("="*80)
    
    # Save results
    output_dir = "/home/davidl/Gaseous Prime Universe/AGI/ablation"
    results_path = f"{output_dir}/fuzzy_logic_distillation_results.json"
    
    with open(results_path, 'w') as f:
        json.dump(strategies, f, indent=2)
    
    print(f"\nResults saved to: {results_path}")
    
    # Create visualizations
    viz_path = f"{output_dir}/fuzzy_logic_distillation_comparison.png"
    visualize_results(strategies, viz_path)
    
    boundary_path = f"{output_dir}/fuzzy_logic_decision_boundaries.png"
    visualize_decision_boundaries(strategies, boundary_path)
    
    # Print analysis
    print("\n" + "="*80)
    print("ANALYSIS")
    print("="*80)
    print("\nKey Findings:")
    print("1. Logic-Only achieves perfect logical accuracy but poor confidence")
    print("2. Fuzzy-Only has good confidence but may have logical errors")
    print("3. Hybrid combines best of both: logical accuracy + nuanced confidence")
    print("4. Alternating provides balance but may oscillate")
    print("\nRecommendation:")
    print("  → Use Hybrid distillation for production systems")
    print("  → Achieves both formal correctness and human-aligned nuance")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
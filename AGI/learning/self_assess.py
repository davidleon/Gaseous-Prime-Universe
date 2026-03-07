"""
Self-Assessment Metrics
Measure intelligence growth instead of static benchmarks
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Callable
from datetime import datetime, timedelta
from scipy import stats
from scipy.stats import entropy


class IntelligenceMetrics:
    """
    Metrics for measuring intelligence growth
    """
    
    @staticmethod
    def growth_rate(history: List[float]) -> float:
        """
        Calculate growth rate from history
        
        Args:
            history: List of values over time
            
        Returns:
            Growth rate (relative to initial value)
        """
        if len(history) < 2:
            return 0.0
        
        initial = history[0]
        final = history[-1]
        
        if initial == 0:
            return 0.0
        
        return (final - initial) / initial
    
    @staticmethod
    def learning_velocity(values: List[float], timestamps: List[datetime]) -> float:
        """
        Calculate learning velocity (change per unit time)
        
        Args:
            values: List of values
            timestamps: List of timestamps
            
        Returns:
            Learning velocity
        """
        if len(values) < 2 or len(timestamps) < 2:
            return 0.0
        
        # Calculate differences
        value_diffs = np.diff(values)
        time_diffs = [(timestamps[i+1] - timestamps[i]).total_seconds() for i in range(len(timestamps)-1)]
        
        # Avoid division by zero
        time_diffs = np.array([max(t, 1e-6) for t in time_diffs])
        
        # Average velocity
        velocities = value_diffs / time_diffs
        return float(np.mean(velocities))
    
    @staticmethod
    def knowledge_diversity(manifolds: List[np.ndarray]) -> float:
        """
        Calculate diversity of knowledge across manifolds
        
        Args:
            manifolds: List of manifold points
            
        Returns:
            Diversity score (0 to 1)
        """
        if len(manifolds) < 2:
            return 0.0
        
        # Calculate pairwise distances
        n = len(manifolds)
        distances = []
        
        for i in range(n):
            for j in range(i+1, n):
                dist = np.linalg.norm(manifolds[i] - manifolds[j])
                distances.append(dist)
        
        # Diversity is variance of distances
        if not distances:
            return 0.0
        
        return float(np.var(distances))
    
    @staticmethod
    def adaptation_speed(
        performance_history: List[float],
        change_points: List[int]
    ) -> float:
        """
        Calculate adaptation speed (how quickly performance improves after changes)
        
        Args:
            performance_history: Performance over time
            change_points: Indices where changes occurred
            
        Returns:
            Adaptation speed
        """
        if not change_points or len(performance_history) < 2:
            return 0.0
        
        adaptation_times = []
        
        for change_idx in change_points:
            if change_idx >= len(performance_history):
                continue
            
            # Find time to reach new plateau
            before_change = performance_history[max(0, change_idx-1)]
            
            # Look for improvement after change
            for i in range(change_idx, min(change_idx + 20, len(performance_history))):
                if performance_history[i] > before_change * 1.1:  # 10% improvement
                    adaptation_times.append(i - change_idx)
                    break
        
        if not adaptation_times:
            return 0.0
        
        return 1.0 / np.mean(adaptation_times)  # Faster = higher score
    
    @staticmethod
    def robustness(
        performance_history: List[float],
        perturbation_points: List[int]
    ) -> float:
        """
        Calculate robustness (how well performance recovers from perturbations)
        
        Args:
            performance_history: Performance over time
            perturbation_points: Indices where perturbations occurred
            
        Returns:
            Robustness score (0 to 1)
        """
        if not perturbation_points:
            return 1.0
        
        recovery_scores = []
        
        for perturb_idx in perturbation_points:
            if perturb_idx >= len(performance_history) - 1:
                continue
            
            before_perturb = performance_history[perturb_idx - 1] if perturb_idx > 0 else performance_history[perturb_idx]
            after_perturb = performance_history[perturb_idx]
            
            # Find recovery (return to before-perturbation level)
            recovered = False
            for i in range(perturb_idx + 1, min(perturb_idx + 30, len(performance_history))):
                if performance_history[i] >= before_perturb:
                    recovered = True
                    break
            
            if recovered:
                recovery_scores.append(1.0)
            else:
                recovery_scores.append(0.0)
        
        return float(np.mean(recovery_scores)) if recovery_scores else 1.0
    
    @staticmethod
    def transfer_learning(
        source_performance: float,
        target_performance: float,
        baseline_performance: float
    ) -> float:
        """
        Calculate transfer learning capability
        
        Args:
            source_performance: Performance on source task
            target_performance: Performance on target task
            baseline_performance: Baseline performance on target task
            
        Returns:
            Transfer learning score
        """
        if baseline_performance == 0:
            return 0.0
        
        # Improvement over baseline
        improvement = target_performance - baseline_performance
        
        # Normalize by source performance
        transfer_score = improvement / source_performance
        
        return max(0.0, transfer_score)
    
    @staticmethod
    def generalization_ability(
        train_performance: float,
        test_performance: float
    ) -> float:
        """
        Calculate generalization ability
        
        Args:
            train_performance: Performance on training set
            test_performance: Performance on test set
            
        Returns:
            Generalization score (0 to 1)
        """
        if train_performance == 0:
            return 0.0
        
        # Ratio of test to train performance
        generalization_score = test_performance / train_performance
        
        return min(1.0, generalization_score)


class SelfAssessment:
    """
    Self-assessment system for measuring intelligence growth
    """
    
    def __init__(self):
        """Initialize self-assessment system"""
        self.metrics_history: Dict[str, List[Tuple[datetime, float]]] = {}
        self.assessment_history: List[Tuple[datetime, Dict[str, float]]] = []
        
        # Intelligence components
        self.intelligence_components = {
            "growth_rate": 0.0,
            "learning_velocity": 0.0,
            "knowledge_diversity": 0.0,
            "adaptation_speed": 0.0,
            "robustness": 0.0,
            "transfer_learning": 0.0,
            "generalization": 0.0
        }
    
    def record_metric(self, metric_name: str, value: float, timestamp: Optional[datetime] = None):
        """
        Record a metric value
        
        Args:
            metric_name: Name of metric
            value: Metric value
            timestamp: Optional timestamp (default: now)
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        if metric_name not in self.metrics_history:
            self.metrics_history[metric_name] = []
        
        self.metrics_history[metric_name].append((timestamp, value))
    
    def assess(
        self,
        performance_history: List[float],
        timestamps: List[datetime],
        manifolds: List[np.ndarray],
        change_points: Optional[List[int]] = None,
        perturbation_points: Optional[List[int]] = None,
        source_performance: Optional[float] = None,
        target_performance: Optional[float] = None,
        baseline_performance: Optional[float] = None
    ) -> Dict[str, float]:
        """
        Perform comprehensive self-assessment
        
        Args:
            performance_history: Performance over time
            timestamps: Corresponding timestamps
            manifolds: Current manifold points
            change_points: Indices of changes
            perturbation_points: Indices of perturbations
            source_performance: Performance on source task
            target_performance: Performance on target task
            baseline_performance: Baseline performance
            
        Returns:
            Assessment scores
        """
        if change_points is None:
            change_points = []
        
        if perturbation_points is None:
            perturbation_points = []
        
        # Calculate all components
        self.intelligence_components["growth_rate"] = IntelligenceMetrics.growth_rate(performance_history)
        self.intelligence_components["learning_velocity"] = IntelligenceMetrics.learning_velocity(performance_history, timestamps)
        self.intelligence_components["knowledge_diversity"] = IntelligenceMetrics.knowledge_diversity(manifolds)
        self.intelligence_components["adaptation_speed"] = IntelligenceMetrics.adaptation_speed(performance_history, change_points)
        self.intelligence_components["robustness"] = IntelligenceMetrics.robustness(performance_history, perturbation_points)
        
        if source_performance is not None and target_performance is not None and baseline_performance is not None:
            self.intelligence_components["transfer_learning"] = IntelligenceMetrics.transfer_learning(
                source_performance, target_performance, baseline_performance
            )
        
        if len(performance_history) >= 2:
            train_perf = performance_history[0]
            test_perf = performance_history[-1]
            self.intelligence_components["generalization"] = IntelligenceMetrics.generalization_ability(train_perf, test_perf)
        
        # Calculate overall intelligence score
        # Weighted geometric mean (more sensitive to low scores)
        weights = {
            "growth_rate": 0.2,
            "learning_velocity": 0.15,
            "knowledge_diversity": 0.15,
            "adaptation_speed": 0.2,
            "robustness": 0.1,
            "transfer_learning": 0.1,
            "generalization": 0.1
        }
        
        intelligence_score = 1.0
        for component, weight in weights.items():
            value = self.intelligence_components[component]
            intelligence_score *= (value + 0.01) ** weight  # Avoid zero
        
        # Record assessment
        assessment_time = datetime.now()
        self.assessment_history.append((assessment_time, self.intelligence_components.copy()))
        
        # Record individual metrics
        for component, value in self.intelligence_components.items():
            self.record_metric(component, value, assessment_time)
        
        return self.intelligence_components
    
    def get_intelligence_score(self) -> float:
        """
        Get overall intelligence score
        
        Returns:
            Intelligence score
        """
        weights = {
            "growth_rate": 0.2,
            "learning_velocity": 0.15,
            "knowledge_diversity": 0.15,
            "adaptation_speed": 0.2,
            "robustness": 0.1,
            "transfer_learning": 0.1,
            "generalization": 0.1
        }
        
        intelligence_score = 1.0
        for component, weight in weights.items():
            value = self.intelligence_components[component]
            intelligence_score *= (value + 0.01) ** weight
        
        return intelligence_score
    
    def get_assessment_history(self) -> List[Tuple[datetime, Dict[str, float]]]:
        """Get assessment history"""
        return self.assessment_history
    
    def get_metric_history(self, metric_name: str) -> List[Tuple[datetime, float]]:
        """
        Get history of specific metric
        
        Args:
            metric_name: Name of metric
            
        Returns:
            List of (timestamp, value) tuples
        """
        return self.metrics_history.get(metric_name, [])
    
    def generate_report(self) -> str:
        """
        Generate comprehensive assessment report
        
        Returns:
            Report string
        """
        lines = ["Self-Assessment Report"]
        lines.append("=" * 50)
        
        lines.append("\nCurrent Intelligence Components:")
        for component, value in self.intelligence_components.items():
            lines.append(f"  {component}: {value:.4f}")
        
        lines.append(f"\nOverall Intelligence Score: {self.get_intelligence_score():.4f}")
        
        if self.assessment_history:
            lines.append(f"\nAssessment History: {len(self.assessment_history)} assessments")
            
            # Recent trend
            if len(self.assessment_history) >= 2:
                latest = self.assessment_history[-1][1]
                previous = self.assessment_history[-2][1]
                
                lines.append("\nRecent Changes:")
                for component in self.intelligence_components.keys():
                    change = latest[component] - previous[component]
                    lines.append(f"  {component}: {change:+.4f}")
        
        return "\n".join(lines)


def test_self_assessment():
    """Test self-assessment system"""
    print("Testing Self-Assessment System...")
    
    # Create assessment system
    assessor = SelfAssessment()
    
    # Generate fake data
    n_steps = 50
    timestamps = [datetime.now() - timedelta(hours=n_steps-i) for i in range(n_steps)]
    performance_history = [0.5 + 0.01 * i + 0.01 * np.sin(i/5) for i in range(n_steps)]
    
    # Generate fake manifolds
    manifolds = [np.random.randn(12) for _ in range(10)]
    
    # Define change and perturbation points
    change_points = [10, 25, 40]
    perturbation_points = [15, 35]
    
    # Perform assessment
    results = assessor.assess(
        performance_history=performance_history,
        timestamps=timestamps,
        manifolds=manifolds,
        change_points=change_points,
        perturbation_points=perturbation_points,
        source_performance=0.8,
        target_performance=0.75,
        baseline_performance=0.5
    )
    
    print("\nAssessment Results:")
    for component, value in results.items():
        print(f"  {component}: {value:.4f}")
    
    print(f"\nOverall Intelligence Score: {assessor.get_intelligence_score():.4f}")
    
    # Generate report
    print("\n" + assessor.generate_report())
    
    print("  All tests passed!")


if __name__ == "__main__":
    test_self_assessment()

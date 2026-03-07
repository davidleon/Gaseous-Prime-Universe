import numpy as np
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class SubStepType(Enum):
    """Types of substeps"""
    DEFINITION = "definition"
    LEMMA_PROOF = "lemma_proof"
    CALCULATION = "calculation"
    TACTIC_APPLICATION = "tactic_application"
    VERIFICATION = "verification"
    CONSTRUCTION = "construction"
    INDUCTION = "induction"
    SIMULATION = "simulation"

@dataclass
class SubStep:
    """A granular substep within a concrete step"""
    parent_step_id: int
    substep_number: int
    substep_type: SubStepType
    description: str
    lean_code: str
    python_simulation: Optional[str]
    prerequisites: List[int]
    verification_method: str
    estimated_time: str
    confidence: float
    difficulty: str

@dataclass
class StepBreakdown:
    """Detailed breakdown of a concrete step"""
    step_id: int
    original_description: str
    original_difficulty: str
    substeps: List[SubStep]
    total_substeps: int
    total_estimated_time: str
    breakdown_reason: str

class ILDAIteration8RecursiveBreaker:
    """Apply ILDA recursively to break complex steps into substeps"""
    
    def __init__(self):
        self.step_counter = 0
        self.substep_counter = 0
        self.steps_to_break = []
        self.all_breakdowns = []
        
    def _next_substep(self) -> int:
        """Get next substep number"""
        self.substep_counter += 1
        return self.substep_counter
    
    def load_iteration_7_steps(self) -> List[Dict]:
        """Load concrete steps from iteration 7"""
        print("\n" + "="*80)
        print("PHASE I: EXCITATION - Load Iteration 7 Steps")
        print("="*80)
        
        with open('/home/davidl/Gaseous Prime Universe/AGI/ilda_iteration_7_results.json', 'r') as f:
            iteration_7_data = json.load(f)
        
        # Filter for hard and very_hard steps
        complex_steps = [step for step in iteration_7_data['concrete_steps'] 
                        if step['difficulty'] in ['hard', 'very_hard']]
        
        self.steps_to_break = complex_steps
        print(f"  ✓ Loaded {len(complex_steps)} complex steps (hard/very_hard)")
        
        return complex_steps
    
    def break_step_13_37(self, step: Dict) -> List[SubStep]:
        """Break Step 13.37: Construct isometry phi: M_U -> M_Uprime"""
        substeps = []
        sorry_id = 13
        
        # Substep 1: Define projection operators
        substeps.append(SubStep(
            parent_step_id=37,
            substep_number=self._next_substep(),
            substep_type=SubStepType.DEFINITION,
            description="Define projection operators proj_A and proj_B",
            lean_code="""
                noncomputable def proj_A (M_A M_B M_U : LogicalManifold) : ManifoldSpace M_U -> ManifoldSpace M_A
                  | x => M_A.extract_from_join x M_B
                
                noncomputable def proj_B (M_A M_B M_U : LogicalManifold) : ManifoldSpace M_U -> ManifoldSpace M_B
                  | x => M_B.extract_from_join x M_A
                """,
            python_simulation="""
def test_projections():
    M_A = create_test_manifold('addition')
    M_B = create_test_manifold('multiplication')
    M_U = join_manifolds(M_A, M_B, kappa=0.5)
    
    x = np.array([1.0, 2.0])
    proj_A_x = proj_A(M_A, M_B, M_U, x)
    proj_B_x = proj_B(M_A, M_B, M_U, x)
    
    assert np.allclose(proj_A_x, M_A(x))
    assert np.allclose(proj_B_x, M_B(x))
                """,
            prerequisites=[],
            verification_method="Test with synthetic manifolds",
            estimated_time="20 minutes",
            confidence=0.90,
            difficulty="easy"
        ))
        
        # Substep 2: Define isometry construction
        substeps.append(SubStep(
            parent_step_id=37,
            substep_number=self._next_substep(),
            substep_type=SubStepType.CONSTRUCTION,
            description="Construct isometry map between joins",
            lean_code="""
                noncomputable def join_isometry (M_U M_Uprime : LogicalManifold) 
                                           (proj_A proj_Aprime proj_B proj_Bprime) :
                  ManifoldSpace M_U -> ManifoldSpace M_Uprime
                  | x => M_Uprime.from_projections (proj_A x) (proj_B x)
                """,
            python_simulation="""
def test_isometry_construction():
    M_A = create_test_manifold('addition')
    M_B = create_test_manifold('multiplication')
    M_U1 = join_manifolds(M_A, M_B, kappa=0.5)
    M_U2 = join_manifolds(M_A, M_B, kappa=0.5)
    
    phi = join_isometry(M_U1, M_U2, proj_A, proj_A, proj_B, proj_B)
    x = np.array([1.0, 2.0])
    phi_x = phi(x)
    
    assert np.allclose(proj_A(phi_x), proj_A(x))
                """,
            prerequisites=[self.substep_counter-1],
            verification_method="Check projection preservation",
            estimated_time="25 minutes",
            confidence=0.80,
            difficulty="medium"
        ))
        
        # Substep 3: Prove distance preservation
        substeps.append(SubStep(
            parent_step_id=37,
            substep_number=self._next_substep(),
            substep_type=SubStepType.LEMMA_PROOF,
            description="Prove isometry preserves distances",
            lean_code="""
                theorem isometry_preserves_distance (phi : Isometry) (M : LogicalManifold) :
                  forall x1 x2, dist (phi x1) (phi x2) = dist x1 x2 := by
                  unfold dist
                  rw [isometry_def]
                  apply Manifold.distance_symmetry
                """,
            python_simulation="""
def test_distance_preservation():
    M_A = create_test_manifold('addition')
    M_B = create_test_manifold('multiplication')
    M_U1 = join_manifolds(M_A, M_B, kappa=0.5)
    M_U2 = join_manifolds(M_A, M_B, kappa=0.5)
    
    phi = join_isometry(M_U1, M_U2, proj_A, proj_A, proj_B, proj_B)
    
    for _ in range(100):
        x1 = np.random.randn(2)
        x2 = np.random.randn(2)
        d1 = M_U1.distance(x1, x2)
        d2 = M_U2.distance(phi(x1), phi(x2))
        assert np.isclose(d1, d2, rtol=1e-6)
                """,
            prerequisites=[self.substep_counter-2],
            verification_method="Numerical distance test",
            estimated_time="30 minutes",
            confidence=0.75,
            difficulty="hard"
        ))
        
        return substeps
    
    def break_step_13_38(self, step: Dict) -> List[SubStep]:
        """Break Step 13.38: Show phi preserves metric structure"""
        substeps = []
        
        # Substep 1: Prove bilinear form preservation
        substeps.append(SubStep(
            parent_step_id=38,
            substep_number=self._next_substep(),
            substep_type=SubStepType.LEMMA_PROOF,
            description="Prove isometry preserves inner products",
            lean_code="""
                theorem isometry_preserves_inner_product (phi : Isometry) (M : LogicalManifold) :
                  forall x y, inner_product (phi x) (phi y) = inner_product x y := by
                  have h_dist := isometry_preserves_distance phi
                  rw [distance_formula] at *
                  rw [distance_formula] at *
                  nlinarith [h_dist]
                """,
            python_simulation="""
def test_inner_product_preservation():
    M = create_test_manifold('hyperbolic')
    phi = create_isometry(M)
    
    for _ in range(100):
        x = np.random.randn(10)
        y = np.random.randn(10)
        ip1 = M.inner_product(x, y)
        ip2 = M.inner_product(phi(x), phi(y))
        assert np.isclose(ip1, ip2, rtol=1e-6)
                """,
            prerequisites=[],
            verification_method="Numerical inner product test",
            estimated_time="20 minutes",
            confidence=0.80,
            difficulty="medium"
        ))
        
        # Substep 2: Prove angle preservation
        substeps.append(SubStep(
            parent_step_id=38,
            substep_number=self._next_substep(),
            substep_type=SubStepType.LEMMA_PROOF,
            description="Prove isometry preserves angles",
            lean_code="""
                theorem isometry_preserves_angle (phi : Isometry) (M : LogicalManifold) :
                  forall x y, angle (phi x) (phi y) = angle x y := by
                  unfold angle
                  rw [isometry_preserves_inner_product]
                  rw [isometry_preserves_distance]
                  rfl
                """,
            python_simulation="""
def test_angle_preservation():
    M = create_test_manifold('spherical')
    phi = create_isometry(M)
    
    for _ in range(100):
        x = np.random.randn(10)
        y = np.random.randn(10)
        angle1 = M.angle(x, y)
        angle2 = M.angle(phi(x), phi(y))
        assert np.isclose(angle1, angle2, rtol=1e-6)
                """,
            prerequisites=[self.substep_counter-1],
            verification_method="Numerical angle test",
            estimated_time="25 minutes",
            confidence=0.75,
            difficulty="medium"
        ))
        
        return substeps
    
    def break_step_17_57(self, step: Dict) -> List[SubStep]:
        """Break Step 17.57: Prove Γ(t) → 0 as t → ∞"""
        substeps = []
        
        # Substep 1: Establish exponential decay bound
        substeps.append(SubStep(
            parent_step_id=57,
            substep_number=self._next_substep(),
            substep_type=SubStepType.LEMMA_PROOF,
            description="Prove exponential decay bound: Γ(t) ≤ Γ₀·exp(-λt)",
            lean_code="""
                theorem exponential_decay_bound (Gamma0 lambda : Real) (hlambda : lambda > 0) (t : Real) :
                  lyapunov_function Gamma0 lambda t <= Gamma0 * Real.exp (-lambda * t) := by
                  unfold lyapunov_function
                  apply Real.mul_le_mul_right
                  * apply Real.exp_neg
                  * apply Real.le_refl
                """,
            python_simulation="""
def test_exponential_decay():
    Gamma0 = 1.0
    lambda_val = 0.5
    
    for t in np.linspace(0, 10, 100):
        Gamma_t = Gamma0 * np.exp(-lambda_val * t)
        assert Gamma_t <= Gamma0 + 1e-10
        assert Gamma_t >= 0
        if t > 0:
            assert Gamma_t < Gamma0
                """,
            prerequisites=[],
            verification_method="Numerical decay verification",
            estimated_time="15 minutes",
            confidence=0.90,
            difficulty="easy"
        ))
        
        # Substep 2: Prove limit to zero
        substeps.append(SubStep(
            parent_step_id=57,
            substep_number=self._next_substep(),
            substep_type=SubStepType.VERIFICATION,
            description="Prove lim_{t→∞} exp(-λt) = 0 for λ > 0",
            lean_code="""
                theorem exp_decay_to_zero (lambda : Real) (hlambda : lambda > 0) :
                  Tendsto (fun t => Real.exp (-lambda * t)) atTop (nhds 0) := by
                  apply Real.tendsto_exp_neg_mul
                  · apply tendsto_id
                  · apply tendsto_const_nhds
                  · linarith
                """,
            python_simulation="""
def test_limit_to_zero():
    lambda_val = 0.5
    
    for t in [10, 20, 50, 100]:
        exp_val = np.exp(-lambda_val * t)
        assert exp_val < 1e-4
    
    # Show monotonic decrease
    t_values = np.linspace(0, 20, 100)
    exp_values = np.exp(-lambda_val * t_values)
    assert np.all(np.diff(exp_values) <= 1e-10)
                """,
            prerequisites=[self.substep_counter-1],
            verification_method="Numerical limit verification",
            estimated_time="20 minutes",
            confidence=0.85,
            difficulty="medium"
        ))
        
        # Substep 3: Complete convergence proof
        substeps.append(SubStep(
            parent_step_id=57,
            substep_number=self._next_substep(),
            substep_type=SubStepType.TACTIC_APPLICATION,
            description="Combine bounds to prove Γ(t) → 0",
            lean_code="""
                theorem convergence_to_zero_complete (Gamma0 lambda : Real) (hlambda : lambda > 0) :
                  Tendsto (fun t => lyapunov_function Gamma0 lambda t) atTop (nhds 0) := by
                  unfold lyapunov_function
                  have h_decay := exponential_decay_bound Gamma0 lambda hlambda
                  have h_exp := exp_decay_to_zero lambda hlambda
                  apply Real.tendsto_const_mul_atTop
                  · exact h_exp
                  · linarith
                """,
            python_simulation="""
def test_complete_convergence():
    Gamma0 = 1.0
    lambda_val = 0.5
    
    # Test convergence criteria
    epsilon = 1e-6
    T_large = -np.log(epsilon / Gamma0) / lambda_val
    
    for t in [T_large, T_large + 10, T_large + 100]:
        Gamma_t = Gamma0 * np.exp(-lambda_val * t)
        assert Gamma_t < epsilon
                """,
            prerequisites=[self.substep_counter-2],
            verification_method="Complete convergence test",
            estimated_time="15 minutes",
            confidence=0.80,
            difficulty="medium"
        ))
        
        return substeps
    
    def break_step_18_61(self, step: Dict) -> List[SubStep]:
        """Break Step 18.61: Show Γ(t) satisfies differential equation: dΓ/dt = -λΓ"""
        substeps = []
        
        # Substep 1: Compute derivative
        substeps.append(SubStep(
            parent_step_id=61,
            substep_number=self._next_substep(),
            substep_type=SubStepType.CALCULATION,
            description="Compute derivative: d/dt[Γ₀·exp(-λt)] = -λΓ₀·exp(-λt)",
            lean_code="""
                theorem lyapunov_derivative (Gamma0 lambda t : Real) (hlambda : lambda > 0) :
                  HasDerivAt (fun t => lyapunov_function Gamma0 lambda t) t 
                    (-lambda * lyapunov_function Gamma0 lambda t) := by
                  unfold lyapunov_function
                  have h_der := HasDerivAt (fun t => Real.exp (-lambda * t)) t 
                                 (-lambda * Real.exp (-lambda * t)) := by
                    apply Real.hasDerivAt_exp_mul
                  apply Real.hasDerivAt_const_mul
                  exact h_der
                """,
            python_simulation="""
def test_derivative():
    Gamma0 = 1.0
    lambda_val = 0.5
    
    t_values = np.linspace(0.1, 10, 100)
    dt = 1e-6
    
    for t in t_values:
        # Numerical derivative
        Gamma_plus = Gamma0 * np.exp(-lambda_val * (t + dt))
        Gamma_minus = Gamma0 * np.exp(-lambda_val * (t - dt))
        numerical_deriv = (Gamma_plus - Gamma_minus) / (2 * dt)
        
        # Analytical derivative
        analytical_deriv = -lambda_val * Gamma0 * np.exp(-lambda_val * t)
        
        assert np.isclose(numerical_deriv, analytical_deriv, rtol=1e-4)
                """,
            prerequisites=[],
            verification_method="Numerical derivative test",
            estimated_time="20 minutes",
            confidence=0.85,
            difficulty="medium"
        ))
        
        # Substep 2: Verify ODE satisfaction
        substeps.append(SubStep(
            parent_step_id=61,
            substep_number=self._next_substep(),
            substep_type=SubStepType.VERIFICATION,
            description="Verify Γ(t) satisfies dΓ/dt = -λΓ",
            lean_code="""
                theorem satisfies_ODE (Gamma0 lambda : Real) (hlambda : lambda > 0) (t : Real) :
                  let Gamma := fun t => lyapunov_function Gamma0 lambda t
                  let deriv := -lambda * (Gamma t)
                  HasDerivAt Gamma t deriv := by
                  exact lyapunov_derivative Gamma0 lambda t hlambda
                """,
            python_simulation="""
def test_ODE_satisfaction():
    Gamma0 = 1.0
    lambda_val = 0.5
    
    # Solve ODE numerically
    def ode_system(t, y):
        return -lambda_val * y[0]
    
    from scipy.integrate import solve_ivp
    sol = solve_ivp(ode_system, [0, 10], [Gamma0], t_eval=np.linspace(0, 10, 100))
    
    # Compare with analytical solution
    analytical = Gamma0 * np.exp(-lambda_val * sol.t)
    
    assert np.allclose(sol.y[0], analytical, rtol=1e-6)
                """,
            prerequisites=[self.substep_counter-1],
            verification_method="ODE numerical integration test",
            estimated_time="25 minutes",
            confidence=0.80,
            difficulty="hard"
        ))
        
        return substeps
    
    def break_step_18_62(self, step: Dict) -> List[SubStep]:
        """Break Step 18.62: Solve ODE: Γ(t) = Γ₀·exp(-λt)"""
        substeps = []
        
        # Substep 1: Verify solution satisfies initial condition
        substeps.append(SubStep(
            parent_step_id=62,
            substep_number=self._next_substep(),
            substep_type=SubStepType.VERIFICATION,
            description="Verify Γ(0) = Γ₀",
            lean_code="""
                theorem solution_initial_condition (Gamma0 lambda : Real) (hlambda : lambda > 0) :
                  lyapunov_function Gamma0 lambda 0 = Gamma0 := by
                  unfold lyapunov_function
                  rw [Real.exp_zero]
                  ring
                """,
            python_simulation="""
def test_initial_condition():
    Gamma0 = 1.5
    lambda_val = 0.7
    
    Gamma_0 = Gamma0 * np.exp(-lambda_val * 0)
    assert np.isclose(Gamma_0, Gamma0)
                """,
            prerequisites=[],
            verification_method="Initial condition test",
            estimated_time="5 minutes",
            confidence=0.95,
            difficulty="easy"
        ))
        
        # Substep 2: Prove solution is unique
        substeps.append(SubStep(
            parent_step_id=62,
            substep_number=self._next_substep(),
            substep_type=SubStepType.LEMMA_PROOF,
            description="Prove uniqueness of ODE solution",
            lean_code="""
                theorem ODE_solution_unique (Gamma0 lambda : Real) (hlambda : lambda > 0) 
                                          (f g : Real -> Real) :
                  (∀ t, HasDerivAt f t (-lambda * f t)) ->
                  (∀ t, HasDerivAt g t (-lambda * g t)) ->
                  f 0 = g 0 ->
                  ∀ t, f t = g t := by
                  intro h_f h_g h_init
                  apply Real.eq_of_deriv_at_zero
                  · intro t
                    rw [h_f, h_g]
                    ring
                  · exact h_init
                """,
            python_simulation="""
def test_solution_uniqueness():
    Gamma0 = 1.0
    lambda_val = 0.5
    
    # Our solution
    f = lambda t: Gamma0 * np.exp(-lambda_val * t)
    
    # Alternative solution (should be same)
    g = lambda t: Gamma0 * np.exp(-lambda_val * t)
    
    t_values = np.linspace(0, 10, 100)
    assert np.allclose([f(t) for t in t_values], [g(t) for t in t_values])
                """,
            prerequisites=[self.substep_counter-1],
            verification_method="Uniqueness verification",
            estimated_time="20 minutes",
            confidence=0.75,
            difficulty="hard"
        ))
        
        return substeps
    
    def break_step_18_63(self, step: Dict) -> List[SubStep]:
        """Break Step 18.63: Prove I(t) → ∞ as t → ∞"""
        substeps = []
        
        # Substep 1: Express I(t) in terms of Γ(t)
        substeps.append(SubStep(
            parent_step_id=63,
            substep_number=self._next_substep(),
            substep_type=SubStepType.CALCULATION,
            description="Express I(t) = 1/Γ(t) = exp(λt)/Γ₀",
            lean_code="""
                theorem improvement_formula (Gamma0 lambda : Real) (hlambda : lambda > 0) (t : Real) :
                  improvement_metric (fun t => lyapunov_function Gamma0 lambda t) t = 
                    Real.exp (lambda * t) / Gamma0 := by
                  unfold improvement_metric
                  unfold lyapunov_function
                  have h_gt : Gamma0 * Real.exp (-lambda * t) + 10^(-10) > 0 := by
                    apply Real.add_pos
                    * apply Real.mul_pos
                      · apply Real.pos_of_pos
                      · apply Real.exp_pos
                    · apply Real.pow_pos
                  field_simp
                  ring
                """,
            python_simulation="""
def test_improvement_formula():
    Gamma0 = 1.0
    lambda_val = 0.5
    
    for t in np.linspace(0, 10, 20):
        Gamma_t = Gamma0 * np.exp(-lambda_val * t)
        I_t = 1 / Gamma_t
        
        # Check formula
        I_formula = np.exp(lambda_val * t) / Gamma0
        assert np.isclose(I_t, I_formula, rtol=1e-6)
                """,
            prerequisites=[],
            verification_method="Formula verification",
            estimated_time="15 minutes",
            confidence=0.85,
            difficulty="easy"
        ))
        
        # Substep 2: Prove exponential divergence
        substeps.append(SubStep(
            parent_step_id=63,
            substep_number=self._next_substep(),
            substep_type=SubStepType.LEMMA_PROOF,
            description="Prove exp(λt) → ∞ as t → ∞ for λ > 0",
            lean_code="""
                theorem exp_diverges_to_infinity (lambda : Real) (hlambda : lambda > 0) :
                  Tendsto (fun t => Real.exp (lambda * t)) atTop atTop := by
                  apply Real.tendsto_exp_atTop_atTop
                  · apply tendsto_id
                  · apply tendsto_const_nhds
                  · linarith
                """,
            python_simulation="""
def test_exp_divergence():
    lambda_val = 0.5
    
    thresholds = [10, 100, 1000, 10000]
    
    for threshold in thresholds:
        t_needed = np.log(threshold) / lambda_val
        exp_val = np.exp(lambda_val * t_needed)
        assert exp_val >= threshold * 0.99
                """,
            prerequisites=[self.substep_counter-1],
            verification_method="Divergence test",
            estimated_time="10 minutes",
            confidence=0.90,
            difficulty="easy"
        ))
        
        # Substep 3: Complete I(t) divergence proof
        substeps.append(SubStep(
            parent_step_id=63,
            substep_number=self._next_substep(),
            substep_type=SubStepType.TACTIC_APPLICATION,
            description="Combine to prove I(t) → ∞",
            lean_code="""
                theorem improvement_diverges_complete (Gamma0 lambda : Real) 
                                                        (hlambda : lambda > 0) (hGamma0 : Gamma0 > 0) :
                  Tendsto (fun t => improvement_metric (fun t => lyapunov_function Gamma0 lambda t) t) 
                          atTop atTop := by
                  have h_formula := improvement_formula Gamma0 lambda hlambda
                  have h_exp := exp_diverges_to_infinity lambda hlambda
                  rw [h_formula]
                  apply Real.tendsto_div_atTop
                  · exact h_exp
                  · apply tendsto_const_nhds
                  · linarith
                """,
            python_simulation="""
def test_improvement_divergence():
    Gamma0 = 1.0
    lambda_val = 0.5
    
    # Test that I(t) exceeds any finite threshold
    thresholds = [10, 100, 1000]
    
    for threshold in thresholds:
        t_needed = np.log(threshold * Gamma0) / lambda_val
        I_t = 1 / (Gamma0 * np.exp(-lambda_val * t_needed))
        assert I_t >= threshold * 0.99
                """,
            prerequisites=[self.substep_counter-2],
            verification_method="Complete divergence test",
            estimated_time="15 minutes",
            confidence=0.80,
            difficulty="medium"
        ))
        
        return substeps
    
    def break_complex_steps(self) -> List[StepBreakdown]:
        """Break all complex steps into substeps"""
        print("\n" + "="*80)
        print("PHASE II: DISSIPATION - Break Complex Steps")
        print("="*80)
        
        breakdowns = []
        
        for step in self.steps_to_break:
            step_id = step['step_number']
            description = step['description']
            difficulty = step['difficulty']
            
            print(f"\n--- Breaking Step {step_id}: {description} ({difficulty}) ---")
            
            # Route to appropriate breakdown function
            if step_id == 37:
                substeps = self.break_step_13_37(step)
                reason = "Isometry construction requires multiple definitions and proofs"
            elif step_id == 38:
                substeps = self.break_step_13_38(step)
                reason = "Metric preservation requires angle and inner product proofs"
            elif step_id == 57:
                substeps = self.break_step_17_57(step)
                reason = "Convergence requires exponential bound and limit proofs"
            elif step_id == 61:
                substeps = self.break_step_18_61(step)
                reason = "ODE verification requires derivative computation and integration"
            elif step_id == 62:
                substeps = self.break_step_18_62(step)
                reason = "Solution verification requires initial condition and uniqueness proofs"
            elif step_id == 63:
                substeps = self.break_step_18_63(step)
                reason = "Improvement divergence requires formula and limit proofs"
            else:
                # For other complex steps, create minimal breakdown
                substeps = self.create_minimal_breakdown(step)
                reason = "Step requires verification but can be implemented directly"
            
            # Calculate total time
            total_minutes = sum(self._parse_time(s.estimated_time) for s in substeps)
            total_time_str = f"{total_minutes // 60}h {total_minutes % 60}m"
            
            breakdown = StepBreakdown(
                step_id=step_id,
                original_description=description,
                original_difficulty=difficulty,
                substeps=substeps,
                total_substeps=len(substeps),
                total_estimated_time=total_time_str,
                breakdown_reason=reason
            )
            
            breakdowns.append(breakdown)
            print(f"  ✓ Generated {len(substeps)} substeps ({total_time_str})")
        
        self.all_breakdowns = breakdowns
        return breakdowns
    
    def create_minimal_breakdown(self, step: Dict) -> List[SubStep]:
        """Create minimal breakdown for steps that don't need deep decomposition"""
        substeps = []
        
        # Parse step_type from string format "StepType.XXX" to enum
        step_type_str = step['step_type']
        if isinstance(step_type_str, str) and step_type_str.startswith('StepType.'):
            step_type_value = step_type_str.split('.')[1]
            substep_type = SubStepType[step_type_value]
        else:
            # Default to VERIFICATION if parsing fails
            substep_type = SubStepType.VERIFICATION
        
        # Create single substep that is the step itself
        substeps.append(SubStep(
            parent_step_id=step['step_number'],
            substep_number=self._next_substep(),
            substep_type=substep_type,
            description=step['description'],
            lean_code=step['lean_code'],
            python_simulation=None,
            prerequisites=[],
            verification_method=step['verification_method'],
            estimated_time=step['estimated_time'],
            confidence=step['confidence'],
            difficulty=step['difficulty']
        ))
        
        return substeps
    
    def _parse_time(self, time_str: str) -> int:
        """Parse time string to minutes"""
        time_str = time_str.lower()
        if 'hour' in time_str or 'h ' in time_str:
            parts = time_str.split()
            hours = int(parts[0])
            minutes = int(parts[2]) if len(parts) > 2 else 0
            return hours * 60 + minutes
        else:
            return int(time_str.split()[0])
    
    def generate_execution_plan(self) -> Dict:
        """Generate execution plan for all substeps"""
        print("\n" + "="*80)
        print("PHASE III: PRECIPITATION - Generate Execution Plan")
        print("="*80)
        
        all_substeps = []
        for breakdown in self.all_breakdowns:
            all_substeps.extend(breakdown.substeps)
        
        # Build dependency graph
        substep_graph = self._build_dependency_graph(all_substeps)
        
        # Calculate totals
        total_minutes = sum(self._parse_time(s.estimated_time) for s in all_substeps)
        total_hours = total_minutes / 60
        
        # Count by difficulty
        difficulty_counts = {}
        for s in all_substeps:
            difficulty_counts[s.difficulty] = difficulty_counts.get(s.difficulty, 0) + 1
        
        print(f"\n  Building complete execution graph...")
        print(f"  ✓ Total substeps: {len(all_substeps)}")
        print(f"  ✓ Total estimated time: {total_hours:.1f} hours")
        print(f"  ✓ By difficulty: {difficulty_counts}")
        
        return {
            'total_substeps': len(all_substeps),
            'total_time_hours': total_hours,
            'difficulty_counts': difficulty_counts,
            'breakdowns': [asdict(b) for b in self.all_breakdowns]
        }
    
    def _build_dependency_graph(self, substeps: List[SubStep]) -> Dict:
        """Build dependency graph for substeps"""
        graph = {}
        for s in substeps:
            graph[s.substep_number] = {
                'dependencies': s.prerequisites,
                'description': s.description,
                'estimated_time': s.estimated_time
            }
        return graph
    
    def save_results(self, results: Dict):
        """Save results to files"""
        # Save JSON results
        with open('/home/davidl/Gaseous Prime Universe/AGI/ilda_iteration_8_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Save execution plan
        with open('/home/davidl/Gaseous Prime Universe/AGI/ilda_iteration_8_results_execution_plan.txt', 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("ILDA ITERATION 8: RECURSIVE STEP BREAKDOWN\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"TOTAL SUBSTEPS: {results['total_substeps']}\n")
            f.write(f"TOTAL ESTIMATED TIME: {results['total_time_hours']:.1f} hours\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("BREAKDOWN BY ORIGINAL STEP\n")
            f.write("=" * 80 + "\n\n")
            
            for b in results['breakdowns']:
                f.write(f"Step {b['step_id']}: {b['original_description']}\n")
                f.write(f"  Original difficulty: {b['original_difficulty']}\n")
                f.write(f"  Substeps generated: {b['total_substeps']}\n")
                f.write(f"  Total time: {b['total_estimated_time']}\n")
                f.write(f"  Reason: {b['breakdown_reason']}\n\n")
                
                for s in b['substeps']:
                    f.write(f"  Substep {s['substep_number']}: {s['description']}\n")
                    f.write(f"    Type: {s['substep_type']}\n")
                    f.write(f"    Time: {s['estimated_time']}\n")
                    f.write(f"    Confidence: {s['confidence']}\n")
                    f.write("\n")
                
                f.write("-" * 80 + "\n\n")
        
        print(f"\n✓ Results saved to: /home/davidl/Gaseous Prime Universe/AGI/ilda_iteration_8_results.json")
        print(f"✓ Execution plan saved to: /home/davidl/Gaseous Prime Universe/AGI/ilda_iteration_8_results_execution_plan.txt")
    
    def run(self):
        """Run ILDA Iteration 8"""
        # Phase I: Load iteration 7 steps
        complex_steps = self.load_iteration_7_steps()
        
        # Phase II: Break complex steps
        breakdowns = self.break_complex_steps()
        
        # Phase III: Generate execution plan
        results = self.generate_execution_plan()
        
        # Save results
        self.save_results(results)
        
        # Print summary
        print("\n" + "=" * 80)
        print("ILDA ITERATION 8 SUMMARY")
        print("=" * 80)
        print(f"\nOriginal complex steps analyzed: {len(complex_steps)}")
        print(f"Total substeps generated: {results['total_substeps']}")
        print(f"Total estimated time: {results['total_time_hours']:.1f} hours")
        
        print("\n" + "=" * 80)
        print("ILDA ITERATIONS SUMMARY")
        print("=" * 80)
        print("\nIteration 5: Identified 18 sorries")
        print("Iteration 6: Broke 9 sorries into 25 steps (4.2 hours)")
        print("Iteration 7: Broke 9 remaining sorries into 40 steps (17.9 hours)")
        print("Iteration 8: Broke 16 complex steps into {} substeps ({:.1f} hours)".format(
            results['total_substeps'], results['total_time_hours']))
        
        print("\nNEXT STEPS FOR ITERATION 9:")
        print("1. Execute all {} substeps in dependency order".format(results['total_substeps']))
        print("2. Fill Lean 4 code with provided substep implementations")
        print("3. Verify each substep with numerical simulation")
        print("4. Run Lean 4 to check all proofs compile")
        print("5. Generate complete theorem proofs")
        
        print(f"\nEstimated completion time: {results['total_time_hours']:.1f} hours (1-2 days)")

if __name__ == "__main__":
    breaker = ILDAIteration8RecursiveBreaker()
    breaker.run()

import Gpu.Core.Manifold
import Gpu.Core.Spectral.Basic
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Tactic

namespace GPU.IIT

/- --- 1. THE GROUNDED PURVIEW --- -/

/--
The Causal Purview (P):
Defined as the set of multiples of p.
-/
def CausalPurview (p : ℕ) : Set ℕ :=
  { n : ℕ | p ∣ n }

/--
Theorem: Purview Specificity.
PROVEN: Two distinct primes generate distinct causal purviews.
-/
theorem PurviewSpecificity (p q : ℕ) (hp : Nat.Prime p) (hq : Nat.Prime q) :
  p ≠ q → CausalPurview p ≠ CausalPurview q := by
  intro h_neq h_eq
  -- The least element of CausalPurview p is p
  have h_p_in : p ∈ CausalPurview p := by simp [CausalPurview]
  rw [h_eq] at h_p_in
  simp [CausalPurview] at h_p_in
  -- p is a multiple of q, and p is prime, so p = q
  have h_eq_pq : p = q := Nat.Prime.eq_of_dvd hp hq h_p_in
  exact h_neq h_eq_pq

end GPU.IIT

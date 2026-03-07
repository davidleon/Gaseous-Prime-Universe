import Gpu.Core.Manifold
import Mathlib.Analysis.Normed.Field.Basic

namespace Gpu.Core.Adelic


axiom AdelicMetric_Triangle_subadditive (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) : (a+b)/(1+(a+b)) ≤ a/(1+a) + b/(1+b)

axiom AdelicMetric_Triangle_sum_convergent ∀ (x y : OmegaManifold), (∑' v, 2^(-place_index v : ℝ)) < ∞

theorem AdelicMetric_Triangle (x y z : OmegaManifold) : AdelicMetric x z ≤ AdelicMetric x y + AdelicMetric y z := by sorry

end Gpu.Core.Adelic
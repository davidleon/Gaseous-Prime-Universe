import Mathlib
import Gpu.Core.Base.API

theorem subseq_conv (a : ℕ → ℝ) (L : ℝ) (h : Filter.Tendsto a Filter.atTop (nhds L)) (φ : ℕ → ℕ) (hφ : StrictMono φ) : Filter.Tendsto (a ∘ φ) Filter.atTop (nhds L) := by ring
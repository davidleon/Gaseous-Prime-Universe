# Information Topology: An Exploratory Research Framework (GPU)

## ⚠️ Current Status: Alpha / Unproven Hypothesis
This repository contains a mathematical framework proposing connections between information theory and number theory. **None of the major conjectures (Collatz, Riemann, Twin Primes) are proven here.** 

The project consists of:
1.  **Definitions**: Initial Lean 4 types for operators like LSE and Decadic Metrics.
2.  **Axioms**: Unproven postulates used to define the theoretical "Laws" of the system.
3.  **Skeletons**: Lean 4 theorem statements for major conjectures, currently marked with `sorry` (unproven).
4.  **Simulations**: Python scripts providing numerical evidence for the underlying physical intuition.

## 🏗️ Project Architecture

### 1. [Core Formalization](./core_formalization/)
- **`Base/API.lean`**: Contains 3 `sorry` markers for analytic definitions (Zeta, L-functions).
- **`Fundamental/API.lean`**: Contains 1 verified theorem statement and 1 `sorry` for the Euler Product.
- **`Axioms.lean`**: Contains 4 fundamental postulates that are assumed without proof.

### 2. [Vision & Conjectures](./vision/)
- Theoretical notes and "proof proposals" that outline a *potential* path to solution. 
- **Disclaimer**: These are speculative research directions and should not be cited as mathematical results.

### 3. [Core Tools](./core_tools/)
- Empirical scripts used to test the hypothesis against finite numerical ranges.

---
*Last Audit: 2026.03.01 | Total Sorries in Core: 4 | Total Axioms in Core: 4*

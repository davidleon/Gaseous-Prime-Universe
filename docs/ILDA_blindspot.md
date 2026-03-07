# ILDA Blind Spots: Insolvable or Fundamentally Difficult Components

This document tracks components of the Collatz formalization that ILDA has identified as insolvable or requiring fundamental breakthroughs beyond current methodology.

## 2. Circular Dependency (CycleDriftRelation ↔ cycle_m_pos)

**Location**: `core_formalization/Gpu/Conjectures/Collatz/TheGap.lean:1165-1226`
**Lines with sorry**: 1173 (missing h_min parameter), 1281 (prove minimum element property), 1204 (CycleDriftRelation)

**Issue**: Mutual dependency between two lemmas:

- `CycleDriftRelation` (line 1165) calls `cycle_m_pos` to prove m > 0
- `cycle_m_pos` (line 1211) calls `CycleDriftRelation` in its proof (line 1215)

This creates an infinite regress:
```
CycleDriftRelation needs m > 0
  → calls cycle_m_pos
    → needs CycleDriftRelation (for contradiction proof)
      → needs m > 0
        → calls cycle_m_pos
          → ...
```

**Additional problem**: The call to `cycle_m_pos` at line 1173 is missing the `h_min` parameter, which is marked as "sorry -- requires min condition".

**Why it's insolvable**: This is a structural issue with the proof organization. The lemmas need to be refactored to break the circular dependency.

**Required breakthrough**: Refactor the proof structure:
1. Extract the m > 0 proof into a separate lemma that doesn't depend on CycleDriftRelation
2. Or restructure CycleDriftRelation to not require m > 0
3. Or prove both simultaneously using mutual induction

## 1. Induction Strategy Mismatch (drift_succ lemma)

**Location**: `core_formalization/Gpu/Conjectures/Collatz/TheGap.lean:1010-1090`
**Lines with sorry**: 1080 (even case), 1114 (odd case)

**Issue**: The `drift_succ` lemma attempts to prove by induction on iteration count, but the sum representation is parameterized by odd step count. This creates a fundamental mismatch:

- Induction hypothesis: m iterations → m odd steps
- Collatz reality: m iterations may have fewer than m odd steps (even steps)

**Even case problem**:
- LHS: n_m * 2^K = 3^m * n + Σ_{i=0}^{m-1} 3^{m-1-i} * 2^{a(i)}
- RHS (target): 3^{m+1} * n + Σ_{i=0}^{m} 3^{m-i} * 2^{a'(i)}
- But even step doesn't add an odd step, so m shouldn't become m+1
- Proof leads to contradiction: 0 = 2*3^m*n + 2*Σ + 2^{K+v} (impossible for positive terms)

**Odd case problem**:
- Has division by 2^K terms: 3^{m+1} * n/2^K + 3*Σ * 2^{a(i)-K}
- These don't simplify to match target structure without additional assumptions
- The +1 term from 3*n_m + 1 needs to be absorbed, but algebraic structure doesn't match

**Why it's insolvable**: The induction strategy assumes a 1:1 correspondence between iterations and odd steps, but Collatz map does not guarantee this. An even step (n/2^v) adds 1 iteration without adding any odd steps.

**Required breakthrough**: Reformulate induction to track both iteration count and odd step count simultaneously, or use a different induction strategy altogether (e.g., induction on total divisions count, or use generating functions).

## 2. Axiomatic Components

### 2.1 ComputerSearchLimit
**Location**: `TheGap.lean:77`
**Status**: Computational axiom - cannot be proven mathematically without computer verification
**Reason**: Based on Simons-de Weger exhaustive search up to k=3e8

### 2.2 continued_fraction_floor
**Location**: `TheGap.lean:154`
**Status**: Deep number-theoretic bound
**Reason**: Relates m/k ratio to exponential lower bound on n; requires transcendence theory

### 2.3 LMN_coefficient_matching
**Location**: `TheGap.lean:258`
**Status**: Baker's theorem coefficient
**Reason**: The constant 24.34 comes from Baker's theory of linear forms in logarithms; proving this requires deep transcendence number theory

## 3. Spectral Theory Components

### 3.1 weak_norm_contraction
**Location**: `StructuralProof.lean:424`
**Status**: Requires spectral gap proof for Collatz transfer operator
**Reason**: Need to prove Lasota-Yorke inequality and quasi-compactness for non-smooth map

### 3.2 NoDivergenceGoal
**Location**: `StructuralProof.lean:25`
**Status**: Functional analysis conjecture
**Reason**: Requires proving existence of spectral gap for transfer operator on infinite-dimensional space

## Summary

Total components identified as requiring fundamental breakthroughs: 6

- **Induction strategy**: 1 (fundamental reformulation needed)
- **Computational axioms**: 1 (requires computer verification)
- **Deep number theory**: 2 (transcendence theory, Baker's theorem)
- **Spectral theory**: 2 (operator theory on non-smooth systems)

These components represent the frontier of current mathematical knowledge. Proving them would require significant advances in transcendental number theory, operator theory, or a completely new approach to the Collatz problem.
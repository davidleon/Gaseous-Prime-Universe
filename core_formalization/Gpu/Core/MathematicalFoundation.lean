-- MathematicalFoundation.lean: Central module for Mathematical Foundation package
-- REFACTORED: Original 3666-line file split into modular components
--
-- Original file has been refactored into:
--   - MathematicalFoundation/OmegaManifold.lean (Omega manifold structure)
--   - MathematicalFoundation/ILDA.lean (ILDA decomposition operator)
--   - MathematicalFoundation/FuzzyLogic.lean (Fuzzy logic and extension principle)
--   - MathematicalFoundation/FuzzyManifold.lean (Fuzzy manifold geometry)
--   - MathematicalFoundation/FuzzyManifoldGeometry.lean (Geodesics and exponential maps)
--   - MathematicalFoundation/PhaseLocking.lean (Phase locking and discretization)
--   - MathematicalFoundation/GenerativeOmega.lean (Omega as spectrum of interference)
--
-- This file now serves as the main entry point, importing all refactored modules.

import Gpu.Core.MathematicalFoundation.MathematicalFoundation

-- Re-export all definitions for backward compatibility
open GPU

-- All types and definitions are now available through:
--   - OmegaManifold
--   - ILDA
--   - FuzzyLogic
--   - FuzzyManifold
--   - FuzzyManifoldGeometry
--   - PhaseLocking
--   - GenerativeOmega
-- MathematicalFoundation.lean: Main module importing all refactored components
-- This file serves as the central import point for the MathematicalFoundation package
-- The original large file has been refactored into modular components for better maintainability

import Gpu.Core.MathematicalFoundation.OmegaManifold
import Gpu.Core.MathematicalFoundation.ILDA
import Gpu.Core.MathematicalFoundation.FuzzyLogic
import Gpu.Core.MathematicalFoundation.FuzzyManifold
import Gpu.Core.MathematicalFoundation.FuzzyManifoldGeometry
import Gpu.Core.MathematicalFoundation.PhaseLocking
import Gpu.Core.MathematicalFoundation.GenerativeOmega

namespace GPU

-- Re-export key types and definitions for convenience
export OmegaManifold (OmegaManifold, compose, compositionIdentity)
export FuzzyLogic (FuzzySet, FuzzyRealLine, extensionPrinciple)
export FuzzyManifold (FuzzyLogicManifold, fuzzyMetric, TangentSpace, TangentVector)
export PhaseLocking (PhaseLockingCondition, LockedManifold, quantumPhaseLocking)
export GenerativeOmega (FuzzyState, interferenceOperator, StandingWave, ResonantMode)

end GPU
import Lake
open Lake DSL

package «primes» {
  -- add package configuration options here
}

@[default_target]
lean_lib «PrimeDistStatement» {
  -- add library configuration options here
}

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"
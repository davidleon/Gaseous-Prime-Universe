import Lake
open Lake DSL

package «gpu» {
}

lean_lib «Gpu» {
}

lean_lib «FamousProblems» {
}

lean_lib «PrimeDistStatement» {
}

@[default_target]
lean_exe «gpu» {
  root := `Main
}

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

import Lake
open Lake DSL

package join_operator {
  -- add package configuration options here
}

lean_lib «JoinOperator» {
  -- add library configuration options here
}

@[default_target]
lean_exe join_operator {
  root := `Main
}
# Tools

> **Legend.** `*` after a field name marks a property that is required by the JSON schema. For input parameters this means the caller must pass the value. For output fields it means the value is always present within its enclosing object. Nested `*` is scoped to the parent object's presence — required nested fields are only guaranteed when the optional parent object is emitted.

## DebuggerToolset

- [xdebug_control_session](tools/xdebug_control_session.md) — Controls the execution of a debug session.
- [xdebug_evaluate_expression](tools/xdebug_evaluate_expression.md) — Evaluates an expression in the context of the current stack frame.
- [xdebug_get_debugger_status](tools/xdebug_get_debugger_status.md) — Returns the current status of the debugger including all active debug sessions.
- [xdebug_get_frame_values](tools/xdebug_get_frame_values.md) — Returns the values visible in the specified stack frame as a tree structure.
- [xdebug_get_stack](tools/xdebug_get_stack.md) — Returns the call stack for a thread in the debug session.
- [xdebug_get_threads](tools/xdebug_get_threads.md) — Returns the list of threads in the debug session.
- [xdebug_get_value_by_path](tools/xdebug_get_value_by_path.md) — Gets the value of a nested object by following a path of property names.
- [xdebug_list_breakpoints](tools/xdebug_list_breakpoints.md) — Lists all breakpoints in the project or in a specific file.
- [xdebug_remove_breakpoint](tools/xdebug_remove_breakpoint.md) — Removes breakpoints filtered by owner and optional selectors.
- [xdebug_run_to_line](tools/xdebug_run_to_line.md) — Resumes execution to a target line.
- [xdebug_set_breakpoint](tools/xdebug_set_breakpoint.md) — Creates or updates a breakpoint or a logpoint (a non-suspending "Evaluate and log" breakpoint).
- [xdebug_set_variable](tools/xdebug_set_variable.md) — Mutates a variable value by path in the selected stack frame.
- [xdebug_start_debugger_session](tools/xdebug_start_debugger_session.md) — Start a debugger session for either an existing run configuration by name or a code location

## ExecutionToolset

- [execute_run_configuration](tools/execute_run_configuration.md) — Run either an existing run configuration by name or a temporary run configuration created from a code location (`filePath` + `line`) in the current project, then wait up to specified timeout for it to finish.
- [get_run_configurations](tools/get_run_configurations.md) — Returns either project run configurations or executable code locations, depending on the input.

## RiderDebuggerToolset

- [ignore_exception](tools/ignore_exception.md) — Stop the debugger from breaking on a given .NET exception type ("ignore" the exception).


# Rider MCP Tools — Reference

All tools: `mcp__<prefix>__<tool>`. **Never call without loading the schema first — use `ToolSearch(query: "select:mcp__<prefix>__<tool>")` before any call.**

---

## execute_tool mode

Some Rider MCP configurations expose only `execute_tool` instead of individual tools. In CLI mode, param names differ from direct-tool names — wrong names cause silent "Missing required parameters" failures.

**Detect mode:** After ToolSearch, if only `execute_tool` is returned → CLI mode. Call `ToolSearch(query: "select:mcp__<prefix>__execute_tool")` to get the live CLI schema.

---

## Search

### `search_symbol`
Semantic lookup — finds classes, methods, fields by name. Entry point when you know a symbol name but not its file.

### `search_text`
IDE-indexed full-text search. Prefer over rg/grep when IDE index, generated/reflected UE code, or unsaved state matters.

### `search_file`
Find files by glob pattern.

### `skill_search`
Unified search with explicit mode: file (glob), text (literal), or regex.

---

## Code Intelligence

### `get_symbol_info`
**Position-based** — read the file first to find the symbol's line/column. Use to confirm: nullable return, editor-only, threading guarantees, API contract.

### `analyze_calls`
Call hierarchy analysis. Supports C++, Java, Kotlin, Python, C#. If overloads match, returns disambiguation list — resubmit with full signature. If "No call hierarchy provider found" → fall back to Grep.

---

## Diagnostics

### `get_file_problems`
File-level errors and warnings. Fix all errors and warnings before building.

### `lint_files`
Batch lint across multiple files. Catches cross-file include violations and project-level style rules.

### `get_project_problems`
Project-level issues. Run after a successful build, filter to changed files.

### `post_edit_quality_check`
Post-edit gate. Runs reformat + lint in one call.

---

## Build

### `build_solution_start`
Start a build. Never use shell UBT calls — always use this.

### `build_solution_state`
Poll build status until complete.

---

## Run Configurations

### `get_run_configurations`
List available run configurations.

### `execute_run_configuration`
Launch a run configuration.

---

## UE Editor Connection

### `ue_status`
One-stop check: editor health + PIE state + recent logs. **Call this first** before any UE live-state tool. If not connected → RiderLink not loaded or editor not running.

### `ue_health`
Minimal connection check (no log fetch).

### `ue_get_logs`
Fetch UE editor logs with optional category/pattern/verbosity filter.

### `ue_play`
Control PIE (play/pause/resume/stop/frame/state).

---

## UE Python Runtime Inspection

### `ue_execute_python`
Run Python inside the live UE editor. PIE must be running for game-state queries.  
**Critical: single-line constraint** — no `\n`, use `;` and comprehensions.  
`GameplayTag` constructor: positional only — `unreal.GameplayTag("Tag.Name")`, not keyword arg.

---

## UE Asset & Tag Tools

### `search_assets`
Search UE assets by name, base class, or package path.

### `search_tags`
Search gameplay tags by prefix.

### `get_class_hierarchy`
Get all Blueprint assets inheriting from a C++ class.

### `get_asset_properties`
Read UPROPERTY values from a `.uasset` file. Requires editor running.

### `find_default_value_overrides`
Find every asset that overrides a reflected field's default. Works **without** the editor running.

---

## UE Input Simulation

### `simulate_input`
Simulate player input. Each mode has its own set of named params.

---

## Debugger (xdebug)

### `xdebug_set_breakpoint`
Set standard, conditional, or logpoint breakpoints.

### `xdebug_get_debugger_status`
Get current debugger state.

### `xdebug_get_stack`
Get current call stack.

### `xdebug_get_frame_values`
Get local variable values for a stack frame.

### `xdebug_evaluate_expression`
Evaluate an expression in the current debug context.

### `xdebug_control_session`
Step over/into/out, resume, pause, or stop the debug session.

### `xdebug_run_to_line`
Run execution to a specific file/line.

### `xdebug_start_debugger_session`
Start a debug session from a run configuration.

---

## Refactoring

### `rename_refactoring`
Rename a symbol project-wide.

### `extract_method`
Extract a code range into a new method.

### `safe_delete`
Delete a symbol only if it has no remaining usages.

---

## Viewport & Screenshot

### `take_screenshot`
Capture editor, game, or asset screenshot.

### `viewport_camera`
Get, set, move, or focus the viewport camera.

### `spawn_actor`
Spawn an actor in the editor.

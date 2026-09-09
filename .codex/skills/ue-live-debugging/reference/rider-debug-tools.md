# Rider MCP — Live Debugging Workflow Patterns

For full tool parameter reference see `reference/rider-mcp-tools.md`.

---

## Debugging Session Patterns

### "I have a crash callstack, where do I start?"

1. `ue_status` — check editor connection and recent logs
2. `search_symbol` — locate the top project function in the callstack
3. Read the file using standard Read tool — find the crashing line
4. `analyze_calls` — trace callers; fall back to Grep if provider not found
5. `get_file_problems` on the crashing file — Rider may flag the root cause
6. `get_symbol_info` at the symbol — verify API contract

### "I suspect function X is being called incorrectly"

1. `search_symbol` — locate the file
2. `analyze_calls` — find all callers
3. Read each caller using standard Read tool — check arguments
4. `get_file_problems` on suspect callers
5. `get_symbol_info` at X's declaration — verify expected contract

### "The bug is intermittent — can't reliably reproduce"

1. `search_text` for timer bindings and lambda captures near the suspect class
2. `get_file_problems` on the handler file — look for raw pointer captures
3. Add `ensure()` + `UE_LOG` at the suspect site using standard Edit tool
4. `build_solution_start` → reproduce → `ue_get_logs`

### "Works in editor, crashes in packaged build"

1. `search_text` for `WITH_EDITOR` in `*.cpp` and `*.h`
2. `get_symbol_info` at types in the crash path — check if editor-only
3. `search_text` for `GEditor` — doesn't exist in packages
4. `lint_files` on the affected files

### "Live PIE — inspect runtime state now"

1. `ue_status` — confirm PIE running
2. `ue_execute_python` with a single-line script to query game state

See `reference/ue-python-inspection.md` for ready-to-use GAS/ASC/stat-tag one-liners.

### "Set breakpoints and step through"

**Prerequisite — `DebugGame Editor` build required for game-module breakpoints.**  
In `Development Editor` the compiler inlines game code; breakpoints report "No executable code associated with this line." Verify the configuration before setting any breakpoint. If the response contains `breakpointErrorsTail` with that message, stop and ask the user to rebuild in `DebugGame Editor`.

1. `ue_status` — check editor connected
2. `xdebug_set_breakpoint` — check response for `breakpointErrorsTail` "No executable code" → if present STOP, rebuild needed
3. `ue_play` — start PIE if not running
4. Ask the user to trigger the action manually in the PIE viewport
5. `xdebug_get_debugger_status` — confirm paused
6. `xdebug_get_stack`
7. `xdebug_get_frame_values` — inspect local variables
8. `xdebug_evaluate_expression`
9. `xdebug_control_session`

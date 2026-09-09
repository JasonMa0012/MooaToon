---
name: ue-live-debugging
description: "Use when debugging UE C++ crashes, runtime bugs, or unexpected behavior with Rider MCP available. Value over bash/grep: analyze_calls traces C++ call hierarchies (ReSharper backend); get_file_problems surfaces IDE-detected issues; get_symbol_info confirms API contracts; xdebug_set_breakpoint sets live breakpoints; ue_execute_python queries live PIE state. DO NOT TRIGGER for: pure build errors with no runtime component, net-new feature work, Blueprint-only work. When Rider MCP is unavailable, runs in reduced mode — Bash/Grep only, IDE diagnostics skipped."
allowed-tools: Read Glob Grep Bash Write Edit ToolSearch
metadata:
  argument-hint: "[bug description, suspect function/class, or crash context]"
---

# UE Live Debugging

Rider MCP debugging workflow: find the suspect symbol, trace who calls it, see what the IDE already knows is wrong.

---

## GATE — mandatory checks before any debugging work

### 1. UE Project Check

Verify the current working directory contains a `.uproject` file:

```bash
find . -maxdepth 1 -name "*.uproject" | head -1
```

If **no `.uproject` found** → STOP.

> "This skill requires an Unreal Engine project (a `.uproject` file must be in the working directory). The current directory does not appear to be a UE project. Navigate to the project root and retry."

### 2. Task Is Debugging-Related Check

The task must involve **debugging or investigating a runtime or compile-time issue** in C++ or Blueprint code. If there is no debugging component → STOP and inform the user this skill only handles debugging.

### 3. Build Configuration Check — Required Before Setting C++ Breakpoints

Before placing any breakpoints in **game module** C++ code, verify the binary was compiled in `DebugGame Editor` (or `Debug Editor`). In `Development Editor` the compiler inlines and optimises away most function entry points — breakpoints silently fail with:

> "The breakpoint will not currently be hit. No executable code is associated with this line."

**How to check:** After `xdebug_set_breakpoint`, inspect the response for `breakpointErrorsTail` entries containing that message. If present → STOP. Instruct the user to switch Rider's build configuration to `DebugGame Editor` and rebuild before continuing. Do not attempt to fire the repro until the breakpoint is confirmed bound.

**Engine-only breakpoints** (RiderLink, UE core) are unaffected — this check applies only to the project's own game modules.

### 4. Rider MCP Availability Check

Check the `<system-reminder>` deferred-tool list for Rider MCP tools. Load live schemas with ToolSearch before calling any tool. Schemas are **authoritative for parameter names** — never guess. If `execute_tool` is the only tool returned, use CLI mode (see `reference/rider-mcp-tools.md — execute_tool mode`).

If **no Rider MCP tools appear in the deferred list**:

> "Rider MCP tools are unavailable. Open Rider with this project loaded and the MCP server enabled, then retry. Falling back to Bash/Grep — call hierarchy and IDE diagnostics will not run."

Proceed with Bash/Grep/Read only, skipping all `mcp__<prefix>__*` steps. Document that Rider intelligence steps were skipped.

---

## Path Selection

**Fast path** for targeted fixes — known function, single file, clear root cause:
1. Verify `.uproject` (Gate 1)
2. Locate the function with `search_symbol` or rg
3. Read the file using the standard Read tool; confirm the bug
4. Apply fix with the standard Edit tool
5. Run `get_file_problems` if Rider MCP is available
6. Build and verify

**Full workflow** for crash investigation, unknown root cause, GC/threading bugs, or multi-file changes → continue to Checklist below.

## Checklist

Use the agent's native planning/todo mechanism when available. For simple one-file tasks, keep the plan implicit and proceed directly. For complex investigations, track:

1. **GATE** — UE project check + task check + Rider prefix resolution
2. **Triage** — classify the entry point: crash dump, log error, or live repro
3. **Locate** — find the suspect symbol; read its definition and call hierarchy
4. **Analyze** — trace callers/callees; find IDE-detected problems on suspect files
5. **Instrument** — identify breakpoint locations; add targeted logging if needed
6. **Reproduce** — confirm the issue triggers at the identified location
7. **Fix** — apply the minimal correct fix using the standard Edit tool
8. **Verify** — build and confirm the issue no longer reproduces

---

## Workflow

**Search routing:** use rg/Grep for portable text discovery; use Rider `search_text`/`search_file` when IDE index, generated/reflected UE code, or unsaved editor state helps. Use Rider semantic tools (`search_symbol`, `analyze_calls`, `get_symbol_info`, `get_file_problems`, build) for code intelligence. `analyze_calls` supports C++ (ReSharper backend) — if it returns "No call hierarchy provider found", fall back to Grep.

### Step 0 — Triage: Classify the Entry Point

| Entry point | Go to |
|-------------|-------|
| Crash dump / `.dmp` + `.log` in `Saved/Crashes/` | **Crash Dump Analysis** (below) |
| Output log errors / warnings only | **Log Analysis** (below) |
| Reproducible runtime bug with known repro steps | Step 1 directly |
| Live PIE running — inspect game state now | **Live PIE Inspection** (below) |

#### Crash Dump Analysis

Find crash artifacts in `Saved/Crashes/` (editor) or the platform crash folder — see `reference/crash-patterns.md` for locations and minidump instructions.

**Read the crash log first:**
```bash
find Saved/Crashes -name "*.log" | sort -r | head -1 | xargs tail -100
```
Look for `Fatal error`, `Assertion failed`, `Unhandled Exception`, or `call stack` near the end.

**Identify the crash signature** from the callstack address pattern — see `reference/crash-patterns.md — Quick Diagnosis Table`.

**Map the callstack to source**: take the topmost non-engine frame and find it with `search_symbol`.

Continue from **Step 1** using that symbol.

#### Live PIE Inspection

When PIE is running, use `ue_execute_python` to query live game state before reading source files — often resolves the question in one call.

**Script must be a single line** — no `\n`, no indented blocks. Use `;` and comprehensions.  
See `reference/ue-python-inspection.md` for ready-to-use query patterns and API pitfalls.

Typical first queries (adapt to project-specific classes):
- World + player valid: `import unreal; w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world(); pc=unreal.GameplayStatics.get_player_controller(w,0); print(w,pc)`
- Pawn class: `...; p=pc.get_controlled_pawn(); print(p.get_class().get_name() if p else None)`
- ASC on PlayerState: `...; asc=pc.player_state.get_component_by_class(unreal.AbilitySystemComponent); print(asc.get_name() if asc else None)`
- Active gameplay tags: `...; print(list(asc.get_owned_gameplay_tags()))`

After confirming runtime state, continue from **Step 1** to locate the responsible source code.

#### Log Analysis

```bash
find Saved/Logs -name "*.log" | sort -r | head -1
grep -n "Fatal\|Error\|Assertion failed\|ensure(" Saved/Logs/<Project>.log | tail -50
grep -n "Warning" Saved/Logs/<Project>.log | grep -v "LogTemp\|LogSlate" | tail -30
```

See `reference/crash-patterns.md — Log Patterns` for common entries and root causes. Continue from **Step 1**.

---

### Step 1 — Locate the Suspect Code

Use `search_symbol` to find the suspect class or function. Read the source files using the standard Read tool.

If starting from a crash address or log string rather than a known symbol, use `search_text` restricted to `*.cpp`.

### Step 2 — Trace the Call Hierarchy

Use `analyze_calls` — it supports C++ via the ReSharper C++ backend.

If the tool returns "No call hierarchy provider found" (symbol not indexed), fall back to Grep to find callers. Read the function body directly to find callees.

See `reference/ue-debug-patterns.md — Call Hierarchy Analysis` for what to look for in results.

### Step 3 — Get Symbol Info for Context

`get_symbol_info` is position-based — use the standard Read tool first to find the symbol's exact line and column.

Use to confirm API contracts — whether a function is editor-only, can return nullptr, or has threading guarantees. Do not rely on training-data assumptions for version-specific UE APIs.

### Step 4 — Run IDE Diagnostics on Suspect Files

Run `get_file_problems` on all suspect files (`.h` and `.cpp`). For multiple files, use `lint_files`.

- **Error** — likely directly related to the bug; address first
- **Warning** — check if it matches the crash symptom
- **Hint / Info** — note for context; not blockers

### Step 5 — Set Breakpoints and Launch the Debugger

Do not just tell the user where to set breakpoints — **set them via MCP**. Pick the last point of known-good state, not the crash site.

**Load the required tools first** (if not already loaded):
```
ToolSearch(query: "select:mcp__<prefix>__xdebug_set_breakpoint,mcp__<prefix>__xdebug_get_debugger_status,mcp__<prefix>__xdebug_get_frame_values,mcp__<prefix>__xdebug_get_stack,mcp__<prefix>__ue_play,mcp__<prefix>__ue_status,mcp__<prefix>__execute_run_configuration,mcp__<prefix>__get_run_configurations")
```

**5a — Check editor and PIE state** using `ue_status`.
- If not connected → launch the editor using `get_run_configurations` then `execute_run_configuration`.
- If connected and PIE idle → proceed to 5b.
- If PIE already running → proceed to 5b directly.

**5b — Set breakpoints** using `xdebug_set_breakpoint`. Set standard, conditional, or logpoint breakpoints as appropriate. See `reference/ue-debug-patterns.md — Breakpoint Placement Strategies` for placement rules.

**5c — Start PIE** using `ue_play` if not already running.

**5d — Wait for breakpoint hit**, then inspect using `xdebug_get_debugger_status`, `xdebug_get_stack`, `xdebug_get_frame_values`.

### Step 6 — Add Targeted Instrumentation (if needed)

If a live debugger session is not feasible, add `UE_LOG` statements using the standard Edit tool.

See `reference/ue-debug-patterns.md — Instrumentation Rules`. After editing, run `get_file_problems` to confirm no new errors.

### Step 7 — Fix

Apply the fix using the standard Edit tool.

After editing: run `get_file_problems` on the changed file (and `.h` if touched). Fix the root cause, not the symptom — see `reference/ue-debug-patterns.md — Fix: Root Cause vs Symptom`.

### Step 8 — Build and Verify

Run `build_solution_start` and poll `build_solution_state` until complete.

After a successful build:
1. Reproduce the original issue — confirm it no longer occurs
2. Run `get_project_problems` on the changed module; address new warnings on your files
3. Remove any instrumentation logging added in Step 6
4. Use `reformat_file` on changed files

---

see: reference/rider-mcp-tools.md — ALL Rider MCP tools: complete parameter reference, execute_tool mode table, UE editor/asset/debugger tools
see: reference/rider-debug-tools.md — Debugging workflow patterns: crash callstack, intermittent bugs, packaged build crashes, live PIE inspection, breakpoint sequences
see: reference/ue-debug-patterns.md — UE debugging patterns: call hierarchy analysis, instrumentation rules, fix guidance, breakpoint placement, GC/threading patterns
see: reference/crash-patterns.md — Crash patterns: address signatures, GC crashes, assertion failures, async loading, Slate null widgets, log patterns
see: reference/ue-python-inspection.md — UE Python runtime inspection: single-line scripting rules, world/player/component access, GAS/stat-tag queries, GameplayTag API pitfalls, common errors

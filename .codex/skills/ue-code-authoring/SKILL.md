---
name: ue-code-authoring
description: "Use when writing or modifying UE C++ (classes, actors, components, subsystems, interfaces, function libraries) with Rider MCP available. Value over bash/grep: IDE diagnostics catch UHT/reflection errors and missing module deps without a full build; lint_files enforces cross-file consistency. DO NOT TRIGGER for: Blueprint-only tasks, editor automation with no C++. When Rider MCP is unavailable, runs in reduced mode — standard file tools only, IDE diagnostics skipped."
allowed-tools: Read Glob Grep Bash Write Edit ToolSearch
metadata:
  argument-hint: "[C++ class, component, or system to create/modify]"
---

# Code Author

Unreal Engine C++ authoring workflow backed by **Rider MCP** for IDE-grade code quality.  
Three additions over a plain editor approach: (1) Rider diagnostics catch issues before a full build, (2) `lint_files` enforces project-wide consistency, (3) `get_project_problems` surfaces cross-file issues invisible to grep.

---

## GATE — mandatory checks before any code is written

### 1. UE Project Check

Verify the current working directory contains a `.uproject` file:

```bash
find . -maxdepth 1 -name "*.uproject" | head -1
```

If **no `.uproject` found** → STOP.

> "This skill requires an Unreal Engine project (a `.uproject` file must be in the working directory). The current directory does not appear to be a UE project. Navigate to the project root and retry."

### 2. Task Is Coding-Related Check

The task must involve **writing or modifying C++ code**. If the request has no C++ authoring component → STOP and inform the user this skill only handles C++ source authoring.

### 3. Rider MCP Availability Check

Check the `<system-reminder>` deferred-tool list for Rider MCP tools. Load live schemas with ToolSearch before calling any tool. Schemas are **authoritative for parameter names** — never guess. If `execute_tool` is the only tool returned, use CLI mode (see `reference/rider-mcp-tools.md — execute_tool mode`).

If **no Rider MCP tools appear in the deferred list**:

> "Rider MCP tools are unavailable. Open Rider with this project loaded and the MCP server enabled, then retry. Falling back to standard file tools — IDE diagnostics will not run."

Proceed with standard tools (Read/Write/Edit/Grep/Bash) only, skipping all `mcp__<prefix>__*` steps. Document that quality steps were skipped.

---

## Path Selection

**Fast path** for small, scoped edits — one file, no reflection macro, module dependency, public API, replication, or UObject lifetime changes:
1. Verify `.uproject` (Gate 1)
2. Locate files with rg/Grep or Rider `search_symbol`/`search_text`
3. Read the nearest existing pattern (1–2 files)
4. Edit the minimum files
5. Run `get_file_problems` on changed files if Rider MCP is available
6. Show git diff

**Full workflow** when changing reflection macros, module dependencies, public APIs, replication, UObject lifetime, or multiple files → continue to Checklist below.

## Checklist

Use the agent's native planning/todo mechanism when available. For simple one-file tasks, keep the plan implicit and proceed directly. For complex changes, track:

1. **GATE** — UE project check + task check + Rider prefix resolution
2. **Clarify** — ask targeted questions if the request is ambiguous (skip if clear)
3. **Pre-flight** — read `.uproject`, `Build.cs`, existing patterns via Rider symbol search
4. **Write code** — create or modify `.h`/`.cpp` with standard Write/Edit tools
5. **Rider diagnostics** — `get_file_problems` per changed file; fix all errors and warnings
6. **Batch lint** *(if multiple files changed or new patterns introduced)* — `lint_files`; fix remaining issues
7. **Build** — `build_solution_start`; poll `build_solution_state` until done; fix errors
8. **Post-build quality** *(for non-trivial changes)* — `get_project_problems`; address Critical/Important
9. **Reformat** — `reformat_file` on each changed file

---

## Workflow

**Search routing:** use rg/Grep for portable text discovery; use Rider `search_text`/`search_file` when IDE index, generated/reflected UE code, unsaved editor state, or result compactness is likely to help. Use Rider semantic tools (`search_symbol`, `get_file_problems`, `lint_files`, build, `get_project_problems`) for code intelligence.

### Step 0 — Clarify (if ambiguous)

Skip if the request names a specific class, system, or file change.

Ask **one question at a time**, max two questions total:

- **"Is this for a multiplayer game?"** — affects `Replicated` properties, `GetLifetimeReplicatedProps`, authority guards
- **"Should this integrate with GAS?"** — affects `UAbilitySystemComponent`, `FGameplayTag` parameters, attribute access
- **"Is there an existing base class I should extend?"** — check with `search_symbol` before asking

### Step 1 — Pre-flight

Read project context before writing anything: `.uproject` file and `Source/<Module>/<Module>.Build.cs` using the standard Read tool.

Search for existing patterns using `search_symbol`. Browse the directory layout using Glob or `list_directory_tree`.

Read 1–2 existing files of the same type using the standard Read tool to match conventions.

**Determine from pre-flight:** `EngineAssociation` (for `BuildSettingsVersion`), module name and `Build.cs` deps, and the project's naming/include/UPROPERTY patterns.

### Step 2 — Write Code

**Create new files** using the standard Write tool.

**Modify existing files** using the standard Edit tool.

Follow conventions from pre-flight. See `reference/ue-cpp-conventions.md` for UE5 rules, naming prefixes, file placement, and module deps.

### Step 3 — Rider Diagnostics (per file)

After writing each file, run `get_file_problems` on it immediately.

**Act on every result:**
- **Error** → fix before proceeding; re-run `get_file_problems` to confirm clear
- **Warning** → fix unless it's a known intentional pattern (document why if skipping)
- **Hint / Info** → note for later; don't block on these

Iterate: edit → diagnose → edit until zero errors and zero warnings on all changed files.

### Step 4 — Batch Lint *(skip for isolated single-file fixes)*

If multiple files changed or new patterns were introduced, run `lint_files`.

Fix any issues surfaced here that `get_file_problems` missed (cross-file include violations, project-level style rules).

### Step 5 — Build

Compile via Rider using `build_solution_start` — do NOT shell-build or ask the user to rebuild manually.

Poll using `build_solution_state` until `state != "Running"`.

**On build failure:**
- Read the error output from `build_solution_state`
- Identify which file/line caused the error
- Fix with the standard Edit tool, re-run `get_file_problems` on the fixed file, then rebuild
- **Do NOT proceed to Step 6 with build errors outstanding**

### Step 6 — Post-Build Quality Gate

After a successful build, run `get_project_problems`. Filter results to files you changed. For each issue:
- **Error** → fix immediately (build would have caught these; if new, something is wrong)
- **Warning on your files** → fix unless intentionally deferred

### Step 7 — Reformat

Use `reformat_file` on every file you created or modified.

---

see: reference/rider-mcp-tools.md — ALL Rider MCP tools: complete parameter reference, execute_tool mode table, UE editor/asset/debugger tools
see: reference/rider-tools.md — Code authoring workflow patterns: fix-loop, quality pass, common lookups
see: reference/ue-cpp-conventions.md — UE5 C++ rules, naming prefixes, file placement, module dependencies, BuildSettingsVersion, generated header errors

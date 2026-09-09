---
name: ue-test-authoring
description: "Use when writing or modifying UE automated tests (Automation, CQTest, Functional, Gauntlet, LowLevel) with Rider MCP available. Value over bash/grep: IDE diagnostics catch test registration errors, wrong RunTest return type, and missing includes before a build; get_symbol_info verifies the API under test. DO NOT TRIGGER for: debugging existing test failures (use ue-live-debugging), Blueprint-only testing. When Rider MCP is unavailable, runs in reduced mode — standard file tools only, IDE diagnostics skipped."
allowed-tools: Read Glob Grep Bash Write Edit ToolSearch
metadata:
  argument-hint: "[test type, feature/system to test, or failing scenario]"
---

# UE Test Authoring

End-to-end workflow for writing Unreal Engine automated tests backed by **Rider MCP** for IDE-grade code quality.  
Three additions over plain test writing: (1) Rider diagnostics catch issues before a full build, (2) `lint_files` enforces consistency across test files, (3) `get_project_problems` surfaces cross-file issues invisible to grep.

---

## GATE — mandatory checks before any test code is written

### 1. UE Project Check

Verify the current working directory contains a `.uproject` file:

```bash
find . -maxdepth 1 -name "*.uproject" | head -1
```

If **no `.uproject` found** → STOP.

> "This skill requires an Unreal Engine project (a `.uproject` file must be in the working directory). The current directory does not appear to be a UE project. Navigate to the project root and retry."

### 2. Task Is Test-Authoring Check

The task must involve **writing or modifying test code**. If the user is asking about something that has no test authoring component — e.g. fixing a runtime bug, building the project, or changing non-test source files — clarify scope before proceeding.

If there is no test to write or modify → STOP and ask the user what test they want authored.

### 3. Rider MCP Availability Check

Check the `<system-reminder>` deferred-tool list for Rider MCP tools. Load live schemas with ToolSearch before calling any tool. Schemas are **authoritative for parameter names** — never guess. If `execute_tool` is the only tool returned, use CLI mode (see `reference/rider-mcp-tools.md — execute_tool mode`).

If **no Rider MCP tools appear in the deferred list**:

> "Rider MCP tools are unavailable. Open Rider with this project loaded and the MCP server enabled, then retry. Falling back to standard file tools — IDE diagnostics will not run."

Proceed with standard tools (Read/Write/Edit/Grep/Bash) only, skipping all `mcp__<prefix>__*` steps. Document that quality steps were skipped.

---

## Path Selection

**Fast path** for adding a single test case to an existing test file — no new module, no new framework, no `Build.cs` changes:
1. Verify `.uproject` (Gate 1)
2. Locate the existing test file with rg/Grep or Rider `search_text`
3. Read 1–2 existing test cases in the same file
4. Add the minimal test case using the standard Edit tool
5. Run `get_file_problems` on the changed file if Rider MCP is available
6. Show git diff

**Full workflow** when creating a new test module, adding a new framework, changing `Build.cs`, or modifying multiple test files → continue to Checklist below.

## Checklist

Use the agent's native planning/todo mechanism when available. For simple one-file tasks, keep the plan implicit and proceed directly. For complex changes, track:

1. **GATE** — UE project check + test task check + Rider prefix resolution
2. **Clarify** — ask targeted questions if the framework or scope is ambiguous (skip if clear)
3. **Select framework** — choose the right test framework using the decision guide below
4. **Pre-flight** — read `.uproject`, locate existing test modules, scan patterns via Rider
5. **Write test** — create or modify test `.h`/`.cpp` using framework patterns
6. **Rider diagnostics** — `get_file_problems` per changed file; fix all errors and warnings
7. **Batch lint** *(if multiple test files changed or new patterns introduced)* — `lint_files`; fix remaining issues
8. **Build** — `build_solution_start`; poll `build_solution_state` until done; fix errors
9. **Post-build quality** *(for non-trivial changes)* — `get_project_problems`; address Critical/Important
10. **Reformat** — `reformat_file` on each changed file

---

## Workflow

**Search routing:** use rg/Grep for portable text discovery; use Rider `search_text`/`search_file` when IDE index, generated/reflected UE code, unsaved editor state, or result compactness is likely to help. Use Rider semantic tools (`search_symbol`, `get_file_problems`, `lint_files`, build, `get_project_problems`) for code intelligence.

### Step 0 — Clarify (if ambiguous)

Skip if the request names a specific framework, class, or test scenario.

Ask **one question at a time**, max two questions total:

- **"Is this a pure logic test (no actors, no world) or does it need an in-game context?"** — determines Automation/CQTest vs Functional Test
- **"Does the test need to verify replication or server/client behavior?"** — affects CQTest `PIENetworkComponent` vs plain test
- **"Is there an existing test module I should add to, or should this be a new module?"** — check with `list_directory_tree` before asking

### Step 1 — Select Framework

Pick the minimal framework that covers the testing need. See `reference/ue-test-patterns.md — Framework Selection` for the decision matrix.

### Step 2 — Pre-flight

Read project context before writing any test: `.uproject` file and `Source/<TestModule>/<TestModule>.Build.cs` using the standard Read tool.

Find existing test modules and patterns using `search_text` (look for `IMPLEMENT_SIMPLE_AUTOMATION_TEST`, `TEST_CLASS`, `DEFINE_SPEC`). Use Glob or `list_directory_tree` to browse directory structure.

Use `search_symbol` to locate the module under test for `Build.cs` dependency lookup.

Read 1–2 existing test files in the same area using the standard Read tool to match conventions.

**Determine from pre-flight:** whether a test module exists (add to it vs. create new), which test macros the project uses (match them), and required `PrivateDependencyModuleNames`.

See `reference/ue-test-patterns.md — New Test Module Setup` if a new module is needed.

### Step 3 — Write Test

**Create new test module** (if none exists) — see `reference/ue-test-patterns.md — New Test Module Setup`.

**Create a new test file** using the standard Write tool.

**Modify an existing test file** using the standard Edit tool.

See `reference/ue-test-patterns.md` for ready-to-use patterns for each framework and critical pitfalls.

### Step 4 — Rider Diagnostics (per file)

After writing each file, run `get_file_problems` on it immediately.

**Act on every result:**
- **Error** → fix before proceeding; re-run `get_file_problems` to confirm clear
- **Warning** → fix unless it's a known intentional pattern (document why if skipping)
- **Hint / Info** → note for later; don't block on these

Iterate: edit → diagnose → edit until zero errors and zero warnings on all changed files.

### Step 5 — Batch Lint *(skip for isolated single-file test additions)*

If multiple test files changed or new patterns were introduced, run `lint_files`.

Fix any issues surfaced here that `get_file_problems` missed (cross-file include violations, project-level style rules).

### Step 6 — Build

Compile via Rider using `build_solution_start` — do NOT shell-build or ask the user to rebuild manually.

Poll using `build_solution_state` until `state != "Running"`.

**On build failure:**
- Read the error output from `build_solution_state`
- Identify which file/line caused the error
- Fix with the standard Edit tool, re-run `get_file_problems` on the fixed file, then rebuild
- **Do NOT proceed to Step 7 with build errors outstanding**

### Step 7 — Post-Build Quality Gate *(skip for small test additions)*

For non-trivial changes, run `get_project_problems`. Filter results to files you changed. For each issue:
- **Error** → fix immediately
- **Warning on your files** → fix unless intentionally deferred

### Step 8 — Reformat

Use `reformat_file` on every file you created or modified.

---

see: reference/rider-mcp-tools.md — ALL Rider MCP tools: complete parameter reference, execute_tool mode table, UE editor/asset/debugger tools
see: reference/rider-tools.md — Test authoring workflow patterns: fix-loop, common lookups, test discovery
see: reference/ue-test-patterns.md — Framework patterns (Automation, CQTest, Functional, Gauntlet, LowLevel), new module setup, critical pitfalls

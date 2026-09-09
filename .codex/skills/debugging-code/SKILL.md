---
name: debugging-code
description: Use for debugger-driven runtime root-cause analysis in Rider-supported solutions and projects, including .NET/C#, F#, VB, C++, Unity, Unreal Engine, and other GameDev or mixed-language projects. Trigger when runtime state or control-flow evidence is needed — actual values, branch taken, call order, thread context, whether execution reaches a chosen line — and cannot be derived confidently from source or logs; when pinning the relevant path would otherwise mean reading many files or tracing a deep call chain; or on an explicit request to debug, set breakpoints, step, or inspect runtime values. Do not use for compile-time or syntax errors, source-obvious bugs, failures already pinpointed by logs/tests, or code merely named debug/Debugger.
allowed-tools: execute_tool
---

# Code Debugging

Debugger-first runtime root-cause analysis for solutions opened in Rider, including C#, C++, F#, VB, Unreal Engine, and other GameDev projects.

Invoke every tool through `execute_tool(command="<tool> --arg value ...")`. Do not call the underlying handles directly. Read `reference/tools.md` only for the specific tool you are about to call; do not pre-load the whole tree.

## Goal
Use debugger evidence to answer concrete runtime questions when static code reading is not enough, or to confirm ideas or results from static analysis — including whether execution reaches or does not reach an agent-selected code location via a breakpoint or tracepoint.

## When To Use This Skill
Use this skill when at least one of the following is true:
- runtime state or control-flow evidence is needed (actual values, branch taken, call order, thread context, or whether execution reaches a chosen location), and it cannot be derived confidently from source/logs;
- finding the relevant path would otherwise require reading many files or tracing a long call chain manually;
- the user explicitly asks to use the debugger (breakpoints, stepping, inspect values, debugger session).

If the user manually activates or refers to this skill, treat that as an explicit request to launch and use the debugger when the required tools are available; do not reduce it to a conceptual discussion.

Skip the debugger when any of these holds (use static analysis or log inspection):
- a compile-time / syntax error is visible in source or in the build output;
- the cause is visible without running the code (typo, wrong overload, obvious null-receiver, wrong argument count);
- a single-file logic bug with all state visible at source level;
- a failing test message or log already pinpoints the offending line and value.

## Disambiguation
If the codebase domain contains debug-related concepts, reason explicitly about whether the user is talking about their code or actually asking you to launch the debugger. Do not treat identifiers, features, flags, or log categories named `debug`/`Debugger` — including `System.Diagnostics.Debug` or a `Debug` build configuration — as a debugger request by default.

## Activation Gate (tool availability)
Use this skill only when the debugger MCP tools are available in the current session. Minimum required set:
- `xdebug_set_breakpoint`
- `xdebug_start_debugger_session`
- `xdebug_control_session`
- `xdebug_get_stack`
- at least one value tool: `xdebug_get_frame_values`, `xdebug_get_value_by_path`, or `xdebug_evaluate_expression`
- `get_run_configurations`

If this minimum set is not available: state the blocker explicitly, do not force a debugger workflow, and switch to the best fallback. All tools are documented in [reference/tools.md](reference/tools.md).

## Initial Triage Before Debugging
Start with minimal static triage (error text, stack trace, nearby source). Start debugger work when one of these is true: static analysis leaves multiple plausible runtime hypotheses; deciding between them requires concrete runtime values or exact control flow; stepping through the code is cheaper than reading a large cross-file path; or the user explicitly requested debugger actions.

Before starting a new run, assess whether a current relevant session can be reused. Set the first breakpoint early and collect concrete evidence before making runtime-behavior changes.

## Mandatory Runtime Evidence
Before code edits for runtime-behavior issues (when debugger evidence is available), collect at minimum:
- the paused location (file/line) from a suspended session;
- the top call path via `xdebug_get_stack`;
- when reachability is part of the question, evidence that execution did or did not hit an explicitly chosen breakpoint or tracepoint;
- at least one concrete runtime value via `xdebug_get_frame_values`, `xdebug_get_value_by_path`, or `xdebug_evaluate_expression`.

Do not assert runtime conclusions before this evidence is captured unless you have already stated a clear blocker.

## Reproduction Mode Selection
1. `AUTO`: the agent can run and rerun the scenario directly (run config, test, executable, endpoint). Use `xdebug_start_debugger_session` to launch with debugging, or `execute_run_configuration` for a non-debug run when you only need output or exit code.
2. `ASSISTED`: reproduction requires a user-only action (UI flow, auth, external dependency, hardware interaction).
3. `HYBRID`: try `AUTO` once or twice, then switch to `ASSISTED` if the failure does not reproduce.

If the candidate target is a test, default to `AUTO`. Never ask the user to reproduce before breakpoints are prepared.

Do not modify the user's project setup (NuGet packages, target framework, `.csproj`/`.sln`, run configurations, environment, credentials, services) without explicit approval. If a setup change is needed, state it as a blocker and wait for the user; treat a one-shot instruction as approval scoped to that action only.

## Test Task Execution
- To debug a test, pass `--filePath` + `--line` at the test definition (the `[Fact]` / `[Test]` / `[TestMethod]` method or case); the IDE resolves the framework (xUnit, NUnit, MSTest). For an existing test run configuration, use `--configurationName`. To run a test without debugging (for example, to confirm it fails before setting breakpoints), use `execute_run_configuration` with the same targeting.
- After triggering, inspect the resulting state with `execute_tool(command="xdebug_get_debugger_status")` and continue in the relevant session.
- Do not ask the user to rerun manually unless no available test-running path can reproduce it or reproduction requires user-only setup.

## Argument Hygiene
- Optional parameters are either omitted/null or set to a real value; omitted means omitted.
- Do not encode omitted optional parameters with placeholder strings such as `""`, `"/"`, `"__omit__"`, `"."`, or fake paths.
- Treat IDs and paths as opaque runtime data: copy them from tool outputs instead of synthesizing them.

## Session Binding
- Before preparing breakpoints or launching, call `execute_tool(command="xdebug_get_debugger_status")`.
- If an active relevant session exists, continue inside it instead of starting another.
- Capture the exact `sessionId` and reuse it in all session-scoped calls. If a session stops, times out, or disappears, refresh it via `xdebug_get_debugger_status` before reusing.
- After the paused location changes, do not reuse a stale `frameIndex` or `path`; re-read from the fresh `xdebug_get_stack`.

## Run Configuration Resolution
- Resolve `configurationName` from `get_run_configurations`; its `supportsDynamicLaunchOverrides` gates `--programArguments` / `--workingDirectory` / `--envs` (see [reference/tools/get_run_configurations.md](reference/tools/get_run_configurations.md)).
- Do not construct `dotnet` invocations yourself or push a test filter through `--programArguments` when the config does not support overrides; trust the run configuration, and use launch overrides only when they materially improve reproducibility or observability.

## Breakpoint Ownership And Hygiene
- Always start with `execute_tool(command="xdebug_list_breakpoints")` and treat the returned `owner` (`user` / `agent`) as source of truth.
- Build a baseline snapshot (`breakpointId -> enabled`) before modifying anything.
- Temporarily disable `owner=user` breakpoints not required for the current path via `execute_tool(command="xdebug_set_breakpoint --breakpointId <id> --enabled false")`; restore them only once, at the end of the debugger cycle.
- Avoid broad breakpoint churn between iterations. `xdebug_remove_breakpoint` defaults to `--owner agent`; for global cleanup run two calls: `--owner agent` then `--owner user`.

## Breakpoint Targeting Modes
`xdebug_set_breakpoint` has two mutually exclusive targeting modes (location vs `breakpointId`) — never mix them in one call, and in `breakpointId` mode pass the full desired state since provided fields become the result. After each call confirm the returned `lineText` matches the intended line. Modes and the full contract: [reference/tools/xdebug_set_breakpoint.md](reference/tools/xdebug_set_breakpoint.md).

## Noisy .NET Exceptions
When a session keeps suspending on an expected or handled exception that is not the one under investigation (a first-chance `System.OperationCanceledException`, for example), mute that single type with `execute_tool(command="ignore_exception --exceptionType System.OperationCanceledException")`, then `RESUME`. This sets the exception breakpoint's suspend policy to `NONE` and is **persistent** — it survives the session, exactly like unchecking the exception in the UI — so use it only for the type that is genuinely in the way, and never as a blanket way to silence exception stops. Prefer it over globally muting breakpoints, which would also drop the breakpoints you are relying on.

## Library And Decompiled Source Debugging
Breakpoints can be set in library and framework code. `read_file` reads external source files and the bundled decompiler output for assemblies (and SourceLink / PDB-resolved originals when available). To obtain a path:
- **stack frames**: `xdebug_get_stack` returns `file` paths, including paths into external assemblies — use the path exactly as returned;
- **symbol search**: `search_symbol(q="TypeName", include_external=true)` returns external / library symbol paths.

Always `read_file(file_path=<path>)` to find the exact line before setting a breakpoint in external code; never guess line numbers. Do not edit sources to insert `Console.WriteLine`; use a tracepoint instead.

## Choosing The Entry Point And First Breakpoint
Before the first run, explicitly choose the narrowest reproducible entry point (single test, focused run config, endpoint handler, command handler) and the first breakpoint at the earliest executable line where uncertainty becomes observable (branch decision, mapping boundary, state transition, dynamic dispatch, exception construction). If unsure, place at most 2 coarse breakpoints — one at the entry boundary, one at the suspected failure boundary — run once, then narrow.

## Core Workflow
Copy this checklist and tick items as you advance:

```
Debugger Run Progress:
- [ ] Scope the failure: exact error text, expected vs actual, 2-5 candidate anchors in the runtime path
- [ ] `xdebug_get_debugger_status` → reuse an active relevant session OR plan a new one
- [ ] Pick reproduction mode (AUTO / ASSISTED / HYBRID)
- [ ] Snapshot the breakpoint baseline; disable irrelevant user breakpoints
- [ ] Set initial breakpoints; verify `lineText` for each
- [ ] `xdebug_start_debugger_session ...` OR continue inside the existing session
- [ ] After a fresh start or RESUME: `xdebug_control_session --action WAIT_FOR_PAUSE`
- [ ] At each pause: `xdebug_get_stack` + values / eval (`xdebug_get_frame_values`, `xdebug_get_value_by_path`, `xdebug_evaluate_expression`)
- [ ] Decide next movement (`STEP_OVER` / `STEP_INTO` when evidence is nearby, OR a new breakpoint then `RESUME`)
- [ ] For tracepoints: `xdebug_control_session --action DRAIN_EVENTS`, then read the program's own output in the IDE's Debug tool window
- [ ] Stop on the first proven incorrect state transition or a stated blocker
- [ ] Wrap-up (cleanup + report)
```

Discipline applied at every step:
- Never `RESUME` without an explicitly named expected next stop; after every `RESUME`, always `WAIT_FOR_PAUSE`.
- On wait timeout: `PAUSE`, re-check enabled breakpoints and the expected path; after 2 consecutive timeouts, stop retrying that wait and expand breakpoint coverage.
- Never assert a root cause without concrete runtime values, and make no runtime-behavior edits before it is proven.
- Don't stop at a downstream symptom — climb frames / rewind to the producing state; if the needed location is already past, restart with an earlier breakpoint.
- When a frame points to external / decompiled code, `read_file` it and set deeper breakpoints there; don't skip it.

## Events And Tracepoints
- `breakpointErrorsTail` / `tracepointOutputsTail` (`xdebug_control_session`; see its reference) are **populated only by JVM-based debuggers**. Rider's debugger is not JVM-based, so do not rely on them: preflight a `--condition` with `xdebug_evaluate_expression` in a paused frame, and read tracepoint logging from the program's own output in the IDE's Debug tool window.
- For tracepoint-style logging without suspension, use `execute_tool(command="xdebug_set_breakpoint --filePath <path> --line <n> --isLogMessage true --suspendPolicy NONE")` (or `--isLogStack true`).

## Expression Discipline
`xdebug_evaluate_expression` and `xdebug_set_variable` take a raw expression in the current frame's language (C#, C++, F#, or VB) — see their reference files for the exact input rules. Beyond that contract:
- For global / static symbols in `--condition` and `--expression`, prefer fully-qualified names to avoid `Unresolved reference` caused by missing imports in the debugger expression context.
- The router parses the outer `execute_tool(command=...)` line with `ParametersListUtil`. When the expression contains double quotes, wrap the outer command string in single quotes; when it contains single quotes, wrap the outer in double quotes; avoid mixing both without escaping.
- If paused, preflight a risky `--condition` expression with `xdebug_evaluate_expression` before relying on it.

## Frame Climbing And Rewind
When stopped in a frame, inspect upper frames to reconstruct data provenance: identify who passed the current values and the earliest caller frame where state became incorrect. If the required location is already passed: restart the run with an earlier breakpoint (`AUTO`), or set an earlier breakpoint and ask the user to reproduce again (`ASSISTED`). Do not continue from a point already too late for the needed evidence. When a frame points to external / decompiled code, read it with `read_file` and set breakpoints there if needed to trace provenance deeper.

## Evidence Checklist
Before concluding, capture: the exact failing message/body; exception type and/or status code; the first location where state diverges from expected; concrete offending keys/values (and counts when relevant); the origin/provenance of wrong data; why the pipeline allowed it.

## Wrap-up
After debugging:
1. Clean up: `execute_tool(command="xdebug_remove_breakpoint --owner agent")`, restore disabled user breakpoints to their baseline, and `execute_tool(command="xdebug_control_session --action STOP")` if the session is no longer needed.
2. Report:
   - root cause in one sentence;
   - causal chain in 3-6 bullets;
   - runtime evidence with exact observed values;
   - code references (absolute path plus line);
   - if you fell back instead of debugging, the exact reason and what evidence is still missing.
3. Next action depends on the user's goal: if they asked for diagnosis only, conclude with the report and a recommended next step; if the task implies a code change, implement the fix based on the proven root cause.

## Tool Reference
See [reference/tools.md](reference/tools.md) for the signatures and parameter-by-parameter notes of the 15 `xdebug_*` MCP tools, the Rider-specific `ignore_exception`, and `get_run_configurations` / `execute_run_configuration`.

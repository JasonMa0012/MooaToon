---
name: refactoring-code
description: Use when semantic refactoring is needed in Rider-supported solutions and projects, including .NET/C#, F#, VB, C++, Unity, Unreal Engine, XAML, Razor, and other GameDev or mixed-language projects. Trigger when edits must update declarations and usages across IDE-resolved references — rename symbols, move types or namespaces, safe-delete unused code, extract interface/base class/method, change signatures, or reorganize namespaces. Do not use for file-only moves, config keys, strings, comments, prose-only edits, generated output, or logic changes with unchanged names/signatures.
allowed-tools: execute_tool
metadata:
  author: JetBrains
---

# Code Refactoring

Rider/ReSharper semantic refactorings on a solution open in Rider. Each tool resolves the target through the IDE index and rewrites **every** reference — `nameof`, `<see cref>`, XAML/Razor bindings, C++/Unreal — in one call. Always prefer the tool over a text edit: grep-and-replace *looks* done but silently misses these and leaves the solution broken.

## Invoke a tool

Call through `execute_tool` — the first token is the exact tool name, then `--flag value` pairs. Map each refactor to exactly one tool and issue it directly; the required flags are below, so no lookup is needed first.

```
execute_tool(command="rename_refactoring --filePath API/Services/OrderService.cs --symbolName OrderService --newName OrderProcessor")
```

| Refactor | Tool | Required flags |
|---|---|---|
| Rename a symbol + all usages | `rename_refactoring` | `--filePath --symbolName --newName` |
| Change a method signature (add/remove/reorder params) | `change_api_signature` | `--filePath --methodName --parameters` |
| Move a type to another namespace | `move_type_to_namespace` | `--filePath --typeName --targetNamespace` |
| Sync namespaces to folders | `reorganize_namespaces` | `--scope` |
| Delete a symbol only if unused | `safe_delete` | `--filePath --symbolName` |
| Extract an interface | `extract_interface` | `--filePath --typeName --interfaceName --members` |
| Extract a base class | `extract_base_class` | `--filePath --typeName --baseClassName --members` |
| Extract a method (C# only) | `extract_method` | `--filePath --startLine --endLine --methodName` |

- `--symbolName`/`--typeName` accept `Name` or `Type.Member`. Every tool also takes `--preview true` (analysis only, no writes) — add it first for public-API or many-call-site changes, then re-issue without it to apply.
- `change_api_signature`: **always** pass a **bare** `--methodName` (a qualified `Type.Member` can report "not found") **and** `--declaringType <FullyQualifiedType>` on the very first call — don't wait for an `ambiguous_method` error; the method is usually on an interface/impl pair, and `--declaringType` is harmless when it isn't. `--parameters` is a single-quoted JSON array = the **complete** new parameter list in order: an existing name is kept/moved, an omitted one is removed, a new name needs `type` (and optional `defaultValue` inserted at call sites). Disambiguate remaining overloads with `--currentSignature '["int","string"]'` (the CURRENT parameter types).
- `extract_interface`/`extract_base_class` `--members` is a single-quoted JSON array of member names, e.g. `'["IsMatch","Merge"]'` — not a comma-separated list.
- A multi-part request ("rename `X` **and** move it to `Y`") is one tool per step, in sequence — never folded into one call.
- Only for a tool not in the table, or a genuinely unclear parameter, read `reference/tools/<tool>.md` once (index: `reference/tools.md`). There is no `--describe`.

## Rules

1. **Use the tool; never hand-edit or fall back before a real call has run.** `Missing required parameters: …` (add them from the table), `Tool '<x>' not found` (wrong name — copy from the table), and conflict/ambiguous responses are all **fixable input mistakes** — correct the argument and retry. Fall back to a text edit only if `execute_tool` isn't in your toolset, or a call actually ran and failed in a way no input change can fix.
2. **Trust the success signal — never verify, never build.** On success the response's `touched`/`affects`/`files` counts **are** the confirmation. Do **not** re-read files, re-run `grep`/`rg`, diff the tree, or run the build/tests "to catch fallout" — a build never changes an already-applied refactor, it only burns tokens. Build or test **only** if the user explicitly asked. The one thing worth surfacing: a count of **1** for a type/method/property/field/namespace (declaration only, no callers).
3. **Don't retry blindly** — change an argument between calls. Flags are camelCase; pass real values or omit optional ones (no `""`/`"/"`/fake-path placeholders), and copy paths and names verbatim from `search_*` / `get_symbol_info`.
4. **Library / external symbols can't be refactored** — surface to the user; the change must be made upstream.

## Conflicts, ambiguity, limits

A non-empty `conflicts` list means **no files changed** (except `reorganize_namespaces`, whose conflicts are advisory and still apply). An `ambiguous`/`candidates` list means the name matched several symbols — narrow it (`Type.Member`, or the current overload types). Full conflict-kind handling, escalation thresholds, and known gaps (strings/comments, `<see cref>`, file-not-moved, call-site reflow) are in [reference/conflicts.md](reference/conflicts.md) — read it only when a response actually contains conflicts.

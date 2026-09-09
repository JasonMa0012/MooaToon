# Conflicts, ambiguity, and known limitations

Detailed handling for the cases SKILL.md summarizes. Read this only when a tool actually returns a `conflicts` or `ambiguous` list, or when you hit one of the known limitations below.

## Conflicts

Tools that rewrite or remove use sites (rename, safe-delete, the extract family) can refuse and report **conflicts**. A non-empty `conflicts` list always means **no files were touched**.

Each entry is `{kind, file, context}`: `kind` mirrors ReSharper's `ConflictType` (snake_case); `context` is the engine's localized description; `file` is the first occurrence's path, or `null` for a textual-only conflict or a clash with a compiled-only symbol.

| Kind | Meaning | Action |
|------|---------|--------|
| `same_name_conflict` | New name collides with an existing member in the same scope. | Pick a different name and retry. |
| `default_element_conflict` | Generic element-level conflict without a more specific category. | Read `context`; if it names a colliding member, treat like `same_name_conflict`, else escalate. |
| `cannot_update_usage_conflict` | A call site can't be rewritten safely — downstream code would break. | Escalate to user; do not auto-retry. |
| `cannot_remove`, `cannot_delete_safely`, `cannot_inline_usage_conflict`, `will_be_removed` | Engine refuses to remove/delete/inline/rewrite a use site. | Escalate to user; do not auto-retry. |
| `not_accessible` | The symbol becomes invisible from one or more use sites after the change. | Escalate to user — a visibility regression. |
| `will_be_made_public` | Access widens as a side-effect (e.g. promoted from private). | Narrate the trade-off to the user before retrying. |
| `hierarchy_conflict` | Override/implementation hierarchy clashes with the result. | Escalate to user; cross-type effect. |
| `text_only`, `default_conflict`, `invalid` | Generic textual conflict the engine couldn't categorise structurally. | Read `context`; decide from the message. |

Escalate to the user (instead of auto-deciding) when there are more than 5 conflicts, or any entry is `cannot_update_usage_conflict`, `cannot_remove`, `cannot_delete_safely`, `cannot_inline_usage_conflict`, `will_be_removed`, `not_accessible`, or `hierarchy_conflict`. For a rename, also escalate when `affects.callSites == 0` for a public/protected symbol — it usually means the query resolved to the wrong target.

## Ambiguity

A `--symbolName` can match more than one candidate; each carries `name`, `kind`, `fqn`, `file`, and `line`. Re-issue with a more specific `--symbolName` — use `TypeName.MemberName` rather than a bare short name (a bare name prioritises type-level entries and can miss the member you meant). The candidate list is capped at 5; if you see 5, the name is too broad — narrow it rather than expecting the full set.

For `change_api_signature`, overload ambiguity comes back as `{ok:false, candidates:[...], error:{kind:"ambiguous_method"}}` — disambiguate with `--currentSignature` (the current parameter types, e.g. `'["int","string"]'`) and/or `--declaringType`.

## Known limitations

Not reported in tool output:

- **String and comment occurrences** of an old name or namespace are not updated. Fix them with a regular edit pass afterward.
- **XML-doc `<see cref>` references**: a method rename rewrites `<see cref="Type.Method(int, int)"/>` to `<see cref="NewName"/>`, dropping the containing type and parameter list. Surface to the user after method renames and offer a separate edit pass.
- **Moving a type does not move its file** — only the namespace declaration and references change. If the user also wants the file relocated, do that as a separate file operation.
- **`change_api_signature` may reflow rewritten call sites onto long single lines.** This is cosmetic; do not spend a verification pass on it unless the user asked for formatting.

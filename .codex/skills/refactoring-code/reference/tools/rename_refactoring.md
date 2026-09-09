# rename_refactoring
Rename a symbol declared in the given file and all its usages across the solution, or analyze the rename without mutating files (preview=true).<br/>The symbol is resolved inside `filePath` via the language PSI, so this works for every language the IDE parses (C#, C++, …), not only .NET.<br/>Counts in `affects` come from the reference index, so they include `nameof(...)`, XML doc `<see cref>`, XAML `x:Name`, Razor, C++/Unreal, and other language-aware references.<br/>Pre-apply checks: newName must be a valid identifier for the target language; the backend applies language-specific escaping and validation.<br/>preview does NOT run conflict analysis — it resolves the symbol and counts `affects` only, so a clean preview can still fail on apply. `dryRun` is a deprecated alias of `preview`.<br/>filePath accepts an absolute or solution-relative path (paths from search_* output work as-is); response paths are solution-relative with '/' separators.<br/>Response: {ok, applied, touched, affects, files (first 20), moreFiles, conflicts, ambiguous, resolvedSymbol, note, error}.<br/>Outcomes:<br/>  * ok=true, applied=true, touched=N — rename applied; N = declarations + call sites the engine updated.<br/>  * ok=true, applied=false, touched=0 — preview succeeded; `affects` shows the blast radius the apply would touch.<br/>  * ok=false, conflicts=[…] — a conflict refused the rename; no files were touched. Adjust `newName`.<br/>  * ok=false, error={kind, hint} — kind is one of new_name_invalid, no_renamable_symbol, new_name_matches_current, symbol_invalidated, unknown.<br/>A blank filePath, symbolName or newName is an MCP error.<br/>Use preview=true to audit `affects` before committing on public API renames or any rename that touches many cross-language references.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| filePath* | string | Path to the file that declares the symbol (absolute or solution-relative). |
| symbolName* | string | Symbol to rename, as named in the file: "TypeName", "MemberName" or "TypeName.MemberName". |
| newName* | string | Target identifier. The backend applies language-specific escaping and validation. |
| preview | boolean | Analyze only: resolve the symbol and return `affects` without mutating any files. Does NOT run conflict analysis. |
| dryRun | boolean | Deprecated alias of preview. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| ok* | boolean |  |
| applied* | boolean |  |
| touched* | integer |  |
| affects | object? |  |
| &nbsp;&nbsp;files* | integer |  |
| &nbsp;&nbsp;callSites* | integer |  |
| files* | array[string] |  |
| moreFiles* | integer |  |
| conflicts* | array[object] |  |
| &nbsp;&nbsp;[].kind* | string |  |
| &nbsp;&nbsp;[].file | string? |  |
| &nbsp;&nbsp;[].context* | string |  |
| ambiguous | array[object] |  |
| &nbsp;&nbsp;[].name* | string |  |
| &nbsp;&nbsp;[].kind* | string |  |
| &nbsp;&nbsp;[].fqn | string? |  |
| &nbsp;&nbsp;[].file* | string |  |
| &nbsp;&nbsp;[].line* | integer |  |
| resolvedSymbol | object? |  |
| &nbsp;&nbsp;name* | string |  |
| &nbsp;&nbsp;kind* | string |  |
| &nbsp;&nbsp;fqn | string? |  |
| &nbsp;&nbsp;file* | string |  |
| &nbsp;&nbsp;line* | integer |  |
| note | string? |  |
| error | object? |  |
| &nbsp;&nbsp;kind* | string |  |
| &nbsp;&nbsp;hint | string? |  |

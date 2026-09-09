# safe_delete
symbolName accepts "TypeName", "MemberName" or "TypeName.MemberName".<br/>For an overridable member the whole override/implementation hierarchy is deleted with it.<br/>If the symbol still has usages, NOTHING is deleted: the response is {ok:false, applied:false, conflicts:[...]} — not an MCP error.<br/>preview=true runs the same full conflict analysis and reports what would be deleted (or which conflicts would block the deletion) without changing anything.<br/>filePath accepts an absolute or solution-relative path (paths from search_* output work as-is); response paths are solution-relative with '/' separators.<br/>Response: {ok, applied, deleted, files (first 20), moreFiles, conflicts}.<br/>File or symbol not found is an MCP error.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| filePath* | string | Path to the file containing the symbol (absolute or solution-relative). |
| symbolName* | string | Symbol to delete: "TypeName", "MemberName" or "TypeName.MemberName". |
| preview | boolean | Analyze only: run the full conflict analysis and report what would be deleted without mutating any files. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| ok* | boolean |  |
| applied* | boolean |  |
| deleted* | array[string] |  |
| files* | array[string] |  |
| moreFiles* | integer |  |
| conflicts* | array[object] |  |
| &nbsp;&nbsp;[].kind* | string |  |
| &nbsp;&nbsp;[].file | string? |  |
| &nbsp;&nbsp;[].context* | string |  |


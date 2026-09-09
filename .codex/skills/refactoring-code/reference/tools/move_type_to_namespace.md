# move_type_to_namespace
Set preview=true for a trial run with rollback: affects, files and conflicts are computed, nothing is kept.<br/>Conflicts refuse the refactoring (in preview: would refuse): {ok:false, applied:false, conflicts:[...]} — not an MCP error.<br/>filePath accepts an absolute or solution-relative path (paths from search_* output work as-is); response paths are solution-relative with '/' separators.<br/>Response: {ok, applied, affects:{files,callSites}, files (first 20), moreFiles, conflicts}.<br/>File or type not found is an MCP error.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| filePath* | string | Path to the file containing the type (absolute or solution-relative). |
| typeName* | string | Name of the type to move (e.g., class name, interface name). |
| targetNamespace* | string | Target namespace to move the type to (e.g., 'MyProject.NewNamespace'). |
| preview | boolean | Trial run with rollback: report affects, files and conflicts without keeping any changes. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| ok* | boolean |  |
| applied* | boolean |  |
| affects | object? |  |
| &nbsp;&nbsp;files* | integer |  |
| &nbsp;&nbsp;callSites* | integer |  |
| files* | array[string] |  |
| moreFiles* | integer |  |
| conflicts* | array[object] |  |
| &nbsp;&nbsp;[].kind* | string |  |
| &nbsp;&nbsp;[].file | string? |  |
| &nbsp;&nbsp;[].context* | string |  |


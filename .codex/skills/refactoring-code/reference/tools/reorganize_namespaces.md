# reorganize_namespaces
Scope is required: a project name or a folder path (absolute or solution-relative).<br/>Can touch many files - prefer folder-sized scopes over whole projects.<br/>preview=true performs a trial run with rollback: it reports which files would change, including any conflicts, without keeping changes.<br/>Unlike the other refactoring tools, conflicts here are ADVISORY and do not refuse: the engine adjusts every file it can<br/>and lists the problems it could not fix as conflicts (kind "conflict", description only). applied stays true.<br/>Response: {ok, applied, files (first 20, solution-relative, '/' separators), moreFiles, conflicts}.<br/>Total changed-file count = files.size + moreFiles.<br/>An unknown scope is an MCP error.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| scope* | string | Project name or folder path (absolute or solution-relative) to process. |
| preview | boolean | Trial run with rollback: report which files would change (and any conflicts) without keeping changes. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| ok* | boolean |  |
| applied* | boolean |  |
| files* | array[string] |  |
| moreFiles* | integer |  |
| conflicts* | array[object] |  |
| &nbsp;&nbsp;[].kind* | string |  |
| &nbsp;&nbsp;[].file | string? |  |
| &nbsp;&nbsp;[].context* | string |  |


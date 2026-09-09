# extract_interface
Implementations stay in the type. Fields and static members cannot be extracted to an interface.<br/>If any requested member cannot be extracted or does not exist, NOTHING is changed and an MCP error lists those members.<br/>Engine conflicts also change NOTHING but are returned as {ok:false, applied:false, conflicts:[...]} — not an MCP error.<br/>preview=true runs the same full conflict analysis and reports the would-be result without changing anything.<br/>filePath accepts an absolute or solution-relative path (paths from search_* output work as-is); response paths are solution-relative with '/' separators.<br/>Response: {ok, applied, extractedMembers, targetFile, newTypeText, files (first 20), moreFiles, conflicts}.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| filePath* | string | Path to the file containing the type (absolute or solution-relative). |
| typeName* | string | Name of the source type. |
| interfaceName* | string | Name of the new interface (e.g. 'IMyService'). |
| members* | array[string] | Names of members to include in the interface. |
| preview | boolean | Analyze only: run the full conflict analysis and report the would-be result without mutating any files. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| ok* | boolean |  |
| applied* | boolean |  |
| extractedMembers* | array[string] |  |
| targetFile | string? |  |
| newTypeText | string? |  |
| files* | array[string] |  |
| moreFiles* | integer |  |
| conflicts* | array[object] |  |
| &nbsp;&nbsp;[].kind* | string |  |
| &nbsp;&nbsp;[].file | string? |  |
| &nbsp;&nbsp;[].context* | string |  |


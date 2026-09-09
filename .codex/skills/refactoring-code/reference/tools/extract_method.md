# extract_method
The line range (1-based, inclusive) must cover a complete sequence of statements inside one member.<br/>Parameters, return value and static-ness are inferred automatically.<br/>For top-level statements, the backend may extract a local function when the target language supports it.<br/>preview=true performs a trial run with rollback and reports the resulting signature without keeping any changes.<br/>filePath accepts an absolute or solution-relative path (paths from search_* output work as-is); response paths are solution-relative with '/' separators.<br/>Response: {ok, applied, signature, isLocalFunction, files (first 20), moreFiles}.<br/>File not found, an invalid range or a non-extractable selection is an MCP error.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| filePath* | string | Path to the file (absolute or solution-relative). |
| startLine* | integer | First line of the statement range (1-based, inclusive). |
| endLine* | integer | Last line of the statement range (1-based, inclusive). |
| methodName* | string | Name for the new method. |
| preview | boolean | Analyze only: trial run with rollback, report the would-be signature without keeping any changes. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| ok* | boolean |  |
| applied* | boolean |  |
| signature | string? |  |
| isLocalFunction* | boolean |  |
| files* | array[string] |  |
| moreFiles* | integer |  |


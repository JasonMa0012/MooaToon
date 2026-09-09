# xdebug_get_threads
Use this tool to see all threads and their current status.<br/><br/>Preconditions:<br/>- Session must be suspended.<br/><br/>Next call:<br/>- Use `xdebug_get_stack` for the selected thread.<br/><br/>Pagination:<br/>- `offset`/`limit` are applied after collecting all stacks.<br/><br/>Ordering:<br/>- Active thread first.<br/>- Remaining threads are sorted by descending stack depth.<br/><br/>Schema fields: id, name, state, isCurrent, additionalInfo, additionalInfoTooltip, frameCount.<br/>`additionalInfo`/`additionalInfoTooltip` use additional display info when available.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| sessionId | string | Debug session ID. Use the current ID returned by `xdebug_get_debugger_status` or `xdebug_start_debugger_session`. If a session has stopped, timed out, or disappeared, refresh the session list before reusing an old ID. Format: uses session name as ID by default; if multiple sessions share the same name, ID is `<sessionName>#<executionId>`. If null and exactly one active session exists, it is selected automatically. If multiple sessions are active and sessionId is omitted, the call fails. Default: null. |
| limit | integer | Page size. Default: 50, max: 200. |
| offset | integer | Page offset. Default: 0. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| threads* | array[object] | Threads available in the suspended debug session (paginated). |
| &nbsp;&nbsp;[].id* | string | Thread identifier to pass as `threadId` in `get_stack`. |
| &nbsp;&nbsp;[].name* | string | Human-readable thread name. |
| &nbsp;&nbsp;[].state* | string | Current thread status from debugger perspective. |
| &nbsp;&nbsp;[].isCurrent* | boolean | Whether this thread is currently selected. |
| &nbsp;&nbsp;[].additionalInfo | string? | Additional thread display info when available. |
| &nbsp;&nbsp;[].additionalInfoTooltip | string? | Tooltip for additional thread display info when available. |
| &nbsp;&nbsp;[].frameCount | integer? | Number of stack frames when available. |
| offset* | integer | Requested page offset. |
| limit* | integer | Requested page limit. |
| totalCount* | integer | Total known thread count. |


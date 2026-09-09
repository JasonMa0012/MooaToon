# xdebug_list_breakpoints
Use this tool to see all currently set breakpoints and their properties.<br/><br/>Tip: Call this before RESUME to confirm there is at least one enabled breakpoint that is expected to be hit next.<br/><br/>Behavior:<br/>- If `filePath` is provided, returns only breakpoints in that file.<br/>- Returns rich attributes for each breakpoint (id, type, file, line, enabled, owner, condition, isLogMessage, isLogStack, temporary, suspendPolicy, hitCount).<br/>- `breakpointsMuted` reports the session-wide debugger mute flag when a session is resolved; it does not change per-breakpoint `enabled` values.<br/><br/>Next call:<br/>- If no suitable breakpoint exists, call `xdebug_set_breakpoint`.<br/>- Then continue execution with `xdebug_control_session(action=RESUME)` and `xdebug_control_session(action=WAIT_FOR_PAUSE)`.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| filePath | string | Optional file path to filter breakpoints. Path to the file. Supports project-relative paths, paths with '..', absolute paths, archive entries like '/path/lib.jar!/pkg/Foo.class', and URLs such as 'file://', 'jar://', and 'jrt://'. Any path returned from the other tools can be passed as is (e.g. paths from 'search_*' tools). If not specified, returns all breakpoints. Default: null. |
| sessionId | string | Debug session ID. Use the current ID returned by `xdebug_get_debugger_status` or `xdebug_start_debugger_session`. If a session has stopped, timed out, or disappeared, refresh the session list before reusing an old ID. Format: uses session name as ID by default; if multiple sessions share the same name, ID is `<sessionName>#<executionId>`. If null and exactly one active session exists, it is selected automatically. If multiple sessions are active and sessionId is omitted, the call fails. Default: null. Optional; when omitted, `breakpointsMuted` is returned only if exactly one active session exists. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| breakpoints* | array[object] | List of currently configured breakpoints. |
| &nbsp;&nbsp;[].id* | string | Canonical breakpoint ID (stable across list/remove). |
| &nbsp;&nbsp;[].type* | string | Breakpoint type (line/exception/other). |
| &nbsp;&nbsp;[].file | string? | File path of the breakpoint as provided by the debugger (usually file URL). |
| &nbsp;&nbsp;[].line | integer? | 1-based breakpoint line when available. |
| &nbsp;&nbsp;[].enabled* | boolean | Whether breakpoint is enabled. |
| &nbsp;&nbsp;[].owner* | user \\| agent | Breakpoint ownership marker: `agent` if created/updated by MCP toolset, otherwise `user`. |
| &nbsp;&nbsp;[].condition | string? | Conditional expression for triggering breakpoint, if set. |
| &nbsp;&nbsp;[].logExpression | string? | Evaluate-and-log expression of the logpoint, if set (the value logged when the line is reached). |
| &nbsp;&nbsp;[].isLogMessage* | boolean | Whether breakpoint logs source position when hit. |
| &nbsp;&nbsp;[].isLogStack* | boolean | Whether breakpoint logs stack trace when hit. |
| &nbsp;&nbsp;[].temporary* | boolean | Whether breakpoint is temporary. |
| &nbsp;&nbsp;[].suspendPolicy* | string | Breakpoint suspend policy (all/thread/none). |
| &nbsp;&nbsp;[].hitCount* | integer | Breakpoint hit count, 0 when unavailable. |
| totalCount* | integer | Total count. |
| enabledCount* | integer | Enabled count. |
| breakpointsMuted | boolean | Whether breakpoints are globally muted for the resolved debugger session. |


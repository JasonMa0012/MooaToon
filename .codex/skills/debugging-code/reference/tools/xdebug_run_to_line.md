# xdebug_run_to_line
Use this tool to run until a specific source position without manually stepping.<br/><br/>Preconditions:<br/>- Session must be suspended.<br/>- Target file/line must be valid.<br/><br/>Outcome:<br/>- paused: session paused at or after target.<br/>- stopped: session terminated before pause.<br/>- timeout: no pause/stop within timeout window.<br/><br/>Next call:<br/>- If paused, call `xdebug_get_stack` / `xdebug_get_frame_values` / `xdebug_evaluate_expression`.<br/>- If the session stopped or disappeared, refresh `sessionId` via `xdebug_get_debugger_status` before issuing another session-scoped call.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| sessionId | string | Debug session ID. Use the current ID returned by `xdebug_get_debugger_status` or `xdebug_start_debugger_session`. If a session has stopped, timed out, or disappeared, refresh the session list before reusing an old ID. Format: uses session name as ID by default; if multiple sessions share the same name, ID is `<sessionName>#<executionId>`. If null and exactly one active session exists, it is selected automatically. If multiple sessions are active and sessionId is omitted, the call fails. Default: null. |
| filePath* | string | Target source file path. Path to the file. Supports project-relative paths, paths with '..', absolute paths, archive entries like '/path/lib.jar!/pkg/Foo.class', and URLs such as 'file://', 'jar://', and 'jrt://'. Any path returned from the other tools can be passed as is (e.g. paths from 'search_*' tools). |
| line* | integer | Target line number (1-based). |
| timeout | integer | Timeout in milliseconds waiting for paused/stopped result. Default: 30000. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| sessionId* | string | Session identifier. |
| outcome* | paused \\| stopped \\| timeout | Outcome after attempting run-to-line (paused/stopped/timeout). |
| currentPosition | object? | Current position when outcome is paused and position is known. |
| &nbsp;&nbsp;filePath* | string | File path as provided by the debugger (usually VirtualFile.url). |
| &nbsp;&nbsp;line* | integer | 1-based line number. |
| &nbsp;&nbsp;column | integer? | 1-based column number when available. |
| message | string? | Additional context message (timeout or errors). |


# xdebug_get_stack
Use this tool to see the sequence of method calls that led to the current execution point.<br/><br/>Preconditions:<br/>- Session must be suspended.<br/><br/>Behavior:<br/>- `threadId` should come from `xdebug_get_threads` and matches the debugger thread display name (defaults to active thread).<br/>- Includes frames even when source position is missing (file/line may be null).<br/><br/>Pagination:<br/>- `offset`/`limit` are applied after collecting the full stack.<br/><br/>Frame fields include: index, file, line, isCurrent, presentation.<br/>`file` is reported as provided by the debugger (no path normalization).<br/><br/>Next call:<br/>- Use frame index from the current paused result in `xdebug_get_frame_values`, `xdebug_get_value_by_path`, or `xdebug_evaluate_expression`.<br/>- Do not reuse a cached `frameIndex` after `RESUME`, `STEP_*`, `xdebug_run_to_line`, or any change in paused location.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| sessionId | string | Debug session ID. Use the current ID returned by `xdebug_get_debugger_status` or `xdebug_start_debugger_session`. If a session has stopped, timed out, or disappeared, refresh the session list before reusing an old ID. Format: uses session name as ID by default; if multiple sessions share the same name, ID is `<sessionName>#<executionId>`. If null and exactly one active session exists, it is selected automatically. If multiple sessions are active and sessionId is omitted, the call fails. Default: null. |
| threadId | string | Thread ID to get stack for. This value should come from `xdebug_get_threads` and matches the debugger thread display name, not an opaque numeric ID. If not specified, uses the current/active thread. Default: null. |
| limit | integer | Max frames to return. Default: 200. |
| offset | integer | Page offset. Default: 0. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| frames* | array[object] | Stack frames for the selected thread, ordered from top (index 0) to older frames. |
| &nbsp;&nbsp;[].presentation* | string | Rendered function/method frame label from debugger UI. |
| &nbsp;&nbsp;[].index* | integer | 0-based frame index to use as `frameIndex` in other debugger tools. |
| &nbsp;&nbsp;[].file | string? | Source file path as provided by the debugger when available. |
| &nbsp;&nbsp;[].line | integer? | 1-based source line when available. |
| &nbsp;&nbsp;[].isCurrent* | boolean | Whether this is the currently selected frame. |
| threadId | string? | Thread identifier used to fetch this stack. |
| totalFrames* | integer | Total frame count for the stack. |


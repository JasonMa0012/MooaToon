# xdebug_get_frame_values
Use this tool to inspect local variables, parameters, and fields or other values available at a specific point in the call stack.<br/><br/>Preconditions:<br/>- Session must be suspended.<br/>- Frame index should come from the current paused `xdebug_get_stack` result (0 = top frame).<br/><br/>Format:<br/>- Nodes that have children are marked with `+`.<br/><br/>Next call:<br/>- Use `xdebug_get_value_by_path` to drill into nested fields.<br/>- Use `xdebug_evaluate_expression` for computed checks in the same frame.<br/>- Do not reuse a cached `frameIndex` after `RESUME`, `STEP_*`, `xdebug_run_to_line`, or any change in paused location.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| sessionId | string | Debug session ID. Use the current ID returned by `xdebug_get_debugger_status` or `xdebug_start_debugger_session`. If a session has stopped, timed out, or disappeared, refresh the session list before reusing an old ID. Format: uses session name as ID by default; if multiple sessions share the same name, ID is `<sessionName>#<executionId>`. If null and exactly one active session exists, it is selected automatically. If multiple sessions are active and sessionId is omitted, the call fails. Default: null. |
| frameIndex | integer | Stack frame index as integer (0 = top frame). Obtain this from the current paused `xdebug_get_stack` result; do not reuse a cached frame index after `RESUME`, `STEP_*`, `xdebug_run_to_line`, or any change in paused location. If null, uses the top frame. Default: null. |
| depth | integer | Maximum depth for expanding nested objects (0 = no children (only frame variables), 1 = variables with first level children, 2 = two levels of children, etc.). Default: 0. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |


# xdebug_control_session
Use this tool to step through code, resume execution, pause, or stop the debug session.<br/><br/>Preconditions:<br/>- A debug session must exist.<br/>- `STEP_*` and `RESUME` require a suspended session.<br/><br/>Actions:<br/>- STEP_INTO: Step into the next method call<br/>- STEP_OVER: Step over the current line<br/>- STEP_OUT: Step out of the current method<br/>- RESUME: Resume program execution until the next breakpoint<br/>- PAUSE: Pause program execution<br/>- STOP: Stop the debug session<br/>- WAIT_FOR_PAUSE: Wait until the session pauses (breakpoint hit or paused manually)<br/>- DRAIN_EVENTS: Drain tracepoint outputs for the session (breakpoint errors are drained for all actions)<br/><br/>Important notes:<br/>- If the program is running, use WAIT_FOR_PAUSE or PAUSE before STEP_* / RESUME.<br/>- Use a current `sessionId` from `xdebug_get_debugger_status` or `xdebug_start_debugger_session`. If a session stops, times out, or disappears, refresh the session list before the next session-scoped call.<br/>- RESUME does NOT set breakpoints. If there are no enabled breakpoints (or none will be hit next), the program may run to completion and the session may stop without pausing.<br/>- After RESUME, call WAIT_FOR_PAUSE to confirm the next suspension. If WAIT_FOR_PAUSE times out, consider PAUSE and re-check breakpoints.<br/>- `DRAIN_EVENTS` also requires an existing session; do not reuse a stale `sessionId` after the session has terminated.<br/><br/>Next call:<br/>- After `RESUME`, call `xdebug_control_session(action=WAIT_FOR_PAUSE)`.<br/>- After a paused result, call `xdebug_get_stack` / `xdebug_get_frame_values` / `xdebug_evaluate_expression`.<br/><br/>Status values in the result:<br/>- running: Program is executing<br/>- paused: Execution is suspended (breakpoint, step, or manual pause); paused results also include `frameValues`, a current-frame snapshot in `xdebug_get_frame_values(depth=0)` format when available<br/>- stopped: Debug session has terminated<br/>- `breakpointErrorsTail` is returned for any action<br/>- `tracepointOutputsTail` is returned only for `DRAIN_EVENTS`<br/><br/>Event support scope:<br/>- Breakpoint error and tracepoint output events are currently reported only by JVM-based debuggers (Java, Kotlin, etc.).<br/>- On other debugger backends these event tails can be empty even when breakpoints/logging are configured.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| sessionId | string | Debug session ID. Use the current ID returned by `xdebug_get_debugger_status` or `xdebug_start_debugger_session`. If a session has stopped, timed out, or disappeared, refresh the session list before reusing an old ID. Format: uses session name as ID by default; if multiple sessions share the same name, ID is `<sessionName>#<executionId>`. If null and exactly one active session exists, it is selected automatically. If multiple sessions are active and sessionId is omitted, the call fails. Default: null. |
| action* | STEP_INTO \\| STEP_OVER \\| STEP_OUT \\| RESUME \\| PAUSE \\| STOP \\| WAIT_FOR_PAUSE \\| DRAIN_EVENTS | Action to perform: STEP_INTO, STEP_OVER, STEP_OUT, RESUME, PAUSE, STOP, WAIT_FOR_PAUSE, DRAIN_EVENTS. Event draining is currently populated only by JVM-based debuggers (Java, Kotlin, etc.). |
| timeout | integer | Timeout in milliseconds to wait for action completion. Guidance: STEP_* / PAUSE usually 5000-15000; WAIT_FOR_PAUSE usually 30000-120000 depending on workload and breakpoints. Default: 30000. |
| eventsLimit | integer | Maximum number of latest events to drain per event list. For DRAIN_EVENTS this limit is applied independently to breakpointErrorsTail and tracepointOutputsTail. Default: 100. |
| clearEventsAfterRead | boolean | Compatibility flag. Returned events are always removed from internal buffers, regardless of this value. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| status* | running \\| paused \\| stopped | Session state after the control action. |
| newPosition | object? | Current source position when the session is paused (if available). |
| &nbsp;&nbsp;filePath* | string | File path as provided by the debugger (usually VirtualFile.url). |
| &nbsp;&nbsp;line* | integer | 1-based line number. |
| &nbsp;&nbsp;column | integer? | 1-based column number when available. |
| frameValues | string? | Snapshot of current frame values when the session is paused, using the same text format as `xdebug_get_frame_values` with `depth=0`. |
| breakpointsMuted | boolean | Whether breakpoints are globally muted for this debugger session. |
| message | string? | Additional context message for timeout/already-paused/already-stopped situations. |
| breakpointErrorsTail | array? | Latest drained breakpoint error events. Returned for any control_session action. Indicates errors in breakpoints configuration like invalid conditional/log expressions. Currently populated only by JVM-based debuggers (Java, Kotlin, etc.). |
| &nbsp;&nbsp;[].type* | BREAKPOINT_ERROR \\| TRACEPOINT_OUTPUT | Event type (BREAKPOINT_ERROR or TRACEPOINT_OUTPUT). |
| &nbsp;&nbsp;[].timestampMs* | integer | Unix timestamp in milliseconds when the event was recorded. |
| &nbsp;&nbsp;[].timestampIso* | string | ISO-8601 timestamp when the event was recorded. |
| &nbsp;&nbsp;[].sessionId* | string | Debugger session identifier. |
| &nbsp;&nbsp;[].message* | string | Primary event message. |
| &nbsp;&nbsp;[].breakpointId | string? | Canonical breakpoint ID when available. |
| &nbsp;&nbsp;[].filePath | string? | Breakpoint file path as provided by debugger when available. |
| &nbsp;&nbsp;[].line | integer? | 1-based breakpoint line when available. |
| &nbsp;&nbsp;[].details | string? | Additional event context details when available. |
| tracepointOutputsTail | array? | Latest drained tracepoint output events. Returned only for DRAIN_EVENTS action. Currently populated only by JVM-based debuggers (Java, Kotlin, etc.). |
| &nbsp;&nbsp;[].type* | BREAKPOINT_ERROR \\| TRACEPOINT_OUTPUT | Event type (BREAKPOINT_ERROR or TRACEPOINT_OUTPUT). |
| &nbsp;&nbsp;[].timestampMs* | integer | Unix timestamp in milliseconds when the event was recorded. |
| &nbsp;&nbsp;[].timestampIso* | string | ISO-8601 timestamp when the event was recorded. |
| &nbsp;&nbsp;[].sessionId* | string | Debugger session identifier. |
| &nbsp;&nbsp;[].message* | string | Primary event message. |
| &nbsp;&nbsp;[].breakpointId | string? | Canonical breakpoint ID when available. |
| &nbsp;&nbsp;[].filePath | string? | Breakpoint file path as provided by debugger when available. |
| &nbsp;&nbsp;[].line | integer? | 1-based breakpoint line when available. |
| &nbsp;&nbsp;[].details | string? | Additional event context details when available. |


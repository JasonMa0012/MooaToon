# xdebug_start_debugger_session
(`filePath` + `line`) in the current project.<br/>Use this tool to start a debugger session.<br/>Use this tool with either an existing run configuration name, or with `filePath` + `line`.<br/>When using `filePath` + `line`, a line with a runnable method such as `main`, a test, or another executable<br/>entry point will almost always work. If you are unsure which line to use, `get_run_configurations`<br/>can help discover runnable locations in the file.<br/>The session will be started and you can then use other debugger tools to control execution.<br/><br/>Preconditions:<br/>- When using `configurationName`, pass the exact existing run configuration name; do not pass a test method name or other derived target identifier.<br/>- When using `filePath` + `line`, point at a runnable code location such as `main`, a test, or another executable entry point.<br/>- Set at least one breakpoint first; otherwise the program may run to completion without pausing.<br/>- Pass either `configurationName`, or `filePath` together with `line`. These modes are mutually exclusive.<br/><br/>Behavior:<br/>- Waits for session creation up to `timeout`.<br/>- Applies a grace wait (`graceWaitMs`) after the session starts and returns refreshed state.<br/>- Optional launch overrides (`programArguments`, `workingDirectory`, `envs`) are applied only for this debug launch and are not persisted.<br/>- `get_run_configurations` is the source of truth for override support: only pass launch overrides when the selected run configuration reports `supportsDynamicLaunchOverrides=true`.<br/>- Do not pass these override parameters unless you explicitly need to change the configured launch values for this debug launch.<br/>- Missing/null override parameters keep existing run configuration values unchanged.<br/>- For string overrides (`programArguments`, `workingDirectory`), missing/null or empty string (`""`) keeps the existing value unchanged.<br/>- Pass a whitespace-only string such as `" "` to clear an existing value for this debug launch.<br/><br/>Next call:<br/>- `xdebug_control_session(action=WAIT_FOR_PAUSE)` to wait for first suspension.<br/>- After pause, call `xdebug_get_stack` and `xdebug_get_frame_values` (or `xdebug_evaluate_expression`) for runtime evidence.<br/><br/>Returns a flat result with debugger session metadata plus the execution snapshot fields from the launch:<br/>- `sessionId`, `name`, `status`, and optional `runConfigurationName`<br/>- `output` preview and optional `fullOutputPath`<br/>- optional `exitCode` when process termination is already known

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| configurationName | string | Name of the existing run configuration to debug. |
| filePath | string | File path relative to the project root. Provide together with `line` to start debugging from a code location. |
| line | integer | 1-based line number for `filePath`. Provide together with `filePath` and do not combine with `configurationName`. |
| timeout | integer | Timeout in milliseconds to wait for the debug session to start. Default: 60000. |
| graceWaitMs | integer | Grace wait in milliseconds after session starts to refresh state. Default: 2000. |
| programArguments | string | Optional program arguments override for this launch only. Pass this only when the selected run configuration reports `supportsDynamicLaunchOverrides=true` in `get_run_configurations`. Missing/null or empty string keeps the existing value; whitespace-only string clears it. |
| workingDirectory | string | Optional working directory override for this launch only. Pass this only when the selected run configuration reports `supportsDynamicLaunchOverrides=true` in `get_run_configurations`. Missing/null or empty string keeps the existing value; whitespace-only string clears it. |
| envs | object | Optional environment variable overrides for this launch only. Pass this only when the selected run configuration reports `supportsDynamicLaunchOverrides=true` in `get_run_configurations`. Missing/null keeps existing env unchanged; when provided, values are merged over existing env. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| sessionId* | string | Session identifier to use as `sessionId` in subsequent debugger calls. Uses session name by default; if duplicate names exist, format is `<sessionName>#<executionId>`. |
| name* | string | Human-readable session name. |
| state* | running \\| paused \\| stopped | Current session state. |
| runConfigurationName | string? | Associated run configuration name, if available. |
| breakpointsMuted | boolean | Whether breakpoints are globally muted for this debugger session. |
| exitCode | integer? | Process exit code. Absent when the tool returns before observing process termination, for example when the debuggee continues running after the session starts. |
| output* | string | Captured process output snapshot. When additional output exists, `<truncated>` is appended to the preview. |
| fullOutputPath | string? | Path to a temp file containing the full raw output. The file may continue growing while the process is still running and remains available while the IDE is running. |


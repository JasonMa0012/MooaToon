# execute_run_configuration
Use this tool with either a configuration name returned by `get_run_configurations`, or with a run point<br/>(`filePath` + `line`) returned by `get_run_configurations(filePath = ...)`.<br/><br/>Optional launch overrides (`programArguments`, `workingDirectory`, `envs`) are applied only for this run and are not persisted.<br/>Do not pass these override parameters unless you explicitly need to change the configured launch values for this run.<br/>Missing/null override parameters keep existing run configuration values unchanged.<br/>For string overrides (`programArguments`, `workingDirectory`), missing/null or empty string (`""`) keeps the existing value unchanged.<br/>Pass a whitespace-only string such as `" "` to clear an existing value for this launch.<br/><br/>Pass either `configurationName`, or `filePath` together with `line`. These modes are mutually exclusive.<br/><br/>Behavior:<br/>- When `waitForExit=true`, waits up to `timeout` milliseconds for process termination. If the timeout expires,<br/>  the process keeps running in the background and `exitCode` is omitted from the result.<br/>- When `waitForExit=false`, waits only for the process to start, then returns immediately without applying `timeout`.<br/>- `fullOutputPath` points to a temp file with the full raw output and may continue growing while the process is alive.<br/><br/>Returns the execution result including current output snapshot, optional exit code, and optional `fullOutputPath`.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| configurationName | string | Name of the existing run configuration to execute |
| filePath | string | File path relative to the project root. Provide together with `line` to create and execute a temporary run configuration from code context. |
| line | integer | 1-based line number for `filePath`. Provide together with `filePath` and do not combine with `configurationName`. |
| timeout | integer | Timeout in milliseconds |
| waitForExit | boolean | Whether to wait for process termination. If false, the tool returns immediately after the process starts and ignores `timeout`. |
| programArguments | string | Optional program arguments override for this launch only. Missing/null or empty string keeps the existing value; whitespace-only string clears it. |
| workingDirectory | string | Optional working directory override for this launch only. Missing/null or empty string keeps the existing value; whitespace-only string clears it. |
| envs | object | Optional environment variable overrides for this launch only. Missing/null keeps existing env unchanged; when provided, values are merged over existing env. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| exitCode | integer? | Process exit code. Absent when the tool returns before observing process termination, for example when `waitForExit=false` or when `timeout` expires. |
| timedOut | boolean? | Deprecated |
| output* | string | Captured process output snapshot. The snapshot includes up to the first 10000 characters of process output; when additional output exists, `<truncated>` is appended to the preview. |
| fullOutputPath | string? | Path to a temp file containing the full raw output. The file may continue growing while the process is still running and remains available while the IDE is running. |
| sessionId | string? | Session identifier for this run. Uses the session name by default; if duplicate live run sessions exist, format is `<sessionName>#<executionId>`. |


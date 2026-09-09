# get_run_configurations
Without `filePath`, this tool lists the project's existing run configurations. The result includes configuration<br/>names and, when available, launch details such as program arguments, working directory, environment variables,<br/>and `supportsDynamicLaunchOverrides`.<br/><br/>`supportsDynamicLaunchOverrides` is the source-of-truth capability flag for one-time launch overrides<br/>(`programArguments`, `workingDirectory`, `envs`) in `execute_run_configuration` and `xdebug_start_debugger_session`.<br/>Only pass those override parameters when this flag is `true` for the selected configuration.<br/><br/>With `filePath`, this tool discovers executable entry points (run points) in that file, such as test methods,<br/>main methods, or other executable entry points where the IDE shows a Run gutter icon. The result contains `filePath` and<br/>`runPoints`; use the returned line numbers with `execute_run_configuration` to run from code.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| filePath | string | Optional file path relative to the project root. When provided, returns run points (executable entry points) in the file instead of project-wide run configurations. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| configurations | array? | Project run configurations. Present when the tool is called without `filePath`. |
| &nbsp;&nbsp;[].name* | string | Run configuration name. Pass this value as `configurationName` to `execute_run_configuration`. |
| &nbsp;&nbsp;[].description | string? | Human-readable run configuration type or description shown by the IDE, when available. |
| &nbsp;&nbsp;[].supportsDynamicLaunchOverrides* | boolean | Whether this run configuration supports one-time dynamic launch overrides for `programArguments`, `workingDirectory`, and `envs`. Use this field as the source of truth before passing those override parameters to `execute_run_configuration` or `xdebug_start_debugger_session`. |
| &nbsp;&nbsp;[].commandLine | string? | Configured command line or program arguments for this run configuration, when available. |
| &nbsp;&nbsp;[].workingDirectory | string? | Configured working directory for this run configuration, when available. |
| &nbsp;&nbsp;[].environment | object? | Configured environment variables for this run configuration, when available. |
| filePath | string? | File path relative to the project root for which `runPoints` were collected. Present only when the tool is called with `filePath`. |
| runPoints | array? | Executable entry points discovered in `filePath`, such as test methods, main methods, or other executable entry points. Present only when the tool is called with `filePath`. |
| &nbsp;&nbsp;[].line* | integer | 1-based line number of the executable code location. |
| &nbsp;&nbsp;[].description | string? | IDE-provided description or tooltip for this run point, when available. |
| &nbsp;&nbsp;[].elementText | string? | Short source snippet for the PSI element associated with this run point, when available. |


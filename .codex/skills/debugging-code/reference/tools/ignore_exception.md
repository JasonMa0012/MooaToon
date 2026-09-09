# ignore_exception
Use this when a debug session keeps suspending on a noisy or expected exception (for example a handled<br/>`System.OperationCanceledException`) and you want execution to continue past it without pausing.<br/><br/>Behavior:<br/>- Resolves the exception breakpoint for `exceptionType` (creating one if it does not exist yet, as long as<br/>  the type can be resolved in the current solution) and sets it so the debugger no longer suspends on that<br/>  exception (suspend policy NONE). This also overrides a broad "break on all exceptions" setting for this type.<br/>- The change is persistent (like toggling the exception breakpoint in the UI); it is not limited to the<br/>  current pause and survives resume.<br/>- `exceptionType` must be the full name of a .NET exception type that is resolvable in the current solution,<br/>  e.g. `System.NullReferenceException`. Generic type arguments are normalized automatically<br/>  (e.g. `My.Exception<T>` -> ``My.Exception`1``). If the type cannot be resolved, the tool fails.<br/><br/>After ignoring, resume execution with `xdebug_control_session(action=RESUME)`.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| exceptionType* | string | Full .NET type name of the exception to ignore, e.g. `System.NullReferenceException`. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| exceptionType* | string |  |
| ignored* | boolean |  |
| message* | string |  |


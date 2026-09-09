# xdebug_remove_breakpoint
Use this tool to remove previously set breakpoints.<br/><br/>Behavior:<br/>- `owner` defaults to `agent`.<br/>- If only `owner` is provided, removes all breakpoints of that owner.<br/>- If `breakpointId` is provided, removes matching breakpoint(s) for the selected owner.<br/>- If `filePath`+`line` are provided, removes matching line breakpoint(s) for the selected owner.<br/>- If multiple selectors are provided, all of them are combined (logical AND).<br/>- Idempotent: removing a non-existing breakpoint returns removed=false.<br/>- To remove all breakpoints regardless of owner, call twice: once with `owner=user`, once with `owner=agent`.<br/><br/>Next call:<br/>- Use `xdebug_list_breakpoints` to verify the remaining set.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| breakpointId | string | Canonical breakpoint ID returned by `xdebug_set_breakpoint` or `xdebug_list_breakpoints`. |
| filePath | string | Optional input: Path to the file. Supports project-relative paths, paths with '..', absolute paths, archive entries like '/path/lib.jar!/pkg/Foo.class', and URLs such as 'file://', 'jar://', and 'jrt://'. Any path returned from the other tools can be passed as is (e.g. paths from 'search_*' tools). |
| line | integer | Optional input: line number (1-based) of the breakpoint to remove. |
| owner | user \\| agent | Breakpoint owner filter. Default: agent. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| removed* | boolean | Whether at least one breakpoint was removed. |
| removedCount* | integer | Number of breakpoints removed at the requested location. |
| breakpointId | string? | Removed breakpoint ID when operation targeted one ID. |
| totalBreakpoints* | integer | Current total number of breakpoints after removal. |
| message | string? | Additional note when no matching breakpoint is found. |


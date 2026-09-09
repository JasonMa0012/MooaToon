# change_api_signature
`parameters` is the COMPLETE desired parameter list in the new order:<br/>  * an entry matching an existing parameter name keeps it (moved to the new position);<br/>  * an existing parameter missing from the list is REMOVED;<br/>  * an unknown name is ADDED - `type` is required, `defaultValue` is the argument inserted at call sites.<br/>CAUTION: removing a parameter does NOT rewrite references to it inside method bodies - they are<br/>reported as warnings instead. Use preview=true first to see the impact (resulting signature,<br/>call sites, overrides, files, warnings) without changing anything.<br/>preview validates the change against the code model and counts the impact; it does NOT search for conflicts.<br/>If several overloads match `methodName`, the response is {ok:false, applied:false, candidates:[...], error:{kind:"ambiguous_method"}};<br/>disambiguate with `currentSignature` - the CURRENT parameter types, e.g. ["int", "string"] - and/or<br/>`declaringType` (distinguishes a base method from its override in the same file).<br/>filePath accepts an absolute or solution-relative path (paths from search_* output work as-is); response paths are solution-relative with '/' separators.<br/>Response: {ok, applied, newSignature, affects:{files,callSites}, updatedOverrides, files (first 20), moreFiles, warnings, candidates, error}.<br/>The affects counts come from a reference search, so they include usages the rewrite leaves untouched (e.g. nameof(...) and XML-doc cref).<br/>File or method not found and invalid parameter types are MCP errors.

## Parameters
| Name | Type | Description |
| --- | --- | --- |
| filePath* | string | Path to the file containing the method (absolute or solution-relative). |
| methodName* | string | Name of the method. |
| parameters* | array[object] | Complete desired parameter list in the new order. |
| &nbsp;&nbsp;[].name* | string |  |
| &nbsp;&nbsp;[].type | string? |  |
| &nbsp;&nbsp;[].defaultValue | string? |  |
| currentSignature | array[string] | Optional overload disambiguator: the CURRENT parameter types, e.g. ["int", "string"]. |
| declaringType | string | Optional disambiguator: name of the type DECLARING the wanted method (short or namespace-qualified). |
| preview | boolean | Analyze only: validate the change and report the would-be signature, impact and warnings without mutating any files. |
| rootFolder | string | The path to the root folder of the Rider solution or project. Pass this value ALWAYS if you are aware of it. It reduces numbers of ambiguous calls.<br/>In the case you know only the current working directory you can use it as the root folder path.<br/>If you're not aware about the root folder path you can ask user about it. |

## Output
| Name | Type | Description |
| --- | --- | --- |
| ok* | boolean |  |
| applied* | boolean |  |
| newSignature | string? |  |
| affects | object? |  |
| &nbsp;&nbsp;files* | integer |  |
| &nbsp;&nbsp;callSites* | integer |  |
| updatedOverrides* | integer |  |
| files* | array[string] |  |
| moreFiles* | integer |  |
| warnings* | array[string] |  |
| candidates | array[string] |  |
| error | object? |  |
| &nbsp;&nbsp;kind* | string |  |
| &nbsp;&nbsp;hint | string? |  |


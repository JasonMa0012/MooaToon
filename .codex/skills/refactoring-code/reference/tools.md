# Tools

> **Legend.** `*` after a field name marks a property that is required by the JSON schema. For input parameters this means the caller must pass the value. For output fields it means the value is always present within its enclosing object. Nested `*` is scoped to the parent object's presence — required nested fields are only guaranteed when the optional parent object is emitted.

## RiderRefactoringToolset

- [change_api_signature](tools/change_api_signature.md) — Change a method's signature: reorder, add and remove parameters, updating the whole override/implementation hierarchy and all call sites across the solution.
- [extract_base_class](tools/extract_base_class.md) — Extract a base class from a type: a new base class is created next to the type in the same file, the type inherits from it, and the selected members are MOVED to the base class.
- [extract_interface](tools/extract_interface.md) — Extract an interface from a type: a new interface with the chosen members is created next to the type in the same file and the type implements it.
- [extract_method](tools/extract_method.md) — Extract a method or function from a range of statements.
- [move_type_to_namespace](tools/move_type_to_namespace.md) — Move a type (class, struct, interface, enum, etc.) to another namespace and update all references across the solution.
- [rename_refactoring](tools/rename_refactoring.md) — Rename a Rider symbol and all its usages across the solution, or analyze the rename without mutating files (preview=true).
- [reorganize_namespaces](tools/reorganize_namespaces.md) — Synchronize namespaces with the folder structure (Adjust Namespaces) within the given scope, fixing using directives and references across the solution.
- [safe_delete](tools/safe_delete.md) — Safe Delete a symbol (type or member): delete it only if it has no remaining usages, otherwise refuse and report the usages as conflicts.


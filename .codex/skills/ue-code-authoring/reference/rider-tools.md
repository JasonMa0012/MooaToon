# Rider MCP — Code Authoring Workflow Patterns

For full tool parameter reference see `reference/rider-mcp-tools.md`.

---

## Fix-loop for a single file

1. Write/Edit file using standard Write or Edit tool
2. `get_file_problems` → errors? → Edit to fix → back to 2
3. No errors → move on

## Full quality pass

1. Write all files using standard Write or Edit tool
2. `get_file_problems` on each file → fix all errors + warnings
3. `lint_files` on all changed files → fix remaining issues
4. `build_solution_start` → poll `build_solution_state`
5. Succeeded? → `get_project_problems` → fix issues on changed files
6. `reformat_file` on each changed file

## Common lookups

### "Does this class already exist?"
Use `search_symbol` to check. Use Glob or `list_directory_tree` to check file layout.

### "What module does X belong to?"
Use `search_symbol` to find the file path → derive module from `Source/<Module>/...`. Read the `Build.cs` to check dependencies.

### "Where is this UPROPERTY used?"
Use `search_text` with paths `["*.cpp", "*.h"]`.

### "Is there an existing base class I should extend?"
Use `search_symbol`. Then use `get_symbol_info` — read the file first to find line/column.

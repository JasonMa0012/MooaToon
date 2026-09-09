# Rider MCP — Test Authoring Workflow Patterns

For full tool parameter reference see `reference/rider-mcp-tools.md`.

---

## Fix-loop for a test file

1. Write/Edit file using standard Write or Edit tool
2. `get_file_problems` → errors? → Edit to fix → back to 2
3. No errors → `lint_files` → fix remaining issues
4. `build_solution_start` → poll `build_solution_state`
5. Succeeded? → `get_project_problems` → fix warnings on your files
6. `reformat_file`

## Common lookups

### "Does a test module already exist?"
Use Glob or `list_directory_tree` to look for `*Tests` dirs. Use `search_file` to find `Build.cs` files and check `Type=Editor`. Use `search_text` to find `IMPLEMENT_MODULE`.

### "What is the correct API to test?"
Use `search_symbol` to find the declaration file. Read the `.h` using the standard Read tool. Use `get_symbol_info` to confirm the contract.

### "Find existing tests for this feature"
Use `search_text` for `IMPLEMENT_SIMPLE_AUTOMATION_TEST`, `TEST_CLASS`, or `DEFINE_SPEC` in `*.cpp`. Use `search_file` for `*Tests*.cpp`.

### "Who calls the function I'm testing?"
Use `analyze_calls` to find callers. Or fall back to Grep.

@echo off
setlocal
rem Repository path is relative to this script. Patch path is relative to the repository.
set "REPOSITORY_PATH=..\MooaToon-Engine"
set "EPIC_REMOTE=epic"
set "TARGET_BRANCH=5.8"
set "PATCH_PATH=diff.patch"
python "%~dp0ApplyPatch.py" --repository "%REPOSITORY_PATH%" --epic-remote "%EPIC_REMOTE%" --target-branch "%TARGET_BRANCH%" --patch "%PATCH_PATH%"
exit /b %errorlevel%

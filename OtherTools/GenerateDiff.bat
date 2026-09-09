@echo off
setlocal
rem Repository path is relative to this script's directory.
set "REPOSITORY_PATH=..\MooaToon-Engine"
set "EPIC_REMOTE=epic"
rem Empty means the current branch name.
set "BASE_BRANCH="
rem Upgrade destination; displayed only, not used as the diff baseline.
set "TARGET_BRANCH=5.8"
rem Repository-relative directories or files. Add or remove one line per path.
set "EXCLUDE_PATHS="
set "EXCLUDE_PATHS=%EXCLUDE_PATHS%;Engine/Plugins/MooaToonThirdparty"
set "EXCLUDE_PATHS=%EXCLUDE_PATHS%;Engine/Build/Commit.gitdeps.xml"
rem Output path is relative to the repository root.
set "OUTPUT_PATH=diff.patch"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0GenerateDiff.ps1" -RepositoryPath "%REPOSITORY_PATH%" -EpicRemote "%EPIC_REMOTE%" -BaseBranch "%BASE_BRANCH%" -TargetBranch "%TARGET_BRANCH%" -ExcludePathsText "%EXCLUDE_PATHS%" -OutputPath "%OUTPUT_PATH%"
exit /b %errorlevel%

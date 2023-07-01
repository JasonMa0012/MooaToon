@echo off

echo ^============================================================
echo =                Updating MooaToon Engine                  =
echo ============================================================^

set repoURL=https://github.com/Jason-Ma-0012/MooaToon-Engine.git
set repoName=MooaToon-Engine
set branchName=5.2
set PROMPT_ARGUMENT=--prompt --threads=16

cd %repoName%

git checkout %branchName%
git pull --depth=50 origin %branchName%
git merge origin/%branchName%

if not %errorlevel% == 0 (
    color 04
    echo Merge failed, please run Clean after backup files.
    pause
)else (
    echo %repoName% successfully update.
    timeout /t 10
)
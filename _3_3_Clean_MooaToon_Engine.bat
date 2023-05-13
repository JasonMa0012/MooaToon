@echo off


set repoURL=https://github.com/Jason-Ma-0012/MooaToon-Engine.git
set repoName=MooaToon-Engine
set branchName=5.2

cd %repoName%

echo ===================================================
git status -s | find "."
echo ===================================================
if %errorlevel% == 0 (
   color 04
   set /p input=You have modified files, discard and continue?  [Enter]
)

git reset --hard
git clean -df

echo %repoName% successfully clean.
timeout /t 10

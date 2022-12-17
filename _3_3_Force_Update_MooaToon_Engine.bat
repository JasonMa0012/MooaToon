@echo off


set repoURL=https://github.com/Jason-Ma-0012/MooaToon-Engine.git
set repoName=MooaToon-Engine
set branchName=5.1

cd %repoName%

echo ===================================================
git status -s | find "."
echo ===================================================
if %errorlevel% == 0 (
   color 04
   set /p input=You have modified files, discard and continue?  [Enter]
)

git reset --hard
git checkout -b %branchName%_temp FETCH_HEAD
git branch -D %branchName%
git branch -m %branchName%_temp %branchName%


echo %repoName% successfully update.
timeout /t 5
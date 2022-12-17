@echo off

setlocal enabledelayedexpansion

set repoURL=https://github.com/Jason-Ma-0012/MooaToon-Engine.git
set repoName=MooaToon-Engine
set branchName=5.1


if not exist %repoName% mkdir %repoName%
cd %repoName%

git init

:loop
git fetch --depth=1 %repoURL% %branchName%
if not %errorlevel% == 0 (
   echo Fetch failed, retrying in 5 seconds...
   timeout /t 5 /nobreak
   goto loop
)

git status | find "working tree clean"
if not %errorlevel% == 0 (
   git status
   color 4 0
   set /p input=You have modified files, discard and continue? (y/n)
   if not "%input%" == "y" exit
)

git reset --hard
git checkout -b %branchName%_temp FETCH_HEAD
git branch -D %branchName%
git branch -m %branchName%_temp %branchName%


echo %repoName% successfully update.
timeout /t 5
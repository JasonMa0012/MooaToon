@echo off


set repoURL=https://github.com/Jason-Ma-0012/MooaToon-Engine.git
set repoName=MooaToon-Project
set branchName=5.1_MooaToonProject


git checkout %branchName%
git pull origin %branchName%
git merge origin %branchName%

if not %errorlevel% == 0 (
    echo Merge failed, please run Force Update after backup files.
    pause
)else (
    echo %repoName% successfully update.
    timeout /t 5
)
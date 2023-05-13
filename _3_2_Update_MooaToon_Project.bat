@echo off


set repoURL=https://github.com/Jason-Ma-0012/MooaToon-Engine.git
set repoName=MooaToon-Project
set branchName=5.2_MooaToonProject

cd %repoName%

git checkout %branchName%
git pull --depth=50 origin %branchName%
git merge origin/%branchName%

if not %errorlevel% == 0 (
    color 04
    echo Merge failed, please run Force Clean after backup files.
    pause
)else (
    echo %repoName% successfully update.
    timeout /t 10
)
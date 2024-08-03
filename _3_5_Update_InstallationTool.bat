@echo off

setlocal enabledelayedexpansion


echo ============================================================
echo ==               Updating Installation Tool               ==
echo ============================================================


set repoURL=https://github.com/JasonMa0012/MooaToon.git
set branchName=main


if exist .git (
    git pull origin %branchName% --depth=100
) ^
else (
    git init
    git remote add origin %repoURL%
    git pull --depth=1 origin %branchName%
    git checkout %branchName% -f
)


echo successfully update.
timeout/t 10
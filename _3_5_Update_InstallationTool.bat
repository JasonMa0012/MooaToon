@echo off

setlocal enabledelayedexpansion

call _0_2_Set_CMD_And_Git_Proxy.bat


echo ============================================================
echo ==               Updating Installation Tool               ==
echo ============================================================


set repoURL=https://github.com/JasonMa0012/MooaToon.git
set branchName=main


if exist .git (
    git pull origin %branchName% --depth=50
) ^
else (
    git init
    git remote add origin %repoURL%
    git pull --depth=1 origin %branchName%
    git checkout %branchName% -f
)


echo successfully update.
timeout/t 10
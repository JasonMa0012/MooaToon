@echo off

echo ============================================================
echo ==               Installing MooaToon Project              ==
echo ============================================================


setlocal enabledelayedexpansion


call _2_5_Settings.bat

if not exist %projectFolderName% mkdir %projectFolderName%
cd %projectFolderName%


git init
git remote add origin %repoURL%
git checkout -b temp
git branch -D %branchName%
git pull --depth=1 origin %branchName%
git checkout %branchName% -f
git branch -D temp


echo %projectFolderName% successfully cloned.
timeout /t 10
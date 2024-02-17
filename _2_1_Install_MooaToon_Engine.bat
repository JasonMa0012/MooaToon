@echo off

echo ============================================================
echo ==               Installing MooaToon Engine               ==
echo ============================================================


setlocal enabledelayedexpansion


call _2_5_Settings.bat

if not exist %engineFolderName% mkdir %engineFolderName%
cd %engineFolderName%


git init
git remote add origin %repoURL%
git checkout -b temp
git branch -D %branchName%
git pull --depth=1 origin %branchName%
git checkout %branchName% -f
git branch -D temp


echo %engineFolderName% successfully cloned.
timeout /t 10

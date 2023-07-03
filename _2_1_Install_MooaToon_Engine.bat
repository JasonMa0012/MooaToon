@echo off

echo ^============================================================
echo ==               Installing MooaToon Engine               ==
echo ============================================================^


setlocal enabledelayedexpansion

git init

call _2_5_Settings.bat

if not exist %engineFolderName% mkdir %engineFolderName%
cd %engineFolderName%


:loop
git fetch --depth=1 %repoURL% %engineBranchName%
if not %errorlevel% == 0 (
   echo Fetch failed, retrying in 5 seconds...
   timeout /t 10 /nobreak
   goto loop
)

git checkout FETCH_HEAD
git remote add origin %repoURL%
git pull origin %engineBranchName%
git checkout %engineBranchName%
git merge origin/%engineBranchName%


echo %engineFolderName% successfully cloned.
timeout /t 10

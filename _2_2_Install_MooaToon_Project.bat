@echo off

echo ^============================================================
echo ==               Installing MooaToon Project              ==
echo ============================================================^


setlocal enabledelayedexpansion

git init

call _2_5_Settings.bat


if not exist %projectFolderName% mkdir %projectFolderName%
cd %projectFolderName%


:loop
git fetch --depth=1 %repoURL% %projectBranchName%
if not %errorlevel% == 0 (
   echo Fetch failed, retrying in 5 seconds...
   timeout /t 10 /nobreak
   goto loop
)

git checkout FETCH_HEAD
git remote add origin %repoURL%
git pull origin %projectBranchName%
git checkout %projectBranchName%
git merge origin/%projectBranchName%


echo %projectFolderName% successfully cloned.
timeout /t 10
@echo off

echo ============================================================
echo ==               Installing MooaToon Engine               ==
echo ============================================================


setlocal enabledelayedexpansion


call _2_5_Settings.bat


git clone %repoURL% %engineFolderName% -b %engineBranchName% --depth=1 --recurse-submodules


echo %engineFolderName% successfully cloned.
timeout /t 10

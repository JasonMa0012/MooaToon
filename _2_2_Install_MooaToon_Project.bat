@echo off

echo ============================================================
echo ==               Installing MooaToon Project              ==
echo ============================================================


setlocal enabledelayedexpansion


call _2_5_Settings.bat


git clone %repoURL% %projectFolderName% -b %projectBranchName% --depth=1


echo %projectFolderName% successfully cloned.
timeout /t 10
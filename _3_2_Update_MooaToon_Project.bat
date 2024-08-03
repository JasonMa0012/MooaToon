@echo off

echo ============================================================
echo ==               Updating MooaToon Project                ==
echo ============================================================


call _2_5_Settings.bat

pushd %projectFolderName%

git pull origin %projectBranchName% --depth=100

popd

if not %errorlevel% == 0 (
    color 04
    echo Merge failed, please run Force Clean after backup files.
    pause
)else (
    echo %projectFolderName% successfully update.
    timeout /t 10
)
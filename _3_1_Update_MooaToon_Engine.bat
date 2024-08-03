@echo off

echo ============================================================
echo ==               Updating MooaToon Engine                 ==
echo ============================================================


call _2_5_Settings.bat

pushd %engineFolderName%

git pull origin %engineBranchName% --depth=100
git submodule update --init --recursive

popd

if not %errorlevel% == 0 (
    color 04
    echo Merge failed, please run Clean after backup files.
    pause
)else (
    echo %engineFolderName% successfully update.
    timeout /t 10
)
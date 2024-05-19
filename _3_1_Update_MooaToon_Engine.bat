@echo off

echo ============================================================
echo ==               Updating MooaToon Engine                 ==
echo ============================================================


call _2_5_Settings.bat

cd %engineFolderName%

git pull --depth=50
git submodule update --init --recursive

if not %errorlevel% == 0 (
    color 04
    echo Merge failed, please run Clean after backup files.
    pause
)else (
    echo %engineFolderName% successfully update.
    timeout /t 10
)
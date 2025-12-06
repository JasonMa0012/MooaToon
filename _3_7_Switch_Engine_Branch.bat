@echo off

echo ============================================================
echo ==               Updating MooaToon Engine                 ==
echo ============================================================


call _2_5_Settings.bat

color 04

echo Switching to the %engineBranchName% branch, all local modifications will be overwritten!!! Press any key to continue.

pause

color 07

pushd %engineFolderName%

git fetch origin %engineBranchName% --depth=1
git checkout -B %engineBranchName% -f
git submodule update --init --recursive

popd

timeout /t 10
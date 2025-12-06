@echo off

echo ============================================================
echo ==               Updating MooaToon Project                ==
echo ============================================================


call _2_5_Settings.bat

color 04

echo Switching to the %projectBranchName% branch, all local modifications will be overwritten!!! Press any key to continue.

pause

color 07

pushd %projectFolderName%

git fetch origin %projectBranchName% --depth=1
git checkout -B %projectBranchName% -f
git submodule update --init --recursive

popd

timeout /t 10
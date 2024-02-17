@echo off
setlocal

echo ============================================================
echo ==               Setup Unreal Engine                      ==
echo ============================================================


call _2_5_Settings.bat

call %engineFolderName%/Setup.bat

echo Setup successful

timeout /t 10
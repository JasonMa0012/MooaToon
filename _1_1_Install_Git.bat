@echo off

cd InstallTools

echo Installing Git...

Git-2.38.1-64-bit.exe /silent

git -h

echo Git installed successfully!
pause
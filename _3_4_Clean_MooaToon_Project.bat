@echo off


call _2_5_Settings.bat

pushd %projectFolderName%

echo ===================================================
git status -s | find "."
echo ===================================================
if %errorlevel% == 0 (
   color 04
   set /p input=You have modified files, discard and continue?  [Enter]
)

git reset --hard
git clean -df

popd

echo %projectFolderName% successfully clean.
timeout /t 10
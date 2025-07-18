@echo off

call _2_5_Settings.bat

@echo on

cd %engineFolderName%

call GenerateProjectFiles.bat

call _build.bat

LocalBuilds\Engine\Windows\Engine\Binaries\Win64\UnrealEditor.exe %cd%\..\%projectFolderName%\MooaToon_Project.uproject

pause
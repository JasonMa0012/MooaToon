@echo off
set "scriptRoot=%~dp0"
call "%scriptRoot%_2_5_Settings.bat"
"%scriptRoot%%engineFolderName%\Engine\Binaries\Win64\UnrealEditor-Win64-Debug.exe" "%scriptRoot%%projectFolderName%\MooaToon_Project.uproject" -log

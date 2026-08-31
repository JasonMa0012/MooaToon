@echo off
call _2_5_Settings.bat
%engineFolderName%\Engine\Binaries\Win64\UnrealEditor-Win64-Debug.exe %projectFolderName%\MooaToon_Project.uproject -log

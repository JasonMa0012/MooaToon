@echo off
call _2_5_Settings.bat
call %engineFolderName%\GenerateProjectFiles.bat
call %engineFolderName%\Engine\Build\BatchFiles\Build.bat -Target="UnrealEditor Win64 Debug" -Target="ShaderCompileWorker Win64 Debug -Quiet" -WaitMutex -FromMsBuild
%engineFolderName%\Engine\Binaries\Win64\UnrealEditor-Win64-Debug.exe %projectFolderName%\MooaToon_Project.uproject -log

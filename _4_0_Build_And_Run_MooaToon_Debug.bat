@echo off
set "scriptRoot=%~dp0"
call "%scriptRoot%_2_5_Settings.bat"
call "%scriptRoot%%engineFolderName%\GenerateProjectFiles.bat"
call "%scriptRoot%%engineFolderName%\Engine\Build\BatchFiles\Build.bat" -Target="UnrealEditor Win64 Debug" -Target="ShaderCompileWorker Win64 Debug -Quiet" -WaitMutex -FromMsBuild
"%scriptRoot%%engineFolderName%\Engine\Binaries\Win64\UnrealEditor-Win64-Debug.exe" "%scriptRoot%%projectFolderName%\MooaToon_Project.uproject" -log

@echo off

echo ============================================================
echo ==               Building MooaToon Engine                 ==
echo ============================================================


call _2_5_Settings.bat

@echo on

call %engineFolderName%\GenerateProjectFiles.bat

call %engineFolderName%\Engine\Build\BatchFiles\Build.bat -Target="UnrealEditor Win64 Development" -Target="ShaderCompileWorker Win64 Development -Quiet" -WaitMutex -FromMsBuild

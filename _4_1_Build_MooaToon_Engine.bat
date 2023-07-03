@echo off

echo ^============================================================
echo ==               Building MooaToon Engine                 ==
echo ============================================================^


@echo on

call _2_5_Settings.bat

call %engineFolderName%\GenerateProjectFiles.bat

call %engineFolderName%\Engine\Build\BatchFiles\Build.bat -Target="UnrealEditor Win64 Development" -Target="ShaderCompileWorker Win64 Development -Quiet" -WaitMutex -FromMsBuild

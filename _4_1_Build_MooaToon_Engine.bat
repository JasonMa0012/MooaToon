@echo off

echo ^============================================================
echo =                Building MooaToon Engine                  =
echo ============================================================^


set repoName=MooaToon-Engine

call %repoName%\GenerateProjectFiles.bat

call %repoName%\Engine\Build\BatchFiles\Build.bat -Target="UnrealEditor Win64 Development" -Target="ShaderCompileWorker Win64 Development -Quiet" -WaitMutex -FromMsBuild

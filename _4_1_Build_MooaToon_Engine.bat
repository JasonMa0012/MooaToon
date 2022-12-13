rem @echo off

set repoName=MooaToon-Engine

%repoName%\GenerateProjectFiles.bat
timeout /t 5

%repoName%\Engine\Build\BatchFiles\Build.bat -Target="UnrealEditor Win64 Development" -Target="ShaderCompileWorker Win64 Development -Quiet" -WaitMutex -FromMsBuild

timeout /t 5
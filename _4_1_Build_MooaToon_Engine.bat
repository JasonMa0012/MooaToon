rem @echo off


set repoName=MooaToon-Engine


%repoName%\Engine\Build\BatchFiles\Build.bat -Target="UnrealEditor Win64 Development" -Target="ShaderCompileWorker Win64 Development -Quiet" -WaitMutex -FromMsBuild

if not %errorlevel% == 0 pause
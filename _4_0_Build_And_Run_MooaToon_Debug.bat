@echo off
setlocal

echo ============================================================
echo ==          Building and Running MooaToon Debug           ==
echo ============================================================

set "scriptRoot=%~dp0"
pushd "%scriptRoot%"

call "%scriptRoot%_2_5_Settings.bat"
if errorlevel 1 goto :failed

echo Generating Unreal project files...
call "%scriptRoot%%engineFolderName%\GenerateProjectFiles.bat"
if errorlevel 1 goto :failed

echo Building UnrealEditor and ShaderCompileWorker Debug targets...
call "%scriptRoot%%engineFolderName%\Engine\Build\BatchFiles\Build.bat" -Target="UnrealEditor Win64 Debug" -Target="ShaderCompileWorker Win64 Debug -Quiet" -WaitMutex -FromMsBuild
if errorlevel 1 goto :failed

echo Running MooaToon Project with hardware Ray Tracing enabled...
call "%scriptRoot%%engineFolderName%\Engine\Binaries\Win64\UnrealEditor-Win64-Debug.exe" "%scriptRoot%%projectFolderName%\MooaToon_Project.uproject" -log
set "exitCode=%errorlevel%"
popd
exit /b %exitCode%

:failed
set "exitCode=%errorlevel%"
popd
exit /b %exitCode%

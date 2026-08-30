@echo off
setlocal

echo ============================================================
echo =                Running MooaToon Project                  =
echo ============================================================


set "scriptRoot=%~dp0"
pushd "%scriptRoot%" || (
    echo Failed to switch to the MooaToon root directory: "%scriptRoot%"
    exit /b 1
)

call "%scriptRoot%_2_5_Settings.bat"
if errorlevel 1 (
    echo Failed to load MooaToon settings.
    popd
    exit /b 1
)

set "editorExe=%scriptRoot%%engineFolderName%\Engine\Binaries\Win64\UnrealEditor-Win64-Debug.exe"
set "projectFile=%scriptRoot%%projectFolderName%\MooaToon_Project.uproject"

if not exist "%editorExe%" (
    echo UnrealEditor Debug executable was not found: "%editorExe%"
    popd
    exit /b 1
)

if not exist "%projectFile%" (
    echo MooaToon project file was not found: "%projectFile%"
    popd
    exit /b 1
)

@echo on

"%editorExe%" "%projectFile%" -log
set "exitCode=%errorlevel%"

@echo off
popd
endlocal & exit /b %exitCode%

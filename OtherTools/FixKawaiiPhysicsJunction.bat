@echo off
setlocal

if "%~1"=="" (
    echo Usage: %~nx0 "C:\path\to\KawaiiPhysics_MooaToon"
    echo Exit code: 2
    pause
    exit /b 2
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0FixKawaiiPhysicsJunction.ps1" -KawaiiPhysicsSourcePath "%~1"
set "exitCode=%errorlevel%"
echo.
echo Exit code: %exitCode%
pause
exit /b %exitCode%

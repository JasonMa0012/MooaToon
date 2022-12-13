@echo off

setlocal enabledelayedexpansion

set repoName=MooaToon-Engine

cd %repoName%

:loop
Setup.bat
if not %errorlevel% == 0 (
   echo Setup failed, retrying in 3 seconds...
   timeout /t 3 /nobreak
   goto loop
)

echo Setup successful

timeout /t 5
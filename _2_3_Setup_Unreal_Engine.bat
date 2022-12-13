@echo off
setlocal

set repoName=MooaToon-Engine

cd %repoName%


rem pushd "%~dp0"

rem Figure out if we should append the -prompt argument
set PROMPT_ARGUMENT=
for %%P in (%*) do if /I "%%P" == "--prompt" goto no_prompt_argument
for %%P in (%*) do if /I "%%P" == "--force" goto no_prompt_argument
set PROMPT_ARGUMENT=--prompt --threads=16
:no_prompt_argument

:loop
rem Sync the dependencies...
.\Engine\Binaries\DotNET\GitDependencies\win-x64\GitDependencies.exe %PROMPT_ARGUMENT% %*
if %ERRORLEVEL% NEQ 0 (
   echo Setup failed, retrying in 3 seconds...
   timeout /t 3 /nobreak
   goto loop
)

rem Setup the git hooks...
if not exist .git\hooks goto no_git_hooks_directory
echo Registering git hooks...
echo #!/bin/sh >.git\hooks\post-checkout
echo Engine/Binaries/DotNET/GitDependencies/win-x64/GitDependencies.exe %* >>.git\hooks\post-checkout
echo #!/bin/sh >.git\hooks\post-merge
echo Engine/Binaries/DotNET/GitDependencies/win-x64/GitDependencies.exe %* >>.git\hooks\post-merge
:no_git_hooks_directory

rem Install prerequisites...
echo Installing prerequisites...
start /wait Engine\Extras\Redist\en-us\UEPrereqSetup_x64.exe /quiet /norestart

rem Register the engine installation...
if not exist .\Engine\Binaries\Win64\UnrealVersionSelector-Win64-Shipping.exe goto :no_unreal_version_selector
.\Engine\Binaries\Win64\UnrealVersionSelector-Win64-Shipping.exe /register
:no_unreal_version_selector


echo Setup successful

timeout /t 5
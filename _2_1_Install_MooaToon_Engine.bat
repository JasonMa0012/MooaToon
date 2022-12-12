setlocal enabledelayedexpansion

set repoURL=https://github.com/Jason-Ma-0012/MooaToon-Engine.git
set repoName=MooaToon-Engine
set branchName=5.1

rem if exist %repoName% rd %repoName%

if not exist %repoName% mkdir %repoName%
cd %repoName%

git init

:loop
git fetch %repoURL% %branchName%
if errorlevel 1 
(
   echo Fetch failed, retrying in 5 seconds...
   timeout /t 5 /nobreak
   goto loop
)

git checkout FETCH_HEAD
git remote add origin %repoURL%
git pull origin %branchName%
git checkout %branchName%

echo %repoName% successfully cloned.

Setup.bat
GenerateProjectFiles.bat
UE5.sln

pause
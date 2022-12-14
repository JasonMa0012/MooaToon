setlocal enabledelayedexpansion

set repoURL=https://github.com/Jason-Ma-0012/MooaToon-Engine.git
set repoName=MooaToon-Project
set branchName=5.1_MooaToonProject


if not exist %repoName% mkdir %repoName%
cd %repoName%

git init

:loop
git fetch --depth=1 %repoURL% %branchName%
if not %errorlevel% == 0 (
   echo Fetch failed, retrying in 5 seconds...
   timeout /t 5 /nobreak
   goto loop
)

git reset --hard
git checkout -b %branchName%_temp FETCH_HEAD
git branch -D %branchName%
git branch -m %branchName%_temp %branchName%


echo %repoName% successfully update.
timeout /t 5
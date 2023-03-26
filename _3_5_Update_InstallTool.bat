setlocal enabledelayedexpansion

set repoURL=https://github.com/JasonMa0012/MooaToon.git
set branchName=main


git init

git checkout %branchName%
git pull --depth=50 origin %branchName%
git merge origin/%branchName%

echo successfully update.
timeout /t 10
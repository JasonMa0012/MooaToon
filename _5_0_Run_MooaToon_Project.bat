@echo off

echo ^============================================================
echo =                Running MooaToon Project                  =
echo ============================================================^

@echo on

set engineName=MooaToon-Engine
set projectName=MooaToon-Project

%engineName%\Engine\Binaries\Win64\UnrealEditor.exe %cd%\%projectName%\MooaToon_Project.uproject

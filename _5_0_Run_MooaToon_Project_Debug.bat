@echo off

echo ============================================================
echo =                Running MooaToon Project                  =
echo ============================================================


call _2_5_Settings.bat

@echo on

%engineFolderName%\Engine\Binaries\Win64\UnrealEditor-Win64-Debug.exe %cd%\%projectFolderName%\MooaToon_Project.uproject

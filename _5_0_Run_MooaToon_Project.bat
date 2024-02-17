@echo off

echo ============================================================
echo =                Running MooaToon Project                  =
echo ============================================================


call _2_5_Settings.bat

@echo on

%engineFolderName%\Engine\Binaries\Win64\UnrealEditor.exe %cd%\%projectFolderName%\MooaToon_Project.uproject

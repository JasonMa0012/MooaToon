@echo off

echo ^============================================================
echo =                Running MooaToon Project                  =
echo ============================================================^


@echo on

call _2_5_Settings.bat

%engineFolderName%\Engine\Binaries\Win64\UnrealEditor.exe %cd%\%projectFolderName%\MooaToon_Project.uproject

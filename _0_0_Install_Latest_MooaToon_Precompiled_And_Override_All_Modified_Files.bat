@echo off

rem call _3_5_Update_InstallTool.bat

call _2_5_Settings.bat

set MooaRootDir=%cd%

InstallTools\Install.exe %MooaRootDir% %engineBranchName%

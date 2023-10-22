@echo off

call _3_5_Update_InstallationTool.bat

call _2_5_Settings.bat

set MooaRootDir=%cd%

InstallationTools\Install.exe %MooaRootDir% %engineBranchName%

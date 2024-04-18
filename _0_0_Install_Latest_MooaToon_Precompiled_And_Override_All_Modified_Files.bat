@echo off

call _2_5_Settings.bat

set MooaRootDir=%cd%

InstallationTools\Install.exe %MooaRootDir% %engineBranchName%

pause
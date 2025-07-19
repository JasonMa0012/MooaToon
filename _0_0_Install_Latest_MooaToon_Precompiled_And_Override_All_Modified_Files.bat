@echo off

call _0_2_Set_CMD_And_Git_Proxy.bat

call _2_5_Settings.bat

set MooaRootDir=%cd%

InstallationTools\Install.exe %MooaRootDir% %engineBranchName% 5

call _0_3_Cancel_CMD_And_Git_Proxy.bat

pause
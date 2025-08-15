@echo off

cd..

set MooaRootDir=%cd%

call _2_5_Settings.bat

call _3_1_Update_MooaToon_Engine.bat

call _3_2_Update_MooaToon_Project.bat

ReleaseTools\Release.exe %MooaRootDir% %engineBranchName% %projectBranchName% --Clean --BuildEngine --ZipEngine --ZipProject --Release
pause
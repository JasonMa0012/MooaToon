cd..
set MooaRootDir=%cd%

call _2_5_Settings.bat

ReleaseTools\Release.exe %MooaRootDir% %engineBranchName% %projectBranchName% --Clean --BuildEngine --ZipEngine --ZipProject --Release
pause
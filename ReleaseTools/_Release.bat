cd..
set MooaRootDir=%cd%

call _2_5_Settings.bat

ReleaseTools\Release.exe %MooaRootDir% %engineBranchName% --Clean --BuildEngine --CleanEngine --ZipEngine --ZipProject --Release
@echo off

rem call _3_5_Update_InstallTool.bat

set MooaRootDir=%cd%

InstallTools\Install.exe %MooaRootDir% --Clean --DownloadEngine --DownloadProject --UnzipEngine --UnzipProject

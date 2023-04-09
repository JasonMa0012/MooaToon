@echo off
set MooaRootDir=%cd%

InstallTools\Install.exe %MooaRootDir% --Clean --DownloadEngine --DownloadProject --UnzipEngine --UnzipProject

timeout /t 10
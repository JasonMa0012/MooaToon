@echo off

cd InstallTools
echo Installing Visual Studio 2022...


vs_Community.exe --wait --nocache --addProductLang En-us --add Microsoft.VisualStudio.Workload.ManagedDesktop --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.NativeGame --add Microsoft.VisualStudio.Workload.Universal --add Component.Unreal.Ide --add Component.Unreal --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64

rem --quiet --norestart
rem --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 
rem --add Microsoft.VisualStudio.Component.VC.140 
rem --add Microsoft.VisualStudio.Component.VC.ATL 

echo Visual Studio 2022 installed successfully!

rem echo Setting up Visual Studio 2022 for Unreal Engine 5...

rem "C:\Program Files (x86)\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvarsall.bat" x86_amd64

rem echo Visual Studio 2022 setup complete!

pause
@echo off

cd InstallationTools
echo Installing Visual Studio 2022...


rem https://learn.microsoft.com/zh-cn/visualstudio/install/workload-component-id-vs-community?view=vs-2022
rem https://learn.microsoft.com/zh-cn/visualstudio/install/use-command-line-parameters-to-install-visual-studio?view=vs-2022

vs_Community.exe --wait --addProductLang En-us ^
 --add Microsoft.VisualStudio.Component.Windows10SDK.18362 ^
 --add Microsoft.VisualStudio.Component.VC.14.38.17.8.x86.x64 ^
 --add Microsoft.VisualStudio.Component.VC.14.38.17.8.x86.x64.Spectre ^
 --add Microsoft.VisualStudio.Component.VC.14.38.17.8.CLI.Support ^
 --add Microsoft.VisualStudio.Component.VC.14.38.17.8.ATL ^
 --add Microsoft.VisualStudio.Component.VC.14.38.17.8.MFC ^
 --add Microsoft.VisualStudio.Workload.ManagedDesktop ^
 --add Microsoft.VisualStudio.Workload.NativeDesktop ^
 --add Microsoft.VisualStudio.Workload.NativeGame ^
 --add Microsoft.VisualStudio.Workload.Universal ^
 --add Microsoft.NetCore.Component.Runtime.6.0 ^
 --add Microsoft.Net.Component.4.6.2.TargetingPack


rem --quiet --norestart

echo Visual Studio 2022 installed successfully!

rem echo Setting up Visual Studio 2022 for Unreal Engine 5...

rem "C:\Program Files (x86)\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvarsall.bat" x86_amd64

rem echo Visual Studio 2022 setup complete!

pause
@echo off

cd InstallationTools
echo Installing Visual Studio 2022...


rem https://learn.microsoft.com/zh-cn/visualstudio/install/workload-component-id-vs-community?view=vs-2022
rem https://learn.microsoft.com/zh-cn/visualstudio/install/use-command-line-parameters-to-install-visual-studio?view=vs-2022
rem https://dev.epicgames.com/documentation/zh-cn/unreal-engine/unreal-engine-5-7-release-notes#platform-sdk-upgrades

vs_Community.exe --wait --addProductLang En-us ^
 --add Microsoft.VisualStudio.Workload.ManagedDesktop ^
 --add Microsoft.VisualStudio.Workload.NativeDesktop ^
 --add Microsoft.VisualStudio.Workload.NativeGame ^
 --add Microsoft.VisualStudio.Workload.Universal ^
 --add Microsoft.VisualStudio.Component.Windows11SDK.22621 ^
 --add Microsoft.VisualStudio.Component.VC.14.44.17.14.x86.x64 ^
 --add Microsoft.VisualStudio.Component.VC.14.44.17.14.x86.x64.Spectre ^
 --add Microsoft.VisualStudio.Component.VC.14.44.17.14.CLI.Support ^
 --add Microsoft.VisualStudio.Component.VC.14.44.17.14.ATL ^
 --add Microsoft.VisualStudio.Component.VC.14.44.17.14.MFC ^
 --add Microsoft.NetCore.Component.Runtime.8.0


rem --quiet --norestart

echo Visual Studio 2022 installed successfully!

rem echo Setting up Visual Studio 2022 for Unreal Engine 5...

rem "C:\Program Files (x86)\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvarsall.bat" x86_amd64

rem echo Visual Studio 2022 setup complete!

pause
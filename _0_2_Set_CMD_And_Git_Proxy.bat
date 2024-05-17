@echo off
setlocal EnableDelayedExpansion

chcp 65001

rem Check if proxy is enabled
for /f "tokens=3" %%a in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable') do set proxyEnabled=%%a

rem If proxy is not enabled
if "!proxyEnabled!"=="0x0" (
	 echo.
	 echo ========================================================
    echo The global proxy is not enabled. Users in mainland China may encounter network problems. 
	 echo If you need to set a proxy, please enable the global proxy and run again.
	 echo ========================================================
	 echo.
)

rem If proxy is enabled
if "!proxyEnabled!"=="0x1" (
	 echo.
	 echo ========================================================
    echo Proxy is enabled. Do you want to enable proxy for CMD and Git?
	 echo ========================================================
	 echo.
    set /p userChoice=Please enter y/n:
	 echo.
    
    if /I "!userChoice!"=="y" (
	     echo.
        echo Reading proxy server information...
	     echo.

        rem Read proxy server and port
        for /f "tokens=2,*" %%a in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer') do set proxyServer=%%b

	     echo.
        echo Proxy server: !proxyServer!
	     echo.

        rem Set proxy for CMD
        set http_proxy=http://!proxyServer!
        set https_proxy=https://!proxyServer!

	     echo.
        echo CMD proxy settings completed.
	     echo.

        rem Set proxy for Git
        git config --global http.proxy http://!proxyServer!
        git config --global https.proxy https://!proxyServer!

	     echo.
        echo Git proxy settings completed.
	     echo.
    )
)

timeout /t 10

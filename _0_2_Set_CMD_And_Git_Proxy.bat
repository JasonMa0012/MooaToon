@echo off
setlocal EnableDelayedExpansion

chcp 65001

rem Check if proxy is enabled
for /f "tokens=3" %%a in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable') do set proxyEnabled=%%a

rem If proxy is not enabled
if "!proxyEnabled!"=="0x0" (
	 echo.
	 echo ========================================================
    echo 全局代理未启用, 中国大陆地区的用户可能会遇到网络问题.
	 echo 如需设置代理, 请开启全局代理后再次运行.
    echo The global proxy is not enabled. Users in mainland China may encounter network problems. 
	 echo If you need to set a proxy, please enable the global proxy and run again.
	 echo ========================================================
	 echo.
)

rem If proxy is enabled
if "!proxyEnabled!"=="0x1" (
	 echo.
	 echo ========================================================
    echo 全局代理已启用, 是否需要为CMD和Git开启代理?
    echo Proxy is enabled. Do you want to enable proxy for CMD and Git?
	 echo ========================================================
	 echo.
    set /p userChoice=请输入y/n / Please enter y/n:
	 echo.
    
    if /I "!userChoice!"=="y" (
	     echo.
        echo 正在读取全局代理服务器信息...
        echo Reading proxy server information...
	     echo.

        rem Read proxy server and port
        for /f "tokens=2,*" %%a in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer') do set proxyServer=%%b

	     echo.
        echo 代理服务器: !proxyServer!
        echo Proxy server: !proxyServer!
	     echo.

        rem Set proxy for CMD
        set http_proxy=http://!proxyServer!
        set https_proxy=https://!proxyServer!

	     echo.
        echo CMD代理设置完成
        echo CMD proxy settings completed.
	     echo.

        rem Set proxy for Git
        git config --global http.proxy http://!proxyServer!
        git config --global https.proxy https://!proxyServer!

	     echo.
        echo Git代理设置完成
        echo Git proxy settings completed.
	     echo.
    )
)

timeout /t 10

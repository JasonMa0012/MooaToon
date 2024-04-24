@echo off
setlocal EnableDelayedExpansion

chcp 65001

rem :: Ask user if they want to unset previously set proxy
echo.
echo ========================================================
echo 是否需要取消设置代理?
echo Do you want to unset the proxy?
echo ========================================================
echo.
set /p userChoiceCancel=请输入y/n / Please enter y/n:
echo.

if /I "!userChoiceCancel!"=="y" (
    rem  :: Unset CMD proxy settings
    set http_proxy=
    set https_proxy=

    echo.
    echo CMD代理已取消
    echo CMD proxy has been unset.
    echo.

    rem  :: Unset Git proxy settings
    git config --global --unset http.proxy
    git config --global --unset https.proxy

    echo.
    echo Git代理已取消
    echo Git proxy has been unset.
    echo.
)

timeout /t 10
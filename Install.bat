@echo off
title Install Codex Switcher Suite
cls
echo ============================================================
echo INSTALLING CODEX LAUNCHER SUITE TO DESKTOP
echo ============================================================
echo.
set "REPO_DIR=%~dp0"
set "DESKTOP_DIR=C:\Users\Ludwig Rivera\Desktop"

echo Copying unified launcher...
copy /y "%REPO_DIR%Codex Switcher.bat" "%DESKTOP_DIR%\"

echo.
echo Codex Switcher copied to Desktop successfully!
echo.
pause

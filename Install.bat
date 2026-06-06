@echo off
title Install Codex Switcher Launchers
cls
echo ============================================================
echo INSTALLING CODEX SWITCHER LAUNCHERS TO DESKTOP
echo ============================================================
echo.
set "REPO_DIR=%~dp0"
set "DESKTOP_DIR=C:\Users\Ludwig Rivera\Desktop"

echo Copying launchers...
copy /y "%REPO_DIR%Codex Profile 1.bat" "%DESKTOP_DIR%\"
copy /y "%REPO_DIR%Codex Profile 2.bat" "%DESKTOP_DIR%\"
copy /y "%REPO_DIR%Codex Profile 3.bat" "%DESKTOP_DIR%\"
copy /y "%REPO_DIR%Codex Profile 4.bat" "%DESKTOP_DIR%\"
copy /y "%REPO_DIR%Codex Usage Summary.bat" "%DESKTOP_DIR%\"

echo.
echo Launchers copied to Desktop successfully!
echo.
pause

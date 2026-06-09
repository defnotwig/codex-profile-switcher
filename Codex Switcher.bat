@echo off
setlocal EnableExtensions EnableDelayedExpansion
title Codex Switcher Suite

set "REPO_DIR=C:\Users\Ludwig Rivera\Documents\codex-profile-switcher"
set "MANAGE_PY=%REPO_DIR%\manage_profiles.py"

:: Initialize the config if it does not exist
python "%MANAGE_PY%" init

:main_menu
cls
if "%PLAYED_ANIMATION%"=="" (
    python "%MANAGE_PY%" logo
    set "PLAYED_ANIMATION=1"
) else (
    python "%MANAGE_PY%" logo-static
)
echo ============================================================
echo SCANNING AND AUTO-BINDING ACCOUNTS...
echo ============================================================
python "%MANAGE_PY%" autobind
echo.

echo ============================================================
echo CODEX ACCOUNTS USAGE SUMMARY AND STATS
echo ============================================================
python "%MANAGE_PY%" show-stats
echo.

echo ============================================================
echo PROFILE SLOTS
echo ============================================================
python "%MANAGE_PY%" show-menu
echo.
echo ============================================================
echo ACTIONS
echo ============================================================
echo [1-8] Switch to profile slot and launch Codex
echo [L]   Log in a new account (launches browser login)
echo [U]   Unbind/Remove an account from a slot
echo [R]   Refresh summary and slots
echo [Q]   Quit
echo.

choice /C 12345678LURQ /N /M "Select option [1-8, L, U, R, Q]: "
set "choice_err=%errorlevel%"

if "%choice_err%"=="12" goto :quit
if "%choice_err%"=="11" goto :main_menu
if "%choice_err%"=="10" goto :unbind
if "%choice_err%"=="9" goto :login

:: Handle Slot switching (1 to 8)
set /a "slot_num=%choice_err%"
goto :switch

:login
echo.
echo Closing Codex to avoid file lock conflicts...
call :kill_codex
echo Starting Codex login flow...
echo Please sign in in the browser window that opens.
call npx @loongphy/codex-auth login
echo.
echo Auto-binding new account...
python "%MANAGE_PY%" autobind
echo.
pause
goto :main_menu

:unbind
echo.
set /p "unbind_slot=Enter slot number to unbind [1-8]: "
echo "%unbind_slot%"| findstr /r "^[1-8]$" >nul
if %errorlevel% neq 0 (
    echo Invalid slot number. Must be between 1 and 8.
    pause
    goto :main_menu
)
python "%MANAGE_PY%" unbind "%unbind_slot%"
echo.
pause
goto :main_menu

:switch
echo.
:: Get the email for this slot
set "TARGET_EMAIL="
for /f "delims=" %%i in ('python "%MANAGE_PY%" get "%slot_num%"') do set "TARGET_EMAIL=%%i"

if "%TARGET_EMAIL%"=="" (
    echo Profile slot %slot_num% is empty.
    echo.
    echo Would you like to log in a new account to bind to this slot?
    echo [1] Yes, log in and bind account
    echo [2] No, back to menu
    echo.
    choice /C 12 /N /M "Enter choice [1-2]: "
    if "!errorlevel!"=="1" (
        echo.
        echo Closing Codex to avoid file lock conflicts...
        call :kill_codex
        echo Starting Codex login flow...
        call npx @loongphy/codex-auth login
        echo.
        echo Binding newly logged-in account...
        python "%MANAGE_PY%" autobind
    )
    goto :main_menu
)

echo Closing Codex to avoid file lock conflicts...
call :kill_codex
echo Switching account to %TARGET_EMAIL%...
call npx @loongphy/codex-auth switch "%TARGET_EMAIL%"
echo.
echo Reopening Codex...
call :launch_codex
echo.
echo Switch completed successfully!
timeout /t 3
goto :main_menu

:quit
exit /b 0

:kill_codex
taskkill /IM codex.exe /F >nul 2>&1
timeout /t 1 /nobreak >nul
exit /b 0

:launch_codex
set "CODEX_EXE="
for /f "delims=" %%I in ('dir /b /s /a:-d "%LOCALAPPDATA%\OpenAI\Codex\bin\*\codex.exe" 2^>nul') do (
  set "CODEX_EXE=%%~fI"
)
if not defined CODEX_EXE if exist "%LOCALAPPDATA%\Programs\Codex\Codex.exe" set "CODEX_EXE=%LOCALAPPDATA%\Programs\Codex\Codex.exe"

if defined CODEX_EXE (
  start "" "%CODEX_EXE%" app
) else (
  start "" codex app
)
exit /b 0

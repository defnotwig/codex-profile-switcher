@echo off
setlocal EnableExtensions EnableDelayedExpansion

:: ==========================================
:: CODEX PROFILE CONFIGURATION
:: ==========================================
SET "ACCOUNT_EMAIL="
:: ==========================================

SET "MY_PATH=%~f0"
SET "AUTO_BIND_HELPER=C:\Users\Ludwig Rivera\Documents\codex-profile-switcher\auto_bind_profiles.py"
SET "UPDATE_HELPER=C:\Users\Ludwig Rivera\Documents\codex-profile-switcher\update_profile.py"

:: Check if account is set
if "%ACCOUNT_EMAIL%"=="" (
    cls
    echo ============================================================
    echo CODEX PROFILE SLOT 4 - EMPTY
    echo ============================================================
    echo This profile slot is currently empty.
    echo.
    echo Would you like to log in a new account to bind to this slot?
    echo [1] Yes, log in and bind account
    echo [2] No, exit
    echo.
    set /p "choice=Enter choice [1-2]: "
    if "!choice!"=="1" (
        echo.
        echo Starting Codex login flow...
        echo Please sign in in the browser window that opens.
        call npx @loongphy/codex-auth login
        
        echo.
        echo Binding newly logged-in account...
        python "!AUTO_BIND_HELPER!"
        
        echo.
        echo Profile bound! Reopening Codex...
        call :restart_codex
        exit /b 0
    )
    exit /b 0
)

:: If account is set, check if it's currently active
python -c "import subprocess; out=subprocess.check_output(['npx', '@loongphy/codex-auth', 'list'], text=True, shell=True); active=[line.split()[2] for line in out.splitlines() if line.strip().startswith('*')]; open('active.tmp', 'w').write(active[0] if active else '')"
set "ACTIVE_EMAIL="
if exist active.tmp (
    set /p "ACTIVE_EMAIL="<active.tmp
    del active.tmp
)

cls
echo ============================================================
echo CODEX PROFILE 4 - %ACCOUNT_EMAIL%
echo ============================================================
if /I "%ACTIVE_EMAIL%"=="%ACCOUNT_EMAIL%" (
    echo Status: Currently ACTIVE
) else (
    echo Status: Currently INACTIVE
)
echo.
echo [1] Switch to this profile and open Codex (Default in 5 seconds)
echo [2] Unbind/Remove this account from this profile slot
echo [3] Exit
echo.

set "choice=1"
choice /C 123 /T 5 /D 1 /N /M "Select option [1-3] (auto-selecting 1 in 5s): "
if errorlevel 3 goto :exit
if errorlevel 2 goto :unbind
if errorlevel 1 goto :switch

:switch
echo.
if /I not "%ACTIVE_EMAIL%"=="%ACCOUNT_EMAIL%" (
    echo Switching account to %ACCOUNT_EMAIL%...
    call npx @loongphy/codex-auth switch "%ACCOUNT_EMAIL%"
) else (
    echo Profile is already active.
)
echo Reopening Codex...
call :restart_codex
exit /b 0

:unbind
echo.
echo Unbinding account %ACCOUNT_EMAIL% from this slot...
python "!UPDATE_HELPER!" "!MY_PATH!" "" & echo Profile slot cleared. & pause & exit /b 0

:exit
exit /b 0

:restart_codex
taskkill /IM codex.exe /F >nul 2>&1
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

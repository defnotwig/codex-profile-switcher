@echo off
title Codex Accounts Usage Summary
cls
echo Scanning and auto-binding profiles...
python "C:\Users\Ludwig Rivera\Documents\codex-profile-switcher\auto_bind_profiles.py"
echo.
echo ============================================================
echo CODEX ACCOUNTS USAGE SUMMARY AND STATS
echo ============================================================
echo.
call npx @loongphy/codex-auth list
echo.
echo ============================================================
pause

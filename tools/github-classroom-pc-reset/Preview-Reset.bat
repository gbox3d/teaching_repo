@echo off
setlocal
title Preview GitHub Classroom Reset
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0GitHub-Classroom-Reset.ps1" -RemoveSshKeys -RemoveVSCodeAuth
set "RESET_EXIT=%ERRORLEVEL%"
echo.
pause
exit /b %RESET_EXIT%

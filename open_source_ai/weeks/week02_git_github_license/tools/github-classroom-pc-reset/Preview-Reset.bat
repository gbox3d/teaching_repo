@echo off
setlocal
title Preview GitHub Classroom Reset
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0GitHub-Classroom-Reset.ps1" -RemoveSshKeys -RemoveVSCodeAuth
echo.
pause

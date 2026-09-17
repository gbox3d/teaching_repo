@echo off
setlocal
title GitHub Classroom Shared-PC Reset

echo ========================================================
echo  GitHub Classroom Shared-PC Reset
echo ========================================================
echo.
echo This removes Git/GitHub credentials for the CURRENT user.
echo It also removes standard SSH keys and VS Code GitHub auth.
echo Browser cookies are NOT removed.
echo.
choice /C YN /N /M "Continue? [Y/N]: "
if errorlevel 2 goto :cancel

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0GitHub-Classroom-Reset.ps1" -Execute -Force -RemoveSshKeys -RemoveVSCodeAuth
set "RESET_EXIT=%ERRORLEVEL%"

echo.
if "%RESET_EXIT%"=="0" (
    echo Reset finished successfully.
) else (
    echo Reset finished with one or more warnings. Review the messages above.
)
pause
exit /b %RESET_EXIT%

:cancel
echo.
echo Cancelled. Nothing was changed.
pause
exit /b 0

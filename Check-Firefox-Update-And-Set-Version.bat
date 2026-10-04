@echo off
setlocal
cd /d "%~dp0"
title Rinswa Browser - Check Firefox Update ^& Set Version
color 0B

echo =======================================================
echo    RINSWA BROWSER - UPDATE CHECKER ^& VERSION TOOL
echo          Developed and made by Arindam Makar
echo =======================================================
echo.

:: Detect Python environment
set "PYTHON_EXE=python"
where python >nul 2>nul
if not %ERRORLEVEL%==0 (
    if exist "C:\Users\arind\AppData\Local\Python\pythoncore-3.11-64\python.exe" (
        set "PYTHON_EXE=C:\Users\arind\AppData\Local\Python\pythoncore-3.11-64\python.exe"
    ) else if exist "C:\Python311\python.exe" (
        set "PYTHON_EXE=C:\Python311\python.exe"
    ) else if exist "C:\Python312\python.exe" (
        set "PYTHON_EXE=C:\Python312\python.exe"
    ) else (
        echo [ERROR] Python 3 was not found in PATH or standard install locations!
        echo Please ensure Python is installed before continuing.
        echo.
        pause
        exit /b 1
    )
)

"%PYTHON_EXE%" scripts\check-and-update-version.py %*
if not %ERRORLEVEL%==0 (
    echo.
    echo [NOTE] Process finished with code %ERRORLEVEL%.
    pause
    exit /b %ERRORLEVEL%
)

exit /b 0

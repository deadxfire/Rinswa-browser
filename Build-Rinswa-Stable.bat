@echo off
cd /d "%~dp0"

set "RINSWA_VERSION=1.0.5"
if exist "rinswa-version.txt" (
    set /p RINSWA_VERSION=<"rinswa-version.txt"
)
set "RINSWA_VERSION=%RINSWA_VERSION: =%"

title Rinswa Browser Stable v%RINSWA_VERSION% - Build System
color 0B

echo =======================================================
echo          RINSWA BROWSER STABLE (v%RINSWA_VERSION%) BUILD
echo          Developed and made by Arindam Makar
echo =======================================================
echo.
echo Version:   %RINSWA_VERSION% Stable (Official Release Engine)
echo Directory: rinswa-stable\
echo Output:    rinswa-stable\obj-rinswa\dist\
echo.
echo What this script will do:
echo 1. Verify modern Firefox Stable engine source.
echo 2. Set version to %RINSWA_VERSION% Stable and remove Nightly/experimental flags.
echo 3. Inject custom Rinswa branding, Cyber-Glass theme, and icons.
echo 4. Compile the full Gecko engine.
echo 5. Package the standalone installer (.exe) into rinswa-stable\obj-rinswa\dist\
echo.
echo Press any key to start building Rinswa Stable...
pause >nul

IF NOT EXIST "C:\mozilla-build\start-shell.bat" (
    echo.
    echo [ERROR] MozillaBuild is not installed at C:\mozilla-build\
    echo Please install MozillaBuild before continuing.
    goto :fail
)

IF NOT EXIST "rinswa-stable" (
    echo.
    echo [ERROR] The rinswa-stable source folder is missing!
    echo Ensure the worktree exists.
    goto :fail
)

echo.
echo [Step 0/4] Preparing Rinswa asset generation...
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\gen-branding-assets.ps1
IF NOT %ERRORLEVEL%==0 (
    echo [ERROR] Failed to generate branding icons.
    goto :fail
)

echo.
echo Handing execution over to MozillaBuild environment...
call C:\mozilla-build\start-shell.bat /c/Users/arind/OneDrive/Documents/Project/browser/scripts/build-stable.sh
IF NOT %ERRORLEVEL%==0 goto :fail

echo.
echo =======================================================
echo               STABLE BUILD COMPLETE!
echo =======================================================
echo.
echo Standalone Installer: rinswa-stable\obj-rinswa\dist\install\sea\
echo Portable Build:       rinswa-stable\obj-rinswa\dist\
echo.
if exist "rinswa-stable\obj-rinswa\dist\install\sea" (
    explorer "rinswa-stable\obj-rinswa\dist\install\sea"
) else (
    explorer "rinswa-stable\obj-rinswa\dist"
)
pause
exit /b 0

:fail
echo.
echo =======================================================
echo                 STABLE BUILD FAILED
echo =======================================================
echo An error occurred during the build pipeline.
echo Check the console output above for the specific error.
echo.
pause
exit /b 1

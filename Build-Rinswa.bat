@echo off
title Rinswa Browser Build System
color 0B

echo =======================================================
echo               RINSWA BROWSER BUILD SYSTEM
echo           Developed and made by Arindam Makar
echo =======================================================
echo.
echo What this script will do:
echo 1. Verify modern Firefox/Gecko engine source.
echo 2. Download compiler dependencies and Windows SDK components.
echo 3. Inject custom Rinswa UI, branding, and icons.
echo 4. Compile the full Gecko engine (takes 1-3 hours).
echo 5. Package the standalone installer (.exe) into obj-rinswa\dist\
echo.
echo WARNING: This process is computationally intensive and will
echo push your CPU to 100%%. DO NOT CLOSE THIS WINDOW!
echo.
pause

cd /d "%~dp0"

IF NOT EXIST "C:\mozilla-build\start-shell.bat" (
    echo.
    echo [ERROR] MozillaBuild is not installed at C:\mozilla-build\
    echo Please install MozillaBuild before continuing.
    goto :fail
)

IF NOT EXIST "mozilla-central" (
    echo.
    echo [ERROR] The mozilla-central source folder is missing!
    echo Ensure the repository clone exists.
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
call C:\mozilla-build\start-shell.bat /c/Users/arind/OneDrive/Documents/Project/browser/scripts/build-pipeline.sh
IF NOT %ERRORLEVEL%==0 goto :fail

echo.
echo =======================================================
echo                    BUILD COMPLETE!
echo =======================================================
echo.
echo Standalone Installer: mozilla-central\obj-rinswa\dist\install\sea\
echo Portable Build:       mozilla-central\obj-rinswa\dist\
echo.
if exist "mozilla-central\obj-rinswa\dist\install\sea" (
    explorer "mozilla-central\obj-rinswa\dist\install\sea"
) else (
    explorer "mozilla-central\obj-rinswa\dist"
)
pause
exit /b 0

:fail
echo.
echo =======================================================
echo                    BUILD FAILED
echo =======================================================
echo An error occurred during the build pipeline.
echo Check the console output above for the specific error.
echo.
pause
exit /b 1

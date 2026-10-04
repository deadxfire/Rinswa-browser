@echo off
cd /d "%~dp0"
call Check-Firefox-Update-And-Set-Version.bat %*
exit /b %ERRORLEVEL%

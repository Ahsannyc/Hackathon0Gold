@echo off
REM Cross Domain Integrator - Easy Manual Trigger
REM This script runs the Cross Domain Integrator from anywhere
REM Usage: Double-click this file or run: run-cross-domain.bat

setlocal enabledelayedexpansion

REM Get the directory where this script is located
cd /d "%~dp0"

echo.
echo ======================================================================
echo CROSS DOMAIN INTEGRATOR - Manual Trigger
echo ======================================================================
echo.
echo Timestamp: %date% %time%
echo Location: %CD%
echo.
echo [RUNNING] Cross Domain Integrator...
echo.

REM Run the integrator
python skills/cross_domain_integrator.py

REM Capture exit code
set EXIT_CODE=%ERRORLEVEL%

echo.
echo ======================================================================
if %EXIT_CODE% equ 0 (
    echo [SUCCESS] Integration completed successfully!
) else (
    echo [ERROR] Process exited with code %EXIT_CODE%
)
echo ======================================================================
echo.
echo Next: Check /Pending_Approval/ and /Approved/ folders
echo Summary: Logs/cross_domain_*.md
echo.
pause

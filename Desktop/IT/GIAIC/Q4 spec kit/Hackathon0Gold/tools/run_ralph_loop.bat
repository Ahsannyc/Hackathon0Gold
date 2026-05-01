@echo off
REM Ralph Wiggum Loop Convenience Wrapper for Windows
REM Usage: run_ralph_loop.bat task_id "Your task description" [--max-iterations N] [--use-promise]

setlocal enabledelayedexpansion

if "%2"=="" (
    echo Ralph Wiggum Loop Executor
    echo.
    echo Usage: %0 ^<task_id^> ^<prompt^> [options]
    echo.
    echo Options:
    echo   --max-iterations N    Maximum iterations (default: 10)
    echo   --use-promise         Wait for promise signal instead of file move
    echo.
    echo Examples:
    echo   %0 invoices_daily "Process all invoices"
    echo   %0 social_weekly "Post weekly content" --max-iterations 20
    exit /b 1
)

set TASK_ID=%1
set PROMPT=%2
set MAX_ITERATIONS=10
set USE_PROMISE=
shift
shift

REM Parse optional arguments
:parse_args
if "%1"=="" goto run_task
if "%1"=="--max-iterations" (
    set MAX_ITERATIONS=%2
    shift
    shift
    goto parse_args
)
if "%1"=="--use-promise" (
    set USE_PROMISE=--use-promise
    shift
    goto parse_args
)
shift
goto parse_args

:run_task
echo.
echo ========================================================
echo          Ralph Wiggum Loop Executor
echo ========================================================
echo.
echo Task ID:          %TASK_ID%
echo Prompt:           %PROMPT%
echo Max Iterations:   %MAX_ITERATIONS%
echo Use Promise:      %USE_PROMISE%
echo.

REM Get script directory
set SCRIPT_DIR=%~dp0
REM Remove trailing backslash
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%
REM Get vault directory (parent of tools)
for %%A in ("%SCRIPT_DIR%\..") do set VAULT_DIR=%%~fA

REM Verify executor exists
if not exist "%SCRIPT_DIR%\ralph_wiggum_executor.py" (
    echo Error: ralph_wiggum_executor.py not found
    exit /b 1
)

REM Create required directories
if not exist "%VAULT_DIR%\Plans" mkdir "%VAULT_DIR%\Plans"
if not exist "%VAULT_DIR%\Done" mkdir "%VAULT_DIR%\Done"
if not exist "%VAULT_DIR%\Logs" mkdir "%VAULT_DIR%\Logs"
if not exist "%VAULT_DIR%\.ralph-state" mkdir "%VAULT_DIR%\.ralph-state"

REM Build and run command
set PYTHON_CMD=python "%SCRIPT_DIR%\ralph_wiggum_executor.py" "%TASK_ID%" "%PROMPT%" --max-iterations %MAX_ITERATIONS% %USE_PROMISE%

echo Starting Ralph Wiggum loop...
echo.

REM Change to vault directory
pushd "%VAULT_DIR%"

REM Run executor
%PYTHON_CMD%
set RESULT=%ERRORLEVEL%

REM Show results
echo.
if %RESULT% equ 0 (
    echo Task completed successfully [OK]
    if exist ".ralph-state\%TASK_ID%.json" (
        echo.
        echo Task State:
        type ".ralph-state\%TASK_ID%.json"
    )
) else (
    echo Task execution failed or incomplete [ERROR]
    if exist ".ralph-state\%TASK_ID%.json" (
        echo.
        echo Task State ^(for debugging^):
        type ".ralph-state\%TASK_ID%.json"
    )
    echo.
    echo Debugging tips:
    echo   1. Check logs: type Logs\ralph_wiggum.log ^| more
    echo   2. Check task file: type Plans\TASK_%TASK_ID%.md
    echo   3. Check state: type .ralph-state\%TASK_ID%.json
)

popd
exit /b %RESULT%

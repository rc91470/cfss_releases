@echo off
REM Quick start script for CFSS development

echo ================================
echo CFSS Quick Start
echo ================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Virtual environment not found!
    echo Running initial setup...
    echo.
    call setup_dev_windows.bat
    if errorlevel 1 (
        echo Setup failed!
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check if in virtual environment
if not defined VIRTUAL_ENV (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

echo Virtual environment active: %VIRTUAL_ENV%
echo.

echo Available commands:
echo.
echo [1] Run CFSS Application
echo [2] Build Windows Executable  
echo [3] Create Release Package
echo [4] Open VS Code
echo [5] Run Tests (if available)
echo [6] Exit
echo.

set /p "choice=Enter your choice (1-6): "

if "%choice%"=="1" (
    echo.
    echo Starting CFSS Application...
    python cfss_app.py
) else if "%choice%"=="2" (
    echo.
    echo Building Windows executable...
    call build_windows.bat
) else if "%choice%"=="3" (
    echo.
    echo Creating release package...
    call release_windows.bat
) else if "%choice%"=="4" (
    echo.
    echo Opening VS Code...
    code .
) else if "%choice%"=="5" (
    echo.
    echo Running tests...
    if exist "tests" (
        python -m pytest tests/
    ) else (
        echo No tests directory found.
        echo You can create tests in a 'tests' directory.
    )
) else if "%choice%"=="6" (
    echo.
    echo Goodbye!
    exit /b 0
) else (
    echo.
    echo Invalid choice. Please select 1-6.
    pause
    goto start
)

echo.
pause

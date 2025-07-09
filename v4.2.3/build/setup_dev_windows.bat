@echo off
REM Windows Development Setup Script for CFSS
REM This script sets up the development environment

echo ================================
echo CFSS Windows Development Setup
echo ================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8+ from python.org
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

python --version
echo.

echo Checking if virtual environment exists...
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
    echo.
) else (
    echo Virtual environment already exists.
    echo.
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

echo Virtual environment activated: %VIRTUAL_ENV%
echo.

echo Installing/updating pip...
python -m pip install --upgrade pip

echo.
echo Installing development dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install requirements!
        pause
        exit /b 1
    )
) else (
    echo WARNING: requirements.txt not found. Installing basic dependencies...
    pip install customtkinter pygame natsort
)

echo.
echo Installing development tools...
pip install pyinstaller black isort flake8

echo.
echo Creating necessary directories...
if not exist "data" mkdir "data"
if not exist "sounds" mkdir "sounds"
if not exist "test_results" mkdir "test_results"
if not exist "releases" mkdir "releases"

echo.
echo Checking for required files...
if not exist "cfss_app.py" (
    echo WARNING: cfss_app.py not found!
    echo This is the main application file.
)

if not exist "data_manager.py" (
    echo WARNING: data_manager.py not found!
)

if not exist "circuit_manager.py" (
    echo WARNING: circuit_manager.py not found!
)

if not exist "scan_controller.py" (
    echo WARNING: scan_controller.py not found!
)

echo.
echo Setting up VS Code configuration...
if not exist ".vscode" mkdir ".vscode"

if exist "windows_vscode_settings.json" (
    copy "windows_vscode_settings.json" ".vscode\settings.json" /y >nul
    echo VS Code settings configured for Windows development.
) else (
    echo WARNING: windows_vscode_settings.json not found!
)

echo.
echo Creating launch configuration for debugging...
(
echo {
echo     "version": "0.2.0",
echo     "configurations": [
echo         {
echo             "name": "Python: CFSS App",
echo             "type": "python",
echo             "request": "launch",
echo             "program": "${workspaceFolder}/cfss_app.py",
echo             "console": "integratedTerminal",
echo             "justMyCode": false,
echo             "args": []
echo         }
echo     ]
echo }
) > ".vscode\launch.json"

echo.
echo ================================
echo Setup completed successfully!
echo ================================
echo.
echo Your Windows development environment is ready!
echo.
echo Next steps:
echo 1. Open VS Code in this directory: code .
echo 2. Install recommended extensions when prompted
echo 3. Run the application with: python cfss_app.py
echo 4. Build executable with: build_windows.bat
echo 5. Create release with: release_windows.bat
echo.
echo Virtual environment is activated and ready to use.
echo To deactivate: deactivate
echo To reactivate: .venv\Scripts\activate.bat
echo.

set /p "open_vscode=Would you like to open VS Code now? (y/n): "
if /i "%open_vscode%"=="y" (
    echo Opening VS Code...
    code .
)

echo.
echo Development setup completed.
pause

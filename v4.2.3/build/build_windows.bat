@echo off
REM CFSS Windows Build Script for DEVELOPMENT TESTING ONLY
REM 
REM WARNING: This is for local development testing only!
REM WARNING: All official builds should be done in the cfss_releases repository
REM WARNING: This development repository should NOT contain .exe files
REM
REM For official releases:
REM 1. Use the build scripts in cfss_releases repository
REM 2. Never commit .exe files to this repository  
REM 3. Keep development and distribution separate

echo ================================
echo CFSS Windows Development Build
echo FOR LOCAL TESTING ONLY
echo ================================
echo.
echo WARNING: This is for local testing only - not for distribution!
echo.

REM SECURITY: Run security check first (if available)
echo SECURITY: Running pre-build security check...
if exist "security_check.sh" (
    bash security_check.sh
    if errorlevel 1 (
        echo WARNING: Security check found customer data - proceeding with cleanup...
    )
) else (
    echo WARNING: security_check.sh not found - proceeding with standard cleanup...
)

REM SECURITY: Clean data folder to prevent customer data in build
echo SECURITY: Cleaning data folder to prevent customer data inclusion...
if exist "data" (
    echo   Backing up data folder...
    if not exist "data_backups" mkdir "data_backups"
    xcopy "data" "data_backups\data_backup_%DATE:/=-%_%TIME::=-%" /E /I /Q > nul
    echo   Clearing data folder contents...
    del /Q "data\*.csv" 2>nul
    echo   ✅ Data folder cleaned - no customer data will be included in build
) else (
    echo   Data folder doesn't exist, creating empty one...
    mkdir "data"
)

REM Create empty .gitkeep file to preserve folder structure
echo. > "data\.gitkeep"

REM Check if virtual environment is active
if not defined VIRTUAL_ENV (
    echo ERROR: Virtual environment not detected!
    echo Please activate your virtual environment first:
    echo   .venv\Scripts\activate
    echo.
    pause
    exit /b 1
)

echo Virtual environment: %VIRTUAL_ENV%
echo.

REM Check if required files exist
if not exist "cfss_app.py" (
    echo ERROR: cfss_app.py not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found!
    pause
    exit /b 1
)

echo Installing/updating dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller!
    pause
    exit /b 1
)

echo.
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec"

echo.
echo Building CFSS application...
echo This may take several minutes...

pyinstaller --onefile --windowed --name="CFSS_v4.2.3" --add-data "data;data" --add-data "sounds;sounds" cfss_app.py data_manager.py circuit_manager.py scan_controller.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo Check the output above for error details.
    pause
    exit /b 1
)

echo.
echo ================================
echo Build completed successfully!
echo ================================
echo.
echo Executable location: dist\CFSS_v4.2.3.exe
echo.

REM Check if executable was created
if exist "dist\CFSS_v4.2.3.exe" (
    echo File size:
    dir "dist\CFSS_v4.2.3.exe" | find "CFSS_v4.2.3.exe"
    echo.
    echo The application is ready for distribution!
    echo.
    
    set /p "test_run=Would you like to test run the application? (y/n): "
    if /i "%test_run%"=="y" (
        echo.
        echo Starting CFSS application...
        start "" "dist\CFSS_v4.2.3.exe"
    )
) else (
    echo ERROR: Executable not found after build!
    exit /b 1
)

echo.
echo Build script completed.
pause

@echo off
REM CFSS v4.3.11 Installation Script
REM Enhanced with component validation and data preservation

echo ========================================
echo CFSS v4.3.11 Installation 
echo ========================================
echo.
echo This version includes enhanced auto-updater fixes:
echo - Validates critical folders (sounds, data) after updates
echo - Restores missing components automatically  
echo - Preserves your existing data and CSV files
echo.

set INSTALL_DIR=%~dp0
set TARGET_DIR=%PROGRAMFILES%\CFSS

echo Installing CFSS v4.3.11...
echo Source: %INSTALL_DIR%
echo Target: %TARGET_DIR%
echo.

REM Create target directory
if not exist "%TARGET_DIR%" (
    echo Creating installation directory...
    mkdir "%TARGET_DIR%"
)

REM Copy main executable
if exist "%INSTALL_DIR%CFSS_v4.3.11.exe" (
    echo ✓ Installing main executable...
    copy "%INSTALL_DIR%CFSS_v4.3.11.exe" "%TARGET_DIR%\" > nul
    if errorlevel 1 (
        echo ❌ Failed to install executable
        goto :error
    )
) else (
    echo ❌ Error: CFSS_v4.3.11.exe not found!
    goto :error
)

REM Handle data folder (preserve existing, create if new install)
if exist "%TARGET_DIR%\data" (
    echo ✓ Preserving existing data folder (CSV files and database)
) else (
    echo ✓ Creating data folder for new installation...
    mkdir "%TARGET_DIR%\data"
    if exist "%INSTALL_DIR%data\README.txt" (
        copy "%INSTALL_DIR%data\README.txt" "%TARGET_DIR%\data\" > nul
    )
)

REM Handle sounds folder (always ensure it exists with correct files)
echo ✓ Installing sounds folder (critical for proper operation)...
if not exist "%TARGET_DIR%\sounds" mkdir "%TARGET_DIR%\sounds"
if exist "%INSTALL_DIR%sounds" (
    xcopy "%INSTALL_DIR%sounds\*.*" "%TARGET_DIR%\sounds\" /Y /Q > nul
    if errorlevel 1 (
        echo ❌ Failed to install sounds folder
        goto :error
    )
) else (
    echo ❌ Warning: sounds folder missing from installation package!
)

echo.
echo ========================================
echo Installation Validation
echo ========================================

REM Validate installation
set VALIDATION_PASSED=1

echo Checking executable...
if exist "%TARGET_DIR%\CFSS_v4.3.11.exe" (
    echo ✓ Executable: Found
) else (
    echo ❌ Executable: Missing
    set VALIDATION_PASSED=0
)

echo Checking sounds folder (critical for proper feedback)...
if exist "%TARGET_DIR%\sounds\match.mp3" (
    echo ✓ match.mp3: Found
) else (
    echo ❌ match.mp3: Missing - will cause Windows popups instead of green ring
    set VALIDATION_PASSED=0
)

if exist "%TARGET_DIR%\sounds\nonmatch.mp3" (
    echo ✓ nonmatch.mp3: Found  
) else (
    echo ❌ nonmatch.mp3: Missing - will cause Windows popups instead of red ring
    set VALIDATION_PASSED=0
)

echo Checking data folder...
if exist "%TARGET_DIR%\data" (
    echo ✓ Data folder: Found
) else (
    echo ❌ Data folder: Missing
    set VALIDATION_PASSED=0
)

echo.
if %VALIDATION_PASSED%==1 (
    echo ✅ Installation successful! CFSS v4.3.11 ready to use.
    echo.
    echo Enhanced Features in v4.3.11:
    echo - Auto-updater validates and restores missing components
    echo - Better handling of sounds folder during updates
    echo - Data preservation during updates
    echo.
    echo Run: "%TARGET_DIR%\CFSS_v4.3.11.exe"
) else (
    echo ❌ Installation completed with warnings!
    echo Some components may be missing - CFSS may not work properly.
)

pause
exit /b 0

:error
echo ❌ Installation failed!
pause
exit /b 1

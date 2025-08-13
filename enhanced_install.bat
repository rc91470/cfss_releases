@echo off
REM CFSS Enhanced Installation Script v4.2.4+
REM Validates installation and ensures all components are present

echo ========================================
echo CFSS Enhanced Installation Script
echo ========================================
echo.

set INSTALL_DIR=%~dp0
set TARGET_DIR=%PROGRAMFILES%\CFSS

echo Installing CFSS v4.2.4...
echo Source: %INSTALL_DIR%
echo Target: %TARGET_DIR%
echo.

REM Create target directory
if not exist "%TARGET_DIR%" (
    echo Creating installation directory...
    mkdir "%TARGET_DIR%"
)

REM Copy main executable
if exist "%INSTALL_DIR%CFSS_v4.2.4.exe" (
    echo ✓ Copying main executable...
    copy "%INSTALL_DIR%CFSS_v4.2.4.exe" "%TARGET_DIR%\" > nul
    if errorlevel 1 (
        echo ❌ Failed to copy executable
        goto :error
    )
) else (
    echo ❌ Error: CFSS_v4.2.4.exe not found!
    goto :error
)

REM Copy data folder
if exist "%INSTALL_DIR%data" (
    echo ✓ Copying data folder...
    if not exist "%TARGET_DIR%\data" mkdir "%TARGET_DIR%\data"
    xcopy "%INSTALL_DIR%data\*.*" "%TARGET_DIR%\data\" /Y /Q > nul
    if errorlevel 1 (
        echo ❌ Failed to copy data folder
        goto :error
    )
) else (
    echo ❌ Warning: data folder not found!
    echo Creating empty data folder...
    mkdir "%TARGET_DIR%\data"
    echo This folder should contain CSV files with circuit data. > "%TARGET_DIR%\data\README.txt"
    echo Contact your administrator to get the correct CSV files. >> "%TARGET_DIR%\data\README.txt"
)

REM Copy sounds folder (CRITICAL for proper operation)
if exist "%INSTALL_DIR%sounds" (
    echo ✓ Copying sounds folder...
    if not exist "%TARGET_DIR%\sounds" mkdir "%TARGET_DIR%\sounds"
    xcopy "%INSTALL_DIR%sounds\*.*" "%TARGET_DIR%\sounds\" /Y /Q > nul
    if errorlevel 1 (
        echo ❌ Failed to copy sounds folder
        goto :error
    )
) else (
    echo ❌ Warning: sounds folder not found!
    echo This is CRITICAL - without sounds, you'll get Windows popups instead of proper feedback
    echo Creating empty sounds folder...
    mkdir "%TARGET_DIR%\sounds"
    echo CFSS requires these sound files for proper operation: > "%TARGET_DIR%\sounds\README.txt"
    echo - match.mp3: Played when scan finds a match >> "%TARGET_DIR%\sounds\README.txt"
    echo - nonmatch.mp3: Played when scan finds no match >> "%TARGET_DIR%\sounds\README.txt"
    echo - complete.mp3: Played when scan is complete >> "%TARGET_DIR%\sounds\README.txt"
    echo. >> "%TARGET_DIR%\sounds\README.txt"
    echo Without these files, CFSS will show Windows error popups >> "%TARGET_DIR%\sounds\README.txt"
    echo instead of the normal red/green visual feedback and tones. >> "%TARGET_DIR%\sounds\README.txt"
    echo. >> "%TARGET_DIR%\sounds\README.txt"
    echo Download the complete installation package from GitHub. >> "%TARGET_DIR%\sounds\README.txt"
)

REM Copy documentation
if exist "%INSTALL_DIR%*.md" (
    echo ✓ Copying documentation...
    copy "%INSTALL_DIR%*.md" "%TARGET_DIR%\" > nul 2>&1
)

echo.
echo ========================================
echo Installation Validation
echo ========================================

REM Validate installation
set VALIDATION_PASSED=1

echo Checking executable...
if exist "%TARGET_DIR%\CFSS_v4.2.4.exe" (
    echo ✓ Executable: Found
) else (
    echo ❌ Executable: Missing
    set VALIDATION_PASSED=0
)

echo Checking data folder...
if exist "%TARGET_DIR%\data" (
    echo ✓ Data folder: Found
    dir "%TARGET_DIR%\data\*.csv" > nul 2>&1
    if errorlevel 1 (
        echo ⚠️ Warning: No CSV files found in data folder
        echo   You'll need CSV files for serial number lookup to work
    ) else (
        echo ✓ CSV files: Found
    )
) else (
    echo ❌ Data folder: Missing
    set VALIDATION_PASSED=0
)

echo Checking sounds folder...
if exist "%TARGET_DIR%\sounds" (
    echo ✓ Sounds folder: Found
    if exist "%TARGET_DIR%\sounds\match.mp3" (
        echo ✓ match.mp3: Found
    ) else (
        echo ❌ match.mp3: Missing - you'll get Windows popups instead of green ring
        set VALIDATION_PASSED=0
    )
    if exist "%TARGET_DIR%\sounds\nonmatch.mp3" (
        echo ✓ nonmatch.mp3: Found
    ) else (
        echo ❌ nonmatch.mp3: Missing - you'll get Windows popups instead of red ring  
        set VALIDATION_PASSED=0
    )
    if exist "%TARGET_DIR%\sounds\complete.mp3" (
        echo ✓ complete.mp3: Found
    ) else (
        echo ❌ complete.mp3: Missing - no completion sound
        set VALIDATION_PASSED=0
    )
) else (
    echo ❌ Sounds folder: Missing - CRITICAL ISSUE
    set VALIDATION_PASSED=0
)

echo.
echo ========================================
echo Installation Results
echo ========================================

if %VALIDATION_PASSED%==1 (
    echo ✅ Installation completed successfully!
    echo All required components are present.
    echo.
    echo You can run CFSS from: "%TARGET_DIR%\CFSS_v4.2.4.exe"
    echo.
    echo Creating desktop shortcut...
    powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\CFSS v4.2.4.lnk'); $Shortcut.TargetPath = '%TARGET_DIR%\CFSS_v4.2.4.exe'; $Shortcut.WorkingDirectory = '%TARGET_DIR%'; $Shortcut.Save()"
    echo ✓ Desktop shortcut created
) else (
    echo ❌ Installation completed with WARNINGS!
    echo Missing components detected - CFSS may not work properly.
    echo.
    echo RECOMMENDED ACTION:
    echo 1. Download the COMPLETE ZIP package from GitHub
    echo 2. Extract the FULL package (not just the .exe file)
    echo 3. Run install.bat again
    echo.
    echo Current installation: "%TARGET_DIR%"
)

echo.
echo Installation log saved to: "%TARGET_DIR%\installation.log"
echo.

REM Create installation log
echo CFSS Installation Log > "%TARGET_DIR%\installation.log"
echo ===================== >> "%TARGET_DIR%\installation.log"
echo Date: %DATE% %TIME% >> "%TARGET_DIR%\installation.log"
echo Source: %INSTALL_DIR% >> "%TARGET_DIR%\installation.log"
echo Target: %TARGET_DIR% >> "%TARGET_DIR%\installation.log"
echo Validation Passed: %VALIDATION_PASSED% >> "%TARGET_DIR%\installation.log"

pause
exit /b 0

:error
echo.
echo ❌ Installation failed!
echo Check that you have administrator privileges and try again.
pause
exit /b 1

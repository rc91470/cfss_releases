# CFSS - Copper/Fiber Serial Scanner

![CFSS Logo](https://img.shields.io/badge/CFSS-v4.2.2-blue?style=for-the-badge&logo=desktop)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Professional fiber optic and copper circuit scanning application with auto-updater, SharePoint integration, and comprehensive reporting capabilities.**

## 🚀 Quick Download - Latest Version (v4.2.2)

### Windows
[![Download Windows](https://img.shields.io/badge/Download-Windows-0078D4?style=for-the-badge&logo=windows)](https://github.com/rc91470/cfss_releases/releases/download/v4.2.2/CFSS_v4.2.2_Windows.zip)

**File:** `CFSS_v4.2.2_Windows.zip` (~23MB)

### macOS
[![Download macOS](https://img.shields.io/badge/Download-macOS-000000?style=for-the-badge&logo=apple)](https://github.com/rc91470/cfss_releases/releases/download/v4.2.2/CFSS-macOS-4.2.2.tar.gz)

**File:** `CFSS-macOS-4.2.2.tar.gz` (~20MB)

---

## 📋 What's New in v4.2.2

### ✨ New Features
- **Auto-updater functionality** - Automatically checks for and installs updates
- **Enhanced SharePoint integration** - Seamless CSV sync and data export
- **Smart progress migration** - Preserves scan progress when updating circuit data
- **Issue tracking system** - Comprehensive problem tracking and resolution notes
- **Improved user interface** - Better input validation and error handling

### 🔧 Bug Fixes
- Fixed input field focus and validation issues
- Improved CSV import error handling
- Enhanced database stability and performance
- Better error messages and user feedback

### 🛠️ Technical Improvements
- Optimized scanning workflow
- Enhanced data export capabilities
- Improved cross-platform compatibility
- Better memory management

---

## 📦 Installation Instructions

### Windows Installation

1. **Download** the Windows zip file from the link above
2. **Extract** the zip file to your desired location (e.g., `C:\CFSS\`)
3. **Run** `CFSS_v4.2.2.exe` from the extracted folder
4. **Optional:** Create a desktop shortcut for easy access

**Requirements:**
- Windows 10 or higher
- 100MB free disk space
- No additional software required (self-contained)

### macOS Installation

1. **Download** the macOS tar.gz file from the link above
2. **Extract** the archive (double-click or use `tar -xzf CFSS-macOS-4.2.2.tar.gz`)
3. **Move** the CFSS app to your Applications folder (optional)
4. **Run** the CFSS application
5. **Allow** the app to run if prompted by macOS security

**Requirements:**
- macOS 10.14 (Mojave) or higher
- 100MB free disk space
- May require allowing app in Security & Privacy settings

---

## 🛠️ Quick Fix Scripts

### Windows PowerShell Script
```powershell
# Quick CFSS Windows Setup and Troubleshooting
# Save as: cfss_windows_fix.ps1

Write-Host "CFSS Windows Quick Fix Script" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green

# Check if CFSS is running
$cfssProcess = Get-Process -Name "CFSS*" -ErrorAction SilentlyContinue
if ($cfssProcess) {
    Write-Host "Stopping CFSS process..." -ForegroundColor Yellow
    Stop-Process -Name "CFSS*" -Force
    Start-Sleep -Seconds 2
}

# Clear temporary files
$tempPath = "$env:TEMP\CFSS*"
if (Test-Path $tempPath) {
    Write-Host "Clearing temporary files..." -ForegroundColor Yellow
    Remove-Item $tempPath -Recurse -Force -ErrorAction SilentlyContinue
}

# Reset user settings (if corrupted)
$userSettings = "$env:APPDATA\CFSS"
if (Test-Path $userSettings) {
    Write-Host "Backing up user settings..." -ForegroundColor Yellow
    Copy-Item $userSettings "$userSettings.backup" -Recurse -Force -ErrorAction SilentlyContinue
}

# Check for Windows updates
Write-Host "Checking Windows version..." -ForegroundColor Cyan
$osVersion = [System.Environment]::OSVersion.Version
Write-Host "Windows Version: $($osVersion.Major).$($osVersion.Minor)" -ForegroundColor Cyan

if ($osVersion.Major -lt 10) {
    Write-Host "WARNING: Windows 10 or higher recommended" -ForegroundColor Red
}

Write-Host "Quick fix completed!" -ForegroundColor Green
Write-Host "Try running CFSS again." -ForegroundColor Green
```

### macOS Shell Script
```bash
#!/bin/bash
# Quick CFSS macOS Setup and Troubleshooting
# Save as: cfss_macos_fix.sh
# Run with: bash cfss_macos_fix.sh

echo "🍎 CFSS macOS Quick Fix Script"
echo "=============================="

# Kill any running CFSS processes
echo "🔄 Stopping CFSS processes..."
pkill -f "CFSS" 2>/dev/null || true
sleep 2

# Clear quarantine attribute (common macOS issue)
echo "🔓 Clearing quarantine attributes..."
find /Applications -name "*CFSS*" -exec xattr -d com.apple.quarantine {} \; 2>/dev/null || true

# Check macOS version
echo "🔍 Checking macOS version..."
sw_vers -productName
sw_vers -productVersion

# Check if Gatekeeper is blocking the app
echo "🛡️  Checking Gatekeeper status..."
spctl --status

# Clear user caches
echo "🧹 Clearing user caches..."
rm -rf ~/Library/Caches/CFSS* 2>/dev/null || true
rm -rf ~/Library/Application\ Support/CFSS* 2>/dev/null || true

# Set execute permissions
echo "🔧 Setting execute permissions..."
find /Applications -name "*CFSS*" -type f -exec chmod +x {} \; 2>/dev/null || true

echo "✅ Quick fix completed!"
echo "💡 If the app still won't run, try:"
echo "   1. Right-click the app and select 'Open'"
echo "   2. Go to System Preferences > Security & Privacy > General"
echo "   3. Click 'Open Anyway' for CFSS"
```

---

## 🔧 Troubleshooting

### Common Issues

#### Windows
- **App won't start:** Run as administrator, check antivirus settings
- **Database errors:** Clear `%APPDATA%\CFSS` folder
- **CSV import fails:** Check file permissions and format
- **Auto-updater issues:** Ensure internet connection and firewall settings

#### macOS
- **"App can't be opened":** Allow in Security & Privacy settings
- **Quarantine issues:** Run `xattr -d com.apple.quarantine /path/to/CFSS.app`
- **Performance issues:** Close other applications, restart app
- **CSV sync problems:** Check OneDrive permissions and sync status

### Support Resources
- **GitHub Issues:** [Report bugs and request features](https://github.com/rc91470/cfss_releases/issues)
- **Documentation:** Check included README files in download
- **Logs:** Found in application data folder for debugging

---

## 🔄 Update Process

### Automatic Updates (Recommended)
1. Open CFSS application
2. Click "Check for Updates" in the File menu
3. Follow the prompts to download and install
4. Restart the application

### Manual Updates
1. Download the latest version from this page
2. Close the current CFSS application
3. Extract/install the new version
4. Run the new version (settings are preserved)

---

## 📊 Features Overview

### Core Functionality
- **Multi-circuit scanning** - Handle multiple fiber/copper circuits simultaneously
- **Barcode scanning** - Efficient serial number capture and validation
- **Progress tracking** - Real-time scan progress with visual feedback
- **Export capabilities** - Multiple output formats for reporting

### Advanced Features
- **SharePoint integration** - Seamless data sync and collaboration
- **Smart migration** - Preserve work when updating circuit data
- **Issue tracking** - Comprehensive problem resolution system
- **Auto-updater** - Always stay current with latest features

### Technical Features
- **Database-driven** - Reliable SQLite backend
- **Cross-platform** - Native Windows and macOS support
- **Customizable** - Flexible configuration options
- **Extensible** - Plugin architecture for custom features

---

## 📝 System Requirements

### Minimum Requirements
- **OS:** Windows 10 or macOS 10.14+
- **RAM:** 4GB (8GB recommended)
- **Storage:** 500MB free space
- **Network:** Internet connection for updates and SharePoint sync

### Recommended Requirements
- **OS:** Windows 11 or macOS 12+
- **RAM:** 8GB or higher
- **Storage:** 1GB free space
- **Network:** Stable broadband connection

---

## 🤝 Contributing

This is a release-only repository. For development, issues, and contributions, please visit the main development repository.

---

## 📜 License

This project is licensed under the MIT License. See the included LICENSE file for details.

---

## 🔗 Links

- **Latest Release:** [v4.2.2](https://github.com/rc91470/cfss_releases/releases/tag/v4.2.2)
- **All Releases:** [Release History](https://github.com/rc91470/cfss_releases/releases)
- **Issues:** [Report Problems](https://github.com/rc91470/cfss_releases/issues)

---

*Last updated: July 8, 2025*

# ![CFSS Logo](https://img.shields.io/badge/CFSS-v4.3.10-blue?style=for-the-badge&logo=desktop)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Professional fiber optic and copper circuit scanning application with auto-updater, SharePoint integration, and comprehensive reporting capabilities.**

---

## 🚀 Quick Download - Latest Release (v4.3.10)

### Windows v4.3.10 ✅ AVAILABLE
[![Download Windows](https://img.shields.io/badge/Download-Windows%20v4.3.10-0078d4?style=for-the-badge&logo=windows)](https://github.com/rc91470/cfss_releases/releases/download/v4.3.10/CFSS_v4.3.10_Windows.exe)
**File:** `CFSS_v4.3.10_Windows.exe` (~25MB)  
**Instructions:** Direct executable - no extraction required

### macOS v4.3.10 ✅ AVAILABLE
[![Download macOS](https://img.shields.io/badge/Download-macOS%20v4.3.10-000000?style=for-the-badge&logo=apple)](https://github.com/rc91470/cfss_releases/releases/download/v4.3.10/CFSS-macOS-4.3.10.tar.gz)

**File:** `CFSS-macOS-4.3.10.tar.gz� (~22MB)

---

## 🔄 Version Status

### Current Release: v4.3.10
✅ **Windows COMPLETE** - Available for download and auto-update  
✅ **macOS COMPLETE** - Available for download and auto-update

#### Features in v4.3.10:
- **XSR Circuit Support** - XSR circuits now follow CSW rules with Port 1 location columns
- **Enhanced Auto-updater** - Seamless updates with improved user experience
- **Version Synchronization** - Fixed duplicate update prompts
- **Streamlined Build Process** - Simplified development and release workflow

#### Bug Fixes:
- Fixed auto-updater download URL detection for .exe files
- Resolved "File is not a zip file" errors in update process
- Eliminated command prompt popups during updates
- Fixed version synchronization preventing duplicate update notifications
- Enhanced multi-jumper circuit handling for XSR circuits

---

## 📋 What's New in v4.3.10

### ✨ New Features
- **XSR Circuit Support** - XSR circuits follow CSW rules for Port 1 location display
- **Enhanced Auto-updater** - Direct .exe file handling with seamless user experience
- **Version Synchronization** - Eliminated duplicate update prompts
- **Streamlined Workflow** - Simplified build and release process

### 🔷 Bug Fixes
- Fixed auto-updater download URL detection using file extensions
- Resolved ZIP file handling errors in update process
- Eliminated command prompt visibility during updates
- Fixed version synchronization between app and updater
- Enhanced circuit scanning logic for XSR multi-jumper configurations

---

## 💵 Installation

### Windows (v4.3.10 - Available Now)
1. **Download** the .exe file using the link above
2. **Run** the executable directly - no extraction required
3. **Auto-updater** will handle future updates seamlessly

### macOS (Current: v4.3.10)
1. **Download** the TAR.GZ file from the link above
2. **Extract** the file (double-click or use `tar -xzf`)
3. **Move** `CFSS.app` to your Applications folder
4. **Run** the app

#### macOS "App is Damaged" Error?
If you get a security warning, **don't click "Move to Trash"**. Instead:

**Quick Fix:**
```bash
# Remove quarantine attributes
xattr -cr /Applications/CFSS.app

# Set proper permissions
chmod -R 755 /Applications/CFSS.app

# Launch the app
open /Applications/CFSS.app
```

---

## 🔄 Auto-Updates

CFSS includes an enhanced auto-updater that:
- Checks for new releases from this repository
- Downloads and installs updates seamlessly without user intervention
- Preserves user data and settings
- Works on both Windows and macOS
- Handles direct .exe file updates on Windows
- Provides clean update experience without command prompts

---

## 🔧 Troubleshooting

### Windows Issues

#### Auto-updater Problems
- **Issue**: Update fails with "File is not a zip file"
- **Fix**: This was resolved in v4.3.8+ with direct .exe file handling

#### Installation Issues
-=�**Issue**: Windows Defender blocks the executable
- **Fix**: Add exception for CFSS executable or temporarily disable real-time protection

### macOS Issues

#### "App is Damaged" Error
- =**Cause**: macOS Gatekeeper security feature
- **Solution**: Use the fix commands above or manually remove quarantine attributes
- =#### Permission Denied
- **Cause**: Incorrect file permissions after extraction
- **Solution**: Run `chmod -R 755 /Applications/CFSS.app`

### General Issues

#### Circuit Not Loading
- **Check**: CSV file format matches expected columns
- **Check**: File path doesn't contain special characters
- **Check**: CSV file is not locked by another application

#### Scanning Problems
- **Check**: Scanner is properly connected and powered
- **Check**: Scanner drivers are installed
- **Try**: Restart the application

---

## 📗 Support

### Issues and Bug Reports
- **Development issues**: [cfss repository](https://github.com/rc91470/cfss/issues)
- **Release issues**: [cfss_releases repository](https://github.com/rc91470/cfss_releases/issues)

### Quick Help
- **Windows**: Download and run the .exe file directly
- **macOS**: Extract, move to Applications, run fix script if needed
- **Updates**: App will check automatically and update seamlessly

---

## 📗 Support

### Issues and Bug Reports
- **Development issues**: [cfss repository](https://github.com/rc91470/cfss/issues)
- **Release issues**: [cfss_releases repository](https://github.com/rc91470/cfss_releases/issues)

---

## 📀 License

MIT License - See the development repository for full license details.

---

**Latest Stable:** [v4.3.10](https://github.com/rc91470/cfss_releases/releases/latest) | **Development:** [cfss](https://github.com/rc91470/cfss) | **Issues:** [Report Bug](https://github.com/rc91470/cfss_releases/issues)
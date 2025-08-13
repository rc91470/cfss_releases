# ![CFSS Logo](https://img.shields.io/badge/CFSS-v4.4.1-blue?style=for-the-badge&logo=desktop)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Professional fiber optic and copper circuit scanning application with auto-updater, SharePoint integration, and comprehensive reporting capabilities.**

---

## 🚀 Quick Download - Latest Release (v4.4.1)

### macOS v4.2.4 ✅ AVAILABLE
[![Download macOS](https://img.shields.io/badge/Download-macOS%20v4.2.4-000000?style=for-the-badge&logo=apple)](https://github.com/rc91470/cfss_releases/releases/download/v4.2.4/CFSS-macOS-4.2.4.tar.gz)

**File:** `CFSS-macOS-4.2.4.tar.gz` (~22MB)  
**SHA256:** [Checksum](https://github.com/rc91470/cfss_releases/releases/download/v4.2.4/CFSS-macOS-4.2.4.tar.gz.sha256)  
**Alternative:** [Browse all releases](https://github.com/rc91470/cfss_releases/releases/tag/v4.2.4)

### Windows v4.4.1 ✅ AVAILABLE
[![Download Windows](https://img.shields.io/badge/Download-Windows%20v4.4.1-0078d4?style=for-the-badge&logo=windows)](https://github.com/rc91470/cfss_releases/raw/main/v4.4.1/CFSS_v4.4.1_Windows_2025-08-13_14-15-44.zip)

**File:** `CFSS_v4.4.1_Windows_2025-08-13_14-15-44.zip` (~40MB)  
**Executable:** `CFSS_v4.4.1_Windows.exe`  
**Direct Download:** [CFSS_v4.4.1_Windows.exe](https://github.com/rc91470/cfss_releases/raw/main/v4.4.1/CFSS_v4.4.1_Windows.exe)

---

## 🔄 Version Status

### Current Release: v4.4.1
✅ **Windows COMPLETE** - Available for download and auto-update  
✅ **macOS STABLE** - v4.2.4 Available for download and auto-update

#### Features in v4.4.1:
- **CRITICAL FIX** - Serial number synchronization between save and display functions
- **Enhanced Auto-Updater** - Component validation and restoration
- **Sounds Folder Validation** - Fixes Windows popup issues with proper audio feedback
- **ZIP File Handling** - Proper update file management and extraction
- **Missing Component Detection** - Automatically restores critical folders and files
- **Cross-platform Compatibility** - Both Windows and macOS support

#### Bug Fixes:
- **FIXED:** Serial number mismatch in save functions causing data inconsistencies
- Fixed Windows popup errors when sounds folder missing
- Enhanced auto-updater now validates and restores missing components
- Improved ZIP file extraction and nested directory handling
- Better error handling and user feedback during updates
- Proper version display in application interface

> **Both platforms built from identical source code for complete feature parity and version synchronization.**

---

## 📋 What's New in v4.4.0

### 🔧 Enhanced Auto-Updater
- **Component Validation**: Automatically checks for missing critical folders and files
- **Sounds Folder Detection**: Ensures audio feedback files are present (no more Windows popups!)
- **ZIP File Support**: Proper handling of compressed update packages
- **Missing Component Restoration**: Automatically restores critical folders from update archives
- **Nested Directory Handling**: Correctly extracts updates regardless of archive structure

### 🎵 Audio Feedback System
- **match.mp3**: Green ring feedback for successful matches
- **nonmatch.mp3**: Red ring feedback for failed matches  
- **complete.mp3**: Completion sound for finished scans
- **Windows Popup Fix**: No more system error dialogs when audio files missing

### 🛠️ Technical Improvements
- **Enhanced Error Handling**: Better user feedback during update process
- **Version Synchronization**: Proper version display in application interface
- **Cross-Platform Updates**: Unified update system for Windows and macOS
- **Backup and Restore**: Automatic backup of critical components before updates

### ✨ New Features
- **High-DPI dialog support** - Fixed, resizable dialogs for all screens
- **Authoritative version** - Both platforms built from identical source
- **Auto-updater reliability** - Robust versioning and update process
- **All previous DPI scaling removed**

### 🔧 Bug Fixes
- Fixed all dialog sizing and scaling issues
- Improved button layout and dialog usability
- Enhanced error handling and user feedback
- Fixed auto-updater repository references

---

## 📱 Installation

### Windows (v4.2.4 - Available Now)
1. **Download** the ZIP file using the link above
2. **Extract** to your desired location  
3. **Run** `CFSS_v4.2.4.exe` from the extracted folder

### macOS (Current: v4.2.4)
1. **Download** the TAR.GZ file from the link above
2. **Extract** the file (double-click or use `tar -xzf`)
3. **Move** `CFSS.app` to your Applications folder
4. **Run** the app

#### macOS "App is Damaged" Error?
If you get a security warning, **don't click "Move to Trash"**. Instead:

**Option 1: Quick Fix (Download Script)**
```bash
# Download and run the fix script
curl -L https://github.com/rc91470/cfss_releases/raw/main/releases/macos_fix.sh -o macos_fix.sh
chmod +x macos_fix.sh
./macos_fix.sh
```

**Option 2: Manual Fix**
```bash
# Remove quarantine attributes
xattr -cr /Applications/CFSS.app

# Set proper permissions
chmod -R 755 /Applications/CFSS.app

# Launch the app
open /Applications/CFSS.app
```

**Option 3: Download Fix Script**
[![Download Fix Script](https://img.shields.io/badge/Download-macOS%20Fix-FF6B35?style=for-the-badge&logo=apple)](https://github.com/rc91470/cfss_releases/raw/main/releases/macos_fix.sh)

---

## 🏗️ Repository Structure

This is a **distribution-only** repository. For development, see [cfss](https://github.com/rc91470/cfss).

### 📁 Directory Layout
```
cfss_releases/
├── README.md                    # This file
├── CHANGELOG.md                 # Version history
├── documentation/               # User guides and help
│   ├── installation/
│   ├── troubleshooting/
│   └── user_guide/
├── releases/                    # Platform-specific releases
│   ├── windows/
│   │   ├── latest/              # Latest Windows build (v4.2.4)
│   │   ├── v4.2.2/              # Previous Windows build
│   │   └── v4.2.3/              # ✅ RELEASED
│   └── macos/
│       ├── latest/              # Latest macOS build (v4.2.4)
│       ├── v4.2.2/              # Previous macOS build
│       └── v4.2.3/              # ✅ RELEASED
├── scripts/                     # Build and release automation
└── v4.2.3/                     # Version 4.2.3 source & builds
    ├── src/                     # Source code for v4.2.3
    ├── build/                   # macOS build artifacts
    ├── build_macos.sh           # macOS build script (completed)
    └── build_windows.bat        # Windows build script (needs execution)
```

### �� Platform Separation
- **Windows builds**: `releases/windows/`
- **macOS builds**: `releases/macos/`
- **Shared scripts**: `scripts/`
- **Documentation**: `documentation/`

Each platform maintainer should only modify their respective platform directories to avoid conflicts.

---

## 📖 Documentation

- **[Installation Guide](documentation/installation/)** - Detailed installation instructions
- **[User Guide](documentation/user_guide/)** - How to use CFSS
- **[Troubleshooting](documentation/troubleshooting/)** - Common issues and solutions
- **[Changelog](CHANGELOG.md)** - Version history and release notes

---

## 🔄 Auto-Updates

CFSS includes an auto-updater that:
- Checks for new releases from this repository
- Downloads and installs updates automatically
- Preserves user data and settings
- Works on both Windows and macOS

---

## 🤝 For Developers

### Building v4.2.4
**macOS**: ✅ Complete - Available for download  
**Windows**: ✅ Complete - Available for download

Both platforms are now built and available from the same v4.2.4 source code.

### Version Synchronization Rules
- ✅ **DO**: Build from the same source code version
- ✅ **DO**: Keep both platforms in sync
- ✅ **DO**: Test both platforms before release
- ❌ **DON'T**: Release with mismatched versions
- ❌ **DON'T**: Update version numbers until both platforms are ready

### Repository Rules
- ✅ **DO**: Modify only your platform's directories
- ✅ **DO**: Use the provided source code in version directories
- ✅ **DO**: Update documentation when adding features
- ❌ **DON'T**: Modify other platform's build files
- ❌ **DON'T**: Commit source code changes (use cfss repository)
- ❌ **DON'T**: Include customer data in builds

---

## 📈 Version History

| Version | Date | Windows | macOS | Notes |
|---------|------|---------|-------|-------|
| v4.2.4  | 2025-07-09 | ✅ Available | ✅ Available | High-DPI fixes, unified codebase |
| v4.2.3  | 2025-07-05 | ✅ | ✅ | SharePoint integration |
| v4.2.1  | 2025-06-28 | ✅ | ❌ | Issue tracking |
| v4.2.0  | 2025-06-15 | ✅ | ✅ | Major release |

---

## 🛠️ Support

### Issues and Bug Reports
- **Development issues**: [cfss repository](https://github.com/rc91470/cfss/issues)
- **Release issues**: [cfss_releases repository](https://github.com/rc91470/cfss_releases/issues)

### Quick Help
- **Windows**: Extract and run the .exe file
- **macOS**: Extract, move to Applications, run fix script if needed
- **Updates**: App will check automatically, or download manually

---

## 📄 License

MIT License - See the development repository for full license details.

---

**Latest Stable:** [v4.2.2](https://github.com/rc91470/cfss_releases/releases/latest) | **Development:** [cfss](https://github.com/rc91470/cfss) | **Issues:** [Report Bug](https://github.com/rc91470/cfss_releases/issues)

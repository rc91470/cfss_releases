# CFSS - Copper/Fiber Serial Scanner

![CFSS Logo](https://img.shields.io/badge/CFSS-v4.2.2-blue?style=for-the-badge&logo=desktop)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Professional fiber optic and copper circuit scanning application with auto-updater, SharePoint integration, and comprehensive reporting capabilities.**

---

## �� Quick Download - Latest Stable Release (v4.2.2)

### Windows
[![Download Windows](https://img.shields.io/badge/Download-Windows-0078D4?style=for-the-badge&logo=windows)](https://github.com/rc91470/cfss_releases/releases/download/v4.2.2/CFSS_v4.2.2_Windows.zip)

**File:** `CFSS_v4.2.2_Windows.zip` (~25MB)

### macOS
[![Download macOS](https://img.shields.io/badge/Download-macOS-000000?style=for-the-badge&logo=apple)](https://github.com/rc91470/cfss_releases/releases/download/v4.2.2/CFSS-macOS-4.2.2.tar.gz)

**File:** `CFSS-macOS-4.2.2.tar.gz` (~22MB)

---

## 🔄 Version 4.2.3 Status

### macOS v4.2.3
✅ **READY** - Built and available in `releases/macos/v4.2.3/`
- **File:** `CFSS-macOS-4.2.3.tar.gz`
- **Features:** Enhanced DPI scaling, auto-updater fixes, dialog improvements

### Windows v4.2.3
❌ **NEEDS BUILD** - Windows maintainer needs to build from v4.2.3 source
- **Source:** Available in `v4.2.3/src/`
- **Build Script:** `v4.2.3/build_windows.bat`
- **Target:** `CFSS_v4.2.3_Windows.zip`

> **Note:** v4.2.3 will not be released until both platforms are ready to ensure version synchronization.

---

## 📋 What's New in v4.2.3

### ✨ New Features
- **Enhanced DPI scaling** - Perfect display on high-resolution screens
- **Auto-updater fixes** - Now correctly points to cfss_releases repository
- **Smart dialog layouts** - Responsive UI that adapts to screen size
- **Enhanced SharePoint integration** - Improved CSV sync and data export
- **Issue tracking system** - Comprehensive problem tracking and resolution notes
- **Smart progress migration** - Preserves scan progress when updating circuit data

### 🔧 Bug Fixes
- Fixed font scaling issues on high-DPI displays
- Improved button layout and dialog sizing
- Enhanced error handling and user feedback
- Fixed auto-updater repository references

---

## 📱 Installation

### Windows (Current: v4.2.2)
1. **Download** the ZIP file from the link above
2. **Extract** to your desired location
3. **Run** `CFSS_v4.2.2.exe`

### macOS (Current: v4.2.2)
1. **Download** the TAR.GZ file from the link above
2. **Extract** the file (double-click or use `tar -xzf`)
3. **Move** `CFSS.app` to your Applications folder
4. **Run** the app

#### macOS "App is Damaged" Error?
If you get a security warning, **don't click "Move to Trash"**. Instead:

**Option 1: Quick Fix (Copy & Paste)**
```bash
# Download and run the fix script
curl -L https://github.com/rc91470/cfss_releases/releases/download/v4.2.2/macos_fix.sh -o macos_fix.sh
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
[![Download Fix Script](https://img.shields.io/badge/Download-macOS%20Fix-FF6B35?style=for-the-badge&logo=apple)](https://github.com/rc91470/cfss_releases/releases/download/v4.2.2/macos_fix.sh)

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
│   │   ├── latest/              # Latest Windows build (v4.2.2)
│   │   ├── v4.2.2/              # Stable Windows build
│   │   └── v4.2.3/              # ❌ NEEDS BUILD
│   └── macos/
│       ├── latest/              # Latest macOS build (v4.2.2)
│       ├── v4.2.2/              # Stable macOS build
│       └── v4.2.3/              # ✅ READY
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

### Building v4.2.3
**macOS**: ✅ Complete
**Windows**: ❌ Needs Windows maintainer to:
1. Navigate to `v4.2.3/`
2. Run `build_windows.bat`
3. Copy results to `releases/windows/v4.2.3/`
4. Update `releases/windows/latest/`

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
| v4.2.3  | TBD | ❌ Needs Build | ✅ Ready | DPI scaling, auto-updater fixes |
| v4.2.2  | 2025-07-05 | ✅ | ✅ | SharePoint integration |
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

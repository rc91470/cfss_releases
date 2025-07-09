# CFSS Development Guide

## 🚨 CRITICAL: Customer Data Protection

**NEVER commit customer data to this repository!**

The build process automatically protects against this, but developers must be aware:

### What is Customer Data?
- **CSV files** containing real circuit information
- **Database files** with scan progress
- **Log files** that might contain serial numbers
- **Export files** with scan results
- **Configuration files** with SharePoint paths

### Protection Measures
1. **Automatic Build Protection**: Build scripts clean data folder
2. **Git Protection**: Comprehensive `.gitignore` 
3. **Security Checks**: Run `./security_check.sh` before building
4. **Documentation**: See `SECURITY_MEASURES.md` for complete details

## 🏗️ Architecture Overview

### Core Components
- **`cfss_app.py`**: Main application and UI
- **`data_manager.py`**: Database operations and data handling
- **`circuit_manager.py`**: Circuit loading and management
- **`scan_controller.py`**: Scan state and progress tracking
- **`auto_updater.py`**: Automatic update system

### Key Features (v4.2.3)
- **DPI Scaling**: All UI elements scale for high-resolution displays
- **Issue Tracking**: Comprehensive problem/resolution tracking
- **Auto-Updates**: Seamless update system
- **SharePoint Integration**: Direct sync and export
- **Smart Migration**: Preserves progress during CSV updates

## 🔧 Development Environment

### Setup
```bash
# Clone repository
git clone https://github.com/rc91470/cfss_app.git
cd cfss_app

# Windows setup
setup_dev_windows.bat

# macOS setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Daily Development
```bash
# Windows
start_dev.bat

# macOS
source .venv/bin/activate
python cfss_app.py
```

## 🔒 Security Workflow

### Before Any Build
1. **Run security check**: `./security_check.sh`
2. **Review warnings**: Address any customer data found
3. **Use build scripts**: They automatically clean data

### Before Any Commit
1. **Check git status**: `git status`
2. **Review .gitignore**: Ensure it covers all customer data
3. **Run security check**: `./security_check.sh`
4. **Never force-add** ignored files

## 📊 Database Schema

### Core Tables
- **`circuits`**: Circuit metadata and hash tracking
- **`scan_progress`**: Scan state and progress per jumper
- **`issue_tracking`**: Problem tracking and resolution notes

### Issue Tracking Fields
- **Problem identification**: Circuit, location, expected serial
- **Resolution tracking**: What was wrong, how it was fixed
- **Analytics**: Resolution rates, recurring issues

## 🎨 UI Design Guidelines

### DPI Scaling
- **Use `get_scaled_size()`** for all dimensions
- **Use scaled fonts**: `DIALOG_FONT_*` constants
- **Test on high-DPI displays**: 3840x2400+ screens

### Dialog Design
- **Minimum sizes**: Use `minsize()` for all dialogs
- **Responsive buttons**: Stack vertically on smaller screens
- **Proper centering**: Center dialogs on screen
- **Focus management**: Use `transient()` and `grab_set()`

## 🔄 Auto-Updater System

### How It Works
1. **Startup check**: Compares local version to GitHub releases
2. **Background download**: Downloads new version if available
3. **Verification**: Checks download integrity
4. **Installation**: Replaces current version
5. **Restart**: Launches new version

### Development Notes
- **Version format**: Use semantic versioning (v4.2.3)
- **GitHub integration**: Reads from cfss_releases repository
- **Cross-platform**: Works on Windows and macOS
- **Rollback protection**: Keeps previous version until verified

## 🔄 CSV Migration System

### Smart Migration
- **Preserves progress**: Matches existing scan data to new CSV data
- **Backup creation**: Creates backups of existing progress
- **Progress reporting**: Shows what was preserved vs. lost
- **User control**: Allows users to choose migration strategy

### Implementation
- **Hash-based detection**: Detects CSV changes efficiently
- **Location matching**: Matches scan progress by location identifiers
- **Incremental updates**: Only processes changed data

## 🔗 SharePoint Integration

### CSV Sync
- **Folder remembering**: Saves SharePoint folder for future use
- **Change detection**: Only syncs updated files
- **Smart migration**: Preserves progress during sync

### Data Export
- **Direct export**: Exports scan data directly to SharePoint
- **Multiple formats**: JSON data + text summary
- **Device tracking**: Includes device and user information

## 🧪 Testing Guidelines

### Before Release
1. **Test on both platforms**: Windows and macOS
2. **Test high-DPI displays**: 3840x2400+ screens
3. **Test with customer data**: Verify security measures work
4. **Test auto-updater**: Verify update process works
5. **Test SharePoint integration**: Verify sync and export

### Security Testing
1. **Build with customer data**: Verify it's excluded
2. **Check build contents**: Ensure no sensitive data
3. **Test git operations**: Verify .gitignore works
4. **Run security checks**: Use `./security_check.sh`

## 📦 Build Process

### ⚠️ **CRITICAL: Repository Separation**

**This repository (cfss) is for DEVELOPMENT ONLY:**
- ✅ Source code, development tools, documentation
- ❌ NO .exe, .app, .dmg, or other build artifacts
- ❌ NO distribution builds or releases

**The cfss_releases repository is for DISTRIBUTION:**
- ✅ Compiled builds (.exe, .app files)
- ✅ Public releases and user documentation
- ✅ Official build scripts for distribution

### Development Testing (Local Only)
```bash
# For local development testing only
./build_macos.sh     # Creates .app in dist/ for testing
build_windows.bat    # Creates .exe in dist/ for testing
```

**⚠️ These create files in dist/ for local testing - NEVER commit these files!**

### Official Builds and Releases
**Use the cfss_releases repository:**
1. **Clone cfss_releases**: `git clone https://github.com/rc91470/cfss_releases.git`
2. **Copy latest source**: Copy source files from this repo to cfss_releases
3. **Build there**: Use the build scripts in cfss_releases
4. **Release there**: Create GitHub releases in cfss_releases

### Build Process Flow (Development Testing)
1. **Security check**: Scans for customer data
2. **Data backup**: Backs up existing customer data
3. **Data cleaning**: Removes all CSVs from data folder
4. **Build**: Creates executable with empty data structure
5. **Local testing**: Test the build locally (DO NOT DISTRIBUTE)

### Build Process Flow (Official Release)
1. **Use cfss_releases repository**: Never build for distribution in this repo
2. **Copy source code**: From this repo to cfss_releases
3. **Build and release**: In cfss_releases repository only

## 🚀 Release Process

### Steps
1. **Update version**: In `cfss_app.py` (APP_VERSION and VERSION)
2. **Build locally**: Use platform-specific build script
3. **Test thoroughly**: All features and security measures
4. **Run release automation**: Copy files to cfss_releases repository
5. **Create GitHub release**: In the public repository

### Release Notes
- **Update public README**: In cfss_releases repository
- **Update CHANGELOG**: Document new features and fixes
- **Include troubleshooting**: Update troubleshooting guides

## 📝 Code Style Guidelines

### Python Style
- **PEP 8 compliance**: Use standard Python style
- **Meaningful names**: Clear variable and function names
- **Error handling**: Comprehensive try/catch blocks
- **Logging**: Use logging module for debugging

### UI Code
- **Consistent scaling**: Use scaling functions throughout
- **Responsive design**: Handle different screen sizes
- **Accessible colors**: High contrast, readable text
- **Keyboard navigation**: Support keyboard shortcuts

## 🔍 Debugging Tips

### Common Issues
- **Audio problems**: Check pygame initialization
- **CSV loading issues**: Check file format and encoding
- **Database errors**: Check SQLite file permissions
- **UI scaling issues**: Test on different DPI settings

### Debug Tools
- **Logging**: Check `cfss_app.log` for errors
- **Database inspection**: Use SQLite browser for database issues
- **Security check**: Run `./security_check.sh` for data issues
- **Build verification**: Check build contents manually

## 📞 Support

### For Development Issues
- **Check logs**: `cfss_app.log` for runtime errors
- **Review documentation**: This guide and `SECURITY_MEASURES.md`
- **Test security**: Use `./security_check.sh`

### For Release Issues
- **Check build process**: Verify all steps completed
- **Test on target platform**: Ensure compatibility
- **Verify security**: Confirm no customer data in build

---

**Remember**: Customer data protection is paramount. When in doubt, check the security measures and never commit sensitive data.

# CFSS Installation Guide

This guide will help you install and set up CFSS (Copper/Fiber Serial Scanner) on your computer.4. **Configure** your cable scanning parameters
5. **Start** your first network cable scan!
## System Requirements

### Windows
- **Operating System**: Windows 10 or later (64-bit)
- **Memory**: 4 GB RAM minimum, 8 GB recommended
- **Storage**: 500 MB available disk space
- **Additional**: .NET Framework 4.7.2 or later

### macOS
- **Operating System**: macOS 10.15 (Catalina) or later
- **Memory**: 4 GB RAM minimum, 8 GB recommended
- **Storage**: 500 MB available disk space
- **Processor**: Intel or Apple Silicon

## Installation Methods

### Windows Installation

#### Method 1: Windows Installer (Recommended)
1. **Download** the Windows Installer from the [releases page](https://github.com/rc91470/cfss_releases/releases/latest)
2. **Run** the installer as Administrator
3. **Follow** the installation wizard steps
4. **Launch** CFSS from the Start Menu or desktop shortcut

#### Method 2: Portable Version
1. **Download** the Windows Portable ZIP from the [releases page](https://github.com/rc91470/cfss_releases/releases/latest)
2. **Extract** the ZIP file to your desired location
3. **Run** `cfss_app.exe` from the extracted folder
4. **Optional**: Create a desktop shortcut for easy access

### macOS Installation

#### Method 1: macOS App (Recommended)
1. **Download** the macOS DMG from the [releases page](https://github.com/rc91470/cfss_releases/releases/latest)
2. **Open** the DMG file
3. **Drag** CFSS.app to your Applications folder
4. **Launch** CFSS from Launchpad or Applications folder

> **Note**: You may need to allow the app in System Preferences > Security & Privacy if you see a warning about an unidentified developer.

#### Method 2: Portable Version
1. **Download** the macOS ZIP from the [releases page](https://github.com/rc91470/cfss_releases/releases/latest)
2. **Extract** the ZIP file to your desired location
3. **Run** the CFSS application from the extracted folder

## Initial Setup

### First Launch
1. **Start** CFSS application
2. **Configure** your data directory (default: `Documents/CFSS_Data`)
3. **Set up** SharePoint integration (if required)
4. **Configure** scanning parameters for your network cables

### SharePoint Configuration (Optional)
If you need SharePoint integration:
1. **Go to** Settings > SharePoint Configuration
2. **Enter** your SharePoint URL and credentials
3. **Test** the connection
4. **Save** the configuration

### Database Setup
CFSS will automatically create its database on first run:
- **Location**: `%APPDATA%/CFSS/cfss_app.db` (Windows) or `~/Library/Application Support/CFSS/cfss_app.db` (macOS)
- **Backup**: Automatic backups are created in the `scan_backups` folder

## Verification

To verify your installation:
1. **Launch** CFSS
2. **Check** that the interface loads without errors
3. **Test** basic functionality by creating a test scan of a network cable
4. **Verify** that data is being saved correctly

## Troubleshooting

### Common Issues

#### Windows
- **"Application failed to start"**: Install/update .NET Framework
- **"Permission denied"**: Run as Administrator
- **"Database error"**: Check write permissions to Documents folder

#### macOS
- **"App can't be opened"**: Allow in System Preferences > Security & Privacy
- **"Damaged app"**: Re-download from official source
- **"Permission denied"**: Check file permissions

### Getting Help
If you encounter issues:
1. **Check** the [Troubleshooting Guide](troubleshooting.md)
2. **Review** the [User Guide](user_guide.md)
3. **Search** existing [GitHub Issues](https://github.com/rc91470/cfss_releases/issues)
4. **Create** a new issue with detailed information

## Updating

### Automatic Updates
CFSS will check for updates automatically and notify you when a new version is available.

### Manual Updates
1. **Download** the latest version from the [releases page](https://github.com/rc91470/cfss_releases/releases/latest)
2. **Close** CFSS completely
3. **Install** the new version (will upgrade existing installation)
4. **Launch** CFSS to verify the update

## Uninstallation

### Windows
- **Installer version**: Use "Add or Remove Programs" in Windows Settings
- **Portable version**: Simply delete the application folder

### macOS
- **App version**: Move CFSS.app to Trash
- **Portable version**: Delete the application folder

> **Note**: User data and settings are stored separately and will not be removed during uninstallation.

## Next Steps

After installation:
1. **Read** the [User Guide](user_guide.md) for detailed usage instructions
2. **Review** the [Quick Reference](quick_reference.md) for common tasks
3. **Configure** your scanning parameters
4. **Start** your first circuit scan!

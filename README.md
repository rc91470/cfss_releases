# CFSS Circuit Scanner v4.3.10 (Windows) | v4.2.3 (macOS)

Professional fiber optic and copper circuit scanning application with auto-updater.

## Quick Download - Latest Release

### Windows v4.3.10
[Download Windows](https://github.com/rc91470/cfss_releases/releases/download/v4.3.10/CFSS_v4.3.10.exe)

File: `CFSS_v4.3.10.exe` (~38MB)
Instructions: Direct executable - no extraction required

### macOS v4.2.3
[Download macOS](https://github.com/rc91470/cfss_releases/releases/download/v4.2.3/CFSS-macOS-4.2.3.tar.gz)

File: `CFSS-macOS-4.2.3.tar.gz` (21MB)

**Note:** macOS v4.3.10 build is in progress. Current stable version is v4.2.3.

## Features in Windows v4.3.10
- XSR Circuit Support - XSR circuits now follow CSW rules with Port 1 location columns
- Enhanced Auto-updater - Seamless updates with improved user experience
- Version Synchronization - Fixed duplicate update prompts
- Streamlined Build Process - Simplified development and release workflow

## macOS v4.2.3 Features
- Enhanced DPI scaling for high-resolution displays
- Auto-updater fixes with proper repository references
- Smart dialog layouts with responsive UI
- Enhanced SharePoint integration
- Issue tracking system with comprehensive problem tracking

## Installation

### Windows (v4.3.10)
1. Download the .exe file from the link above
2. Run the executable directly - no extraction required
3. Auto-updater will handle future updates seamlessly

### macOS (v4.2.3)
1. Download the TAR.GZ file from the link above
2. Extract the file (double-click or use `tar -xzf`)
3. Move CCFSS.app` to your Applications folder
4. Run the app

If you get a security warning, run:
```bash
xattr -cr /Applications/CFSS.app
chmod -R 755 /Applications/CFSS.app
open /Applications/CFSS.app
```

## Troubleshooting

### Windows Issues
- If Windows Defender blocks the executable, add an exception
- Auto-update failures: Resolved in v4.3.8+ with direct .exe handling

### macOS Issues
- "App is Damaged" error: Use the fix commands above
- Permission denied: Run `chmod -R 755 /Applications/CFSS.app`

## Support

- Development issues: [cfss repository](https://github.com/rc91470/cfss/issues)
- Release issues: [cfss_releases repository](https://github.com/rc91470/cfss_releases/issues)

---

Latest Stable: [Windows v4.3.10](https://github.com/rc91470/cfss_releases/releases/latest) | [macOS v4.2.3](https://github.com/rc91470/cfss_releases/releases/tag/v4.2.3) | Development: [cfss](https://github.com/rc91470/cfss)

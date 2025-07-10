# CFSS v4.2.4 Release

**Release Date:** July 9, 2025  
**Version:** v4.2.4  
**Platform:** Windows  

## What's New in v4.2.4

### High-DPI Display Support
- **Smart DPI Detection**: Automatically detects screen resolution and DPI settings
- **Proper Dialog Sizing**: All dialogs now scale appropriately for high-resolution displays (3840x2400, 192 DPI, etc.)
- **Readable Fonts**: Font sizes automatically scale based on display DPI
- **Cross-Platform Compatibility**: Enhanced scaling works on both Windows and macOS

### Features
- All previous v4.2.3 features including auto-updater
- Enhanced SharePoint integration with smart CSV syncing
- Comprehensive issue tracking and resolution notes
- Smart progress migration when updating CSV files
- Improved scan workflow with better error handling

### Installation
1. Download `CFSS_v4.2.4_Windows_2025-07-09_21-18-59.zip`
2. Extract to your desired location
3. Run `CFSS_v4.2.4.exe`

### Requirements
- Windows 10 or later
- No additional dependencies required

### High-DPI Laptop Testing
This version has been specifically tested and optimized for high-resolution laptops:
- ✅ 3840x2400 displays at 192 DPI
- ✅ All dialogs properly sized and readable
- ✅ All buttons visible without scrolling
- ✅ Text large enough to read but not oversized
- ✅ Main UI appropriately scaled

### File Contents
- `CFSS_v4.2.4.exe` - Main application executable
- `data/` - Sample circuit data and documentation
- `sounds/` - Audio feedback files

### Notes
- This is the authoritative cross-platform version with high-DPI dialog fixes
- Built from Mac brother's latest code with proper DPI scaling
- Compatible with existing scan data and progress files

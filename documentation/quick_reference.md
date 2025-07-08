# CFSS Quick Reference

Quick reference guide for common tasks in CFSS (Copper/Fiber Serial Scanner).

## Quick Start

### Basic Scan Process
1. **Connect** cable to scanner
2. **Select** cable type
3. **Click** "Start Scan"
4. **Wait** for completion
5. **Save** results

### Essential Settings
- **Cable Type**: Auto-detect or manual selection
- **Scan Resolution**: Standard (fast) or High (detailed)
- **Test Voltage**: 5V (standard) or 12V (high power)
- **Auto-save**: Enabled by default

## Common Tasks

### Starting a New Scan
- **Shortcut**: Ctrl+N
- **Menu**: File > New Scan
- **Button**: "New Scan" in toolbar

### Saving Results
- **Auto-save**: Enabled by default
- **Manual save**: Ctrl+S
- **Save As**: Ctrl+Shift+S
- **Location**: Documents/CFSS_Data/

### Exporting Data
- **CSV**: File > Export > CSV
- **PDF**: File > Export > PDF Report
- **Excel**: File > Export > Excel Format
- **Images**: File > Export > Save Images

### Viewing Previous Scans
- **Open**: Ctrl+O
- **Recent**: File > Recent Scans
- **Browse**: File > Open > Browse
- **Search**: Edit > Find Scans

## Cable Types Quick Reference

### Copper Cables
| Type | Pairs | Common Uses |
|------|-------|-------------|
| Cat5 | 4 | Basic Ethernet |
| Cat5e | 4 | Gigabit Ethernet |
| Cat6 | 4 | Gigabit+, PoE |
| Cat6a | 4 | 10 Gigabit |
| Cat7 | 4 | High-speed data |
| Cat8 | 4 | Data center |

### Fiber Optic Cables
| Type | Mode | Wavelength | Distance |
|------|------|------------|----------|
| OM1 | Multi-mode | 850nm | 300m |
| OM2 | Multi-mode | 850nm | 600m |
| OM3 | Multi-mode | 850nm | 1000m |
| OM4 | Multi-mode | 850nm | 1100m |
| OS1 | Single-mode | 1310/1550nm | 40km+ |
| OS2 | Single-mode | 1310/1550nm | 80km+ |

## Scan Parameters

### Copper Cable Settings
- **Test Voltage**: 5V (standard), 12V (high power)
- **Frequency**: 1MHz (standard), 10MHz (high-res)
- **Length Range**: 1m - 500m
- **Resolution**: 0.1m (standard), 0.01m (high-res)

### Fiber Optic Settings
- **Wavelength**: 850nm, 1310nm, 1550nm
- **Pulse Width**: 10ns (standard), 1ns (high-res)
- **Range**: 1m - 200km
- **Resolution**: 1m (standard), 0.1m (high-res)

## Error Codes

### Common Copper Errors
- **C001**: Open circuit (wire break)
- **C002**: Short circuit (wires touching)
- **C003**: Crossed wires (incorrect pairing)
- **C004**: High resistance (poor connection)
- **C005**: Impedance mismatch

### Common Fiber Errors
- **F001**: High loss (dirty connector)
- **F002**: No signal (fiber break)
- **F003**: High reflectance (bad splice)
- **F004**: Multiple reflections
- **F005**: Wavelength mismatch

## Keyboard Shortcuts

### File Operations
- **Ctrl+N**: New scan
- **Ctrl+O**: Open file
- **Ctrl+S**: Save
- **Ctrl+P**: Print
- **Ctrl+E**: Export

### Scan Operations
- **F5**: Start scan
- **Esc**: Stop scan
- **Ctrl+R**: Repeat last scan
- **Ctrl+T**: Test connection

### View Operations
- **Ctrl++**: Zoom in
- **Ctrl+-**: Zoom out
- **Ctrl+0**: Reset zoom
- **Ctrl+F**: Find/Search

## Status Indicators

### Scan Status
- **🟢 Ready**: Scanner connected and ready
- **🟡 Scanning**: Scan in progress
- **🔴 Error**: Hardware or connection issue
- **⚪ Offline**: Scanner not connected

### Result Quality
- **✅ Pass**: Cable meets specifications
- **⚠️ Warning**: Minor issues detected
- **❌ Fail**: Cable does not meet specs
- **❓ Unknown**: Unable to determine status

## Common Issues & Quick Fixes

### Hardware Issues
- **Scanner not detected**: Check USB connection
- **Scan fails**: Verify cable connections
- **Slow performance**: Close other applications
- **No results**: Check cable type selection

### Software Issues
- **App won't start**: Run as administrator
- **Database error**: Check disk space
- **Export fails**: Verify file permissions
- **Slow loading**: Clear cache files

## File Locations

### Default Directories
- **Scan Data**: `Documents/CFSS_Data/`
- **Backups**: `Documents/CFSS_Data/Backups/`
- **Exports**: `Documents/CFSS_Data/Exports/`
- **Templates**: `Documents/CFSS_Data/Templates/`

### Configuration Files
- **Settings**: `%APPDATA%/CFSS/settings.json`
- **Database**: `%APPDATA%/CFSS/cfss_app.db`
- **Logs**: `%APPDATA%/CFSS/cfss_app.log`

## Support Contacts

### Quick Help
- **F1**: Context-sensitive help
- **Help menu**: Built-in documentation
- **Website**: Complete user manual
- **Forum**: Community support

### Technical Support
- **GitHub Issues**: Bug reports and feature requests
- **Email**: Technical support team
- **Chat**: Real-time support (business hours)

## Version Information

### Current Version: 4.2.0
- **Release Date**: July 2025
- **New Features**: Enhanced scanning, improved UI
- **Bug Fixes**: Multiple stability improvements
- **Requirements**: Windows 10+, macOS 10.15+

---

💡 **Tip**: Keep this reference handy during cable testing sessions for quick access to common settings and troubleshooting steps!

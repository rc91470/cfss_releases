# CFSS (Copper/Fiber Serial Scanner) - Downloads

[![Latest Release](https://img.shields.io/github/v/release/rc91470/cfss_releases)](https://github.com/rc91470/cfss_releases/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/rc91470/cfss_releases/total)](https://github.com/rc91470/cfss_releases/releases)

A comprehensive copper and fiber serial scanning system for network cable testing and jumper cable serial number verification.

## 📥 Download Latest Version

### Windows
- **[Download Windows Package](https://github.com/rc91470/cfss_releases/releases/latest/download/CFSS_v4.2.0_Windows.zip)** (Complete package)

### macOS
- **[Download macOS Package](https://github.com/rc91470/cfss_releases/releases/latest/download/CFSS-macOS-4.2.0.tar.gz)** (Complete package)
- **[Download macOS Fix Script](https://github.com/rc91470/cfss_releases/releases/latest/download/macos_fix.sh)** (If you see "damaged" app error)

## 🚀 Key Features

### Core Functionality
- **Serial Number Verification**: Scan jumper cable serials and compare against expected values
- **Multiple Circuit Support**: Load and manage multiple network circuits from CSV files
- **Progress Tracking**: Visual progress bars showing completion percentage
- **SharePoint Integration**: Streamlined CSV sync and data export functionality

### User Interface
- **Modern Interface**: Clean, professional interface with dark theme
- **Cross-Platform**: Available for both macOS and Windows
- **Real-time Updates**: Live progress tracking and statistics
- **Issue Management**: Track and resolve scanning discrepancies

### Workflow
1. **Load Data**: Click "Sync CSVs" to import circuit data from SharePoint
2. **Select Circuit**: Choose your circuit and jumper configuration
3. **Start Scanning**: Use barcode scanner or manual entry for serial verification
4. **Track Progress**: Monitor completion with real-time progress bars
5. **Export Results**: Generate reports when scanning is complete

## 🛠️ macOS "Damaged" App Fix

If you see "CFSS.app is damaged", this is normal for unsigned apps:

**Quick Fix**: Download and run the `macos_fix.sh` script from the release assets:
```bash
chmod +x macos_fix.sh
./macos_fix.sh
```

**Manual Fix**:
```bash
xattr -cr CFSS.app
```

See [macOS Troubleshooting](documentation/MACOS_TROUBLESHOOTING.md) for detailed instructions.

## 📚 Documentation

- **[Installation Guide](documentation/INSTALLATION_GUIDE.md)** - Complete setup instructions
- **[macOS Troubleshooting](documentation/MACOS_TROUBLESHOOTING.md)** - macOS-specific setup and fixes
- **[Windows Troubleshooting](documentation/WINDOWS_TROUBLESHOOTING.md)** - Windows-specific setup and fixes
- **[User Guide](documentation/user_guide.md)** - How to use CFSS
- **[Quick Reference](documentation/quick_reference.md)** - Common tasks and shortcuts

## 🔧 System Requirements

### macOS
- macOS 10.14 (Mojave) or later
- 4 GB RAM minimum, 8 GB recommended
- 50 MB available disk space
- Intel or Apple Silicon processor

### Windows
- Windows 10 or later (64-bit)
- 4 GB RAM minimum, 8 GB recommended
- 50 MB available disk space

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a complete list of changes in each version.

## 🐛 Issue Reporting

If you encounter any issues:

1. **Check** the [Troubleshooting Guide](documentation/troubleshooting.md)
2. **Search** existing [Issues](https://github.com/rc91470/cfss_releases/issues)
3. **Create** a new issue with detailed information

## 📄 License

This software is distributed under a proprietary license. See the included license file for details.

## 🔒 Security

For security-related issues, please contact us privately rather than opening a public issue.

---

**Note**: This is the public release repository for CFSS. Source code is maintained in a private repository for security and intellectual property protection.

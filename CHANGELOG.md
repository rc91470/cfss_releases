# Changelog

All notable changes to CFSS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Upcoming features will be listed here

### Changed
- Changes will be listed here

### Fixed
- Bug fixes will be listed here

## [4.2.1] - 2025-07-07

### Added
- **Auto-updater**: Automatic update checking and installation from GitHub releases
- User-friendly update dialog with download progress and automatic restart
- Cross-platform update support for both Windows and macOS

### Fixed
- **UI Focus Issues**: Dialog windows now properly take focus when displayed
- **Input Validation**: Input fields are disabled until data is loaded to prevent errors
- **Field Clearing**: Input fields are properly cleared after SharePoint sync operations
- User data preservation during updates (circuits, progress, scan states remain intact)

### Changed
- Updated to use cfss_releases repository for distribution and updates
- Enhanced error handling and user feedback for update operations
- Improved startup sequence with integrated update checking

## [4.2.0] - 2025-07-06

### Added
- **SharePoint Integration** - Streamlined CSV sync and data export functionality
- **Better Progress Tracking** - Visual progress bars and comprehensive statistics
- **Issue Management** - Track and resolve scanning discrepancies
- **Cross-Platform Support** - Available for both macOS and Windows
- **Serial Number Verification** - Scan jumper cable serials and compare against expected values
- **Multiple Circuit Support** - Load and manage multiple network circuits from CSV files

### Changed
- **Improved UI** - Modern interface with better user experience
- **Enhanced Performance** - Optimized for large CSV file handling
- **Better Documentation** - Comprehensive guides included with download

### Fixed
- **macOS Compatibility** - Fixed "damaged app" issues with proper signing
- **Windows Stability** - Improved reliability on Windows 10/11
- **CSV Loading** - Better handling of large CSV files
- **Progress Tracking** - More accurate completion percentages

### Technical Details
- **App Size**: 50MB for both platforms
- **Archive Size**: 21MB (macOS), 22MB (Windows)
- **Build Date**: July 6, 2025
- **System Requirements**: Windows 10+ (64-bit), macOS 10.14+

## [4.1.0] - 2025-06-15

### Added
- Initial public release
- Core copper and fiber cable scanning functionality
- Data management and export capabilities for network testing
- SharePoint integration
- Multi-platform support (Windows, macOS)

### Changed
- Migrated from internal tool to standalone application
- Improved user interface design
- Enhanced reporting capabilities

### Fixed
- Various stability improvements
- Performance optimizations
- Bug fixes from beta testing

---

## Download Links

- **[Latest Release](https://github.com/rc91470/cfss_releases/releases/latest)**
- **[All Releases](https://github.com/rc91470/cfss_releases/releases)**

## Support

For support and questions:
- Check the [Troubleshooting Guide](documentation/troubleshooting.md)
- Report issues on [GitHub Issues](https://github.com/rc91470/cfss_releases/issues)
- Review the [User Guide](documentation/user_guide.md)

# CFSS (Copper/Fiber Serial Scanner) - Private Development Repository

**Current Version: v4.2.3**

This is the **private development repository** for CFSS. This contains the source code, development tools, and internal documentation.

## 🔒 Repository Structure

This project now uses a **3-repository structure** for better organization and security:

### 1. **cfss_app** (Private - This Repository)
- **Purpose**: Source code and development
- **Contains**: Python source code, build scripts, dev tools
- **Access**: Private - development team only
- **Location**: `https://github.com/rc91470/cfss_app`

### 2. **cfss_releases** (Public)
- **Purpose**: Binary distribution and user support
- **Contains**: Compiled binaries, documentation, installation guides
- **Access**: Public - end users
- **Location**: `https://github.com/rc91470/cfss_releases`

### 3. **cfss_central_management** (Private)
- **Purpose**: Central management application
- **Contains**: Admin tools, server configurations
- **Access**: Private - admin team only

## 🚀 Development Workflow

### For Development
1. **Work in this repository** (cfss_app) for all code changes
2. **Test locally** using the development environment
3. **Build releases** using the build scripts
4. **Use the release automation** to push binaries to public repo

### For Releases
1. **Test locally** using `build_windows.bat` or `build_macos.sh` (development testing only)
2. **Switch to cfss_releases repository** for official builds:
   ```bash
   cd ../cfss_releases
   # Follow the build and release process documented there
   ```
3. **Review** the built files in the cfss_releases repository
4. **Create GitHub release** in the cfss_releases repository

## 📁 Original Application Description

A cross-platform desktop application for scanning and verifying jumper cable serial numbers in network infrastructure. This tool helps network technicians ensure proper cable connections by comparing scanned serial numbers against expected values from circuit documentation.

## Platform Support

- **Windows 10/11**: Full support with native executable
- **macOS**: Compatible with macOS 10.14+ (Intel and Apple Silicon)
- **Cross-Platform**: Built with Python for maximum compatibility

## Features

### Core Functionality
- **Serial Number Verification**: Scan jumper cable serials and compare against expected values
- **Multiple Circuit Support**: Load and manage multiple network circuits from CSV files
- **Progress Tracking**: Visual progress bars showing completion percentage (matches only)
- **Persistent State**: Automatically saves and resumes scan progress across sessions

### User Interface (v4.2.3 Improvements)
- **Modern Dark Theme**: Clean, professional interface built with CustomTkinter
- **DPI Scaling Support**: Automatically scales fonts and UI elements for high-resolution displays (3840x2400+)
- **Responsive Dialogs**: All dialogs now scale properly with different screen sizes
- **Enhanced Font Support**: Improved readability with scalable fonts (Courier 14pt for summaries, 12pt for notes)
- **Real-time Feedback**: Visual and audio feedback for matches, non-matches, and completion
- **Search Functionality**: Quickly jump to specific locations within circuits
- **Status Tracking**: Track matches, non-matches, and skipped items with reasons

### Data Management
- **CSV Import**: Import circuit data from CSV files with standardized column formats
- **Smart Migration**: Preserves scan progress when CSV files are updated
- **SharePoint Integration**: Sync CSVs from SharePoint and export results directly
- **Smart Sorting**: Intelligent sorting based on circuit type and jumper position
- **Deduplication**: Automatic removal of duplicate entries during import
- **Export Results**: Generate detailed text reports of scan results

### Issue Tracking & Resolution (NEW in v4.2.3)
- **Non-Match Resolution**: Enhanced dialog for recording resolution notes when issues are fixed
- **Issue Tracking Database**: Comprehensive tracking of all problems and their resolutions
- **Resolution Notes**: Detailed notes about what was wrong and how it was fixed
- **Issue Reports**: Generate comprehensive reports showing resolution patterns
- **Problem Analytics**: Identify recurring issues and track resolution rates

### Audio Feedback
- **Cross-Platform Audio**: Uses pygame for reliable audio playback on all platforms
- **Match Sound**: Confirmation tone for successful matches
- **Non-Match Sound**: Alert tone for mismatches or issues  
- **Completion Sound**: Celebration tone when circuit is 100% complete

### Security & Data Protection (v4.2.3)
- **Customer Data Protection**: Multi-layer security prevents customer data in builds
- **Automatic Backups**: Customer data is backed up locally before any operations
- **Git Protection**: Comprehensive .gitignore prevents accidental commits
- **Security Checks**: Pre-build verification ensures no sensitive data in distribution

## Supported Circuit Types

- **Standard Circuits**: A-location to Z-location connections
- **CSW Circuits**: Special handling for CSW (Circuit Switch) configurations
- **Multi-Jumper Circuits**: Support for circuits with multiple jumper segments
- **Port-based Connections**: Handles various port numbering schemes (1, 2, 4, 7, etc.)

### Technical Specifications

### Requirements
- **Windows**: Windows 10/11, audio output device
- **macOS**: macOS 10.14+ (Mojave or later), audio output device
- **Development**: Python 3.11+ with required dependencies

### Auto-Updater (v4.2.3)
- **Automatic Updates**: Checks for new releases on startup
- **Cross-Platform**: Works on both Windows and macOS
- **Background Updates**: Downloads and installs updates seamlessly
- **Rollback Protection**: Maintains previous version until update is verified

### File Formats
- **Input**: CSV files with network circuit data
- **Output**: Text-based reports with tabular formatting
- **Database**: SQLite for persistent storage and state management
- **Exports**: JSON format for SharePoint integration

### Architecture
- **Modular Design**: Separate managers for data, circuits, and scan control
- **SQLite Backend**: Fast, reliable data storage and retrieval
- **Cross-Platform Audio**: Pygame mixer for consistent audio across platforms
- **Efficient Processing**: Hash-based change detection for fast CSV reloading
- **DPI Awareness**: Automatic scaling for high-resolution displays
- **Issue Tracking**: Comprehensive database for problem resolution tracking

## Installation

### Windows
1. Download the latest Windows release (.exe) from the releases page
2. Extract to desired directory
3. Place CSV circuit files in the data folder
4. Run `cfss_app.exe`

### macOS
1. Download the latest macOS release (.app or .dmg) from the releases page
2. Install/extract to Applications folder or desired location
3. Place CSV circuit files in the data folder
4. Run the application (may need to allow in Security & Privacy settings)

### From Source (Both Platforms)
```bash
# Clone the repository
git clone [repository-url]
cd cfss_app

# Install dependencies
pip install -r requirements.txt

# Run the application
python cfss_app.py
```

## Usage

1. **Load Circuits**: Place CSV files in the data folder or use "Import CSV(s)"
2. **Select Circuit**: Choose from the circuit dropdown
3. **Select Jumper**: Choose which jumper segment to scan
4. **Scan Serials**: Use barcode scanner or manual entry
5. **Track Progress**: Monitor completion via progress bar and statistics
6. **Export Results**: Save scan results to text reports

## CSV Format Requirements

Your CSV files should include these columns:
- Length, A location, A device, A interface, A jumper serial
- Port 1-8 location, container, cassette, port, jumper serial
- Z location, Z device, Z interface, Z jumper serial

## Key Benefits

- **Cross-Platform**: Works on both Windows and macOS environments
- **Accuracy**: Eliminates human error in cable verification
- **Efficiency**: Faster than manual documentation methods  
- **Reliability**: Persistent state prevents data loss
- **Flexibility**: Handles various circuit types and configurations
- **Reporting**: Professional documentation for compliance and records

## Development

Built with Python using modern, cross-platform libraries:
- **CustomTkinter**: Modern UI framework (cross-platform)
- **SQLite**: Database management (built into Python)
- **Pygame**: Cross-platform audio system
- **Natural Sorting**: Intelligent data ordering

### Dependencies
```
customtkinter>=5.0.0
pygame>=2.0.0
natsort>=8.0.0
requests>=2.28.0
```

### Recent Updates (v4.2.3)
- **Enhanced DPI Scaling**: All UI elements now scale properly on high-resolution displays
- **Issue Tracking System**: Comprehensive tracking of problems and their resolutions
- **Auto-Updater**: Automatic update checking and installation
- **Security Hardening**: Multiple layers of customer data protection
- **SharePoint Integration**: Direct sync and export capabilities
- **Smart CSV Migration**: Preserves scan progress when updating circuit data
- **Improved Dialog Layouts**: Better button sizing and layout for all screen sizes

## Building from Source

### For Windows
```bash
pip install pyinstaller
pyinstaller --onefile --windowed cfss_app.py
```

### For macOS
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --osx-bundle-identifier com.yourcompany.cfss cfss_app.py
```

## 🛠️ Development Setup

### Prerequisites
- Python 3.11 or later
- Windows 10+ or macOS 10.15+
- Git with GitHub CLI (`gh`) configured

### Initial Setup
1. **Clone this repository**:
   ```bash
   git clone https://github.com/rc91470/cfss_app.git
   cd cfss_app
   ```

2. **Set up development environment**:
   ```bash
   # Windows
   setup_dev_windows.bat
   
   # macOS
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Start development server**:
   ```bash
   start_dev.bat  # Windows
   python cfss_app.py  # macOS/Linux
   ```

## 🔧 Build Process

### ⚠️ **IMPORTANT: Development vs Distribution**

**This repository is for DEVELOPMENT ONLY!**
- **NO .exe or .app files** should ever be committed here
- **NO distribution builds** should be done in this repository
- This repository contains source code and development tools only

### For Official Builds and Releases
**Use the `cfss_releases` repository for all distribution builds:**
1. **Clone cfss_releases**: `git clone https://github.com/rc91470/cfss_releases.git`
2. **Use the build scripts there** for creating distributable .exe and .app files
3. **Create releases there** for public distribution

### Development Testing (Local Only)
The build scripts in this repository are for **local development testing only**:

```bash
# For local development testing only (creates files in dist/ - not for distribution)
./build_macos.sh     # macOS - creates .app for local testing
build_windows.bat    # Windows - creates .exe for local testing
```

**⚠️ Never commit the generated dist/ or build/ folders!**

### Security First - Customer Data Protection
**🚨 CRITICAL: All builds automatically exclude customer data!**

The build process includes multiple security layers:
- **Automatic CSV cleaning** - No customer data in builds
- **Pre-build security checks** - Scans for sensitive data
- **Comprehensive .gitignore** - Prevents commits of customer data
- **Security documentation** - See `SECURITY_MEASURES.md`

### Repository Separation
- **cfss** (this repo): Private development, source code, no builds
- **cfss_releases**: Public distribution, compiled builds, user documentation

## 📚 Documentation

### Internal Documentation
- Development notes in source code
- API documentation in comments
- Build process documentation in scripts

### Public Documentation
- User guides in the **public repository** at `https://github.com/rc91470/cfss_releases`
- Installation instructions for end users
- Troubleshooting guides for support

## 🔐 Security Notes

- **Never commit** sensitive data (passwords, keys, tokens)
- **Use environment variables** for configuration
- **Review** all commits before pushing
- **Keep dependencies** updated and secure

---

## 📞 Internal Team Information

**Remember**: This is the private development repository. All public-facing content goes in the `cfss_releases` repository.

**Public Repository**: https://github.com/rc91470/cfss_releases

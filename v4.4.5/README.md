# CFSS (Copper/Fiber Serial Scanner) - Development Repository

##  Looking for Downloads?

**This is the source code repository.** For downloads and releases, go to:

###  **[Download CFSS Releases](https://github.com/rc91470/cfss_releases/releases/latest)**

---

**Current Version: v4.4.1**

This is the **private development repository** for CFSS. Contains source code, development tools, and internal documentation.


##  Repository Structure

**2-repository structure** for clean separation:

### 1. **cfss** (Private - This Repository)
- **Purpose**: Source code and active development
- **Contains**: Python source code, build scripts, development tools
- **Access**: Private development team only
- **Location**: https://github.com/rc91470/cfss

### 2. **cfss_releases** (Public)
- **Purpose**: Binary distribution and user support  
- **Contains**: Compiled releases, documentation, installation guides
- **Access**: Public - end users and auto-updater
- **Location**: https://github.com/rc91470/cfss_releases

##  Development Workflow

### Development Process
1. **Work in this repository** for all code changes and features
2. **Test locally** using `python cfss_app.py` in virtual environment
3. **Build releases** using `build_release.bat` (outputs to releases repo)
4. **Use GitHub releases** for distribution and auto-updater compatibility

### Release Process
1. **Update version** in `cfss_app.py` 
2. **Build executable** using `build_release.bat` 
3. **Commit and push** development changes to this repo
4. **Create GitHub release** in cfss_releases repo

##  Application Description

Cross-platform desktop application for scanning and verifying jumper cable serial numbers in network infrastructure. Helps network technicians ensure proper cable connections by comparing scanned serial numbers against expected values.

## Key Features (v4.4.1)

###  Critical Fixes
- **Fixed Serial Number Logic**: Synchronized save and display functions
- **Data Consistency**: Scan results now match saved data exactly

###  Enhanced Auto-Updater
- **Component Validation**: Detects and restores missing files
- **Sounds Folder Restoration**: Fixes Windows popup issues
- **ZIP File Handling**: Improved update management
- **GitHub Integration**: Compatible with GitHub releases API

### Core Functionality
- **Serial Number Verification**: Scan and compare against expected values
- **Multiple Circuit Support**: Load and manage multiple network circuits
- **Progress Tracking**: Visual progress bars and completion status
- **Persistent State**: Auto-saves and resumes scan progress

## Development Setup

### Prerequisites
- Python 3.11+, Windows 10+ or macOS 10.15+, Git access

### Quick Start
```bash
# Clone and setup
git clone https://github.com/rc91470/cfss.git
cd cfss
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux  
source .venv/bin/activate

# Install and run
pip install -r requirements.txt
python cfss_app.py
```

## Building Releases

###  Development vs Distribution
- **This repo**: Development and source code ONLY
- **NO .exe files** committed here
- **Release builds** managed in `cfss_releases` repository

### Build Process
```bash
# Local testing only
build_release.bat    # Creates test build in releases repo

# Official releases: Switch to cfss_releases repo and create GitHub release
```

## Architecture

### Core Components
- **cfss_app.py**: Main application and UI
- **auto_updater.py**: Enhanced auto-updater with validation
- **circuit_manager.py**: Circuit data management  
- **data_manager.py**: CSV import/export and database
- **scan_controller.py**: Serial scanning logic

### Dependencies
```
customtkinter>=5.0.0    # Modern UI framework
pygame>=2.0.0          # Cross-platform audio
natsort>=8.0.0         # Data sorting
requests>=2.28.0       # Auto-updater HTTP
```

## File Structure
```
cfss/
 .venv/                  # Virtual environment
 archive_old_files/      # Historical files
 data/                   # Application data
 sounds/                 # Audio feedback
 cfss_app.py            # Main application
 auto_updater.py        # Enhanced auto-updater
 build_release.bat      # Build script
 requirements.txt       # Dependencies
 WORKFLOW.md           # Development guide
```

## Security & Data Protection
- **Customer Data Protection**: Build excludes all customer CSV data
- **Private Repository**: Source code access restricted
- **Multi-layer Security**: Prevents data leakage

## Support & Documentation
- **Development**: This repository with source code
- **User Support**: https://github.com/rc91470/cfss_releases
- **Releases**: GitHub releases with auto-updater support

---
**Development Repository**: All public releases go in `cfss_releases` repository.

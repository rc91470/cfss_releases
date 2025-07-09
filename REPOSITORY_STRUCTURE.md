# CFSS Releases Repository Structure

This document explains the organization of the cfss_releases repository to prevent conflicts between platform maintainers.

## 📁 Directory Structure

```
cfss_releases/
├── README.md                           # Main repository README
├── CHANGELOG.md                        # Version history
├── REPOSITORY_STRUCTURE.md            # This file
├── DISTRIBUTION_ONLY.md               # Notice about repository purpose
│
├── documentation/                      # Shared documentation
│   ├── installation/
│   ├── troubleshooting/
│   └── user_guide/
│
├── releases/                           # Platform-specific releases
│   ├── windows/                        # Windows maintainer zone
│   │   ├── latest/                     # Latest Windows build
│   │   │   ├── CFSS_v4.2.3_Windows.zip
│   │   │   ├── checksums.txt
│   │   │   └── windows_install.bat
│   │   └── v4.2.3/                     # Version-specific builds
│   │       ├── CFSS_v4.2.3_Windows.zip
│   │       ├── checksums.txt
│   │       └── windows_install.bat
│   │
│   └── macos/                          # macOS maintainer zone
│       ├── latest/                     # Latest macOS build
│       │   ├── CFSS-macOS-4.2.3.tar.gz
│       │   ├── checksums.txt
│       │   └── macos_fix.sh
│       └── v4.2.3/                     # Version-specific builds
│           ├── CFSS-macOS-4.2.3.tar.gz
│           ├── checksums.txt
│           └── macos_fix.sh
│
├── scripts/                            # Shared build automation
│   ├── release_automation.ps1          # Cross-platform release script
│   ├── build_windows.bat               # Windows build script
│   └── build_macos.sh                  # macOS build script
│
└── v4.2.3/                            # Version-specific source & builds
    ├── src/                            # Source code snapshot
    ├── build/                          # Build artifacts
    ├── build_macos.sh                  # macOS build script for this version
    └── build_windows.bat               # Windows build script for this version
```

## 🔧 Platform Maintainer Guidelines

### Windows Maintainer
**Modify only these directories:**
- `releases/windows/`
- `scripts/build_windows.bat`
- `scripts/release_automation.ps1` (Windows-specific sections)

**Responsibilities:**
- Build Windows .exe files
- Update Windows installation scripts
- Maintain Windows-specific documentation
- Test Windows builds before release

### macOS Maintainer  
**Modify only these directories:**
- `releases/macos/`
- `scripts/build_macos.sh`
- `scripts/release_automation.ps1` (macOS-specific sections)

**Responsibilities:**
- Build macOS .app files
- Update macOS fix scripts
- Maintain macOS-specific documentation
- Test macOS builds before release

### Shared Responsibilities
**Both maintainers can modify:**
- `README.md` (coordinate changes)
- `CHANGELOG.md` (add version entries)
- `documentation/` (coordinate changes)

## 🚀 Release Process

### 1. Version Preparation
```bash
# Create version directory
mkdir v4.2.4
cd v4.2.4

# Copy source from development repo
cp -r /path/to/cfss/* src/

# Create build scripts
cp ../scripts/build_macos.sh .
cp ../scripts/build_windows.bat .
```

### 2. Platform Builds
```bash
# Windows maintainer
./build_windows.bat

# macOS maintainer  
./build_macos.sh
```

### 3. Release Deployment
```bash
# Copy to latest directories
cp releases/windows/v4.2.4/* releases/windows/latest/
cp releases/macos/v4.2.4/* releases/macos/latest/

# Update README with new version
# Update CHANGELOG.md
# Create GitHub release
```

## 🛡️ Conflict Prevention

### File Ownership
- **Windows files**: `.exe`, `.bat`, `.ps1` (Windows-specific)
- **macOS files**: `.app`, `.sh`, `.tar.gz` (macOS-specific)
- **Shared files**: `.md`, documentation

### Naming Conventions
- **Windows**: `CFSS_v4.2.3_Windows.zip`
- **macOS**: `CFSS-macOS-4.2.3.tar.gz`
- **Scripts**: `macos_fix.sh`, `windows_install.bat`

### Git Workflow
1. **Pull** latest changes before working
2. **Work** only in your platform directories
3. **Test** thoroughly before committing
4. **Coordinate** with other maintainer for releases
5. **Tag** releases together

## 🔄 Update Process

### Updating Your Platform
1. Update your platform's build in `releases/{platform}/latest/`
2. Create version-specific directory `releases/{platform}/v4.2.x/`
3. Update README badges and download links
4. Update CHANGELOG.md
5. Test the build works correctly

### Coordinated Release
1. Both maintainers prepare their builds
2. Test both platforms work correctly
3. Update shared documentation together
4. Create GitHub release with both files
5. Update README to point to new release

## 📋 Checklist for New Releases

### Pre-Release
- [ ] Windows build tested and working
- [ ] macOS build tested and working  
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] README.md badges updated
- [ ] Version numbers consistent everywhere

### Release
- [ ] GitHub release created
- [ ] Both platform files uploaded
- [ ] Release notes added
- [ ] Download links tested
- [ ] Auto-updater tested (if applicable)

### Post-Release
- [ ] Verify downloads work
- [ ] Test installation on both platforms
- [ ] Monitor for issues
- [ ] Update any external documentation

## 🆘 Emergency Procedures

### Hotfix Process
1. **Identify** the critical issue
2. **Coordinate** with other maintainer
3. **Fix** in the development repository first
4. **Build** hotfix version (increment patch version)
5. **Test** thoroughly
6. **Release** immediately
7. **Document** the hotfix in CHANGELOG.md

### Rollback Process
1. **Identify** the problematic release
2. **Coordinate** rollback with other maintainer
3. **Update** README to point to previous version
4. **Create** new release with rollback files
5. **Document** rollback reason
6. **Fix** issues in development repository

This structure ensures both platform maintainers can work independently while maintaining consistency and preventing conflicts.

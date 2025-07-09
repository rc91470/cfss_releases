# Release Management Guide

This document explains how to create and manage releases for the CFSS project.

## ⚠️ IMPORTANT: Repository Separation

**Development Repository (cfss):**
- Contains source code and development tools
- Used for development testing only
- Should NOT contain .app/.exe files or public releases

**Release Repository (cfss_releases):**
- Contains official build scripts and releases
- All public releases are published here
- Repository: https://github.com/rc91470/cfss_releases

## Quick Start

### 1. Build and Test Locally (Development Only)
```bash
# Build the app for local testing
./build_macos.sh

# Test the built app
open dist/CFSS.app
```
**⚠️ WARNING:** This is for development testing only. Do not distribute this build.

### 2. Create Official Release (Use cfss_releases Repository)
```bash
# Switch to cfss_releases repository
cd /path/to/cfss_releases

# Create a draft release to test
./draft_release.sh

# This creates a draft on GitHub that you can review
```

### 3. Create Official Release (cfss_releases Repository)
```bash
# Make sure you're authenticated with GitHub
gh auth login

# Create the official release in cfss_releases
./release.sh
```

## Release Process

### Prerequisites
- GitHub CLI installed (`brew install gh`)
- GitHub authentication (`gh auth login`)
- Working build environment

### Version Management
```bash
# Update version across all files
./update_version.sh 4.3.0

# Commit the version changes
git add .
git commit -m "Bump version to 4.3.0"
git push
```

### Creating Releases

#### Draft Release (Testing)
- Creates a draft release on GitHub
- Uploads the built app for testing
- Marked as draft (not visible to users)
- Use this to test the release process

#### Official Release
- Creates a public release
- Generates comprehensive release notes
- Uploads the final app bundle
- Automatically tagged with version

### File Structure
```
CFSS/
├── build_macos.sh          # Main build script
├── release.sh              # Official release script
├── draft_release.sh        # Draft release for testing
├── update_version.sh       # Version management
├── .gitignore             # Excludes build artifacts
└── dist/                  # Build output (excluded from git)
    └── CFSS.app          # Built macOS app
```

## GitHub Releases vs Git Repository

### What's in Git
- Source code
- Build scripts
- Documentation
- Configuration files

### What's in Releases
- Compiled .app bundles
- Release archives (.tar.gz)
- Release notes
- Version tags

## Benefits of This Approach

1. **Clean Repository**: No large binary files in git history
2. **Proper Versioning**: Each release is tagged and documented
3. **Easy Distribution**: Users download from GitHub releases
4. **Download Statistics**: Track how many people download each version
5. **Release Notes**: Automatically generated changelog for users

## User Download Instructions

Users can download releases in several ways:

### GitHub Web Interface
1. Go to the repository on GitHub
2. Click "Releases" on the right side
3. Download the latest `.tar.gz` file
4. Extract and run

### Command Line
```bash
# Download latest release
curl -L https://github.com/YOUR_USERNAME/CFSS/releases/latest/download/CFSS-macOS-4.2.0.tar.gz -o CFSS.tar.gz

# Extract
tar -xzf CFSS.tar.gz

# Run
open CFSS.app
```

## Troubleshooting

### Build Fails
- Check that `venv` is properly set up
- Verify all dependencies are installed
- Run `./build_macos.sh` manually to see errors

### Release Creation Fails
- Ensure GitHub CLI is authenticated: `gh auth status`
- Check that the version tag doesn't already exist
- Verify the build completed successfully

### Large File Issues
- The 57MB app size is well within GitHub's 100MB limit
- Archives are compressed and typically smaller
- No Git LFS needed for this project

### macOS Installation Issues

#### "App is damaged and should be moved to the trash"
This is a common macOS security issue, not actual damage. The app isn't signed with an Apple Developer Certificate.

**Solution 1: Command Line Fix**
```bash
# Remove quarantine attributes
xattr -cr /path/to/CFSS.app
```

**Solution 2: System Settings**
1. Go to System Preferences → Security & Privacy → General
2. Click "Allow" next to the blocked app message
3. Or enable "Allow apps downloaded from: Anywhere"

**Solution 3: Right-click Method**
1. Right-click CFSS.app → Open
2. Click "Open" in the security dialog

#### "Cannot verify developer" warning
1. Right-click CFSS.app → Open
2. Click "Open" when prompted
3. The app will be trusted for future runs

#### App won't launch
1. Check that it's in the Applications folder
2. Try running from Terminal: `open /Applications/CFSS.app`
3. Check Console.app for error messages

### Distribution Tips
- Always test downloads on a clean Mac
- Include installation instructions with releases
- Consider code signing for professional distribution

## Best Practices

1. **Always test with draft releases first**
2. **Update version numbers before releasing**
3. **Write meaningful release notes**
4. **Tag releases with semantic versioning (v4.2.0)**
5. **Keep build artifacts out of git (they're in .gitignore)**

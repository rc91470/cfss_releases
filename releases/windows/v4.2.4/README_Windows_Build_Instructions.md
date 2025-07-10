# Windows v4.2.4 Build Instructions

## URGENT: Windows Build Required for v4.2.4

**Status:** ⚠️ **MISSING** - Windows v4.2.4 build not yet created

## Required Files for v4.2.4:
- `CFSS_v4.2.4_Windows.zip` (main Windows build)
- `CFSS_v4.2.4_Windows.zip.sha256` (checksum file)

## Windows Maintainer Instructions:

### 1. Source Code Location:
```bash
# Get the v4.2.4 source from main CFSS repo
git clone https://github.com/rc91470/cfss.git
cd cfss
git checkout main  # v4.2.4 is in main branch
```

### 2. Version Verification:
- Ensure `cfss_app.py` shows `VERSION = "4.2.4"`
- All dialog sizing uses fixed values (no get_scaled_size)
- High-DPI compatibility implemented

### 3. Build Process:
```bash
# Use existing Windows build scripts
.\build_windows.bat
# OR
.\setup_dev_windows.bat  # if needed
```

### 4. Expected Output:
- `CFSS_v4.2.4_Windows.zip` (Windows application bundle)
- Generate SHA256: `certutil -hashfile CFSS_v4.2.4_Windows.zip SHA256`

### 5. Upload to cfss_releases:
```bash
# Copy files to this directory
cp CFSS_v4.2.4_Windows.zip /cfss_releases/releases/windows/v4.2.4/
cp CFSS_v4.2.4_Windows.zip.sha256 /cfss_releases/releases/windows/v4.2.4/

# Also update latest symlink
cp CFSS_v4.2.4_Windows.zip /cfss_releases/releases/windows/latest/
```

### 6. Add to GitHub Release:
```bash
# Add Windows build to existing v4.2.4 release
gh release upload v4.2.4 CFSS_v4.2.4_Windows.zip CFSS_v4.2.4_Windows.zip.sha256
```

## Critical Notes:
- **v4.2.4 is the authoritative cross-platform release**
- **Must use exact same codebase as macOS v4.2.4**
- **DO NOT use any older versions (v4.2.3, etc.)**
- **High-DPI dialog fixes are essential**

## Contact:
If build issues occur, coordinate with macOS maintainer for consistency.

---
**Last Updated:** July 9, 2025
**Required By:** ASAP for complete v4.2.4 release

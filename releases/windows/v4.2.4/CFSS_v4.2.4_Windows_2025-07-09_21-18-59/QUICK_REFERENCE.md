# CFSS Quick Reference Guide

## 🚀 Building & Releasing

### Build the App Locally (Development Testing Only)
```bash
cd /Users/richardcoleman/VSCode/CFSS
./build_macos.sh
```
**Result:** Creates `dist/CFSS.app` for local development testing only
**⚠️ WARNING:** This is for development testing only. All official releases must be done in cfss_releases repository.

### Official Releases (Use cfss_releases Repository)
All official builds and releases are done in the cfss_releases repository:
- Clone: https://github.com/rc91470/cfss_releases
- Follow the build and release process documented there
- Public releases are published at: https://github.com/rc91470/cfss_releases/releases

### Test a Draft Release
```bash
# This must be done in cfss_releases repository
./draft_release.sh
```
**What it does:** Builds app, creates archive, uploads draft to GitHub
**Result:** Draft release at https://github.com/rc91470/cfss_releases/releases

### Create Official Release
```bash
# This must be done in cfss_releases repository
./release.sh
```
**What it does:** Creates official release with proper version tag

### Update Version
```bash
# Update version in cfss development repo first
./update_version.sh 4.3.0
git add .
git commit -m "Bump version to 4.3.0"
git push
# Then update cfss_releases and create release there
```

## 🔧 Fix "App is Damaged" Error

### For Your Local Build
The build script now automatically fixes this, but if needed:
```bash
xattr -cr /path/to/CFSS.app
```

### For Downloaded Apps (Users Getting "App is Damaged" Error)

**⚠️ IMPORTANT: Do NOT click "Move to Trash" - this is normal for unsigned apps**

**Option 1: Use the Fix Script (Easiest)**
```bash
# Download macos_fix.sh from GitHub releases
chmod +x macos_fix.sh
./macos_fix.sh
```

**Option 2: Terminal Method (Most Reliable)**
```bash
# Navigate to where you extracted the app
cd ~/Downloads  # or wherever you extracted it

# Remove quarantine attributes
xattr -cr CFSS.app

# Move to Applications (optional)
mv CFSS.app /Applications/

# Now it should open normally
open /Applications/CFSS.app
```

**Option 3: Right-click Method**
1. **DO NOT** click "Move to Trash" in the first dialog
2. Right-click CFSS.app → **Open** (not double-click)
3. Click **Open** in the security dialog that appears
4. App should now open and be trusted

**Option 4: System Settings (If blocked)**
1. Try to open the app (it will be blocked)
2. System Preferences → Security & Privacy → General
3. Click **"Open Anyway"** next to the blocked app message
4. Try opening the app again

## 🛡️ Windows Defender Warning

### For Windows Users
When you first run `CFSS.exe`, Windows Defender SmartScreen will show a warning:

**"Windows protected your PC" or "Microsoft Defender SmartScreen prevented an unrecognized app from starting"**

**This is normal for unsigned applications. To run the app:**

1. **Click "More info"** in the Windows Defender dialog
2. **Click "Run anyway"** button that appears
3. The app will now start and be trusted for future runs

**Alternative method:**
- Right-click `CFSS.exe` → **Properties** → **Unblock** → **OK**
- Then double-click to run normally

## 📦 Distribution Process

### 1. Prepare Release
```bash
# Update version if needed
./update_version.sh 4.3.0

# Build and test locally
./build_macos.sh

# Test with draft release
./draft_release.sh
```

### 2. Create Official Release
```bash
# Make sure everything is committed
git add .
git commit -m "Ready for release v4.3.0"
git push

# Create the release
./release.sh
```

### 3. Share with Users
- Send them: https://github.com/rc91470/cfss_releases/releases
- Include the installation guide (INSTALLATION_GUIDE.md)

## 🛠️ Development Workflow

### Daily Development
```bash
# Activate virtual environment
source venv/bin/activate

# Run the app for testing
python cfss_app.py

# Or use VS Code task: Cmd+Shift+P → "Run Task" → "Run CFSS App"
```

### Before Releasing
```bash
# Test build
./build_macos.sh

# Test the built app
open dist/CFSS.app

# If satisfied, create draft
./draft_release.sh
```

## 📁 Key Files & Locations

### Build Files
- `build_macos.sh` - Main build script
- `cfss_app.spec` - PyInstaller configuration
- `requirements.txt` - Python dependencies

### Release Files
- `release.sh` - Official releases
- `draft_release.sh` - Test releases
- `update_version.sh` - Version management

### Documentation
- `INSTALLATION_GUIDE.md` - For end users
- `RELEASE_GUIDE.md` - For developers/you
- `README.md` - Project overview

### Built App Location
- `dist/CFSS.app` - The built macOS app
- `dist/CFSS-4.2.0-macOS.zip` - Distribution archive

## 🔍 Troubleshooting

### Build Fails
```bash
# Check Python environment
source venv/bin/activate
python --version

# Reinstall dependencies
pip install -r requirements.txt

# Try building again
./build_macos.sh
```

### Release Fails
```bash
# Check GitHub authentication
gh auth status

# Re-authenticate if needed
gh auth login

# Try again
./draft_release.sh
```

### App Won't Run (Downloaded from GitHub)
**The "App is Damaged" error is normal for unsigned apps. DO NOT trash the app.**

```bash
# First, find where you extracted the app
cd ~/Downloads  # or your extraction location

# Remove quarantine (most important step)
xattr -cr CFSS.app

# Check what attributes were removed
xattr -l CFSS.app  # Should show no quarantine attributes

# Move to Applications and try to open
mv CFSS.app /Applications/
open /Applications/CFSS.app
```

**If still having issues:**
```bash
# Check permissions
ls -la /Applications/CFSS.app/Contents/MacOS/

# Try running the executable directly
/Applications/CFSS.app/Contents/MacOS/cfss_app
```

### Windows Won't Run (Downloaded from GitHub)
**Windows Defender warning is normal for unsigned apps.**

**If you see "Windows protected your PC" or white/invisible dialog boxes:**

1. **Windows Defender Fix:**
   - Click **"More info"** in the Windows Defender dialog
   - Click **"Run anyway"** button that appears
   - App will now be trusted

2. **If dialog boxes have white text on white background:**
   - This is a Windows display scaling issue
   - Try running as administrator: Right-click CFSS.exe → "Run as administrator"
   - Or try changing Windows display scaling to 100% temporarily

3. **Alternative unblock method:**
   - Right-click CFSS.exe → **Properties** → **Unblock** → **OK**
   - Then double-click to run normally

## 📋 Pre-Release Checklist

- [ ] Code is working and tested
- [ ] Version updated if needed (`./update_version.sh`)
- [ ] Local build successful (`./build_macos.sh`)
- [ ] App opens and functions correctly
- [ ] Draft release created and tested (`./draft_release.sh`)
- [ ] Changes committed to git
- [ ] Ready for official release (`./release.sh`)

## 🔗 Important Links

- **GitHub Repo:** https://github.com/rc91470/cfss
- **Releases:** https://github.com/rc91470/cfss_releases/releases
- **VS Code Workspace:** /Users/richardcoleman/VSCode/CFSS

## 💡 Quick Tips

1. **Always test with draft releases first**
2. **The build script automatically fixes the "damaged" error**
3. **Users should download from GitHub Releases, not clone the repo**
4. **Use the macos_fix.sh script for easy "damaged" app fixes**
5. **Windows users: Click "More info" → "Run anyway" for Defender warnings**
6. **If dialog boxes are invisible/white text: Try running as administrator**
7. **Include INSTALLATION_GUIDE.md when sharing**
8. **Keep version numbers semantic (4.2.0, 4.2.1, 4.3.0)**

## 🆘 Emergency Fixes

### Delete Bad Release
```bash
gh release delete v4.2.0  # Replace with actual tag
```

### Rebuild Everything
```bash
rm -rf dist/ build/
./build_macos.sh
```

### Reset Git (if needed)
```bash
git status
git stash  # Save uncommitted changes
git pull origin main
```

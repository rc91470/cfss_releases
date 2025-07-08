# CFSS Installation Guide

## Quick Install

1. **Download** the latest release from [GitHub Releases](https://github.com/rc91470/cfss/releases)
2. **Extract** the ZIP file
3. **Move** CFSS.app to your Applications folder
4. **Run** the app by double-clicking it

## Troubleshooting

### ⚠️ "App is damaged and should be moved to the trash"

This is a common macOS security message - the app isn't actually damaged! This happens because the app isn't signed with an Apple Developer Certificate.

**Quick Fix Options:**

**Option 1: Command Line (Recommended)**
```bash
xattr -cr /Applications/CFSS.app
```

**Option 2: Right-click Method**
1. Right-click CFSS.app → **Open**
2. Click **Open** in the security dialog
3. The app will be trusted for future runs

**Option 3: System Settings**
1. Go to **System Preferences** → **Security & Privacy** → **General**
2. Click **Allow** next to the blocked app message

### ⚠️ "Cannot verify developer" warning

1. Right-click CFSS.app → **Open**
2. Click **Open** when prompted
3. The app will be trusted for future runs

### 🔧 App won't launch

1. Make sure the app is in your **Applications** folder
2. Try running from Terminal: `open /Applications/CFSS.app`
3. Check **Console.app** for error messages

## System Requirements

- macOS 10.14 (Mojave) or later
- 100MB free disk space
- No additional software required

## What is CFSS?

CFSS is a Circuit Finder Search System that helps you search and analyze circuit data efficiently with a modern, user-friendly interface.

## Support

If you encounter issues:
1. Check this guide first
2. Look for similar issues in the [GitHub Issues](https://github.com/rc91470/cfss/issues)
3. Create a new issue if needed

## Privacy

CFSS runs entirely on your computer - no data is sent to external servers.

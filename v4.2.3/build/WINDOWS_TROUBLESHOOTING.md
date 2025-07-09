# Windows Troubleshooting Guide for CFSS

## 🚨 Windows Defender Warning

When you first run `CFSS.exe`, you'll see:
**"Windows protected your PC"** or **"Microsoft Defender SmartScreen prevented an unrecognized app from starting"**

**This is normal for unsigned apps. To fix:**

1. **Click "More info"** in the Windows Defender dialog
2. **Click "Run anyway"** button that appears
3. The app will now start and be trusted for future runs

## 🔍 Dialog Boxes with White/Invisible Text

If you see dialog boxes with 3 buttons but can't read the text (white text on white background):

### Quick Fixes:

1. **Run as Administrator:**
   - Right-click `CFSS.exe` → "Run as administrator"
   - This often fixes display scaling issues

2. **Windows Display Scaling:**
   - Right-click desktop → Display settings
   - Temporarily set "Scale and layout" to 100%
   - Run CFSS, then restore your preferred scaling

3. **Unblock the File:**
   - Right-click `CFSS.exe` → Properties
   - Check "Unblock" box → OK
   - Then double-click to run normally

### What the Dialog Says:
When you get a non-match (scanned serial doesn't match expected), you'll see:
- **"Non-Match Detected"** (red text)
- **Expected:** [expected serial] (blue text)
- **Scanned:** [your scanned serial] (yellow text)
- **"What would you like to do?"**

**The 3 buttons are:**
1. **Skip This Location** - Skip for now, come back later
2. **Record Non-Match** - Mark it as a non-match
3. **Fixed - Add Note** - You fixed the issue, add a note about what was wrong

## 🎯 Keyboard Shortcuts
If you can't see the buttons clearly:
- **Tab** - Navigate between buttons
- **Enter** - Click the selected button
- **Spacebar** - Click the selected button
- **Escape** - Close dialog (same as "Skip This Location")

## 📋 Common Issues & Solutions

### Issue: "App won't start"
**Solution:** Follow the Windows Defender steps above

### Issue: "First launch is very slow"
**Solution:** This is normal - Windows Defender scans the app. Subsequent launches are faster.

### Issue: "Dialog boxes are invisible"
**Solution:** Try running as administrator or adjust display scaling

### Issue: "App crashes when scanning"
**Solution:** Make sure you have the latest version and all CSV files are properly formatted

## 🔗 Need More Help?

- **GitHub Issues**: https://github.com/rc91470/cfss/issues
- **Release Page**: https://github.com/rc91470/cfss_releases/releases/tag/v4.2.0
- **Documentation**: Check README.md in the repository

---

*This guide covers common Windows installation and usage issues. The security warnings are completely normal for unsigned applications downloaded from the internet.*

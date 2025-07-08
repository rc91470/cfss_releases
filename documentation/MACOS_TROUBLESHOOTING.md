# macOS Troubleshooting Guide for CFSS

## 🚨 "App is Damaged" Error - Step-by-Step Fix

If you see "CFSS.app is damaged and can't be opened. You should move it to the Trash", **DO NOT** click "Move to Trash". This is normal for unsigned apps.

### Method 1: Use the Fix Script (Easiest)

1. **Download the fix script** from the GitHub release assets:
   - Go to: https://github.com/rc91470/cfss/releases/tag/v4.2.0
   - Download **macos_fix.sh**

2. **Make it executable and run it**:
   ```bash
   chmod +x macos_fix.sh
   ./macos_fix.sh
   ```

3. **The script will automatically**:
   - Find your CFSS.app
   - Remove quarantine attributes
   - Test opening the app

### Method 2: Terminal Commands (Manual)

1. **Open Terminal** (Applications → Utilities → Terminal)

2. **Navigate to where you extracted CFSS.app**:
   ```bash
   cd ~/Downloads    # or wherever you extracted it
   ```

3. **Remove quarantine attributes**:
   ```bash
   xattr -cr CFSS.app
   ```

4. **Move to Applications** (optional):
   ```bash
   mv CFSS.app /Applications/
   ```

5. **Try to open the app**:
   ```bash
   open /Applications/CFSS.app
   ```

### Method 3: Right-Click Method

1. **Don't double-click** the app - it will show the "damaged" error
2. **Right-click** on CFSS.app → **Open**
3. **Click "Open"** in the security dialog that appears
4. The app should now open and be trusted

### Method 4: System Settings

1. **Try to open the app** (it will be blocked)
2. **Go to System Preferences** → **Security & Privacy** → **General**
3. **Click "Open Anyway"** next to the blocked app message
4. **Try opening the app again**

## 🔍 Verification Steps

After trying any of the above methods, verify the fix worked:

1. **Check for quarantine attributes**:
   ```bash
   xattr -l CFSS.app
   ```
   Should show no quarantine attributes, or be empty.

2. **Test opening the app**:
   ```bash
   open CFSS.app
   ```

## 🆘 If Nothing Works

### Check File Permissions
```bash
ls -la CFSS.app/Contents/MacOS/
chmod +x CFSS.app/Contents/MacOS/cfss_app
```

### Try Running Directly
```bash
/Applications/CFSS.app/Contents/MacOS/cfss_app
```

### Check System Logs
```bash
log show --predicate 'process == "CFSS"' --info --last 5m
```

## 📞 Common Issues & Solutions

### Issue: "Operation not permitted"
**Solution**: Run with sudo:
```bash
sudo xattr -cr CFSS.app
```

### Issue: App opens but crashes immediately
**Solution**: Check Console.app for crash logs or run from terminal to see error messages.

### Issue: "Developer cannot be verified"
**Solution**: This is the same as the "damaged" error. Follow the steps above.

### Issue: Permission denied when running the fix script
**Solution**: Make sure the script is executable:
```bash
chmod +x macos_fix.sh
```

## 🎯 Why This Happens

- macOS Gatekeeper blocks unsigned apps downloaded from the internet
- The app is marked with "quarantine" attributes when downloaded
- This is a security feature, not a bug
- Removing quarantine attributes tells macOS the app is safe

## 📋 Success Checklist

- [ ] Downloaded CFSS-macOS-4.2.0.tar.gz from GitHub releases
- [ ] Extracted the archive: `tar -xzf CFSS-macOS-4.2.0.tar.gz`
- [ ] Removed quarantine: `xattr -cr CFSS.app` OR used the fix script
- [ ] App opens without "damaged" error
- [ ] App functions normally

## 🔗 Need More Help?

- **GitHub Issues**: https://github.com/rc91470/cfss/issues
- **Release Page**: https://github.com/rc91470/cfss/releases/tag/v4.2.0
- **Documentation**: Check README.md in the repository

---

*This guide covers the most common macOS installation issues. The "damaged" error is completely normal and expected for unsigned apps downloaded from the internet.*

# CFSS Troubleshooting Guide

This guide helps you resolve common issues with CFSS (Copper/Fiber Serial Scanner).

## Quick Diagnostics

### Check System Requirements
- **Windows**: Windows 10+ (64-bit), 4GB RAM, .NET Framework 4.7.2+
- **macOS**: macOS 10.15+, 4GB RAM, Intel/Apple Silicon

### Check Installation
- **Verify** CFSS is properly installed and not corrupted
- **Ensure** you have proper permissions to run the application
- **Check** that all required files are present

## Common Issues

### Application Won't Start

#### Windows
**Problem**: "Application failed to start" or "Missing .NET Framework"
**Solution**:
1. Install Microsoft .NET Framework 4.7.2 or later
2. Run Windows Updates
3. Restart your computer
4. Try running CFSS as Administrator

**Problem**: "Access denied" or "Permission error"
**Solution**:
1. Right-click CFSS and select "Run as Administrator"
2. Check that your user account has permissions to the installation folder
3. Temporarily disable antivirus software to test

#### macOS
**Problem**: "App can't be opened because it is from an unidentified developer"
**Solution**:
1. Go to System Preferences > Security & Privacy
2. Click "Open Anyway" next to the CFSS warning
3. Or: Right-click CFSS.app and select "Open"

**Problem**: "App is damaged and can't be opened"
**Solution**:
1. Re-download CFSS from the official source
2. Check that the download completed successfully
3. Verify file integrity using checksums if provided

### Database Issues

**Problem**: "Database connection failed" or "Database is locked"
**Solution**:
1. **Close** all instances of CFSS
2. **Wait** 30 seconds for database locks to clear
3. **Check** database file permissions:
   - Windows: `%APPDATA%/CFSS/cfss_app.db`
   - macOS: `~/Library/Application Support/CFSS/cfss_app.db`
4. **Restart** CFSS

**Problem**: "Database corruption detected"
**Solution**:
1. **Locate** your latest backup in the `scan_backups` folder
2. **Close** CFSS completely
3. **Rename** the corrupted database file (add `.backup` extension)
4. **Restore** from the most recent backup
5. **Restart** CFSS

### Scanning Issues

**Problem**: "Scan failed to start" or "Scanner not responding"
**Solution**:
1. **Check** that your cable scanning hardware is properly connected
2. **Verify** device drivers are installed and up to date
3. **Restart** the scanning service in CFSS settings
4. **Check** Windows Device Manager (Windows) or System Report (macOS)

**Problem**: "Scan progress lost" or "Scan data missing"
**Solution**:
1. **Check** the `scan_backups` folder for recent backups
2. **Restore** from the most recent backup that contains your data
3. **Verify** that automatic backups are enabled in settings

### SharePoint Integration Issues

**Problem**: "SharePoint connection failed"
**Solution**:
1. **Verify** your SharePoint URL and credentials
2. **Test** SharePoint access in a web browser
3. **Check** network connectivity and firewall settings
4. **Update** SharePoint configuration in CFSS settings

**Problem**: "Upload failed" or "Sync errors"
**Solution**:
1. **Check** your SharePoint permissions
2. **Verify** file size limits haven't been exceeded
3. **Try** uploading manually to test SharePoint access
4. **Check** the CFSS log file for detailed error messages

### Performance Issues

**Problem**: "CFSS is running slowly"
**Solution**:
1. **Close** other resource-intensive applications
2. **Increase** available RAM if possible
3. **Clear** old scan data and backups
4. **Check** for available disk space
5. **Restart** CFSS and your computer

**Problem**: "Long scan times" or "Timeouts"
**Solution**:
1. **Reduce** scan resolution or cable length if possible
2. **Check** cable scanning hardware connection and cables
3. **Update** scanning hardware drivers
4. **Increase** timeout values in CFSS settings

## Error Messages

### "Critical Error: Application must close"
1. **Check** the log file: `cfss_app.log`
2. **Note** any error codes or messages
3. **Restart** CFSS
4. **Report** the issue if it persists

### "Memory allocation failed"
1. **Close** other applications to free memory
2. **Restart** CFSS
3. **Consider** upgrading system RAM if this occurs frequently

### "File access denied"
1. **Check** file permissions
2. **Close** any other applications using the same files
3. **Run** CFSS as Administrator (Windows) or with elevated privileges (macOS)

## Log Files and Diagnostics

### Log File Locations
- **Windows**: `%APPDATA%/CFSS/cfss_app.log`
- **macOS**: `~/Library/Application Support/CFSS/cfss_app.log`

### What to Include When Reporting Issues
1. **Error message** (exact text)
2. **Steps** that led to the error
3. **System information** (OS version, RAM, etc.)
4. **Log file** contents (last 50 lines)
5. **Screenshots** if applicable

## Advanced Troubleshooting

### Reset to Factory Settings
1. **Close** CFSS completely
2. **Backup** your scan data
3. **Delete** the configuration folder:
   - Windows: `%APPDATA%/CFSS/`
   - macOS: `~/Library/Application Support/CFSS/`
4. **Restart** CFSS (will recreate default settings)

### Clean Installation
1. **Uninstall** CFSS completely
2. **Delete** any remaining files and folders
3. **Restart** your computer
4. **Download** and install the latest version
5. **Restore** your data from backups

## Getting Help

If these solutions don't resolve your issue:

1. **Search** existing [GitHub Issues](https://github.com/rc91470/cfss_releases/issues)
2. **Create** a new issue with:
   - Detailed description of the problem
   - Steps to reproduce
   - System information
   - Log file contents
   - Screenshots (if applicable)

3. **Contact** support with your issue details

## Prevention Tips

- **Keep** CFSS updated to the latest version
- **Regularly** backup your scan data
- **Monitor** system resources during scanning
- **Keep** your system and drivers updated
- **Use** antivirus software but add CFSS to exclusions if needed

---

**Remember**: Always backup your important scan data before making major changes or troubleshooting!

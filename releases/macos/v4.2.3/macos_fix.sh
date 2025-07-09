#!/bin/bash
# CFSS macOS Fix Script
# Run this script if you get "App is damaged" error

echo "🔧 CFSS macOS Fix Script"
echo "========================"
echo ""

# Check if CFSS.app exists in current directory
if [ -f "CFSS.app/Contents/Info.plist" ]; then
    echo "✅ Found CFSS.app in current directory"
    APP_PATH="CFSS.app"
elif [ -f "/Applications/CFSS.app/Contents/Info.plist" ]; then
    echo "✅ Found CFSS.app in Applications folder"
    APP_PATH="/Applications/CFSS.app"
else
    echo "❌ CFSS.app not found!"
    echo ""
    echo "Please make sure you have:"
    echo "1. Downloaded and extracted CFSS-macOS-4.2.3.tar.gz"
    echo "2. Moved CFSS.app to Applications or current directory"
    echo ""
    echo "Download from: https://github.com/rc91470/cfss_releases/releases"
    exit 1
fi

echo "🔧 Removing quarantine attributes..."
xattr -cr "$APP_PATH"

echo "🔧 Setting proper permissions..."
chmod -R 755 "$APP_PATH"

echo ""
echo "✅ Fix complete! You can now run CFSS.app"
echo ""
echo "If you still get errors, try:"
echo "1. Right-click CFSS.app → Open"
echo "2. Click 'Open' when prompted about unknown developer"
echo ""
echo "Or run from terminal:"
echo "  open '$APP_PATH'"

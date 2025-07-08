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
    echo "1. Downloaded and extracted CFSS-macOS-4.2.0.tar.gz"
    echo "2. The CFSS.app is in the current directory or Applications folder"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "🛡️  Removing quarantine attributes..."
if xattr -cr "$APP_PATH"; then
    echo "✅ Quarantine attributes removed successfully"
else
    echo "❌ Failed to remove quarantine attributes"
    echo "   You may need to run: sudo xattr -cr \"$APP_PATH\""
    exit 1
fi

echo ""
echo "🔍 Checking current attributes..."
ATTRS=$(xattr -l "$APP_PATH" 2>/dev/null)
if [ -z "$ATTRS" ]; then
    echo "✅ No quarantine attributes found - app should open normally"
else
    echo "⚠️  Some attributes still present:"
    echo "$ATTRS"
fi

echo ""
echo "🚀 Attempting to open CFSS..."
if open "$APP_PATH"; then
    echo "✅ CFSS should now open successfully!"
    echo ""
    echo "💡 If this is the first time opening:"
    echo "   - You may see a security dialog"
    echo "   - Click 'Open' to trust the app"
else
    echo "❌ Failed to open CFSS"
    echo ""
    echo "🆘 Manual steps to try:"
    echo "1. Right-click CFSS.app → Open"
    echo "2. Click 'Open' in the security dialog"
    echo "3. Check System Preferences → Security & Privacy → General"
fi

echo ""
echo "📞 Need help? Check the documentation at:"
echo "   https://github.com/rc91470/cfss/releases"

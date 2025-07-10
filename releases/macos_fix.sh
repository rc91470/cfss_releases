#!/bin/bash

# macOS Fix Script for CFSS v4.2.4
# Removes quarantine attributes that may prevent the app from running

echo "🍎 CFSS macOS Fix Script v4.2.4"
echo "================================"
echo ""
echo "This script fixes common macOS issues with downloaded apps:"
echo "• Removes quarantine attributes"
echo "• Sets proper permissions"
echo "• Allows the app to run normally"
echo ""

# Find CFSS.app
if [ -f "CFSS.app/Contents/MacOS/cfss_app" ]; then
    APP_PATH="CFSS.app"
elif [ -f "./CFSS.app/Contents/MacOS/cfss_app" ]; then
    APP_PATH="./CFSS.app"
else
    echo "❌ CFSS.app not found in current directory"
    echo "   Please run this script from the folder containing CFSS.app"
    exit 1
fi

echo "📱 Found CFSS.app at: $APP_PATH"
echo ""

echo "🔧 Removing quarantine attributes..."
xattr -cr "$APP_PATH"

echo "🔧 Setting executable permissions..."
chmod +x "$APP_PATH/Contents/MacOS/cfss_app"

echo ""
echo "✅ Fix complete!"
echo ""
echo "🚀 You can now run CFSS by:"
echo "   • Double-clicking CFSS.app, or"
echo "   • Right-clicking → Open (if prompted by Gatekeeper)"
echo ""
echo "💡 If you still have issues:"
echo "   • Try right-clicking CFSS.app → Open instead of double-clicking"
echo "   • Check System Preferences → Security & Privacy → General"
echo "   • Look for a message about CFSS and click 'Open Anyway'"

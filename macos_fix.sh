#!/bin/bash

# CFSS v4.2.4 macOS Fix Script
# Fixes "App is damaged" error and permission issues

echo "🔧 CFSS v4.2.4 macOS Fix Script"
echo "================================"
echo ""

# Check if CFSS.app exists in common locations
APP_PATH=""
if [ -d "/Applications/CFSS.app" ]; then
    APP_PATH="/Applications/CFSS.app"
elif [ -d "./CFSS.app" ]; then
    APP_PATH="./CFSS.app"
elif [ -d "~/Applications/CFSS.app" ]; then
    APP_PATH="~/Applications/CFSS.app"
else
    echo "❓ Cannot find CFSS.app automatically."
    echo "Please drag and drop CFSS.app here, then press Enter:"
    read APP_PATH
    
    # Remove quotes if user added them
    APP_PATH=$(echo "$APP_PATH" | sed 's/^"\(.*\)"$/\1/')
fi

if [ ! -d "$APP_PATH" ]; then
    echo "❌ Error: CFSS.app not found at: $APP_PATH"
    echo "Please make sure the app is in your Applications folder or current directory."
    exit 1
fi

echo "📍 Found CFSS.app at: $APP_PATH"
echo ""

echo "🔧 Step 1: Removing quarantine attributes..."
xattr -cr "$APP_PATH"
if [ $? -eq 0 ]; then
    echo "✅ Quarantine attributes removed"
else
    echo "⚠️  Could not remove quarantine attributes (this is usually OK)"
fi

echo ""
echo "🔧 Step 2: Setting proper permissions..."
chmod -R 755 "$APP_PATH"
if [ $? -eq 0 ]; then
    echo "✅ Permissions set correctly"
else
    echo "❌ Failed to set permissions"
    exit 1
fi

echo ""
echo "🔧 Step 3: Clearing extended attributes..."
xattr -d com.apple.metadata:kMDItemWhereFroms "$APP_PATH" 2>/dev/null
xattr -d com.apple.quarantine "$APP_PATH" 2>/dev/null
echo "✅ Extended attributes cleared"

echo ""
echo "🎉 Fix complete! CFSS v4.2.4 should now run without issues."
echo ""
echo "💡 To launch CFSS:"
echo "   • Double-click CFSS.app in Applications"
echo "   • Or run: open '$APP_PATH'"
echo ""
echo "🔒 If you still get security warnings:"
echo "   • Right-click CFSS.app → Open (first time only)"
echo "   • Or go to System Preferences → Security → Allow"
echo ""

# Offer to launch the app
echo "🚀 Would you like to launch CFSS now? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "🚀 Launching CFSS v4.2.4..."
    open "$APP_PATH"
else
    echo "👍 CFSS is ready to use when you need it!"
fi

echo ""
echo "✨ Enjoy using CFSS v4.2.4!"

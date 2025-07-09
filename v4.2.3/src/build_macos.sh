#!/bin/bash

# CFSS macOS Build Script for DEVELOPMENT TESTING ONLY
# 
# ⚠️  WARNING: This is for local development testing only!
# ⚠️  All official builds should be done in the cfss_releases repository
# ⚠️  This development repository should NOT contain .app files
#
# For official releases:
# 1. Use the build scripts in cfss_releases repository
# 2. Never commit .app files to this repository
# 3. Keep development and distribution separate

echo "🚀 Starting CFSS macOS Development Build Process..."
echo "⚠️  WARNING: This is for local testing only - not for distribution!"

# SECURITY: Run security check first
echo "🔒 SECURITY: Running pre-build security check..."
if [ -f "security_check.sh" ]; then
    ./security_check.sh
    if [ $? -eq 1 ]; then
        echo "⚠️  Security check found customer data - proceeding with cleanup..."
    fi
else
    echo "⚠️  security_check.sh not found - proceeding with standard cleanup..."
fi

# SECURITY: Clean data folder to prevent customer data in build
echo "🔒 SECURITY: Cleaning data folder to prevent customer data inclusion..."
if [ -d "data" ]; then
    echo "   Backing up data folder to data_backup_$(date +%Y%m%d_%H%M%S)..."
    cp -r data "data_backup_$(date +%Y%m%d_%H%M%S)"
    echo "   Clearing data folder contents..."
    rm -f data/*.csv
    echo "   ✅ Data folder cleaned - no customer data will be included in build"
else
    echo "   Data folder doesn't exist, creating empty one..."
    mkdir -p data
fi

# Create empty .gitkeep file to preserve folder structure
touch data/.gitkeep

# Activate virtual environment
source venv/bin/activate

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/
rm -rf dist/

# Check Python version
echo "🐍 Python version: $(python --version)"

# Install/update build dependencies
echo "📦 Ensuring build dependencies are installed..."
pip install --upgrade pyinstaller

# Create the app bundle
echo "🔨 Building CFSS.app..."
pyinstaller cfss_app.spec

# Check if build was successful
if [ -d "dist/CFSS.app" ]; then
    echo "✅ Build successful!"
    echo "📁 App location: $(pwd)/dist/CFSS.app"
    
    # Set proper permissions
    echo "🔐 Setting permissions..."
    chmod +x "dist/CFSS.app/Contents/MacOS/cfss_app"
    
    # Remove quarantine attributes to prevent "damaged" warning
    echo "🛡️  Removing quarantine attributes..."
    xattr -cr "dist/CFSS.app"
    
    # Create DMG for distribution (optional)
    echo "💿 Creating DMG for distribution..."
    if command -v create-dmg &> /dev/null; then
        create-dmg \
            --volname "CFSS Installer" \
            --window-pos 200 120 \
            --window-size 600 300 \
            --icon-size 100 \
            --icon "CFSS.app" 175 120 \
            --hide-extension "CFSS.app" \
            --app-drop-link 425 120 \
            "dist/CFSS-macOS-4.2.3.dmg" \
            "dist/"
        echo "✅ DMG created: dist/CFSS-macOS-4.2.3.dmg"
    else
        echo "ℹ️  create-dmg not found. You can install it with: brew install create-dmg"
        echo "ℹ️  For now, you can distribute the CFSS.app directly"
    fi
    
    # Create a tar.gz for easy distribution
    echo "📦 Creating TAR.GZ for distribution..."
    cd dist
    tar -czf "CFSS-macOS-4.2.3.tar.gz" "CFSS.app"
    cd ..
    echo "✅ TAR.GZ created: dist/CFSS-macOS-4.2.3.tar.gz"
    
    # Test the app
    echo "🧪 Testing the built app..."
    echo "Opening CFSS.app... (close it to continue)"
    open "dist/CFSS.app"
    
    echo ""
    echo "🎉 Build Complete!"
    echo "📂 Distribution files:"
    echo "   • dist/CFSS.app (macOS app bundle)"
    echo "   • dist/CFSS-macOS-4.2.2.tar.gz (for distribution)"
    if [ -f "dist/CFSS-macOS-4.2.2.dmg" ]; then
        echo "   • dist/CFSS-macOS-4.2.2.dmg (installer)"
    fi
    echo ""
    echo "💡 To distribute to other Macs:"
    echo "   1. Share the TAR.GZ file or DMG"
    echo "   2. Extract: tar -xzf CFSS-macOS-4.2.2.tar.gz"
    echo "   3. Recipients should drag CFSS.app to Applications"
    echo "   4. If macOS says the app is 'damaged':"
    echo "      - Right-click the app → Show Package Contents"
    echo "      - Or run: xattr -cr /path/to/CFSS.app"
    echo "   5. On first run, they may need to right-click → Open (due to Gatekeeper)"
    
else
    echo "❌ Build failed! Check the output above for errors."
    exit 1
fi

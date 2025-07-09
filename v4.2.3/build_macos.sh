#!/bin/bash

# CFSS macOS Build Script for Release v4.2.3
# This script builds the macOS .app for distribution

VERSION="4.2.3"

echo "🚀 Building CFSS v${VERSION} for macOS Release..."
echo "================================================="

# Check if we're in the right directory
if [ ! -f "src/cfss_app.py" ]; then
    echo "❌ Error: src/cfss_app.py not found. Are you in the right directory?"
    exit 1
fi

# Create build directory
mkdir -p build
cd build

# Copy source files
echo "📋 Copying source files..."
cp -r ../src/* .

# SECURITY: Run security check if available
echo "🔒 SECURITY: Running pre-build security check..."
if [ -f "security_check.sh" ]; then
    ./security_check.sh
    if [ $? -ne 0 ]; then
        echo "❌ Security check failed. Aborting build."
        exit 1
    fi
else
    echo "⚠️  Security check script not found, proceeding..."
fi

# Clean any existing build artifacts
echo "🧹 Cleaning build artifacts..."
rm -rf build dist __pycache__ *.spec.bak
find . -name "*.pyc" -delete
find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Remove any customer data
echo "🔒 Removing customer data..."
rm -rf data/*.csv
rm -rf scan_backups/*
rm -rf issue_reports/*
rm -f circuits.db cfss_app.db cfss_app.log
rm -f sharepoint_config.json csv_hash_cache.json
rm -f CFSS_*.json CFSS_*.txt

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Build the application
echo "🔨 Building application..."
pyinstaller cfss_app.spec

# Check if build was successful
if [ ! -d "dist/CFSS.app" ]; then
    echo "❌ Build failed: CFSS.app not found in dist/"
    exit 1
fi

# Fix macOS permissions and signatures
echo "🔧 Fixing macOS permissions..."
chmod -R 755 dist/CFSS.app
xattr -cr dist/CFSS.app

# Create archive
echo "📦 Creating archive..."
cd dist
tar -czf CFSS-macOS-${VERSION}.tar.gz CFSS.app

# Generate checksums
echo "🔒 Generating checksums..."
shasum -a 256 CFSS-macOS-${VERSION}.tar.gz > checksums.txt

# Copy files to release directory
echo "📋 Copying files to release directories..."
mkdir -p ../../releases/macos/v${VERSION}
cp CFSS-macOS-${VERSION}.tar.gz ../../releases/macos/v${VERSION}/
cp checksums.txt ../../releases/macos/v${VERSION}/

# Update latest
cp CFSS-macOS-${VERSION}.tar.gz ../../releases/macos/latest/
cp checksums.txt ../../releases/macos/latest/

# Create macOS fix script
cat > ../../releases/macos/latest/macos_fix.sh << 'FIX_EOF'
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
FIX_EOF

chmod +x ../../releases/macos/latest/macos_fix.sh
cp ../../releases/macos/latest/macos_fix.sh ../../releases/macos/v${VERSION}/

echo ""
echo "✅ Build complete!"
echo "📁 Files created:"
echo "   - v4.2.3/build/dist/CFSS.app"
echo "   - v4.2.3/build/dist/CFSS-macOS-${VERSION}.tar.gz"
echo "   - releases/macos/v${VERSION}/"
echo "   - releases/macos/latest/ (updated)"
echo ""
echo "🚀 Ready for release!"

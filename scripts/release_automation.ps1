# Release Automation Script

# This script helps you copy files from your private development repo 
# to the public release repository

$ErrorActionPreference = "Stop"

# Configuration
$PRIVATE_REPO = "c:\Users\rc914\RCcode\cfss_app"
$PUBLIC_REPO = "c:\Users\rc914\RCcode\cfss_releases"  # You'll create this
$VERSION = "v4.2.0"  # Update this for each release

Write-Host "CFSS Release Automation Script" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green

# Check if public repo exists
if (-not (Test-Path $PUBLIC_REPO)) {
    Write-Host "Public repository not found at: $PUBLIC_REPO" -ForegroundColor Red
    Write-Host "Please create the public repository first:" -ForegroundColor Yellow
    Write-Host "1. Create new GitHub repository 'cfss_releases' (public)" -ForegroundColor Yellow
    Write-Host "2. Clone it to: $PUBLIC_REPO" -ForegroundColor Yellow
    Write-Host "3. Copy the template files from public_release_files/" -ForegroundColor Yellow
    exit 1
}

# Check if release files exist
$releaseFiles = Get-ChildItem "$PRIVATE_REPO\releases" -Filter "*$VERSION*" -ErrorAction SilentlyContinue
if ($releaseFiles.Count -eq 0) {
    Write-Host "No release files found for version $VERSION" -ForegroundColor Red
    Write-Host "Please build the release first using build_windows.bat" -ForegroundColor Yellow
    exit 1
}

Write-Host "Found $($releaseFiles.Count) release files for $VERSION" -ForegroundColor Green

# Create release directories in public repo
$windowsDir = "$PUBLIC_REPO\releases\windows\$VERSION"
$macosDir = "$PUBLIC_REPO\releases\macos\$VERSION"
$latestWindowsDir = "$PUBLIC_REPO\releases\windows\latest"
$latestMacosDir = "$PUBLIC_REPO\releases\macos\latest"

New-Item -ItemType Directory -Path $windowsDir -Force | Out-Null
New-Item -ItemType Directory -Path $macosDir -Force | Out-Null
New-Item -ItemType Directory -Path $latestWindowsDir -Force | Out-Null
New-Item -ItemType Directory -Path $latestMacosDir -Force | Out-Null

# Copy Windows releases
Write-Host "Copying Windows releases..." -ForegroundColor Yellow
Get-ChildItem "$PRIVATE_REPO\releases" -Filter "*Windows*" | ForEach-Object {
    $dest = "$windowsDir\$($_.Name)"
    Copy-Item $_.FullName $dest -Force
    Write-Host "  Copied: $($_.Name)"
    
    # Also copy to latest
    Copy-Item $_.FullName "$latestWindowsDir\$($_.Name)" -Force
}

# Copy macOS releases (if they exist)
$macosFiles = Get-ChildItem "$PRIVATE_REPO\releases" -Filter "*macOS*" -ErrorAction SilentlyContinue
if ($macosFiles.Count -gt 0) {
    Write-Host "Copying macOS releases..." -ForegroundColor Yellow
    $macosFiles | ForEach-Object {
        $dest = "$macosDir\$($_.Name)"
        Copy-Item $_.FullName $dest -Force
        Write-Host "  Copied: $($_.Name)"
        
        # Also copy to latest
        Copy-Item $_.FullName "$latestMacosDir\$($_.Name)" -Force
    }
}

# Generate checksums
Write-Host "Generating checksums..." -ForegroundColor Yellow
$windowsChecksums = @()
$macosChecksums = @()

Get-ChildItem $windowsDir -File | ForEach-Object {
    $hash = Get-FileHash $_.FullName -Algorithm SHA256
    $windowsChecksums += "$($hash.Hash.ToLower())  $($_.Name)"
}

Get-ChildItem $macosDir -File | ForEach-Object {
    $hash = Get-FileHash $_.FullName -Algorithm SHA256
    $macosChecksums += "$($hash.Hash.ToLower())  $($_.Name)"
}

# Save checksums
$windowsChecksums | Out-File "$windowsDir\checksums.txt" -Encoding UTF8
$macosChecksums | Out-File "$macosDir\checksums.txt" -Encoding UTF8

# Copy to latest directories
$windowsChecksums | Out-File "$latestWindowsDir\checksums.txt" -Encoding UTF8
$macosChecksums | Out-File "$latestMacosDir\checksums.txt" -Encoding UTF8

Write-Host "Checksums generated and saved" -ForegroundColor Green

# Update version in README
Write-Host "Updating version references..." -ForegroundColor Yellow
$readmePath = "$PUBLIC_REPO\README.md"
if (Test-Path $readmePath) {
    $content = Get-Content $readmePath -Raw
    $content = $content -replace 'v\d+\.\d+\.\d+', $VERSION
    $content = $content -replace 'CFSS_v\d+\.\d+\.\d+', "CFSS_$VERSION"
    Set-Content $readmePath $content -Encoding UTF8
    Write-Host "README.md updated with version $VERSION" -ForegroundColor Green
}

Write-Host ""
Write-Host "Release automation complete!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Review the copied files in: $PUBLIC_REPO" -ForegroundColor White
Write-Host "2. Commit and push changes to the public repository" -ForegroundColor White
Write-Host "3. Create a GitHub release with tag $VERSION" -ForegroundColor White
Write-Host "4. Upload the release files to the GitHub release" -ForegroundColor White

# Open the public repo directory
Write-Host ""
Write-Host "Opening public repository directory..." -ForegroundColor Yellow
Start-Process explorer.exe $PUBLIC_REPO

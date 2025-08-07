# CFSS Version Bump Script
# Updates version numbers across all files and creates git tags

param(
    [Parameter(Mandatory=$true)]
    [string]$NewVersion,
    
    [Parameter(Mandatory=$false)]
    [string]$ReleaseMessage = "Release v$NewVersion"
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 CFSS Version Bump Script" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green
Write-Host ""

# Validate version format
if (-not ($NewVersion -match '^\d+\.\d+\.\d+$')) {
    Write-Host "❌ Error: Version must be in format X.Y.Z (e.g., 4.2.5)" -ForegroundColor Red
    exit 1
}

$OldVersion = Get-Content "VERSION" -ErrorAction SilentlyContinue
Write-Host "📋 Current Version: v$OldVersion"
Write-Host "📋 New Version: v$NewVersion"
Write-Host ""

# Update VERSION file
Write-Host "🔧 Updating VERSION file..." -ForegroundColor Yellow
$NewVersion | Out-File -FilePath "VERSION" -Encoding utf8 -NoNewline

# Update README.md badge
Write-Host "🔧 Updating README.md version badge..." -ForegroundColor Yellow
$readmeContent = Get-Content "README.md" -Raw
$readmeContent = $readmeContent -replace "CFSS-v\d+\.\d+\.\d+", "CFSS-v$NewVersion"
$readmeContent = $readmeContent -replace "Latest Release \(v\d+\.\d+\.\d+\)", "Latest Release (v$NewVersion)"
$readmeContent = $readmeContent -replace "macOS v\d+\.\d+\.\d+", "macOS v$NewVersion"
$readmeContent = $readmeContent -replace "Windows v\d+\.\d+\.\d+", "Windows v$NewVersion"
$readmeContent | Out-File -FilePath "README.md" -Encoding utf8

# Update RELEASE_MANAGEMENT.md
Write-Host "🔧 Updating RELEASE_MANAGEMENT.md..." -ForegroundColor Yellow
$releaseContent = Get-Content "RELEASE_MANAGEMENT.md" -Raw
$releaseContent = $releaseContent -replace "Current Version: v\d+\.\d+\.\d+", "Current Version: v$NewVersion"
$todayDate = Get-Date -Format "MMMM d, yyyy"
$releaseContent = $releaseContent -replace "Last Updated: .+", "Last Updated: $todayDate"
$releaseContent | Out-File -FilePath "RELEASE_MANAGEMENT.md" -Encoding utf8

Write-Host ""
Write-Host "✅ Version files updated!" -ForegroundColor Green
Write-Host ""

# Git operations
Write-Host "📦 Git operations:" -ForegroundColor Cyan

Write-Host "  • Adding changed files..." -ForegroundColor Yellow
git add VERSION README.md RELEASE_MANAGEMENT.md

Write-Host "  • Creating commit..." -ForegroundColor Yellow
git commit -m "Bump version to v$NewVersion - $ReleaseMessage"

Write-Host "  • Creating git tag..." -ForegroundColor Yellow
git tag -a "v$NewVersion" -m "$ReleaseMessage"

Write-Host "  • Pushing to GitHub..." -ForegroundColor Yellow
git push origin main
git push origin "v$NewVersion"

Write-Host ""
Write-Host "🎉 Version bump complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "  1. Build both platform versions" -ForegroundColor White
Write-Host "  2. Test downloads and installation" -ForegroundColor White
Write-Host "  3. Update release status in RELEASE_MANAGEMENT.md" -ForegroundColor White
Write-Host ""
Write-Host "🔗 GitHub Release: https://github.com/rc91470/cfss_releases/releases/tag/v$NewVersion" -ForegroundColor Blue

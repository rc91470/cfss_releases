# Windows v4.2.3 Build Required

## Status: WINDOWS BUILD NEEDED

The macOS v4.2.3 build is complete and available. The Windows build needs to be created from the same v4.2.3 source code to maintain version synchronization.

## Source Code Location
- **Source**: `/v4.2.3/src/` (contains the exact v4.2.3 source code)
- **Build Script**: `/v4.2.3/build_windows.bat`
- **Target**: `CFSS_v4.2.3_Windows.zip`

## Windows Build Requirements
1. Use the source code from `/v4.2.3/src/`
2. Run the Windows build script: `build_windows.bat`
3. Generate: `CFSS_v4.2.3_Windows.zip`
4. Create checksums.txt
5. Update `releases/windows/latest/` with the new build

## Version Synchronization
- ✅ macOS v4.2.3: Built and available
- ❌ Windows v4.2.3: **NEEDS TO BE BUILT**

Both builds must use the same source code to ensure feature parity and version consistency.

## After Windows Build
1. Update README.md to show both platforms available
2. Create GitHub release with both files
3. Update version history table
4. Test both platforms work correctly

**DO NOT** update version numbers until both platforms are ready for release.

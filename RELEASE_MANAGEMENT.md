# CFSS Release Version Management

## Current Version: v4.2.4

### Release Status:
- ✅ **macOS v4.2.4**: Complete and available
- ✅ **Windows v4.2.4**: Complete and available  
- ✅ **Documentation**: Updated with fixed download links
- ✅ **GitHub Releases**: Tagged and synced

### Last Updated: August 7, 2025

---

## Version Management Workflow

### For New Releases:
1. **Update VERSION file** with new version number
2. **Build and test** both platforms
3. **Update README.md** with new version references
4. **Commit changes** with descriptive message
5. **Create and push git tag**: `git tag -a v4.2.X -m "Release message"`
6. **Push tag to GitHub**: `git push origin v4.2.X`
7. **Update this file** with release status

### Tag Naming Convention:
- Use semantic versioning: `v4.2.X`
- Include descriptive release messages
- Tag the commit with all final changes

### GitHub Releases:
- Tags automatically create GitHub releases
- Files can be attached to releases for reliable downloads
- Release URLs: `https://github.com/rc91470/cfss_releases/releases/download/vX.X.X/filename`

---

## Next Release Preparation (v4.2.5)

### Checklist:
- [ ] Update VERSION file to `4.2.5`
- [ ] Update README badges and version references
- [ ] Build both platform versions
- [ ] Test download links
- [ ] Update documentation
- [ ] Create and push git tag
- [ ] Verify GitHub release creation

---

## Release History:

### v4.2.4 (August 7, 2025)
- ✅ Fixed download link 404 issues
- ✅ Updated to use GitHub Releases URLs
- ✅ Added alternative download options
- ✅ Both platforms complete and available
- ✅ Synchronized version tagging

### v4.2.3 (July 9, 2025)
- ✅ SharePoint integration improvements
- ✅ High-DPI dialog fixes
- ✅ Cross-platform feature parity

### v4.2.2 (July 5, 2025)
- ✅ Enhanced auto-updater
- ✅ Improved error handling

### v4.2.1 (June 28, 2025)
- ✅ Issue tracking system
- ❌ macOS build incomplete

### v4.2.0 (June 15, 2025)
- ✅ Major release with core features
- ✅ Both platforms complete

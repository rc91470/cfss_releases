"""
Safe auto-updater test - shows dialog without downloading
"""
import tkinter as tk
import customtkinter as ctk
from auto_updater import UpdateDialog, AutoUpdater

def test_update_dialog():
    """Test the update dialog with mock data"""
    root = ctk.CTk()
    root.title("CFSS - Update Test")
    root.geometry("600x400")
    
    # Mock update info (like what would come from GitHub API)
    mock_update_info = {
        'version': 'v4.2.1',
        'name': 'CFSS v4.2.1 - Bug Fix Release',
        'body': '''# 🔧 CFSS v4.2.1 - Bug Fix Release

## 🐛 Critical Bug Fixes

### Window Focus Issues Fixed
- Issue Summary and Notes dialogs now properly take focus and stay in front
- No more hidden windows behind the main application
- Dialogs are now properly centered and modal

### Input Validation Improvements
- Input fields are now disabled when no circuit data is loaded
- Prevents confusion when trying to scan without data
- Clear feedback shows "Load circuit data to begin scanning"

### Data Sync Improvements
- Input fields are automatically cleared after SharePoint sync
- No more leftover data from previous sessions
- Clean slate after loading new circuit data

## ✨ New Feature: Auto-Updater

### Automatic Update Checking
- Checks for updates on startup (background, non-intrusive)
- Smart version comparison - only notifies when newer versions available
- Platform-aware - automatically detects Windows vs macOS

### One-Click Updates
- Download and install with progress tracking
- Automatic backup creation before updating
- Auto-restart after successful update
- Safe rollback if update fails''',
        'download_url': 'https://github.com/rc91470/cfss_releases/releases/download/v4.2.0/CFSS_v4.2.0_Windows.zip'
    }
    
    # Create mock updater
    updater = AutoUpdater("v4.1.0", "rc91470", "cfss_releases")
    
    def show_mock_dialog():
        """Show the update dialog with mock data"""
        dialog = UpdateDialog(root, mock_update_info, updater)
        dialog.show()
    
    def check_real_updates():
        """Check for real updates from GitHub"""
        real_updater = AutoUpdater("v4.1.0", "rc91470", "cfss_releases")  # Pretend we're v4.1.0
        update_info = real_updater.check_for_updates()
        
        if update_info:
            print("Real update found!")
            print(f"Version: {update_info['version']}")
            print(f"Download URL: {update_info.get('download_url', 'None')}")
            
            # Show real dialog but don't actually download
            class SafeUpdater(AutoUpdater):
                def download_update(self, download_url, progress_callback=None):
                    print(f"Would download from: {download_url}")
                    return None  # Prevent actual download
                
                def install_update(self, update_file):
                    print("Would install update (but didn't actually download)")
                    return False
            
            safe_updater = SafeUpdater("v4.1.0", "rc91470", "cfss_releases")
            dialog = UpdateDialog(root, update_info, safe_updater)
            dialog.show()
        else:
            tk.messagebox.showinfo("No Updates", "No updates available")
    
    # Instructions
    instructions = ctk.CTkLabel(
        root, 
        text="Auto-Updater Test Options:\n\n"
             "1. Mock Dialog - Shows update dialog with fake data\n"
             "2. Real Check - Checks GitHub but won't actually download\n\n"
             "This is safe - no files will be modified",
        font=("Helvetica", 12),
        justify="left"
    )
    instructions.pack(pady=20)
    
    # Test buttons
    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=20)
    
    ctk.CTkButton(
        button_frame, 
        text="Show Mock Update Dialog", 
        command=show_mock_dialog,
        width=200
    ).pack(pady=5)
    
    ctk.CTkButton(
        button_frame, 
        text="Check Real Updates (Safe)", 
        command=check_real_updates,
        width=200
    ).pack(pady=5)
    
    ctk.CTkButton(
        button_frame, 
        text="Close Test", 
        command=root.quit,
        width=200,
        fg_color="#666666"
    ).pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    test_update_dialog()

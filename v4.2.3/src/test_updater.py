"""
Test script for the auto-updater functionality
"""
import tkinter as tk
import customtkinter as ctk
from auto_updater import AutoUpdater, UpdateDialog

def test_auto_updater():
    # Create a test window
    root = ctk.CTk()
    root.title("Auto-Updater Test")
    root.geometry("400x200")
    
    def test_update_check():
        """Test checking for updates"""
        updater = AutoUpdater("v4.1.0", "rc91470", "cfss_releases")
        update_info = updater.check_for_updates()
        
        if update_info:
            print("Update available:")
            print(f"Version: {update_info['version']}")
            print(f"Download URL: {update_info.get('download_url', 'None')}")
            
            # Show update dialog
            dialog = UpdateDialog(root, update_info, updater)
            dialog.show()
        else:
            print("No updates available")
    
    def test_version_comparison():
        """Test version comparison logic"""
        updater = AutoUpdater("v4.1.0", "rc91470", "cfss_releases")
        
        test_cases = [
            ("v4.2.0", "v4.1.0", True),   # Should be newer
            ("v4.1.0", "v4.1.0", False),  # Should be same
            ("v4.0.0", "v4.1.0", False),  # Should be older
            ("v4.1.1", "v4.1.0", True),   # Should be newer (patch)
        ]
        
        for latest, current, expected in test_cases:
            result = updater._is_newer_version(latest, current)
            status = "✅" if result == expected else "❌"
            print(f"{status} {latest} > {current}: {result} (expected {expected})")
    
    # Create test buttons
    ctk.CTkLabel(root, text="Auto-Updater Test", font=("Helvetica", 16, "bold")).pack(pady=20)
    
    ctk.CTkButton(root, text="Test Update Check", command=test_update_check).pack(pady=10)
    ctk.CTkButton(root, text="Test Version Comparison", command=test_version_comparison).pack(pady=10)
    ctk.CTkButton(root, text="Close", command=root.quit).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    test_auto_updater()

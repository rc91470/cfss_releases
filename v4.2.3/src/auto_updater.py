"""
Auto-updater module for CFSS
Handles checking for updates and downloading/installing them
"""
import requests
import json
import os
import sys
import tempfile
import shutil
import zipfile
import tarfile
import platform
import subprocess
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import threading

class AutoUpdater:
    def __init__(self, current_version: str, repo_owner: str, repo_name: str):
        self.current_version = current_version
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        self.is_windows = platform.system() == "Windows"
        self.is_macos = platform.system() == "Darwin"
        
    def check_for_updates(self) -> Optional[Dict[str, Any]]:
        """Check if a new version is available"""
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            
            release_data = response.json()
            latest_version = release_data['tag_name']
            
            # Compare versions (simple string comparison for now)
            if self._is_newer_version(latest_version, self.current_version):
                return {
                    'version': latest_version,
                    'name': release_data['name'],
                    'body': release_data['body'],
                    'assets': release_data['assets'],
                    'download_url': self._get_download_url(release_data['assets'])
                }
            return None
            
        except Exception as e:
            logging.error(f"Failed to check for updates: {e}")
            return None
    
    def _is_newer_version(self, latest: str, current: str) -> bool:
        """Simple version comparison"""
        # Remove 'v' prefix if present
        latest = latest.lstrip('v')
        current = current.lstrip('v')
        
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]
            
            # Pad with zeros to make same length
            max_len = max(len(latest_parts), len(current_parts))
            latest_parts.extend([0] * (max_len - len(latest_parts)))
            current_parts.extend([0] * (max_len - len(current_parts)))
            
            return latest_parts > current_parts
        except ValueError:
            # Fallback to string comparison
            return latest > current
    
    def _get_download_url(self, assets: list) -> Optional[str]:
        """Get the appropriate download URL for current platform"""
        for asset in assets:
            if self.is_windows and 'Windows' in asset['name']:
                return asset['browser_download_url']
            elif self.is_macos and 'macOS' in asset['name']:
                return asset['browser_download_url']
        return None
    
    def download_update(self, download_url: str, progress_callback=None) -> Optional[str]:
        """Download the update file"""
        try:
            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Get filename from URL
            filename = download_url.split('/')[-1]
            temp_dir = tempfile.mkdtemp()
            temp_file = os.path.join(temp_dir, filename)
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(progress)
            
            return temp_file
            
        except Exception as e:
            logging.error(f"Failed to download update: {e}")
            return None
    
    def install_update(self, update_file: str) -> bool:
        """Install the downloaded update"""
        try:
            if self.is_windows:
                return self._install_windows_update(update_file)
            elif self.is_macos:
                return self._install_macos_update(update_file)
            return False
            
        except Exception as e:
            logging.error(f"Failed to install update: {e}")
            return False
    
    def _install_windows_update(self, update_file: str) -> bool:
        """Install Windows update"""
        try:
            # Extract the zip file
            app_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
            
            with zipfile.ZipFile(update_file, 'r') as zip_ref:
                # Create backup
                backup_dir = os.path.join(app_dir, 'backup_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
                os.makedirs(backup_dir, exist_ok=True)
                
                # Determine current executable path
                if getattr(sys, 'frozen', False):
                    current_exe = sys.executable
                else:
                    # For development mode, look for any CFSS*.exe in the app directory
                    exe_files = [f for f in os.listdir(app_dir) if f.startswith('CFSS') and f.endswith('.exe')]
                    if exe_files:
                        current_exe = os.path.join(app_dir, exe_files[0])
                    else:
                        current_exe = os.path.join(app_dir, 'CFSS.exe')  # Fallback
                    
                # Backup current executable if it exists
                if os.path.exists(current_exe):
                    shutil.copy2(current_exe, backup_dir)
                
                # Extract new files
                zip_ref.extractall(app_dir)
            
            # Create update script that will restart the app
            update_script = os.path.join(app_dir, 'update_restart.bat')
            with open(update_script, 'w') as f:
                f.write('@echo off\n')
                f.write('timeout /t 3 /nobreak > nul\n')  # Increased wait time
                f.write(f'start "" "{current_exe}"\n')
                f.write(f'del "{update_script}"\n')
            
            # Run the update script and exit
            subprocess.Popen([update_script], shell=True)
            return True
            
        except Exception as e:
            logging.error(f"Failed to install Windows update: {e}")
            return False
    
    def _install_macos_update(self, update_file: str) -> bool:
        """Install macOS update"""
        try:
            # Extract the tar.gz file
            app_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
            
            # Determine current app path
            current_app = os.path.join(app_dir, 'CFSS.app')
            
            with tarfile.open(update_file, 'r:gz') as tar_ref:
                # Create backup
                backup_dir = os.path.join(app_dir, 'backup_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
                os.makedirs(backup_dir, exist_ok=True)
                
                # Backup current app bundle
                if os.path.exists(current_app):
                    shutil.copytree(current_app, os.path.join(backup_dir, 'CFSS.app'))
                
                # Extract new files
                tar_ref.extractall(app_dir)
            
            # Create update script that will restart the app
            update_script = os.path.join(app_dir, 'update_restart.sh')
            with open(update_script, 'w') as f:
                f.write('#!/bin/bash\n')
                f.write('sleep 3\n')  # Increased wait time
                f.write(f'open "{current_app}"\n')
                f.write(f'rm "{update_script}"\n')
            
            os.chmod(update_script, 0o755)
            
            # Run the update script and exit
            subprocess.Popen(['/bin/bash', update_script])
            return True
            
        except Exception as e:
            logging.error(f"Failed to install macOS update: {e}")
            return False


class UpdateDialog:
    def __init__(self, parent, update_info: Dict[str, Any], updater: AutoUpdater):
        self.parent = parent
        self.update_info = update_info
        self.updater = updater
        self.dialog = None
        self.progress_bar = None
        self.status_label = None
        
    def show(self):
        """Show the update dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Update Available")
        self.dialog.geometry("500x400")
        self.dialog.configure(bg='#1c2526')
        self.dialog.resizable(False, False)
        
        # Make dialog modal and bring to front
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.dialog.focus_force()
        self.dialog.lift()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"500x400+{x}+{y}")
        
        # Title
        title_label = ctk.CTkLabel(
            self.dialog,
            text=f"Update Available: {self.update_info['version']}",
            font=("Helvetica", 16, "bold"),
            text_color='#00d4ff'
        )
        title_label.pack(pady=(20, 10))
        
        # Release notes
        notes_frame = ctk.CTkFrame(self.dialog, fg_color='#2f3b3c')
        notes_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        notes_text = tk.Text(
            notes_frame,
            wrap=tk.WORD,
            bg='#2f3b3c',
            fg='#b0b8b8',
            font=("Helvetica", 10),
            height=12
        )
        scrollbar = tk.Scrollbar(notes_frame, command=notes_text.yview)
        notes_text.configure(yscrollcommand=scrollbar.set)
        
        notes_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert release notes
        notes_text.insert(tk.END, self.update_info['body'])
        notes_text.configure(state=tk.DISABLED)
        
        # Progress bar (initially hidden)
        self.progress_bar = ctk.CTkProgressBar(self.dialog, width=400)
        self.progress_bar.pack(pady=10, padx=20, fill='x')
        self.progress_bar.pack_forget()  # Hide initially
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.dialog,
            text="",
            font=("Helvetica", 10),
            text_color='#b0b8b8'
        )
        self.status_label.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog, fg_color='transparent')
        button_frame.pack(pady=20)
        
        update_btn = ctk.CTkButton(
            button_frame,
            text="Update Now",
            command=self.start_update,
            fg_color='#00cc66',
            text_color='white',
            font=("Helvetica", 12, "bold")
        )
        update_btn.pack(side='left', padx=5)
        
        later_btn = ctk.CTkButton(
            button_frame,
            text="Later",
            command=self.dialog.destroy,
            fg_color='#666666',
            text_color='white',
            font=("Helvetica", 12)
        )
        later_btn.pack(side='left', padx=5)
        
        skip_btn = ctk.CTkButton(
            button_frame,
            text="Skip This Version",
            command=self.skip_version,
            fg_color='#cc6600',
            text_color='white',
            font=("Helvetica", 12)
        )
        skip_btn.pack(side='left', padx=5)
    
    def start_update(self):
        """Start the update process"""
        if not self.update_info.get('download_url'):
            messagebox.showerror("Error", "No download URL available for your platform")
            return
        
        # Show progress bar
        self.progress_bar.pack(pady=10, padx=20, fill='x')
        self.status_label.configure(text="Downloading update...")
        
        # Disable buttons
        for child in self.dialog.winfo_children():
            if isinstance(child, ctk.CTkButton):
                child.configure(state='disabled')
        
        # Start download in thread
        thread = threading.Thread(target=self.download_and_install)
        thread.daemon = True
        thread.start()
    
    def download_and_install(self):
        """Download and install the update"""
        try:
            # Download
            def progress_callback(progress):
                self.progress_bar.set(progress / 100)
                self.status_label.configure(text=f"Downloading... {progress:.1f}%")
            
            update_file = self.updater.download_update(
                self.update_info['download_url'],
                progress_callback
            )
            
            if not update_file:
                messagebox.showerror("Error", "Failed to download update")
                return
            
            # Install
            self.status_label.configure(text="Installing update...")
            self.progress_bar.set(1.0)
            
            if self.updater.install_update(update_file):
                messagebox.showinfo("Success", "Update installed successfully. The application will restart.")
                self.dialog.destroy()  # Close the update dialog
                self.parent.quit()  # Exit the application
            else:
                messagebox.showerror("Error", "Failed to install update")
                self.dialog.destroy()  # Close dialog on failure too
                
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}")
            self.dialog.destroy()  # Close dialog on exception
        finally:
            # Clean up
            if 'update_file' in locals() and update_file:
                try:
                    os.remove(update_file)
                except:
                    pass
    
    def skip_version(self):
        """Skip this version"""
        # You could save the skipped version to a config file here
        self.dialog.destroy()


def check_for_updates_on_startup(parent, current_version: str, repo_owner: str, repo_name: str):
    """Check for updates when the application starts"""
    def check_updates():
        updater = AutoUpdater(current_version, repo_owner, repo_name)
        update_info = updater.check_for_updates()
        
        if update_info:
            # Show update dialog on main thread
            parent.after(0, lambda: UpdateDialog(parent, update_info, updater).show())
    
    # Check for updates in background thread
    thread = threading.Thread(target=check_updates)
    thread.daemon = True
    thread.start()

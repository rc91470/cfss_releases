"""
Enhanced Auto-updater module for CFSS
Handles checking for updates and downloading/installing them with proper validation
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
from typing import Optional, Dict, Any, List
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
        
        # Critical folders that must exist for proper operation
        self.critical_folders = ['sounds', 'data']
        self.critical_files = {
            'sounds': ['match.mp3', 'nonmatch.mp3', 'complete.mp3'],
            'data': ['README.txt']
        }
        
    def validate_installation(self) -> Dict[str, List[str]]:
        """Validate that all critical files and folders exist"""
        missing = {'folders': [], 'files': []}
        app_dir = self._get_app_dir()
        
        for folder in self.critical_folders:
            folder_path = os.path.join(app_dir, folder)
            if not os.path.exists(folder_path):
                missing['folders'].append(folder)
                logging.warning(f"Missing critical folder: {folder}")
            else:
                # Check critical files in this folder
                if folder in self.critical_files:
                    for file in self.critical_files[folder]:
                        file_path = os.path.join(folder_path, file)
                        if not os.path.exists(file_path):
                            missing['files'].append(f"{folder}/{file}")
                            logging.warning(f"Missing critical file: {folder}/{file}")
        
        return missing
    
    def _get_app_dir(self) -> str:
        """Get the application directory"""
        return os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    
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
        """Compare version strings to see if latest is newer than current"""
        # Remove 'v' prefix if present
        latest = latest.lstrip('v')
        current = current.lstrip('v')
        
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]
            
            # Pad shorter version with zeros
            max_len = max(len(latest_parts), len(current_parts))
            latest_parts += [0] * (max_len - len(latest_parts))
            current_parts += [0] * (max_len - len(current_parts))
            
            return latest_parts > current_parts
        except ValueError:
            # Fallback to string comparison if parsing fails
            return latest > current
    
    def _get_download_url(self, assets: List[Dict[str, Any]]) -> Optional[str]:
        """Get the appropriate download URL for the current platform"""
        if self.is_windows:
            for asset in assets:
                if 'Windows' in asset['name'] and asset['name'].endswith('.zip'):
                    return asset['browser_download_url']
        elif self.is_macos:
            for asset in assets:
                if 'macOS' in asset['name'] and asset['name'].endswith('.tar.gz'):
                    return asset['browser_download_url']
        return None
    
    def download_update(self, url: str, progress_callback=None) -> Optional[str]:
        """Download the update file"""
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip' if self.is_windows else '.tar.gz') as temp_file:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        temp_file.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(progress)
            
            return temp_file.name
            
        except Exception as e:
            logging.error(f"Failed to download update: {e}")
            return None
    
    def install_update(self, update_file: str) -> bool:
        """Install the downloaded update with proper validation"""
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
        """Install Windows update with proper validation"""
        try:
            app_dir = self._get_app_dir()
            
            with zipfile.ZipFile(update_file, 'r') as zip_ref:
                # Create backup
                backup_dir = os.path.join(app_dir, 'backup_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
                os.makedirs(backup_dir, exist_ok=True)
                
                # Get current executable path
                current_exe = self._get_current_exe()
                
                # Backup current executable and critical folders
                if os.path.exists(current_exe):
                    shutil.copy2(current_exe, backup_dir)
                
                for folder in self.critical_folders:
                    folder_path = os.path.join(app_dir, folder)
                    if os.path.exists(folder_path):
                        shutil.copytree(folder_path, os.path.join(backup_dir, folder))
                
                # Extract new files - handle nested directory structure
                self._extract_update_files(zip_ref, app_dir)
                
                # Validate installation after extraction
                missing = self.validate_installation()
                if missing['folders'] or missing['files']:
                    logging.warning(f"Missing components after update: {missing}")
                    # Restore missing critical folders from backup or update archive
                    self._restore_missing_components(zip_ref, app_dir, missing)
            
            # Final validation
            missing = self.validate_installation()
            if missing['folders'] or missing['files']:
                logging.error(f"Critical components still missing after restoration: {missing}")
                messagebox.showerror("Update Warning", 
                    f"Update completed but some components are missing:\n"
                    f"Folders: {', '.join(missing['folders'])}\n"
                    f"Files: {', '.join(missing['files'])}\n\n"
                    f"The application may not work correctly. Please reinstall from the complete ZIP package.")
            
            # Create update script that will restart the app
            self._create_restart_script(current_exe)
            return True
            
        except Exception as e:
            logging.error(f"Failed to install Windows update: {e}")
            return False
    
    def _get_current_exe(self) -> str:
        """Get the path to the current executable"""
        if getattr(sys, 'frozen', False):
            return sys.executable
        else:
            # For development mode, look for any CFSS*.exe in the app directory
            app_dir = self._get_app_dir()
            exe_files = [f for f in os.listdir(app_dir) if f.startswith('CFSS') and f.endswith('.exe')]
            if exe_files:
                return os.path.join(app_dir, exe_files[0])
            else:
                return os.path.join(app_dir, 'CFSS.exe')  # Fallback
    
    def _extract_update_files(self, zip_ref: zipfile.ZipFile, app_dir: str):
        """Extract update files, handling nested directory structure"""
        # Get the list of files in the ZIP
        file_list = zip_ref.namelist()
        
        # Check if files are nested in a directory
        if file_list and '/' in file_list[0]:
            # Find the root directory name
            root_dir = file_list[0].split('/')[0]
            
            # Extract and move files to proper location
            temp_extract_dir = os.path.join(app_dir, 'temp_update_extract')
            zip_ref.extractall(temp_extract_dir)
            
            nested_dir = os.path.join(temp_extract_dir, root_dir)
            if os.path.exists(nested_dir):
                # Move files from nested directory to app directory
                for item in os.listdir(nested_dir):
                    src_path = os.path.join(nested_dir, item)
                    dst_path = os.path.join(app_dir, item)
                    
                    if os.path.isdir(src_path):
                        if os.path.exists(dst_path):
                            shutil.rmtree(dst_path)
                        shutil.move(src_path, dst_path)
                    else:
                        if os.path.exists(dst_path):
                            os.remove(dst_path)
                        shutil.move(src_path, dst_path)
            
            # Clean up temporary extraction directory
            shutil.rmtree(temp_extract_dir)
        else:
            # Direct extraction if not nested
            zip_ref.extractall(app_dir)
    
    def _restore_missing_components(self, zip_ref: zipfile.ZipFile, app_dir: str, missing: Dict[str, List[str]]):
        """Restore missing critical components from the update archive"""
        try:
            # Create a temporary extraction to get missing components
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_ref.extractall(temp_dir)
                
                # Find the actual content directory (handle nested structure)
                content_dir = temp_dir
                if os.path.exists(os.path.join(temp_dir, 'CFSS_')):
                    # Find the nested directory
                    for item in os.listdir(temp_dir):
                        if item.startswith('CFSS_') and os.path.isdir(os.path.join(temp_dir, item)):
                            content_dir = os.path.join(temp_dir, item)
                            break
                
                # Restore missing folders
                for folder in missing['folders']:
                    src_folder = os.path.join(content_dir, folder)
                    dst_folder = os.path.join(app_dir, folder)
                    
                    if os.path.exists(src_folder):
                        if os.path.exists(dst_folder):
                            shutil.rmtree(dst_folder)
                        shutil.copytree(src_folder, dst_folder)
                        logging.info(f"Restored missing folder: {folder}")
                    else:
                        logging.error(f"Could not find {folder} in update archive")
                
                # Restore missing files
                for file_path in missing['files']:
                    src_file = os.path.join(content_dir, file_path)
                    dst_file = os.path.join(app_dir, file_path)
                    
                    if os.path.exists(src_file):
                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                        shutil.copy2(src_file, dst_file)
                        logging.info(f"Restored missing file: {file_path}")
                    else:
                        logging.error(f"Could not find {file_path} in update archive")
        
        except Exception as e:
            logging.error(f"Failed to restore missing components: {e}")
    
    def _create_restart_script(self, current_exe: str):
        """Create script to restart the application"""
        app_dir = self._get_app_dir()
        update_script = os.path.join(app_dir, 'update_restart.bat')
        
        with open(update_script, 'w') as f:
            f.write('@echo off\n')
            f.write('timeout /t 3 /nobreak > nul\n')
            f.write(f'start "" "{current_exe}"\n')
            f.write(f'del "{update_script}"\n')
        
        # Run the update script and exit
        subprocess.Popen([update_script], shell=True)
    
    def _install_macos_update(self, update_file: str) -> bool:
        """Install macOS update - similar validation logic as Windows"""
        try:
            app_dir = self._get_app_dir()
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
                
                # Validate installation
                missing = self.validate_installation()
                if missing['folders'] or missing['files']:
                    logging.warning(f"Missing components after macOS update: {missing}")
            
            # Create update script that will restart the app
            update_script = os.path.join(app_dir, 'update_restart.sh')
            with open(update_script, 'w') as f:
                f.write('#!/bin/bash\n')
                f.write('sleep 3\n')
                f.write(f'open "{current_app}"\n')
                f.write(f'rm "{update_script}"\n')
            
            os.chmod(update_script, 0o755)
            subprocess.Popen(['/bin/bash', update_script])
            return True
            
        except Exception as e:
            logging.error(f"Failed to install macOS update: {e}")
            return False


# UpdateDialog and other classes remain the same as in the original file...
class UpdateDialog:
    def __init__(self, parent, update_info: Dict[str, Any], updater: AutoUpdater):
        self.parent = parent
        self.update_info = update_info
        self.updater = updater
        self.dialog = None
        self.progress_bar = None
        self.status_label = None
        
    def show(self):
        """Show the update dialog with validation warning if needed"""
        # First validate current installation
        missing = self.updater.validate_installation()
        
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Update Available")
        self.dialog.geometry("500x450")  # Slightly taller for validation warning
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
        y = (self.dialog.winfo_screenheight() // 2) - (450 // 2)
        self.dialog.geometry(f"500x450+{x}+{y}")
        
        # Show validation warning if components are missing
        if missing['folders'] or missing['files']:
            warning_frame = ctk.CTkFrame(self.dialog, fg_color='#ff4444')
            warning_frame.pack(fill='x', padx=20, pady=(10, 5))
            
            warning_label = ctk.CTkLabel(
                warning_frame,
                text="⚠️ Missing Components Detected",
                font=("Helvetica", 12, "bold"),
                text_color='white'
            )
            warning_label.pack(pady=5)
            
            details = f"Missing: {', '.join(missing['folders'] + missing['files'])}"
            details_label = ctk.CTkLabel(
                warning_frame,
                text=details,
                font=("Helvetica", 9),
                text_color='white'
            )
            details_label.pack(pady=(0, 5))
        
        # Title
        title_label = ctk.CTkLabel(
            self.dialog,
            text=f"Update Available: {self.update_info['version']}",
            font=("Helvetica", 16, "bold"),
            text_color='#00d4ff'
        )
        title_label.pack(pady=(10, 10))
        
        # Release notes and buttons remain the same...
        # (Include the rest of the UpdateDialog implementation from the original file)

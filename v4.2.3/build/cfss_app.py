import tkinter as tk
from tkinter import messagebox, filedialog
import os
import sys
import logging
from datetime import datetime
import re
import gc
import shutil
import pygame
import customtkinter as ctk
from difflib import SequenceMatcher
import json
import glob
import socket
import getpass
import subprocess
import platform

# Import new manager classes
from data_manager import DataManager
from circuit_manager import CircuitManager
from scan_controller import ScanController

# Import auto-updater
try:
    from auto_updater import check_for_updates_on_startup
    AUTO_UPDATER_AVAILABLE = True
except ImportError:
    AUTO_UPDATER_AVAILABLE = False
    logging.warning("Auto-updater not available - missing dependencies")

# Application version
APP_VERSION = "v4.2.3"  # Increment for next version

pygame.mixer.init()

# High DPI scaling support
def setup_dpi_scaling():
    """Setup DPI scaling for high-resolution displays"""
    try:
        # Enable DPI awareness on Windows
        if platform.system() == "Windows":
            try:
                from ctypes import windll
                windll.shcore.SetProcessDpiAwareness(1)
            except:
                pass
        
        # For macOS, Tkinter usually handles scaling automatically
        # but we'll increase base sizes for better visibility
        
        # Create a temporary root to get DPI info
        temp_root = tk.Tk()
        temp_root.withdraw()
        
        # Get screen DPI
        dpi = temp_root.winfo_fpixels('1i')
        screen_width = temp_root.winfo_screenwidth()
        screen_height = temp_root.winfo_screenheight()
        
        temp_root.destroy()
        
        # Calculate scale factor (96 DPI is standard)
        scale_factor = max(1.0, dpi / 96.0)
        
        # For very high resolution displays, increase scaling
        if screen_width >= 3000 or screen_height >= 2000:
            scale_factor = max(scale_factor, 1.5)
        
        return scale_factor
    except Exception as e:
        logging.error(f"Failed to setup DPI scaling: {e}")
        return 1.0

# Get DPI scale factor
DPI_SCALE = setup_dpi_scaling()

# Scaled font sizes for high-resolution displays
def get_scaled_font_size(base_size):
    """Get scaled font size based on DPI"""
    return int(base_size * DPI_SCALE)

# Scaled dimensions for high-resolution displays
def get_scaled_size(base_size):
    """Get scaled dimensions based on DPI"""
    return int(base_size * DPI_SCALE)

# Font definitions for high-resolution displays
DIALOG_FONT_LARGE = ("Helvetica", get_scaled_font_size(16), "bold")
DIALOG_FONT_MEDIUM = ("Helvetica", get_scaled_font_size(12))
DIALOG_FONT_SMALL = ("Helvetica", get_scaled_font_size(10))
DIALOG_FONT_COURIER = ("Courier", get_scaled_font_size(12))
DIALOG_FONT_COURIER_LARGE = ("Courier", get_scaled_font_size(16))

logging.info(f"DPI Scale Factor: {DPI_SCALE}")
logging.info(f"Screen resolution detected, scaling fonts and UI elements")

def get_app_directory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def get_output_path():
    return get_app_directory()

log_file = os.path.join(get_output_path(), 'cfss_app.log')
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def resource_path(relative_path, writable=False):
    app_dir = get_app_directory()
    if writable:
        return os.path.join(app_dir, relative_path)
    else:
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = app_dir
        return os.path.join(base_path, relative_path)

class CFSS_app:
    VERSION = "4.2.3"  # Updated for auto-updater release

    def __init__(self, root):
        self.root = root
        self.root.title(f"Copper/Fiber Serial Scanner v{self.VERSION}")
        self.root.resizable(True, True)
        self.is_animating = False
        
        try:
            # Initialize Managers
            db_path = os.path.join(get_output_path(), 'cfss_app.db')
            self.db = DataManager(db_path)
            self.circuit_manager = CircuitManager(self.db, get_output_path())
            self.scan_controller = ScanController(self.db)

            # Initial Data Load
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS scan_progress (
                    circuit_name TEXT, jumper_table TEXT, current_index INTEGER,
                    scanned_serials TEXT, PRIMARY KEY (circuit_name, jumper_table)
                )
            ''')
                        # Add this right after the scan_progress table creation:
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS issue_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    circuit_name TEXT NOT NULL,
                    jumper_table TEXT NOT NULL,
                    record_index INTEGER NOT NULL,
                    location TEXT,
                    container TEXT,
                    cassette TEXT,
                    port TEXT,
                    expected_serial TEXT,
                    scanned_serial TEXT,
                    issue_type TEXT NOT NULL,  -- 'skip' or 'non_match'
                    skip_reason TEXT,          -- For skipped items
                    resolution_note TEXT,      -- For resolved non-matches
                    issue_timestamp TEXT NOT NULL,
                    resolution_timestamp TEXT,
                    user_id TEXT,
                    device_id TEXT,
                    status TEXT DEFAULT 'open'  -- 'open', 'resolved', 'skipped'
                )
            ''')
            self.circuit_manager.load_circuits_from_csvs(
                resource_path('data', writable=True),
                resource_path('data')
            )
            self.circuits = self.circuit_manager.get_available_circuits()
            if not self.circuits:
                logging.info("No circuits loaded - user will need to load CSV files")
                self.current_circuit = None
            else:
                self.current_circuit = 'cs_eb' if 'cs_eb' in self.circuits else self.circuits[0]
            
            # Setup UI and initial state
            self.setup_ui()
            if self.current_circuit:
                self.update_jumper_combobox() # This sets the initial jumper table
                self.load_current_scan_state()
                self.display_current_record()
            else:
                # Initialize with empty state
                self.current_jumper_table = None
                self.current_index = 0
                self.scanned_serials = []
            
            # Check initial data state and disable inputs if needed
            self.check_data_loaded_state()
            
            # Check for updates on startup (in background)
            self.check_for_updates_on_startup()

        except Exception as e:
            logging.error(f"Initialization failed: {e}")
            messagebox.showerror("Error", f"Failed to start application: {e}")
            if hasattr(self, 'db'):
                self.db.close()
            sys.exit(1)

    def setup_ui(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.configure(bg='#1c2526')

        self.main_frame = ctk.CTkFrame(self.root, fg_color='#1c2526', corner_radius=10)
        self.main_frame.pack(pady=5, padx=10, fill="both", expand=True)

        # ... (Header and subheader labels are fine) ...
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.content_frame.pack(fill='both', expand=True)
        header_label = ctk.CTkLabel(self.content_frame, text=f"Copper/Fiber Serial Scanner v{self.VERSION}", font=("Helvetica", get_scaled_font_size(32), "bold"), text_color='#00d4ff')
        header_label.pack(pady=2)
        subheader_label = ctk.CTkLabel(self.content_frame, text="Scan jumper serials to verify connections", font=("Helvetica", get_scaled_font_size(9), "italic"), text_color='#b0b8b8')
        subheader_label.pack(pady=2)

        # --- Circuit Selection Frame ---
        self.circuit_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        self.circuit_frame.pack(fill="x", pady=5, padx=10)

        # First row - circuit and jumper selection
        self.circuit_row1 = ctk.CTkFrame(self.circuit_frame, fg_color='transparent')
        self.circuit_row1.pack(fill="x", pady=2)

        ctk.CTkLabel(self.circuit_row1, text="Select Circuit:", text_color='#b0b8b8', font=("Helvetica", 10)).pack(side="left", padx=2)
        circuit_values = self.circuits if self.circuits else ["No circuits loaded - sync CSVs first"]
        self.circuit_combobox = ctk.CTkComboBox(self.circuit_row1, values=circuit_values, state='readonly', font=("Helvetica", 10), width=180, text_color='#b0b8b8', fg_color='#2f3b3c', dropdown_fg_color='#2f3b3c', dropdown_text_color='#b0b8b8', command=self.on_circuit_select)
        if self.current_circuit:
            self.circuit_combobox.set(self.current_circuit)
        else:
            self.circuit_combobox.set("No circuits loaded - sync CSVs first")
        self.circuit_combobox.pack(side='left', padx=5)

        ctk.CTkLabel(self.circuit_row1, text="Select Jumper:", text_color='#b0b8b8', font=("Helvetica", 10)).pack(side='left', padx=2)
        self.jumper_combobox = ctk.CTkComboBox(self.circuit_row1, values=["Jumper 1"], state='readonly', font=("Helvetica", 10), width=100, text_color='#b0b8b8', fg_color='#2f3b3c', dropdown_fg_color='#2f3b3c', dropdown_text_color='#b0b8b8', command=self.on_jumper_select)
        self.jumper_combobox.pack(side='left', padx=5)

        # Second row - SharePoint and management buttons
        self.circuit_row2 = ctk.CTkFrame(self.circuit_frame, fg_color='transparent')
        self.circuit_row2.pack(fill="x", pady=2)

        self.sync_button = ctk.CTkButton(
            self.circuit_row2, 
            text="Sync CSVs", 
            command=self.sync_csvs_from_sharepoint,
            font=("Helvetica", 10), 
            fg_color='#0099cc', 
            text_color='#ffffff', 
            hover_color='#00bfff',
            width=90
        )
        self.sync_button.pack(side='left', padx=2)

        self.export_button = ctk.CTkButton(
            self.circuit_row2, 
            text="Export Data", 
            command=self.export_scan_data_for_sharepoint,
            font=("Helvetica", 10), 
            fg_color='#00cc66', 
            text_color='#ffffff', 
            hover_color='#00ff80',
            width=90
        )
        self.export_button.pack(side='left', padx=2)

        self.help_button = ctk.CTkButton(
            self.circuit_row2, 
            text="SP Help", 
            command=self.show_sharepoint_help,
            font=("Helvetica", 10), 
            fg_color='#9966cc', 
            text_color='#ffffff', 
            hover_color='#b380ff',
            width=70
        )
        self.help_button.pack(side='left', padx=2)

                # Add this after your help_button in the circuit_row2 section:
        self.issues_button = ctk.CTkButton(
            self.circuit_row2, 
            text="Issues", 
            command=self.show_issue_summary,
            font=("Helvetica", 10), 
            fg_color='#ff9966', 
            text_color='#ffffff', 
            hover_color='#ffb380',
            width=70
        )
        self.issues_button.pack(side='left', padx=2)

        self.delete_circuit_button = ctk.CTkButton(
            self.circuit_row2, 
            text="Delete Circuit", 
            command=self.delete_circuit, 
            font=("Helvetica", 10), 
            fg_color='#ff4d4d', 
            text_color='#ffffff', 
            hover_color='#ff6666',
            width=100
        )
        self.delete_circuit_button.pack(side='right', padx=2)

        # --- Record Display Frame (using .grid for better alignment) ---
        self.record_frame = ctk.CTkFrame(self.content_frame, fg_color='#2f3b3c', corner_radius=10, border_width=2, border_color='#2f3b3c')
        self.record_frame.pack(fill='both', expand=True, pady=5, padx=10)
        self.record_label = ctk.CTkLabel(self.record_frame, text="Current Record", font=("Helvetica", 24, "bold"), text_color='#b0b8b8')
        self.record_label.pack(anchor='w', padx=12, pady=12)
        self.import_csv_button = ctk.CTkButton(self.record_frame, text="Import CSV(s)", command=self.import_csv_files, font=("Helvetica", 10, "bold"), fg_color='#0099cc', text_color='#ffffff', hover_color='#00bfff', width=120)
        self.import_csv_button.place(relx=1.0, anchor="ne", x=-10, y=10)

        self.record_inner_frame = ctk.CTkFrame(self.record_frame, fg_color='transparent')
        self.record_inner_frame.pack(fill='x', expand=True, padx=10, pady=5)
        self.record_inner_frame.grid_columnconfigure((0, 1), weight=1)

        # Create and grid all the labels and value displays
        self.port_location_label = self._create_grid_label(self.record_inner_frame, "Location:", 0, 0)
        self.port_location_value = self._create_grid_value(self.record_inner_frame, "", 1, 0)
        self.port_container_label = self._create_grid_label(self.record_inner_frame, "Container:", 0, 1)
        self.port_container_value = self._create_grid_value(self.record_inner_frame, "", 1, 1)
        self.port_cassette_label = self._create_grid_label(self.record_inner_frame, "Cassette:", 2, 0)
        self.port_cassette_value = self._create_grid_value(self.record_inner_frame, "", 3, 0)
        self.port_label = self._create_grid_label(self.record_inner_frame, "Port:", 2, 1)
        self.port_value = self._create_grid_value(self.record_inner_frame, "", 3, 1)
        self.status_label_label = self._create_grid_label(self.record_inner_frame, "Status:", 4, 0)
        self.status_label_value = self._create_grid_value(self.record_inner_frame, "N/A", 5, 0, columnspan=2)
        
        self.progress_label = ctk.CTkLabel(self.record_inner_frame, text="Progress: 0%", font=("Helvetica", 10), text_color='#b0b8b8', anchor="w")
        self.progress_label.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        self.progressbar = ctk.CTkProgressBar(self.record_inner_frame, fg_color='#1c2526', progress_color='#2f3b3c', border_color='#1c2526')
        self.progressbar.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(5, 10))
        self.progressbar.set(0)

        self.skip_reason_var = tk.StringVar(value="Select reason for skipping")
        self.skip_reason_dropdown = ctk.CTkComboBox(
            self.record_inner_frame, 
            values=[
                "Missing", 
                "Not patched in", 
                "Label not scanning",
                "Duplicate label"  # Just add this one
            ], 
            variable=self.skip_reason_var, 
            state='readonly', 
            font=("Helvetica", 10), 
            width=200,
            text_color='#b0b8b8', 
            fg_color='#2f3b3c', 
            dropdown_fg_color='#2f3b3c', 
            dropdown_text_color='#b0b8b8', 
            command=self.skip_reason_selected
        )
        self.skip_reason_dropdown.grid(row=8, column=0, columnspan=2, sticky="w", pady=(5, 0))

        self.search_frame = ctk.CTkFrame(self.record_inner_frame, fg_color='transparent')
        self.search_frame.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        self.search_entry = ctk.CTkEntry(self.search_frame, width=200, font=("Helvetica", 10), fg_color='#2f3b3c', text_color='#b0b8b8', placeholder_text="Search location (e.g. NS1.01)")
        self.search_entry.pack(side='left', padx=2)
        self.search_entry.bind('<Return>', self.search_location)
        self.search_button = ctk.CTkButton(self.search_frame, text="Go", command=self.search_location, font=("Helvetica", 10), fg_color='#0099cc', text_color='#ffffff', hover_color='#00bfff', width=40)
        self.search_button.pack(side='left', padx=2)

        # --- Input Frame ---
        self.input_frame = ctk.CTkFrame(self.content_frame, fg_color='#2f3b3c', corner_radius=10)
        self.input_frame.pack(fill='both', expand=True, pady=5, padx=10)
        ctk.CTkLabel(self.input_frame, text="Scan Serial", font=("Helvetica", get_scaled_font_size(24), "bold"), text_color='#b0b8b8').pack(anchor='w', padx=5, pady=(0, 2))
        self.serial_row = ctk.CTkFrame(self.input_frame, fg_color='transparent')
        self.serial_row.pack(fill='x', padx=0, pady=0)
        self.serial_entry = ctk.CTkEntry(self.serial_row, width=250, font=("Courier", get_scaled_font_size(10), "bold"), fg_color='#2f3b3c', text_color='#b0b8b8', border_color='#1c2526')
        self.serial_entry.pack(side='left', padx=(5, 2), pady=0)
        self.serial_entry.bind('<Return>', self.check_serial)
        self.expected_serial_label = ctk.CTkLabel(self.serial_row, text="Expected Serial: N/A", font=("Courier", get_scaled_font_size(16), "bold"), text_color='#00d4ff')
        self.expected_serial_label.pack(side='left', padx=(10, 5), pady=0)
        self.scan_feedback_label = ctk.CTkLabel(self.input_frame, text="Ready to scan", font=("Helvetica", get_scaled_font_size(12)), text_color='#b0b8b8')
        self.scan_feedback_label.pack(anchor='w', padx=5, pady=(0, 18))

        # --- Lower Buttons and Status Bar ---
        self.lower_frame = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.lower_frame.pack(side='bottom', fill='x', pady=10, padx=10)
        self.save_buttons_frame = ctk.CTkFrame(self.lower_frame, fg_color='transparent')
        self.save_buttons_frame.pack(side='left', padx=5)
        ctk.CTkButton(self.save_buttons_frame, text="Save All", command=self.save_all_circuits, font=("Helvetica", 10), fg_color='#2f3b3c', text_color='#ffffff', hover_color='#00d4ff', width=80).pack(side='left', padx=3)
        ctk.CTkButton(self.save_buttons_frame, text="Save", command=self.save_current_circuit, font=("Helvetica", 10), fg_color='#2f3b3c', text_color='#ffffff', hover_color='#00d4ff', width=80).pack(side='left', padx=3)
        ctk.CTkButton(self.lower_frame, text="Previous", command=self.previous_record, font=("Helvetica", 10), fg_color='#2f3b3c', text_color='#ffffff', hover_color='#00d4ff', width=80).pack(side='right', padx=3, pady=5)
        ctk.CTkButton(self.lower_frame, text="Next", command=self.next_record, font=("Helvetica", 10), fg_color='#2f3b3c', text_color='#ffffff', hover_color='#00d4ff', width=70).pack(side='right', padx=3, pady=5)
        ctk.CTkButton(self.lower_frame, text="Reset", command=self.reset_scan, font=("Helvetica", 10), fg_color='#2f3b3c', text_color='#ffffff', hover_color='#00d4ff', width=70).pack(side='right', padx=3, pady=5)
        ctk.CTkButton(self.lower_frame, text="Reset All", command=self.reset_all_circuits, font=("Helvetica", 10), fg_color='#2f3b3c', text_color='#ffffff', hover_color='#00d4ff', width=80).pack(side='right', padx=3, pady=5)
        self.status_bar = ctk.CTkLabel(self.root, text="Ready", font=("Helvetica", 9), fg_color='#2f3b3c', text_color='#b0b8b8', anchor="w", corner_radius=0, height=20)
        self.status_bar.pack(side='bottom', fill='x', expand=True, pady=0, padx=0)

    def _create_grid_label(self, parent, text, row, col):
        label = ctk.CTkLabel(parent, text=text, text_color='#b0b8b8', font=("Helvetica", 14))
        label.grid(row=row, column=col, sticky="w", pady=(0, 2), padx=5)
        return label

    def _create_grid_value(self, parent, text, row, col, columnspan=1):
        value = ctk.CTkLabel(parent, text=text, font=("Helvetica", 20, 'bold'), text_color='#00d4ff')
        value.grid(row=row, column=col, columnspan=columnspan, sticky="w", pady=(0, 10), padx=5)
        return value

    def on_circuit_select(self, circuit_name):
        if circuit_name == "No circuits loaded - sync CSVs first":
            messagebox.showinfo("Info", "Please sync CSV files first to load circuits.")
            return
        
        self.current_circuit = circuit_name
        self.update_jumper_combobox()
        self.load_current_scan_state()
        self.display_current_record()
        self.update_status_bar(f"Selected circuit: {self.current_circuit}")

    def on_jumper_select(self, jumper_display_name):
        jumper_num = int(jumper_display_name.split()[-1])
        jumper_tables = self.circuit_manager.get_jumper_tables_for_circuit(self.current_circuit)
        self.current_jumper_table = jumper_tables[jumper_num - 1]
        self.load_current_scan_state()
        self.display_current_record()
        self.update_status_bar(f"Selected jumper: {jumper_display_name} for {self.current_circuit}")

        # Replace your existing update_jumper_combobox method with this improved version:
    
    def update_jumper_combobox(self):
        if not self.current_circuit or not self.circuits:
            # No circuit selected or no circuits available
            self.jumper_combobox.configure(values=["No jumpers"], state='disabled')
            self.jumper_combobox.set("No jumpers")
            self.current_jumper_table = None
            return
            
        jumper_tables = self.circuit_manager.get_jumper_tables_for_circuit(self.current_circuit)
        jumper_options = [f"Jumper {i + 1}" for i, _ in enumerate(jumper_tables)]
        
        if jumper_options:
            self.jumper_combobox.configure(values=jumper_options, state='readonly')
            self.jumper_combobox.set(jumper_options[0])
            self.current_jumper_table = jumper_tables[0]
            # Enable state based on number of options
            if len(jumper_options) == 1:
                self.jumper_combobox.configure(state='disabled')  # Only one option, no need to select
        else:
            # Circuit exists but no jumper tables
            self.jumper_combobox.configure(values=["No jumpers"], state='disabled')
            self.jumper_combobox.set("No jumpers")
            self.current_jumper_table = None

    def load_current_scan_state(self):
        total_rows = 0
        if self.current_jumper_table:
            records = self.circuit_manager.get_ordered_jumper_records(self.current_jumper_table)
            total_rows = len(records)
        self.scan_controller.load_state(self.current_circuit, self.current_jumper_table, total_rows)

        # Replace the _get_record_details method with this corrected version:
    
    def _get_record_details(self, circuit_id, jumper_num):
        """Helper to fetch and determine all details for a specific record."""
        details = {}
        main_row = self.circuit_manager.get_main_row(self.current_circuit, circuit_id)
        if not main_row: return None

        length = int(main_row['length'] or 2)
        is_last_jumper = (jumper_num == length // 2)
        has_z_data = main_row['z_location'] and str(main_row['z_location']).strip().upper() not in ('', 'N/A')

        if jumper_num == 1:
            # Special rule for CSW circuits
            if 'csw' in self.current_circuit.lower():
                # CSW: Single jumper (length=2) shows A location, multi-jumper shows Port 1 location
                if length == 2:  # Single jumper
                    details = {
                        'loc_lbl': "A Location:", 'loc_val': main_row['a_location'], 
                        'con_lbl': "A Device:", 'con_val': main_row['a_device'], 
                        'cas_lbl': "A Interface:", 'cas_val': main_row['a_interface'], 
                        'prt_lbl': "", 'prt_val': "", 
                        'serial': main_row['a_jumper_serial']
                    }
                else:  # Multi-jumper
                    details = {
                        'loc_lbl': "Port 1 Location:", 'loc_val': main_row['port_1_location'], 
                        'con_lbl': "Port 1 Container:", 'con_val': main_row['port_1_container'], 
                        'cas_lbl': "Port 1 Cassette:", 'cas_val': main_row['port_1_cassette'], 
                        'prt_lbl': "Port 1:", 'prt_val': main_row['port_1'], 
                        'serial': main_row['port_1_jumper_serial']
                    }
            else:
                # Universal rule for all other circuits: Z data exists = A location, doesn't exist = Port 1 location
                if has_z_data:
                    details = {
                        'loc_lbl': "A Location:", 'loc_val': main_row['a_location'], 
                        'con_lbl': "A Device:", 'con_val': main_row['a_device'], 
                        'cas_lbl': "A Interface:", 'cas_val': main_row['a_interface'], 
                        'prt_lbl': "", 'prt_val': "", 
                        'serial': main_row['a_jumper_serial']
                    }
                else:
                    details = {
                        'loc_lbl': "Port 1 Location:", 'loc_val': main_row['port_1_location'], 
                        'con_lbl': "Port 1 Container:", 'con_val': main_row['port_1_container'], 
                        'cas_lbl': "Port 1 Cassette:", 'cas_val': main_row['port_1_cassette'], 
                        'prt_lbl': "Port 1:", 'prt_val': main_row['port_1'], 
                        'serial': main_row['port_1_jumper_serial']
                    }
        elif is_last_jumper and has_z_data:
            details = {
                'loc_lbl': "Z Location:", 'loc_val': main_row['z_location'], 
                'con_lbl': "Z Device:", 'con_val': main_row['z_device'], 
                'cas_lbl': "Z Interface:", 'cas_val': main_row['z_interface'], 
                'prt_lbl': "", 'prt_val': "", 
                'serial': main_row['z_jumper_serial']
            }
        else:
            if jumper_num == 2:
                p_num = 2
            elif jumper_num == 3:
                p_num = 4
            elif jumper_num == 4:
                p_num = 7
            else:
                p_num = (jumper_num - 1) * 2
            
            details = {
                'loc_lbl': f"Port {p_num} Location:", 'loc_val': main_row[f'port_{p_num}_location'], 
                'con_lbl': f"Port {p_num} Container:", 'con_val': main_row[f'port_{p_num}_container'], 
                'cas_lbl': f"Port {p_num} Cassette:", 'cas_val': main_row[f'port_{p_num}_cassette'], 
                'prt_lbl': f"Port {p_num}:", 'prt_val': main_row[f'port_{p_num}'], 
                'serial': main_row[f'port_{p_num}_jumper_serial']
            }
        
        return {k: (v or "N/A") for k, v in details.items()}

        # Also update your display_current_record method to handle empty states better:
    
    def display_current_record(self):
        if not self.current_circuit or not self.current_jumper_table or not self.circuits:
            self.clear_record_display()
            # Re-enable controls if we have circuits but just no current selection
            if self.circuits:
                self.serial_entry.configure(state='normal')
                self.skip_reason_dropdown.configure(state='readonly')
                self.search_entry.configure(state='normal')
                self.search_button.configure(state='normal')
            return
    
        if self.scan_controller.total_rows == 0:
            self.clear_record_display()
            return
    
        ordered_records = self.circuit_manager.get_ordered_jumper_records(self.current_jumper_table)
        if not ordered_records or self.scan_controller.current_index >= len(ordered_records):
            self.clear_record_display()
            return
            
        current_record = ordered_records[self.scan_controller.current_index]
        jumper_num = int(self.jumper_combobox.get().split()[-1])
        
        details = self._get_record_details(current_record['circuit_id'], jumper_num)
        if not details:
            self.clear_record_display()
            return
    
        # Enable controls since we have valid data
        self.serial_entry.configure(state='normal')
        self.skip_reason_dropdown.configure(state='readonly')
        self.search_entry.configure(state='normal')
        self.search_button.configure(state='normal')
    
        self.port_location_label.configure(text=details['loc_lbl'])
        self.port_location_value.configure(text=details['loc_val'])
        self.port_container_label.configure(text=details['con_lbl'])
        self.port_container_value.configure(text=details['con_val'])
        self.port_cassette_label.configure(text=details['cas_lbl'])
        self.port_cassette_value.configure(text=details['cas_val'])
        self.port_label.configure(text=details['prt_lbl'])
        self.port_value.configure(text=details['prt_val'])
        self.expected_serial_label.configure(text=f"Expected Serial: {details['serial']}")
    
        status = self.scan_controller.get_current_status()
        status_text, status_color = "Ready to scan", "#00d4ff"
        if status is True: status_text, status_color = "Match", "#00cc00"
        elif status is False: status_text, status_color = "Non-Match", "#ff0000"
        elif isinstance(status, str): status_text, status_color = status, "#ff9900"
        self.status_label_value.configure(text=status_text, text_color=status_color)
        
        self.update_progress()

        # Replace your existing check_serial method:
    
    def check_serial(self, event=None):
        if self.is_animating or not self.current_circuit or not self.current_jumper_table: 
            return
        scanned_serial = self.serial_entry.get().strip()
        if not scanned_serial: 
            return
    
        self.is_animating = True
        self.serial_entry.configure(state="disabled")
        self.skip_reason_dropdown.configure(state="disabled")
    
        ordered_records = self.circuit_manager.get_ordered_jumper_records(self.current_jumper_table)
        current_record = ordered_records[self.scan_controller.current_index]
        jumper_num = int(self.jumper_combobox.get().split()[-1])
        details = self._get_record_details(current_record['circuit_id'], jumper_num)
        expected_serial = details.get('serial', 'N/A').strip()
    
        # Check if this location had a previous issue that's now resolved
        previous_status = self.scan_controller.get_current_status()
        was_issue = isinstance(previous_status, str) and previous_status not in ("Ready to scan", "Match", "Non-Match")
    
        if expected_serial.upper() == 'N/A':
            self.scan_controller.record_scan_result(False)
            self.status_label_value.configure(text="N/A Expected", text_color="#ff9900")
            self.pulse_border('#ff9900')
            self.play_non_match_sound()
            # Track as issue if not already tracked
            if not was_issue:
                self.track_issue("non_match", skip_reason="N/A Expected Serial")
        elif scanned_serial.lower() == expected_serial.lower():
            self.scan_controller.record_scan_result(True)
            self.status_label_value.configure(text="Match", text_color="#00cc00")
            self.pulse_border('#00cc00')
            self.play_match_sound()
            # Track resolution if this was previously an issue
            if was_issue:
                self.track_issue_resolution(previous_status, scanned_serial, "Successful rescan")
        else:
            # NON-MATCH - Show resolution dialog
            resolution = self.handle_non_match_resolution(scanned_serial, expected_serial)
            
            if resolution['action'] == 'skip':
                # User chose to skip this location
                self.scan_controller.record_scan_result("Non-match - skipped")
                self.status_label_value.configure(text="Skipped", text_color="#ff9900")
                self.track_issue("skip", skip_reason="Non-match - skipped for later")
                self.pulse_border('#ff9900')
                self.play_non_match_sound()
            elif resolution['action'] == 'record_non_match':
                # User chose to record the non-match
                self.scan_controller.record_scan_result(False)
                self.status_label_value.configure(text="Non-Match", text_color="#ff0000")
                self.track_issue("non_match", scanned_serial=scanned_serial)
                self.pulse_border('#ff0000')
                self.play_non_match_sound()
            elif resolution['action'] == 'resolved':
                # User fixed the issue and provided a note
                self.scan_controller.record_scan_result(True)
                self.status_label_value.configure(text="Resolved", text_color="#00cc66")
                self.track_issue("non_match", scanned_serial=scanned_serial, 
                               resolution_note=resolution['note'], resolved=True)
                self.pulse_border('#00cc66')
                self.play_match_sound()
    
        self.update_progress()
        self.scan_controller.save_state()
        self.root.after(1000, self.after_scan)

    def next_record(self):
        if self.scan_controller.next_record():
            self.display_current_record()
            self.scan_controller.save_state()
            self.update_status_bar(f"Displaying record {self.scan_controller.current_index + 1} of {self.scan_controller.total_rows}")

    def previous_record(self):
        if self.scan_controller.previous_record():
            self.display_current_record()
            self.scan_controller.save_state()
            self.update_status_bar(f"Displaying record {self.scan_controller.current_index + 1} of {self.scan_controller.total_rows}")

    def reset_scan(self):
        if messagebox.askyesno("Confirm Reset", f"Reset scan progress for {self.current_jumper_table}?"):
            self.scan_controller.reset_state()
            self.scan_controller.save_state()
            self.display_current_record()
            self.update_status_bar("Scan reset to start")

    def reset_all_circuits(self):
        if messagebox.askyesno("Confirm Reset All", "Reset ALL scan progress? This cannot be undone."):
            self.scan_controller.reset_all_states()
            self.load_current_scan_state() # Reload to reset local state
            self.display_current_record()
            self.update_status_bar("All circuits reset")

    def skip_reason_selected(self, reason):
        if self.is_animating or not self.current_circuit or not self.current_jumper_table: 
            return
        
        self.is_animating = True
        self.serial_entry.configure(state="disabled")
        self.skip_reason_dropdown.configure(state="disabled")
    
        self.scan_controller.record_scan_result(reason)
        self.status_label_value.configure(text=reason, text_color="#ff9900")
        self.pulse_border('#ff9900')
        self.play_non_match_sound()
        
        # Track the skip issue
        self.track_issue("skip", skip_reason=reason)
        
        self.update_progress()
        self.scan_controller.save_state()
        self.skip_reason_var.set("Select reason for skipping")
        self.root.after(700, self.after_scan)
    def update_progress(self):
        stats = self.scan_controller.get_progress_stats()
        scanned_count = stats['match'] + stats['non_match'] + stats['skipped']
        
        # Progress bar should only show matches as progress
        match_percentage = (stats['match'] / stats['total'] * 100) if stats['total'] > 0 else 0
        
        self.progress_label.configure(text=f"Progress: {match_percentage:.1f}% ({scanned_count}/{stats['total']}) | Matches: {stats['match']} | Non-matches: {stats['non_match']} | Skipped: {stats['skipped']}")
        self.progressbar.set(match_percentage / 100)
        self.progressbar.configure(progress_color=self.get_progress_color(match_percentage))
        
        # Play completion sound only when ALL items are matches (100% matches)
        # Add a 2-second delay so it doesn't interfere with the last match tone
        if stats['match'] == stats['total'] and stats['total'] > 0:
            self.root.after(2000, self.play_completion_sound)

    def _generate_circuit_output(self, file, circuit, circuit_idx=1, total_circuits=1):
        file.write(f"CIRCUIT: {circuit.upper()} ({circuit_idx} of {total_circuits})\n" + "-" * 80 + "\n")
        jumper_tables = self.circuit_manager.get_jumper_tables_for_circuit(circuit)
        if not jumper_tables:
            file.write("\n    No jumper data found for this circuit.\n")
            return

        for jumper_num, jumper_table in enumerate(jumper_tables, 1):
            file.write(f"\nJumper {jumper_num} Data\n")
            
            # Load the scan state for this specific table for the report
            temp_scan_controller = ScanController(self.db)
            records = self.circuit_manager.get_ordered_jumper_records(jumper_table)
            temp_scan_controller.load_state(circuit, jumper_table, len(records))
            scan_data = temp_scan_controller.get_all_scan_data()

            data_to_print = []
            for display_idx, record in enumerate(records):
                main_row = self.circuit_manager.get_main_row(circuit, record['circuit_id'])
                if not main_row: continue
                
                output_row = self._get_jumper_connection_details(main_row, jumper_num)
                
                status = ""
                scan_val = scan_data.get(display_idx)
                if scan_val is True: status = "Match"
                elif scan_val is False: status = "Non-Match"
                elif isinstance(scan_val, str): status = scan_val
                output_row['status'] = status
                data_to_print.append(output_row)

            headers, column_keys = self._get_report_headers(jumper_num)
            self._format_and_write_table(file, headers, data_to_print, column_keys)

    def _get_jumper_connection_details(self, main_row, jumper_num):
        """Helper for report generation to get start/end points of a jumper."""
        details = {}
        length = int(main_row['length'] or 2)
        is_last_jumper = (jumper_num == length // 2)
        has_z_data = main_row['z_location'] and main_row['z_location'] != 'N/A'

        # Start side
        if jumper_num == 1:
            details.update({'start_loc': main_row['a_location'], 'start_dev': main_row['a_device'], 'start_int': main_row['a_interface'], 'start_port': '', 'serial': main_row['a_jumper_serial']})
        else:
            p_start = (jumper_num - 1) * 2
            details.update({'start_loc': main_row[f'port_{p_start}_location'], 'start_dev': main_row[f'port_{p_start}_container'], 'start_int': main_row[f'port_{p_start}_cassette'], 'start_port': main_row[f'port_{p_start}'], 'serial': main_row[f'port_{p_start}_jumper_serial']})

        # End side
        if is_last_jumper and has_z_data:
            details.update({'end_loc': main_row['z_location'], 'end_dev': main_row['z_device'], 'end_int': main_row['z_interface'], 'end_port': ''})
        else:
            p_end = (jumper_num - 1) * 2 + 1
            details.update({'end_loc': main_row[f'port_{p_end}_location'], 'end_dev': main_row[f'port_{p_end}_container'], 'end_int': main_row[f'port_{p_end}_cassette'], 'end_port': main_row[f'port_{p_end}']})
        
        return {k: (v or "") for k, v in details.items()}

    def _get_report_headers(self, jumper_num):
        """Gets the appropriate headers for the text report based on jumper number."""
        if jumper_num == 1:
            p_end = 1
            headers = {'start_loc': 'A Location', 'start_dev': 'A Device', 'start_int': 'A Interface', 'end_loc': f'Port {p_end}/Z Location', 'end_dev': f'Port {p_end}/Z Cont/Dev', 'end_int': f'Port {p_end}/Z Cass/Int', 'end_port': f'Port {p_end} Port', 'serial': 'Jumper Serial', 'status': 'Status'}
            keys = ['start_loc', 'start_dev', 'start_int', 'end_loc', 'end_dev', 'end_int', 'end_port', 'serial', 'status']
        else:
            p_start = (jumper_num - 1) * 2
            p_end = p_start + 1
            headers = {'start_loc': f'Port {p_start} Location', 'start_dev': f'Port {p_start} Container', 'start_int': f'Port {p_start} Cassette', 'start_port': f'Port {p_start} Port', 'end_loc': f'Port {p_end}/Z Location', 'end_dev': f'Port {p_end}/Z Cont/Dev', 'end_int': f'Port {p_end}/Z Cass/Int', 'end_port': f'Port {p_end}/Z Port', 'serial': 'Jumper Serial', 'status': 'Status'}
            keys = ['start_loc', 'start_dev', 'start_int', 'start_port', 'end_loc', 'end_dev', 'end_int', 'end_port', 'serial', 'status']
        return headers, keys

    def save_all_circuits(self):
        self._save_circuits_to_file(all_circuits=True)

    def save_current_circuit(self):
        self._save_circuits_to_file(all_circuits=False)

    def _save_circuits_to_file(self, all_circuits):
        try:
            results_dir = os.path.join(get_output_path(), 'test_results')
            os.makedirs(results_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if all_circuits:
                filename = os.path.join(results_dir, f"cfss_all_results_v{self.VERSION}_{timestamp}.txt")
                circuits_to_save = self.circuits
            else:
                if not self.current_circuit:
                    messagebox.showwarning("Warning", "No circuit selected.")
                    return
                filename = os.path.join(results_dir, f"cfss_{self.current_circuit}_results_v{self.VERSION}_{timestamp}.txt")
                circuits_to_save = [self.current_circuit]

            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Network Copper/Fiber Connection Documentation (v{self.VERSION})\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" + "=" * 80 + "\n\n")
                for i, circuit in enumerate(circuits_to_save, 1):
                    self._generate_circuit_output(f, circuit, i, len(circuits_to_save))
                    f.write("\n" + "=" * 80 + "\n\n")
            
            messagebox.showinfo("Save Complete", f"Results saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving results: {e}")
            messagebox.showerror("Save Error", f"Failed to save results: {e}")

    def _format_and_write_table(self, file, headers, data_rows, column_keys):
        if not data_rows: return
        widths = {key: len(headers[key]) for key in column_keys}
        for row in data_rows:
            for key in column_keys:
                widths[key] = max(widths[key], len(str(row.get(key, ''))))
        
        header_line = " | ".join(headers[key].ljust(widths[key]) for key in column_keys)
        separator_line = "-|-".join("-" * widths[key] for key in column_keys)
        file.write(header_line + "\n" + separator_line + "\n")

        for row in data_rows:
            data_line = " | ".join(str(row.get(key, '')).ljust(widths[key]) for key in column_keys)
            file.write(data_line + "\n")

    # --- Utility and other methods ---
    def clear_record_display(self):
        self.port_location_value.configure(text="N/A")
        self.port_container_value.configure(text="N/A")
        self.port_cassette_value.configure(text="N/A")
        self.port_value.configure(text="N/A")
        self.progress_label.configure(text="Progress: 0%")
        self.progressbar.set(0)
        self.status_label_value.configure(text="Ready to scan", text_color="#00d4ff")

    def after_scan(self):
        self.serial_entry.configure(state="normal")
        self.skip_reason_dropdown.configure(state="readonly")  # Re-enable the dropdown
        self.serial_entry.delete(0, tk.END)
        self.serial_entry.focus()
        self.is_animating = False
        self.next_record()

    def pulse_border(self, color):
        self.record_frame.configure(border_color=color, border_width=3)
        self.root.after(600, lambda: self.record_frame.configure(border_width=2, border_color='#2f3b3c'))

    def get_progress_color(self, percentage):
        # ... (This method can remain as is) ...
        stops = [(0.0, (139, 0, 0)), (0.5, (255, 255, 0)), (1.0, (0, 128, 0))]
        percentage = max(0.0, min(1.0, percentage / 100.0))
        for i in range(len(stops) - 1):
            p1, rgb1 = stops[i]; p2, rgb2 = stops[i+1]
            if p1 <= percentage <= p2:
                frac = (percentage - p1) / (p2 - p1)
                r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * frac)
                g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * frac)
                b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * frac)
                return f'#{r:02x}{g:02x}{b:02x}'
        return '#008000'

    def play_sound(self, sound_name):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(resource_path(f'sounds/{sound_name}.mp3'))
            pygame.mixer.music.play()
        except Exception as e:
            logging.error(f"Error playing sound {sound_name}: {e}")

    def play_match_sound(self): self.play_sound('match')
    def play_non_match_sound(self): self.play_sound('nonmatch')
    def play_completion_sound(self): self.play_sound('complete')
    def update_status_bar(self, message): self.status_bar.configure(text=message)
    def __del__(self): self.db.close()
    
        # Update your import_csv_files method to handle the empty state properly:
    
    def import_csv_files(self):
        # This method now just needs to call the circuit manager and reload the UI
        file_paths = filedialog.askopenfilenames(title="Select CSV files", filetypes=[("CSV Files", "*.csv")])
        if not file_paths: return
        
        data_dir = resource_path('data', writable=True)
        imported_count = 0
        for path in file_paths:
            try:
                shutil.copy(path, data_dir)
                imported_count += 1
            except Exception as e:
                logging.error(f"Failed to import {path}: {e}")
    
        if imported_count > 0:
            messagebox.showinfo("Import Complete", f"Imported {imported_count} file(s). Reloading circuits.")
            self.circuit_manager.load_circuits_from_csvs(data_dir, resource_path('data'))
            self.circuits = self.circuit_manager.get_available_circuits()
            
            if self.circuits:
                self.circuit_combobox.configure(values=self.circuits)
                self.current_circuit = self.circuits[0]
                self.circuit_combobox.set(self.current_circuit)
                # Re-enable controls
                self.serial_entry.configure(state='normal')
                self.skip_reason_dropdown.configure(state='readonly')
                self.search_entry.configure(state='normal')
                self.search_button.configure(state='normal')
                self.on_circuit_select(self.current_circuit)
            else:
                # Still no circuits after import
                self.circuit_combobox.configure(values=["No circuits"])
                self.circuit_combobox.set("No circuits")
                self.clear_record_display()
        else:
            messagebox.showwarning("Import Failed", "No files were imported.")
    
    def delete_circuit(self):
        if not self.current_circuit:
            messagebox.showwarning("Delete Circuit", "No circuit is selected to delete.")
            return
        
        circuit_to_delete = self.current_circuit
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to permanently delete the circuit '{circuit_to_delete}' and all its data? This cannot be undone."):
            return
    
        try:
            self.circuit_manager.delete_circuit_data(circuit_to_delete)
            
            # Delete the CSV file - need to find the correct filename
            data_dir = resource_path('data', writable=True)
            
            # Look for CSV files that match the circuit name (handle different naming conventions)
            possible_names = [
                f"{circuit_to_delete}.csv",
                f"{circuit_to_delete.upper()}.csv",
                f"{circuit_to_delete.replace('_', '-')}.csv",
                f"{circuit_to_delete.replace('_', '-').upper()}.csv"
            ]
            
            csv_deleted = False
            for csv_name in possible_names:
                csv_file_path = os.path.join(data_dir, csv_name)
                if os.path.exists(csv_file_path):
                    os.remove(csv_file_path)
                    logging.info(f"Deleted CSV file: {csv_file_path}")
                    csv_deleted = True
                    break
            
            # If no direct match, search all CSV files in the directory
            if not csv_deleted:
                all_csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
                for csv_file in all_csv_files:
                    csv_basename = os.path.splitext(os.path.basename(csv_file))[0].lower().replace('-', '_')
                    if csv_basename == circuit_to_delete:
                        os.remove(csv_file)
                        logging.info(f"Deleted CSV file: {csv_file}")
                        csv_deleted = True
                        break
            
            if csv_deleted:
                messagebox.showinfo("Delete Complete", f"Circuit '{circuit_to_delete}' and its CSV file have been deleted.")
            else:
                messagebox.showinfo("Delete Complete", f"Circuit '{circuit_to_delete}' has been deleted from database. CSV file not found.")
            
            # Reload circuits and update UI properly
            self.circuits = self.circuit_manager.get_available_circuits()
            
            if self.circuits:
                # Still have circuits available
                self.circuit_combobox.configure(values=self.circuits)
                self.current_circuit = 'cs_eb' if 'cs_eb' in self.circuits else self.circuits[0]
                self.circuit_combobox.set(self.current_circuit)
                self.on_circuit_select(self.current_circuit)
            else:
                # No circuits left - disable everything properly
                self.circuit_combobox.configure(values=["No circuits"])
                self.circuit_combobox.set("No circuits")
                self.current_circuit = None
                self.current_jumper_table = None
                
                # Disable jumper dropdown
                self.jumper_combobox.configure(values=["No jumpers"], state='disabled')
                self.jumper_combobox.set("No jumpers")
                
                # Disable other controls that depend on having data
                self.serial_entry.configure(state='disabled')
                self.skip_reason_dropdown.configure(state='disabled')
                self.search_entry.configure(state='disabled')
                self.search_button.configure(state='disabled')
                
                # Clear the display
                self.clear_record_display()
                self.update_status_bar("No circuits available - import CSV files to continue")
    
        except Exception as e:
            logging.error(f"Failed to delete circuit {circuit_to_delete}: {e}")
            messagebox.showerror("Delete Error", f"An error occurred while deleting the circuit: {e}")
    
    def search_location(self, event=None):
        query = self.search_entry.get().strip().lower()
        if not query or not self.current_circuit or not self.current_jumper_table:
            return
    
        try:
            ordered_records = self.circuit_manager.get_ordered_jumper_records(self.current_jumper_table)
            jumper_num = int(self.jumper_combobox.get().split()[-1])
    
            for idx, record in enumerate(ordered_records):
                details = self._get_record_details(record['circuit_id'], jumper_num)
                if not details:
                    continue
    
                # Search in all displayed fields
                searchable_text = ' '.join([
                    str(details.get('loc_val', '')),
                    str(details.get('con_val', '')),
                    str(details.get('cas_val', '')),
                    str(details.get('prt_val', ''))
                ]).lower()
    
                if query in searchable_text:
                    self.scan_controller.current_index = idx
                    self.scan_controller.save_state()
                    self.display_current_record()
                    self.update_status_bar(f"Jumped to record {idx + 1} matching '{query}'")
                    self.search_entry.delete(0, "end")
                    return
            
            messagebox.showinfo("Not Found", f"No record found matching '{query}' in the current view.")
            self.search_entry.delete(0, "end")
    
        except Exception as e:
            logging.error(f"Error during search: {e}")
            messagebox.showerror("Search Error", f"An error occurred while searching: {e}")

    # Add these methods to the CFSS_app class:

    def export_scan_data_for_sharepoint(self):
        """Export scan data in SharePoint-ready format"""
        try:
            import socket
            import getpass
            from datetime import datetime
            
            # Get device/user info
            device_id = socket.gethostname()
            user_id = getpass.getuser()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create export directory
            export_dir = os.path.join(get_output_path(), 'sharepoint_export')
            os.makedirs(export_dir, exist_ok=True)
            
            # Create unique filename for SharePoint upload
            filename = f"CFSS_ScanData_{device_id}_{user_id}_{timestamp}.json"
            export_path = os.path.join(export_dir, filename)
            
            # Collect all scan data
            export_data = {
                'export_info': {
                    'device_id': device_id,
                    'user_id': user_id,
                    'export_timestamp': timestamp,
                    'app_version': self.VERSION,
                    'total_circuits': len(self.circuits)
                },
                'scan_results': {}
            }
            
            # Process each circuit
            for circuit in self.circuits:
                circuit_data = {'jumpers': {}, 'circuit_stats': {'total_jumpers': 0, 'completed_jumpers': 0}}
                jumper_tables = self.circuit_manager.get_jumper_tables_for_circuit(circuit)
                circuit_data['circuit_stats']['total_jumpers'] = len(jumper_tables)
                
                for jumper_num, jumper_table in enumerate(jumper_tables, 1):
                    # Create temp controller to get scan data
                    temp_controller = ScanController(self.db)
                    records = self.circuit_manager.get_ordered_jumper_records(jumper_table)
                    temp_controller.load_state(circuit, jumper_table, len(records))
                    scan_data = temp_controller.get_all_scan_data()
                    stats = temp_controller.get_progress_stats()
                    
                    # Check if jumper is complete (100% matches)
                    if stats['match'] == stats['total'] and stats['total'] > 0:
                        circuit_data['circuit_stats']['completed_jumpers'] += 1
                    
                    jumper_records = []
                    for idx, record in enumerate(records):
                        main_row = self.circuit_manager.get_main_row(circuit, record['circuit_id'])
                        if not main_row:
                            continue
                            
                        details = self._get_record_details(record['circuit_id'], jumper_num)
                        scan_status = scan_data.get(idx)
                        
                        record_data = {
                            'record_index': idx,
                            'circuit_id': record['circuit_id'],
                            'location': details.get('loc_val', ''),
                            'container': details.get('con_val', ''),
                            'cassette': details.get('cas_val', ''),
                            'port': details.get('prt_val', ''),
                            'expected_serial': details.get('serial', ''),
                            'scan_status': scan_status,  # True, False, or string reason
                            'scanned_timestamp': timestamp if scan_status is not None else None
                        }
                        jumper_records.append(record_data)
                    
                    circuit_data['jumpers'][f'jumper_{jumper_num}'] = {
                        'records': jumper_records,
                        'stats': stats
                    }
                
                export_data['scan_results'][circuit] = circuit_data
            
            # Write to JSON file
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            # Also create a simple summary file
            summary_filename = f"CFSS_Summary_{device_id}_{user_id}_{timestamp}.txt"
            summary_path = os.path.join(export_dir, summary_filename)
            
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(f"CFSS Scan Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Device: {device_id} | User: {user_id} | App Version: {self.VERSION}\n")
                f.write("=" * 60 + "\n\n")
                
                for circuit, data in export_data['scan_results'].items():
                    completed = data['circuit_stats']['completed_jumpers']
                    total = data['circuit_stats']['total_jumpers']
                    f.write(f"Circuit: {circuit.upper()}\n")
                    f.write(f"  Completed Jumpers: {completed}/{total}\n")
                    
                    for jumper_name, jumper_data in data['jumpers'].items():
                        stats = jumper_data['stats']
                        match_pct = (stats['match'] / stats['total'] * 100) if stats['total'] > 0 else 0
                        f.write(f"  {jumper_name.replace('_', ' ').title()}: {match_pct:.1f}% matches ({stats['match']}/{stats['total']})\n")
                    f.write("\n")
        
            messagebox.showinfo("Export Complete", 
                              f"Scan data exported for SharePoint upload:\n\n"
                              f"Data File: {filename}\n"
                              f"Summary: {summary_filename}\n\n"
                              f"Location: {export_dir}\n\n"
                              f"Upload these files to your SharePoint collection folder.")
            
            # Open the export directory for easy access
            import subprocess
            import platform
            if platform.system() == "Windows":
                subprocess.Popen(f'explorer "{export_dir}"')
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(['open', export_dir])
        
        except Exception as e:
            logging.error(f"Export failed: {e}")
            messagebox.showerror("Export Error", f"Failed to export data: {e}")

    def sync_csvs_from_sharepoint(self):
        """Sync CSV files from SharePoint folder"""
        try:
            # This would point to a mapped SharePoint drive or sync folder
            sharepoint_csv_folder = filedialog.askdirectory(
                title="Select SharePoint CSV Folder (OneDrive Sync Location)",
                initialdir=os.path.expanduser("~/OneDrive")  # Common SharePoint sync location
            )
            
            if not sharepoint_csv_folder:
                return
                
            # Copy new/updated CSVs from SharePoint to local data folder
            data_dir = resource_path('data', writable=True)
            import glob
            csv_files = glob.glob(os.path.join(sharepoint_csv_folder, "*.csv"))
            
            if not csv_files:
                messagebox.showinfo("No CSVs Found", "No CSV files found in the selected SharePoint folder.")
                return
                
            updated_count = 0
            for csv_file in csv_files:
                filename = os.path.basename(csv_file)
                local_path = os.path.join(data_dir, filename)
                
                # Check if file is newer or doesn't exist locally
                should_copy = True
                if os.path.exists(local_path):
                    sharepoint_mtime = os.path.getmtime(csv_file)
                    local_mtime = os.path.getmtime(local_path)
                    should_copy = sharepoint_mtime > local_mtime
                
                if should_copy:
                    shutil.copy2(csv_file, local_path)
                    updated_count += 1
                    logging.info(f"Updated CSV from SharePoint: {filename}")
            
            if updated_count > 0:
                messagebox.showinfo("Sync Complete", 
                                  f"Updated {updated_count} CSV file(s) from SharePoint.\n"
                                  f"Reloading circuits...")
                
                # Reload circuits
                self.circuit_manager.load_circuits_from_csvs(data_dir, resource_path('data'))
                self.circuits = self.circuit_manager.get_available_circuits()
                self.circuit_combobox.configure(values=self.circuits)
                if self.circuits:
                    self.on_circuit_select(self.circuits[0])
            else:
                messagebox.showinfo("Sync Complete", "All CSV files are up to date.")
                
        except Exception as e:
            logging.error(f"SharePoint sync failed: {e}")
            messagebox.showerror("Sync Error", f"Failed to sync from SharePoint: {e}")

        # Add these methods to your existing CFSS_app class:
    
    def save_sharepoint_folder(self, folder_path):
        """Save the SharePoint folder path for future use"""
        try:
            config_path = os.path.join(get_output_path(), 'sharepoint_config.json')
            config = {'sharepoint_sync_folder': folder_path}
            with open(config_path, 'w') as f:
                json.dump(config, f)
            logging.info(f"Saved SharePoint folder: {folder_path}")
        except Exception as e:
            logging.error(f"Failed to save SharePoint folder: {e}")
    
    def load_sharepoint_folder(self):
        """Load the saved SharePoint folder path"""
        try:
            config_path = os.path.join(get_output_path(), 'sharepoint_config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    return config.get('sharepoint_sync_folder', '')
            return ''
        except Exception as e:
            logging.error(f"Failed to load SharePoint folder: {e}")
            return ''
    
    # Replace your existing sync_csvs_from_sharepoint method:
    def sync_csvs_from_sharepoint(self):
        """Enhanced sync with smart progress migration"""
        try:
            # Load the previously saved SharePoint folder 
            saved_folder = self.load_sharepoint_folder()
            initial_dir = saved_folder if saved_folder and os.path.exists(saved_folder) else os.path.expanduser("~/OneDrive")
            
            sharepoint_csv_folder = filedialog.askdirectory(
                title="Select SharePoint CSV Distribution Folder (OneDrive Sync Location)",
                initialdir=initial_dir
            )
            
            if not sharepoint_csv_folder:
                return
            
            # Save the selected folder for next time
            self.save_sharepoint_folder(sharepoint_csv_folder)
                
            # Copy new/updated CSVs from SharePoint to local data folder
            data_dir = resource_path('data', writable=True)
            csv_files = glob.glob(os.path.join(sharepoint_csv_folder, "*.csv"))
            
            if not csv_files:
                messagebox.showinfo("No CSVs Found", "No CSV files found in the selected SharePoint folder.")
                return
                
            # Check for existing scan progress
            existing_progress = self.db.fetchone(
                "SELECT COUNT(*) as count FROM scan_progress WHERE scanned_serials != '{}' AND scanned_serials IS NOT NULL AND scanned_serials != ''"
            )
            has_progress = existing_progress and existing_progress['count'] > 0
            
            # Check which files need updating
            files_to_update = []
            for csv_file in csv_files:
                filename = os.path.basename(csv_file)
                local_path = os.path.join(data_dir, filename)
                
                # Check if file is newer or doesn't exist locally
                should_copy = True
                if os.path.exists(local_path):
                    sharepoint_mtime = os.path.getmtime(csv_file)
                    local_mtime = os.path.getmtime(local_path)
                    should_copy = sharepoint_mtime > local_mtime
                
                if should_copy:
                    files_to_update.append((csv_file, local_path, filename))
            
            if not files_to_update:
                messagebox.showinfo("Sync Complete", "All CSV files are up to date.")
                return
            
            # Show user what will happen
            file_list = "\n".join([f"• {f[2]}" for f in files_to_update])
            
            if has_progress:
                choice = messagebox.askyesnocancel(
                    "CSV Updates Found",
                    f"Found {len(files_to_update)} updated CSV file(s):\n\n{file_list}\n\n"
                    f"⚠️ You have existing scan progress.\n\n"
                    f"Smart Migration will:\n"
                    f"• Preserve scan progress for matching locations\n"
                    f"• Create backups of current progress\n"
                    f"• Add new records as unscanned\n"
                    f"• Show you what was preserved vs. lost\n\n"
                    f"Continue with smart migration?\n\n"
                    f"YES: Update with smart migration\n"
                    f"NO: Update and reset all progress\n"
                    f"CANCEL: Don't update"
                )
                
                if choice is None:  # Cancel
                    return
                elif not choice:  # No - reset all progress
                    if messagebox.askyesno("Confirm Reset", "This will delete ALL scan progress. Are you sure?"):
                        self.scan_controller.reset_all_circuits()
                    else:
                        return
            else:
                # No existing progress, just confirm update
                if not messagebox.askyesno("Update CSVs", f"Update {len(files_to_update)} CSV file(s)?"):
                    return
                choice = True  # Proceed with migration (though nothing to migrate)
            
            # Copy updated files
            for csv_file, local_path, filename in files_to_update:
                shutil.copy2(csv_file, local_path)
                logging.info(f"Updated CSV from SharePoint: {filename}")
            
            # Reload circuits with migration
            self.root.config(cursor="wait")
            self.root.update()
            
            try:
                # Load circuits with enhanced processing that returns migration info
                old_circuit_count = len(self.circuits) if hasattr(self, 'circuits') else 0
                
                # The enhanced load method will handle migration automatically
                self.circuit_manager.load_circuits_from_csvs(data_dir, resource_path('data'))
                self.circuits = self.circuit_manager.get_available_circuits()
                
                # Update UI
                if self.circuits:
                    self.circuit_combobox.configure(values=self.circuits)
                    # Try to keep current circuit if it still exists
                    if hasattr(self, 'current_circuit') and self.current_circuit in self.circuits:
                        self.circuit_combobox.set(self.current_circuit)
                    else:
                        self.current_circuit = self.circuits[0]
                        self.circuit_combobox.set(self.current_circuit)
                    self.on_circuit_select(self.current_circuit)
                else:
                    self.circuit_combobox.configure(values=["No circuits"])
                    self.circuit_combobox.set("No circuits")
                    self.current_circuit = None
                    self.clear_record_display()
                
                # Show results to user
                if choice and has_progress:  # Smart migration was used
                    # Check remaining progress after migration
                    remaining_progress = self.db.fetchone(
                        "SELECT COUNT(*) as count FROM scan_progress WHERE scanned_serials != '{}' AND scanned_serials IS NOT NULL AND scanned_serials != ''"
                    )
                    remaining_count = remaining_progress['count'] if remaining_progress else 0
                    
                    messagebox.showinfo("Sync Complete with Smart Migration", 
                                      f"✅ Updated {len(files_to_update)} CSV file(s) from SharePoint\n\n"
                                      f"📊 Smart Migration Results:\n"
                                      f"• Scan progress preserved where locations matched\n"
                                      f"• New records added as unscanned\n"
                                      f"• Progress entries remaining: {remaining_count}\n"
                                      f"• Backups created in scan_backups folder\n\n"
                                      f"Check your current circuit - most progress should be preserved!")
                else:
                    messagebox.showinfo("Sync Complete", 
                                      f"Updated {len(files_to_update)} CSV file(s) from SharePoint.\n"
                                      f"Circuits reloaded successfully.")
            
            finally:
                self.root.config(cursor="")
                # Clear input fields after sync and check data state
                self.clear_input_fields()
                self.check_data_loaded_state()
                
        except Exception as e:
            self.root.config(cursor="")
            logging.error(f"SharePoint sync failed: {e}")
            messagebox.showerror("Sync Error", f"Failed to sync from SharePoint: {e}")
    def export_scan_data_for_sharepoint(self):
        """Export scan data directly to SharePoint collection folder"""
        try:
            # Check if we have a saved SharePoint folder
            saved_folder = self.load_sharepoint_folder()
            if saved_folder and os.path.exists(saved_folder):
                # Look for the collection folder in the parent directory
                parent_dir = os.path.dirname(saved_folder)
                collection_folder = os.path.join(parent_dir, 'Scan_Data_Collection')
                
                if os.path.exists(collection_folder):
                    export_dir = collection_folder
                    export_location_msg = f"SharePoint Collection Folder:\n{collection_folder}"
                else:
                    # Fall back to asking user to select collection folder
                    export_dir = filedialog.askdirectory(
                        title="Select SharePoint Scan Data Collection Folder",
                        initialdir=parent_dir if os.path.exists(parent_dir) else os.path.expanduser("~/OneDrive")
                    )
                    if not export_dir:
                        return
                    export_location_msg = f"Selected Collection Folder:\n{export_dir}"
            else:
                # No saved folder, ask user to select collection folder
                export_dir = filedialog.askdirectory(
                    title="Select SharePoint Scan Data Collection Folder",
                    initialdir=os.path.expanduser("~/OneDrive")
                )
                if not export_dir:
                    return
                export_location_msg = f"Selected Collection Folder:\n{export_dir}"
            
            # Get device/user info
            device_id = socket.gethostname()
            user_id = getpass.getuser()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create unique filename for SharePoint upload
            filename = f"CFSS_ScanData_{device_id}_{user_id}_{timestamp}.json"
            export_path = os.path.join(export_dir, filename)
            
            # Collect all scan data
            export_data = {
                'export_info': {
                    'device_id': device_id,
                    'user_id': user_id,
                    'export_timestamp': timestamp,
                    'app_version': self.VERSION,
                    'total_circuits': len(self.circuits)
                },
                'scan_results': {}
            }
            
            # Process each circuit
            for circuit in self.circuits:
                circuit_data = {'jumpers': {}, 'circuit_stats': {'total_jumpers': 0, 'completed_jumpers': 0}}
                jumper_tables = self.circuit_manager.get_jumper_tables_for_circuit(circuit)
                circuit_data['circuit_stats']['total_jumpers'] = len(jumper_tables)
                
                for jumper_num, jumper_table in enumerate(jumper_tables, 1):
                    # Create temp controller to get scan data
                    temp_controller = ScanController(self.db)
                    records = self.circuit_manager.get_ordered_jumper_records(jumper_table)
                    temp_controller.load_state(circuit, jumper_table, len(records))
                    scan_data = temp_controller.get_all_scan_data()
                    stats = temp_controller.get_progress_stats()
                    
                    # Check if jumper is complete (100% matches)
                    if stats['match'] == stats['total'] and stats['total'] > 0:
                        circuit_data['circuit_stats']['completed_jumpers'] += 1
                    
                    jumper_records = []
                    for idx, record in enumerate(records):
                        main_row = self.circuit_manager.get_main_row(circuit, record['circuit_id'])
                        if not main_row:
                            continue
                        
                        # Temporarily set circuit context for _get_record_details
                        temp_current_circuit = self.current_circuit
                        self.current_circuit = circuit
                        details = self._get_record_details(record['circuit_id'], jumper_num)
                        self.current_circuit = temp_current_circuit
                        
                        if not details:
                            continue
                            
                        scan_status = scan_data.get(idx)
                        
                        record_data = {
                            'record_index': idx,
                            'circuit_id': record['circuit_id'],
                            'location': details.get('loc_val', ''),
                            'container': details.get('con_val', ''),
                            'cassette': details.get('cas_val', ''),
                            'port': details.get('prt_val', ''),
                            'expected_serial': details.get('serial', ''),
                            'scan_status': scan_status,
                            'scanned_timestamp': timestamp if scan_status is not None else None
                        }
                        jumper_records.append(record_data)
                    
                    circuit_data['jumpers'][f'jumper_{jumper_num}'] = {
                        'records': jumper_records,
                        'stats': stats
                    }
                
                export_data['scan_results'][circuit] = circuit_data
            
            # Write to JSON file
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            # Also create a simple summary file
            summary_filename = f"CFSS_Summary_{device_id}_{user_id}_{timestamp}.txt"
            summary_path = os.path.join(export_dir, summary_filename)
            
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(f"CFSS Scan Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Device: {device_id} | User: {user_id} | App Version: {self.VERSION}\n")
                f.write("=" * 60 + "\n\n")
                
                for circuit, data in export_data['scan_results'].items():
                    completed = data['circuit_stats']['completed_jumpers']
                    total = data['circuit_stats']['total_jumpers']
                    f.write(f"Circuit: {circuit.upper()}\n")
                    f.write(f"  Completed Jumpers: {completed}/{total}\n")
                    
                    for jumper_name, jumper_data in data['jumpers'].items():
                        stats = jumper_data['stats']
                        match_pct = (stats['match'] / stats['total'] * 100) if stats['total'] > 0 else 0
                        f.write(f"  {jumper_name.replace('_', ' ').title()}: {match_pct:.1f}% matches ({stats['match']}/{stats['total']})\n")
                    f.write("\n")
        
            messagebox.showinfo("Export Complete", 
                              f"Scan data exported directly to SharePoint!\n\n"
                              f"Data File: {filename}\n"
                              f"Summary: {summary_filename}\n\n"
                              f"{export_location_msg}\n\n"
                              f"Files are now available to your central team.")
            
        except Exception as e:
            logging.error(f"Export failed: {e}")
            messagebox.showerror("Export Error", f"Failed to export data: {e}")

        # Add this new method to handle non-match resolution:
    
    def handle_non_match_resolution(self, scanned_serial, expected_serial):
        """Handle resolution note for non-matches"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Non-Match Resolution")
        dialog.geometry(f"{get_scaled_size(600)}x{get_scaled_size(500)}")
        dialog.minsize(get_scaled_size(550), get_scaled_size(450))
        dialog.configure(bg='#1c2526')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (get_scaled_size(600) // 2)
        y = (dialog.winfo_screenheight() // 2) - (get_scaled_size(500) // 2)
        dialog.geometry(f"{get_scaled_size(600)}x{get_scaled_size(500)}+{x}+{y}")
        
        # Header
        header = tk.Label(dialog, text="Non-Match Detected", 
                         font=DIALOG_FONT_LARGE, 
                         bg='#1c2526', fg='#ff4444')
        header.pack(pady=get_scaled_size(15))
        
        # Details frame
        details_frame = tk.Frame(dialog, bg='#1c2526')
        details_frame.pack(fill='x', padx=get_scaled_size(25), pady=get_scaled_size(10))
        
        tk.Label(details_frame, text=f"Expected: {expected_serial}", 
                 font=DIALOG_FONT_COURIER, bg='#1c2526', fg='#00d4ff').pack(anchor='w')
        tk.Label(details_frame, text=f"Scanned:  {scanned_serial}", 
                 font=DIALOG_FONT_COURIER, bg='#1c2526', fg='#ffaa00').pack(anchor='w')
        
        # Options
        tk.Label(dialog, text="What would you like to do?", 
                 font=DIALOG_FONT_MEDIUM, bg='#1c2526', fg='#b0b8b8').pack(pady=(get_scaled_size(15), get_scaled_size(10)))
        
        # Button frame
        button_frame = tk.Frame(dialog, bg='#1c2526')
        button_frame.pack(fill='x', padx=get_scaled_size(25), pady=get_scaled_size(15))
        
        result = {'action': None, 'note': ''}
        
        def skip_with_note():
            result['action'] = 'skip'
            dialog.destroy()
        
        def record_non_match():
            result['action'] = 'record_non_match'
            dialog.destroy()
        
        def corrected_later():
            # Show resolution note dialog
            show_resolution_dialog()
        
        def show_resolution_dialog():
            dialog.withdraw()  # Hide main dialog
            
            note_dialog = tk.Toplevel(self.root)
            note_dialog.title("Resolution Note")
            note_dialog.geometry(f"{get_scaled_size(650)}x{get_scaled_size(600)}")
            note_dialog.minsize(get_scaled_size(600), get_scaled_size(550))
            note_dialog.configure(bg='#1c2526')
            note_dialog.transient(self.root)
            note_dialog.grab_set()
            
            # Center the dialog
            note_dialog.update_idletasks()
            x = (note_dialog.winfo_screenwidth() // 2) - (get_scaled_size(650) // 2)
            y = (note_dialog.winfo_screenheight() // 2) - (get_scaled_size(600) // 2)
            note_dialog.geometry(f"{get_scaled_size(650)}x{get_scaled_size(600)}+{x}+{y}")
            
            tk.Label(note_dialog, text="What was the problem?", 
                    font=DIALOG_FONT_LARGE, 
                    bg='#1c2526', fg='#b0b8b8').pack(pady=get_scaled_size(15))
            
            # Text entry for resolution note
            note_frame = tk.Frame(note_dialog, bg='#1c2526')
            note_frame.pack(fill='both', expand=True, padx=get_scaled_size(25), pady=get_scaled_size(15))
            
            tk.Label(note_frame, text="Describe what was wrong and how it was fixed:", 
                    font=DIALOG_FONT_MEDIUM, bg='#1c2526', fg='#b0b8b8').pack(anchor='w')
            
            note_text = tk.Text(note_frame, height=6, width=50, 
                               bg='#2f3b3c', fg='#b0b8b8', 
                               font=DIALOG_FONT_MEDIUM,
                               wrap=tk.WORD)
            note_text.pack(fill='both', expand=True, pady=get_scaled_size(10))
            note_text.focus()
            
            # Preset options
            preset_frame = tk.Frame(note_frame, bg='#1c2526')
            preset_frame.pack(fill='x', pady=get_scaled_size(10))
            
            tk.Label(preset_frame, text="Quick options:", 
                    font=DIALOG_FONT_MEDIUM, bg='#1c2526', fg='#b0b8b8').pack(anchor='w')
            
            def insert_preset(text):
                note_text.delete(1.0, tk.END)
                note_text.insert(1.0, text)
            
            # Preset buttons - stack vertically for better layout
            preset_buttons = tk.Frame(preset_frame, bg='#1c2526')
            preset_buttons.pack(fill='x', pady=get_scaled_size(8))
            
            ctk.CTkButton(preset_buttons, text="Wrong Label", 
                         command=lambda: insert_preset("Wrong jumper label was installed - corrected"),
                         fg_color='#0099cc', text_color='white', font=DIALOG_FONT_SMALL, 
                         width=get_scaled_size(180), height=get_scaled_size(40)).pack(pady=3)
            
            ctk.CTkButton(preset_buttons, text="Label Damaged", 
                         command=lambda: insert_preset("Label was damaged/unreadable - replaced"),
                         fg_color='#0099cc', text_color='white', font=DIALOG_FONT_SMALL, 
                         width=get_scaled_size(180), height=get_scaled_size(40)).pack(pady=3)
            
            ctk.CTkButton(preset_buttons, text="Data Error", 
                         command=lambda: insert_preset("Circuit data was incorrect - updated"),
                         fg_color='#0099cc', text_color='white', font=DIALOG_FONT_SMALL, 
                         width=get_scaled_size(180), height=get_scaled_size(40)).pack(pady=3)
            
            # Buttons
            button_frame_note = tk.Frame(note_dialog, bg='#1c2526')
            button_frame_note.pack(side='bottom', pady=15)
            
            def save_note():
                result['action'] = 'resolved'
                result['note'] = note_text.get(1.0, tk.END).strip()
                note_dialog.destroy()
                dialog.destroy()
            
            def cancel_note():
                note_dialog.destroy()
                dialog.deiconify()  # Show main dialog again
            
            ctk.CTkButton(button_frame_note, text="Save Resolution", 
                         command=save_note, fg_color='#00cc66', text_color='white', 
                         font=DIALOG_FONT_MEDIUM, width=get_scaled_size(180), height=get_scaled_size(45)).pack(side='left', padx=get_scaled_size(15))
            
            ctk.CTkButton(button_frame_note, text="Cancel", 
                         command=cancel_note, fg_color='#666666', text_color='white', 
                         font=DIALOG_FONT_MEDIUM, width=get_scaled_size(180), height=get_scaled_size(45)).pack(side='left', padx=get_scaled_size(15))
        
        # Main dialog buttons - stack vertically for better layout
        buttons_container = tk.Frame(button_frame, bg='#1c2526')
        buttons_container.pack(fill='x', pady=get_scaled_size(8))
        
        ctk.CTkButton(buttons_container, text="Skip This Location", 
                     command=skip_with_note, fg_color='#ff9966', text_color='white', 
                     font=DIALOG_FONT_MEDIUM, width=get_scaled_size(250), height=get_scaled_size(45)).pack(pady=get_scaled_size(8))
        
        ctk.CTkButton(buttons_container, text="Record Non-Match", 
                     command=record_non_match, fg_color='#ff4444', text_color='white', 
                     font=DIALOG_FONT_MEDIUM, width=get_scaled_size(250), height=get_scaled_size(45)).pack(pady=get_scaled_size(8))
        
        ctk.CTkButton(buttons_container, text="Fixed - Add Note", 
                     command=corrected_later, fg_color='#00cc66', text_color='white', 
                     font=DIALOG_FONT_MEDIUM, width=get_scaled_size(250), height=get_scaled_size(45)).pack(pady=get_scaled_size(8))
        
        # Wait for user choice
        dialog.wait_window()
        return result
    
    def track_issue(self, issue_type, skip_reason=None, scanned_serial=None, resolution_note=None, resolved=False):
        """Track issues for analysis and reporting"""
        try:
            # Get current record details
            ordered_records = self.circuit_manager.get_ordered_jumper_records(self.current_jumper_table)
            current_record = ordered_records[self.scan_controller.current_index]
            jumper_num = int(self.jumper_combobox.get().split()[-1])
            details = self._get_record_details(current_record['circuit_id'], jumper_num)
            
            # Get user and device info
            device_id = socket.gethostname()
            user_id = getpass.getuser()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            status = 'resolved' if resolved else 'open'
            resolution_timestamp = timestamp if resolved else None
            
            # Insert issue record
            self.db.execute('''
                INSERT INTO issue_tracking 
                (circuit_name, jumper_table, record_index, location, container, cassette, port, 
                 expected_serial, scanned_serial, issue_type, skip_reason, resolution_note,
                 issue_timestamp, resolution_timestamp, user_id, device_id, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.current_circuit,
                self.current_jumper_table, 
                self.scan_controller.current_index,
                details.get('loc_val', ''),
                details.get('con_val', ''),
                details.get('cas_val', ''),
                details.get('prt_val', ''),
                details.get('serial', ''),
                scanned_serial,
                issue_type,
                skip_reason,
                resolution_note,
                timestamp,
                resolution_timestamp,
                user_id,
                device_id,
                status
            ))
            self.db.commit()
            
            logging.info(f"Tracked {issue_type}: {details.get('loc_val', 'Unknown location')}")
            
        except Exception as e:
            logging.error(f"Failed to track issue: {e}")
    
    def track_issue_resolution(self, original_issue, scanned_serial, resolution_note):
        """Track when a previously problematic item is successfully scanned"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Update the most recent unresolved issue for this location
            self.db.execute('''
                UPDATE issue_tracking 
                SET status = 'resolved',
                    resolution_timestamp = ?,
                    scanned_serial = ?,
                    resolution_note = ?
                WHERE circuit_name = ? AND jumper_table = ? AND record_index = ?
                AND status = 'open'
                ORDER BY issue_timestamp DESC
                LIMIT 1
            ''', (
                timestamp,
                scanned_serial,
                resolution_note,
                self.current_circuit,
                self.current_jumper_table,
                self.scan_controller.current_index
            ))
            self.db.commit()
            
            logging.info(f"Tracked resolution of '{original_issue}' with note: {resolution_note}")
            
        except Exception as e:
            logging.error(f"Failed to track issue resolution: {e}")
    
    def generate_issue_report(self):
        """Generate a comprehensive issue analysis report"""
        try:
            results_dir = os.path.join(get_output_path(), 'issue_reports')
            os.makedirs(results_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(results_dir, f"cfss_issue_report_{timestamp}.txt")
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"CFSS Issue Analysis Report\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                # Overall Issue Statistics
                f.write("OVERALL ISSUE STATISTICS\n")
                f.write("-" * 40 + "\n")
                
                # Total issues by type
                issue_stats = self.db.fetchall('''
                    SELECT issue_type, COUNT(*) as count,
                           COUNT(CASE WHEN resolution_timestamp IS NOT NULL THEN 1 END) as resolved
                    FROM issue_tracking 
                    GROUP BY issue_type 
                    ORDER BY count DESC
                ''')
                
                total_issues = sum(row['count'] for row in issue_stats)
                total_resolved = sum(row['resolved'] for row in issue_stats)
                
                f.write(f"Total Issues Tracked: {total_issues}\n")
                f.write(f"Total Resolved: {total_resolved}\n")
                f.write(f"Resolution Rate: {(total_resolved/total_issues*100):.1f}%\n\n" if total_issues > 0 else "Resolution Rate: 0%\n\n")
                f.write("Issues by Type:\n")
                for row in issue_stats:
                    resolution_rate = (row['resolved'] / row['count'] * 100) if row['count'] > 0 else 0
                    f.write(f"  {row['issue_type']}: {row['count']} total, {row['resolved']} resolved ({resolution_rate:.1f}%)\n")
                
                f.write("\n" + "-" * 80 + "\n\n")
                
                # Issues by Circuit
                f.write("ISSUES BY CIRCUIT\n")
                f.write("-" * 40 + "\n")
                
                circuit_stats = self.db.fetchall('''
                    SELECT circuit_name, COUNT(*) as count,
                           COUNT(CASE WHEN resolution_timestamp IS NOT NULL THEN 1 END) as resolved
                    FROM issue_tracking 
                    GROUP BY circuit_name 
                    ORDER BY count DESC
                ''')
                
                for row in circuit_stats:
                    resolution_rate = (row['resolved'] / row['count'] * 100) if row['count'] > 0 else 0
                    f.write(f"  {row['circuit_name'].upper()}: {row['count']} issues, {row['resolved']} resolved ({resolution_rate:.1f}%)\n")
                
                f.write("\n" + "-" * 80 + "\n\n")
                
                # RESOLUTION NOTES SECTION - This is the new part!
                f.write("RESOLUTION NOTES (What was fixed and how)\n")
                f.write("-" * 40 + "\n")
                
                resolved_with_notes = self.db.fetchall('''
                    SELECT circuit_name, location, container, cassette, port, 
                           issue_type, skip_reason, resolution_note, 
                           issue_timestamp, resolution_timestamp, user_id, expected_serial
                    FROM issue_tracking 
                    WHERE resolution_note IS NOT NULL AND resolution_note != ''
                    ORDER BY resolution_timestamp DESC
                    LIMIT 50
                ''')
                
                if resolved_with_notes:
                    for issue in resolved_with_notes:
                        f.write(f"\n📋 Resolution Entry:\n")
                        f.write(f"   Circuit: {issue['circuit_name'].upper()}\n")
                        f.write(f"   Location: {issue['location']} | {issue['container']} | {issue['cassette']} | {issue['port']}\n")
                        f.write(f"   Expected Serial: {issue['expected_serial']}\n")
                        f.write(f"   Issue Type: {issue['issue_type']}\n")
                        if issue['skip_reason']:
                            f.write(f"   Skip Reason: {issue['skip_reason']}\n")
                        f.write(f"   Issue Date: {issue['issue_timestamp']}\n")
                        f.write(f"   Resolved Date: {issue['resolution_timestamp']}\n")
                        f.write(f"   Resolved By: {issue['user_id']}\n")
                        f.write(f"   Resolution Note: {issue['resolution_note']}\n")
                        f.write("   " + "-" * 50 + "\n")
                else:
                    f.write("   No resolution notes found.\n")
                
                f.write("\n" + "-" * 80 + "\n\n")
                
                # Recent Unresolved Issues
                f.write("RECENT UNRESOLVED ISSUES (Last 30 days)\n")
                f.write("-" * 40 + "\n")
                
                recent_issues = self.db.fetchall('''
                    SELECT circuit_name, location, container, cassette, port, issue_type, 
                           skip_reason, issue_timestamp, expected_serial, user_id, device_id
                    FROM issue_tracking 
                    WHERE resolution_timestamp IS NULL 
                    AND date(issue_timestamp) >= date('now', '-30 days')
                    ORDER BY issue_timestamp DESC
                    LIMIT 50
                ''')
                
                if recent_issues:
                    for issue in recent_issues:
                        f.write(f"  {issue['issue_timestamp']} | {issue['circuit_name'].upper()} | ")
                        f.write(f"{issue['location']} | {issue['container']} | {issue['cassette']} | ")
                        f.write(f"{issue['port']} | {issue['issue_type']}")
                        if issue['skip_reason']:
                            f.write(f" | Reason: {issue['skip_reason']}")
                        f.write(f" | Serial: {issue['expected_serial']}\n")
                else:
                    f.write("  No unresolved issues in the last 30 days!\n")
                
                f.write("\n" + "-" * 80 + "\n\n")
                
                # Skip Reason Analysis
                f.write("SKIP REASON ANALYSIS\n")
                f.write("-" * 40 + "\n")
                
                skip_reasons = self.db.fetchall('''
                    SELECT skip_reason, COUNT(*) as count
                    FROM issue_tracking 
                    WHERE skip_reason IS NOT NULL AND skip_reason != ''
                    GROUP BY skip_reason 
                    ORDER BY count DESC
                ''')
                
                if skip_reasons:
                    for reason in skip_reasons:
                        f.write(f"  {reason['skip_reason']}: {reason['count']} occurrences\n")
                else:
                    f.write("  No skip reasons recorded.\n")
                
                f.write("\n" + "-" * 80 + "\n\n")
                
                # Top Problem Locations
                f.write("TOP PROBLEM LOCATIONS (Multiple Issues)\n")
                f.write("-" * 40 + "\n")
                
                problem_locations = self.db.fetchall('''
                    SELECT location, container, cassette, port, COUNT(*) as issue_count,
                           COUNT(CASE WHEN resolution_timestamp IS NOT NULL THEN 1 END) as resolved_count
                    FROM issue_tracking 
                    GROUP BY location, container, cassette, port
                    HAVING COUNT(*) > 1
                    ORDER BY issue_count DESC
                    LIMIT 20
                ''')
                
                if problem_locations:
                    for loc in problem_locations:
                        f.write(f"  {loc['location']} | {loc['container']} | {loc['cassette']} | {loc['port']} ")
                        f.write(f"| {loc['issue_count']} issues, {loc['resolved_count']} resolved\n")
                else:
                    f.write("  No locations with multiple issues found.\n")
            
            messagebox.showinfo("Report Generated", f"Issue report saved to:\n{filename}")
            
            # Offer to open the file
            if messagebox.askyesno("Open Report", "Would you like to open the report file?"):
                import subprocess
                import platform
                if platform.system() == "Windows":
                    subprocess.Popen(['notepad.exe', filename])
                elif platform.system() == "Darwin":  # macOS
                    subprocess.Popen(['open', filename])
            
        except Exception as e:
            logging.error(f"Failed to generate issue report: {e}")
            messagebox.showerror("Report Error", f"Failed to generate issue report: {e}")

    def show_issue_summary(self):
        """Show a quick issue summary dialog with notes access"""
        try:
            # Get basic issue statistics
            total_issues = self.db.fetchone("SELECT COUNT(*) as count FROM issue_tracking")['count']
            resolved_issues = self.db.fetchone("SELECT COUNT(*) as count FROM issue_tracking WHERE resolution_timestamp IS NOT NULL")['count']
            notes_count = self.db.fetchone("SELECT COUNT(*) as count FROM issue_tracking WHERE resolution_note IS NOT NULL AND resolution_note != ''")['count']
            
            top_issues = self.db.fetchall('''
                SELECT issue_type, COUNT(*) as count 
                FROM issue_tracking 
                GROUP BY issue_type 
                ORDER BY count DESC 
                LIMIT 5
            ''')
            
            # Create summary dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Issue Summary")
            dialog.geometry(f"{get_scaled_size(600)}x{get_scaled_size(500)}")
            dialog.minsize(get_scaled_size(550), get_scaled_size(450))
            dialog.configure(bg='#1c2526')
            
            # Fix window focus issues
            dialog.transient(self.root)  # Make dialog modal
            dialog.grab_set()  # Grab all events
            dialog.focus_force()  # Force focus
            dialog.lift()  # Bring to front
            
            # Center the dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (get_scaled_size(600) // 2)
            y = (dialog.winfo_screenheight() // 2) - (get_scaled_size(500) // 2)
            dialog.geometry(f"{get_scaled_size(600)}x{get_scaled_size(500)}+{x}+{y}")
            
            # Summary text
            summary_text = f"Total Issues Tracked: {total_issues}\n"
            summary_text += f"Resolved Issues: {resolved_issues}\n"
            summary_text += f"Resolution Notes: {notes_count}\n"
            summary_text += f"Resolution Rate: {(resolved_issues/total_issues*100):.1f}%\n\n" if total_issues > 0 else "Resolution Rate: 0%\n\n"
            summary_text += "Top Issue Types:\n"
            
            for issue in top_issues:
                summary_text += f"  • {issue['issue_type']}: {issue['count']}\n"
            
            text_label = tk.Label(dialog, text=summary_text, bg='#1c2526', fg='#b0b8b8', 
                                 font=DIALOG_FONT_COURIER_LARGE, justify=tk.LEFT, anchor="nw")
            text_label.pack(padx=get_scaled_size(25), pady=get_scaled_size(25), fill=tk.BOTH, expand=True)
            
            # Enhanced buttons - stack vertically for better layout
            button_frame = tk.Frame(dialog, bg='#1c2526')
            button_frame.pack(side=tk.BOTTOM, pady=get_scaled_size(20))
            
            # Use grid layout for buttons to ensure proper spacing
            ctk.CTkButton(button_frame, text="View Notes", command=lambda: self.show_recent_notes(dialog), 
                         fg_color='#00cc66', text_color='white', font=DIALOG_FONT_MEDIUM, 
                         width=get_scaled_size(150), height=get_scaled_size(45)).grid(row=0, column=0, padx=get_scaled_size(8), pady=3)
            ctk.CTkButton(button_frame, text="Full Report", command=self.generate_issue_report, 
                         fg_color='#0099cc', text_color='white', font=DIALOG_FONT_MEDIUM, 
                         width=get_scaled_size(150), height=get_scaled_size(45)).grid(row=0, column=1, padx=get_scaled_size(8), pady=3)
            ctk.CTkButton(button_frame, text="Close", command=dialog.destroy, 
                         fg_color='#666666', text_color='white', font=DIALOG_FONT_MEDIUM, 
                         width=get_scaled_size(150), height=get_scaled_size(45)).grid(row=0, column=2, padx=get_scaled_size(8), pady=3)
            
        except Exception as e:
            logging.error(f"Failed to show issue summary: {e}")
            messagebox.showerror("Summary Error", f"Failed to show issue summary: {e}")

    def show_recent_notes(self, parent_dialog=None):
        """Show recent resolution notes in a dialog"""
        try:
            # Get recent notes
            recent_notes = self.db.fetchall('''
                SELECT circuit_name, location, container, cassette, port, 
                       resolution_note, resolution_timestamp, user_id, expected_serial
                FROM issue_tracking 
                WHERE resolution_note IS NOT NULL AND resolution_note != ''
                ORDER BY resolution_timestamp DESC
                LIMIT 20
            ''')
            
            # Create notes dialog
            dialog = tk.Toplevel(parent_dialog if parent_dialog else self.root)
            dialog.title("Recent Resolution Notes")
            dialog.geometry(f"{get_scaled_size(900)}x{get_scaled_size(700)}")
            dialog.minsize(get_scaled_size(850), get_scaled_size(650))
            dialog.configure(bg='#1c2526')
            
            # Fix window focus issues
            dialog.transient(parent_dialog if parent_dialog else self.root)  # Make dialog modal
            dialog.grab_set()  # Grab all events
            dialog.focus_force()  # Force focus
            dialog.lift()  # Bring to front
            
            # Center the dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (get_scaled_size(900) // 2)
            y = (dialog.winfo_screenheight() // 2) - (get_scaled_size(700) // 2)
            dialog.geometry(f"{get_scaled_size(900)}x{get_scaled_size(700)}+{x}+{y}")
            
            # Create scrollable text area
            main_frame = tk.Frame(dialog, bg='#1c2526')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=get_scaled_size(15), pady=get_scaled_size(15))
            
            text_widget = tk.Text(main_frame, wrap=tk.WORD, bg='#2f3b3c', fg='#b0b8b8', 
                                 font=DIALOG_FONT_COURIER)
            scrollbar = tk.Scrollbar(main_frame, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Add notes content
            if recent_notes:
                content = "Recent Resolution Notes\n"
                content += "=" * 50 + "\n\n"
                
                for note in recent_notes:
                    content += f"📍 Location: {note['location']} | {note['container']} | {note['cassette']} | {note['port']}\n"
                    content += f"⚡ Circuit: {note['circuit_name'].upper()}\n"
                    content += f"🔢 Expected Serial: {note['expected_serial']}\n"
                    content += f"👤 Resolved By: {note['user_id']}\n"
                    content += f"📅 Date: {note['resolution_timestamp']}\n"
                    content += f"📝 Resolution Note:\n   {note['resolution_note']}\n"
                    content += "\n" + "-" * 60 + "\n\n"
            else:
                content = "No resolution notes found.\n\nNotes are created when you:\n"
                content += "• Encounter a non-match\n• Choose 'Fixed - Add Note'\n• Describe what was wrong and how it was fixed"
            
            text_widget.insert(tk.END, content)
            text_widget.configure(state=tk.DISABLED)
            
            # Close button with proper sizing
            close_btn = ctk.CTkButton(dialog, text="Close", command=dialog.destroy, 
                                     fg_color='#0099cc', text_color='white', font=DIALOG_FONT_MEDIUM,
                                     width=get_scaled_size(150), height=get_scaled_size(45))
            close_btn.pack(pady=get_scaled_size(15))
            
        except Exception as e:
            logging.error(f"Failed to show recent notes: {e}")
            messagebox.showerror("Notes Error", f"Failed to show notes: {e}")
    
    # Replace your existing show_sharepoint_help method:
    def show_sharepoint_help(self):
        """Show help dialog for SharePoint integration"""
        saved_folder = self.load_sharepoint_folder()
        folder_info = f"Current sync folder: {saved_folder}" if saved_folder else "No sync folder saved yet"
        
        help_message = f"""SharePoint Integration Help
    
    {folder_info}
    
    SYNC CSVs FROM SHAREPOINT:
    1. Click 'Sync CSVs' button
    2. Navigate to your OneDrive SharePoint folder
    3. Select the CSV_Distribution folder
    4. App will remember this folder for next time
    5. App will download new/updated CSV files
    6. Circuits will reload and auto-select first circuit
    
    EXPORT SCAN DATA:
    1. Click 'Export Data' button after scanning
    2. App will automatically find the Scan_Data_Collection folder
    3. Or you can select it manually if needed
    4. Files are saved directly to SharePoint
    5. Central team can immediately see your data
    
    SHAREPOINT FOLDER STRUCTURE:
    CFSS_Central_Management/
    ├── CSV_Distribution/          ← Select this for sync
    └── Scan_Data_Collection/      ← Export goes here automatically
    
    WORKFLOW:
    • Central team distributes CSV files via SharePoint
    • Field teams sync CSV files to get latest circuits
    • Field teams scan jumpers using the app
    • Field teams export scan data (goes directly to SharePoint)
    • Central team can immediately see all scan data
    
    FILES CREATED:
    • CFSS_ScanData_[device]_[user]_[timestamp].json
    • CFSS_Summary_[device]_[user]_[timestamp].txt
    
    NOTE: The app remembers your SharePoint folder selection
    and automatically finds the collection folder for exports."""
    
        messagebox.showinfo("SharePoint Integration", help_message)
        
    def check_for_updates_on_startup(self):
        """Check for updates when application starts"""
        if AUTO_UPDATER_AVAILABLE:
            try:
                check_for_updates_on_startup(self.root, APP_VERSION, "rc91470", "cfss_releases")
            except Exception as e:
                logging.error(f"Failed to check for updates: {e}")
        else:
            logging.info("Auto-updater not available - skipping update check")
    
    def show_migration_results(self):
        """Show detailed migration results to the user"""
        try:
            # Get current scan progress stats
            all_progress = self.db.fetchall("SELECT circuit_name, COUNT(*) as progress_count FROM scan_progress WHERE scanned_serials != '{}' GROUP BY circuit_name")
            
            if not all_progress:
                messagebox.showinfo("No Progress Found", "No scan progress found after migration.")
                return
            
            result_text = "Migration Results:\n\n"
            
            for row in all_progress:
                circuit = row['circuit_name']
                progress_count = row['progress_count']
                
                # Get total jumpers for this circuit
                jumper_tables = self.circuit_manager.get_jumper_tables_for_circuit(circuit)
                total_jumpers = len(jumper_tables)
                
                result_text += f"Circuit: {circuit.upper()}\n"
                result_text += f"  Jumpers with preserved progress: {progress_count}/{total_jumpers}\n"
                
                # Get detailed stats for each jumper
                for jumper_table in jumper_tables:
                    progress_row = self.db.fetchone(
                        "SELECT scanned_serials FROM scan_progress WHERE circuit_name = ? AND jumper_table = ?",
                        (circuit, jumper_table)
                    )
                    if progress_row:
                        try:
                            scanned_data = json.loads(progress_row['scanned_serials'])
                            matches = sum(1 for v in scanned_data.values() if v is True)
                            total_scanned = len(scanned_data)
                            jumper_num = jumper_table.split('_jumper')[1]
                            result_text += f"    Jumper {jumper_num}: {matches} matches, {total_scanned} total preserved\n"
                        except:
                            pass
                result_text += "\n"
            
            result_text += "\nNote: New records from CSV updates start as unscanned.\nBackups are available in the scan_backups folder."
            
            # Create a scrollable text dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Migration Results")
            dialog.geometry(f"{get_scaled_size(700)}x{get_scaled_size(600)}")
            dialog.minsize(get_scaled_size(650), get_scaled_size(550))
            dialog.configure(bg='#1c2526')
            
            # Center the dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (get_scaled_size(700) // 2)
            y = (dialog.winfo_screenheight() // 2) - (get_scaled_size(600) // 2)
            dialog.geometry(f"{get_scaled_size(700)}x{get_scaled_size(600)}+{x}+{y}")
            
            text_widget = tk.Text(dialog, wrap=tk.WORD, bg='#2f3b3c', fg='#b0b8b8', font=DIALOG_FONT_COURIER)
            scrollbar = tk.Scrollbar(dialog, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=get_scaled_size(15), pady=get_scaled_size(15))
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=get_scaled_size(15))
            
            text_widget.insert(tk.END, result_text)
            text_widget.configure(state=tk.DISABLED)
            
            # Add close button with proper sizing
            close_btn = ctk.CTkButton(dialog, text="Close", command=dialog.destroy, 
                                     fg_color='#0099cc', text_color='white', font=DIALOG_FONT_MEDIUM,
                                     width=get_scaled_size(150), height=get_scaled_size(45))
            close_btn.pack(pady=get_scaled_size(15))
            
        except Exception as e:
            logging.error(f"Error showing migration results: {e}")
            messagebox.showerror("Error", f"Could not display migration results: {e}")
    
    def disable_inputs_when_no_data(self):
        """Disable input fields when no data is loaded"""
        try:
            self.serial_entry.configure(state='disabled')
            self.search_entry.configure(state='disabled')
            self.skip_reason_dropdown.configure(state='disabled')
            self.scan_feedback_label.configure(text="Load circuit data to begin scanning")
        except Exception as e:
            logging.error(f"Failed to disable inputs: {e}")
    
    def enable_inputs_when_data_loaded(self):
        """Enable input fields when data is loaded"""
        try:
            self.serial_entry.configure(state='normal')
            self.search_entry.configure(state='normal')
            self.skip_reason_dropdown.configure(state='readonly')
            self.scan_feedback_label.configure(text="Ready to scan")
        except Exception as e:
            logging.error(f"Failed to enable inputs: {e}")
    
    def clear_input_fields(self):
        """Clear all input fields"""
        try:
            self.serial_entry.delete(0, tk.END)
            self.search_entry.delete(0, tk.END)
            self.skip_reason_dropdown.set("")
        except Exception as e:
            logging.error(f"Failed to clear input fields: {e}")
    
    def check_data_loaded_state(self):
        """Check if data is loaded and update UI accordingly"""
        if not self.circuits or not self.current_circuit:
            self.disable_inputs_when_no_data()
            return False
        else:
            self.enable_inputs_when_data_loaded()
            return True
            
if __name__ == '__main__':
    try:
        root = ctk.CTk()
        app = CFSS_app(root)
        root.mainloop()
    except Exception as e:
        logging.critical(f"Fatal error: {e}", exc_info=True)
        messagebox.showerror("Fatal Error", f"Application failed to start: {e}")
        sys.exit(1)
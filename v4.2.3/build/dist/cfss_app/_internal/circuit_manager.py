import csv
import glob
import json
import logging
import os
import shutil
import hashlib
from natsort import natsorted
from datetime import datetime

ALLOWED_COLUMNS = [
    "Length", "A location", "A device", "A interface", "A jumper serial",
    "Port 1 location", "Port 1 container", "Port 1 cassette", "Port 1", "Port 1 jumper serial",
    "Port 2 location", "Port 2 container", "Port 2 cassette", "Port 2", "Port 2 jumper serial",
    "Port 3 location", "Port 3 container", "Port 3 cassette", "Port 3", "Port 3 jumper serial",
    "Port 4 location", "Port 4 container", "Port 4 cassette", "Port 4", "Port 4 jumper serial",
    "Port 5 location", "Port 5 container", "Port 5 cassette", "Port 5", "Port 5 jumper serial",
    "Port 6 location", "Port 6 container", "Port 6 cassette", "Port 6", "Port 6 jumper serial",
    "Port 7 location", "Port 7 container", "Port 7 cassette", "Port 7", "Port 7 jumper serial",
    "Port 8 location", "Port 8 container", "Port 8 cassette", "Port 8", "Port 8 jumper serial",
    "Z location", "Z device", "Z interface", "Z jumper serial"
]

def normalize_col(col):
    return col.strip().lower().replace(' ', '_').replace('-', '_')

ALLOWED_COLUMNS_NORM = [normalize_col(col) for col in ALLOWED_COLUMNS]

class CircuitManager:
    def __init__(self, data_manager, output_path):
        self.db = data_manager
        self.output_path = output_path
        self.circuit_jumper_tables = {}

    def get_file_hash(self, filepath):
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def _create_circuit_table(self, circuit_name):
        columns = [f"{normalize_col(col)} TEXT" for col in ALLOWED_COLUMNS]
        columns[0] = "length INTEGER DEFAULT 0"
        columns.insert(0, "id INTEGER PRIMARY KEY AUTOINCREMENT")
        self.db.execute(f"CREATE TABLE IF NOT EXISTS {circuit_name} ({', '.join(columns)})")
        self.db.commit()

    def _create_jumper_table(self, jumper_table_name):
        self.db.execute(f'''
            CREATE TABLE IF NOT EXISTS {jumper_table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                circuit_id INTEGER
            )
        ''')
        self.db.commit()

    def load_circuits_from_csvs(self, csv_dir, bundled_csv_dir):
        os.makedirs(csv_dir, exist_ok=True)
        
        # Check if there are any CSV files in the data directory
        csv_files = glob.glob(os.path.join(csv_dir, '*.csv'))
        
        # If no CSV files, check for bundled files
        if not csv_files:
            bundled_files = glob.glob(os.path.join(bundled_csv_dir, '*.csv')) if bundled_csv_dir != csv_dir else []
            if bundled_files:
                try:
                    for csv_file in bundled_files:
                        shutil.copy2(csv_file, os.path.join(csv_dir, os.path.basename(csv_file)))
                    csv_files = glob.glob(os.path.join(csv_dir, '*.csv'))
                except Exception as e:
                    logging.error(f"Failed to copy bundled CSV files: {e}")
        
        # If still no CSV files, clear any existing circuits and return
        if not csv_files:
            logging.info("No CSV files found in data directory - clearing existing circuits")
            self.clear_all_circuits()
            return

        hash_cache_path = os.path.join(self.output_path, 'csv_hash_cache.json')
        try:
            with open(hash_cache_path, 'r') as f:
                csv_hash_cache = json.load(f)
        except Exception:
            csv_hash_cache = {}

        for csv_file in csv_files:
            circuit_name = os.path.splitext(os.path.basename(csv_file))[0].lower().replace('-', '_')
            file_hash = self.get_file_hash(csv_file)
            
            table_exists = self.db.fetchone("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (circuit_name,))
            
            if table_exists and csv_hash_cache.get(csv_file) == file_hash:
                logging.info(f"Skipping unchanged CSV: {csv_file}")
            else:
                logging.info(f"Processing CSV: {csv_file}")
                self._process_csv(csv_file, circuit_name)
                csv_hash_cache[csv_file] = file_hash

        with open(hash_cache_path, 'w') as f:
            json.dump(csv_hash_cache, f)
        
        self._discover_jumper_tables()

    def _process_csv(self, csv_file, circuit_name):
        self._create_circuit_table(circuit_name)
        
        # Check if circuit exists and prepare migration
        table_exists = self.db.fetchone("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (circuit_name,))
        migration_data = None
        backup_file = None
        
        if table_exists:
            # Create backup before migration
            backup_file = self.backup_scan_progress(circuit_name)
            # Prepare migration data
            migration_data = self._migrate_scan_progress_for_updated_circuit(circuit_name)
        
        # Rebuild circuit (existing code)
        self.db.execute(f"DROP TABLE IF EXISTS {circuit_name}")
        self._create_circuit_table(circuit_name)
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                header_map = {normalize_col(h): h for h in reader.fieldnames}
                keep_headers_norm = [h for h in ALLOWED_COLUMNS_NORM if h in header_map]
                
                for row in reader:
                    norm_row = {normalize_col(k): v for k, v in row.items()}
                    values = [norm_row.get(h, 'N/A') for h in keep_headers_norm]
                    if keep_headers_norm and keep_headers_norm[0] == 'length' and values[0] not in (None, '', 'N/A'):
                        try:
                            values[0] = int(values[0])
                        except (ValueError, TypeError):
                            values[0] = 0
                    
                    placeholders = ', '.join(['?' for _ in keep_headers_norm])
                    self.db.execute(f"INSERT INTO {circuit_name} ({', '.join(keep_headers_norm)}) VALUES ({placeholders})", values)
                
                self.db.commit()
                self._populate_jumper_tables(circuit_name)
                
                # Restore migrated progress after rebuild
                migrated_count = 0
                if migration_data:
                    migrated_count = self._restore_migrated_progress(circuit_name, migration_data)
                
                # Log migration results
                if migrated_count > 0:
                    logging.info(f"Successfully migrated {migrated_count} scan results for {circuit_name}")
                    return {'migrated': migrated_count, 'backup': backup_file}
                elif table_exists:
                    logging.info(f"Circuit {circuit_name} updated but no scan progress could be migrated")
                    return {'migrated': 0, 'backup': backup_file}
                else:
                    logging.info(f"New circuit {circuit_name} processed")
                    return {'migrated': 0, 'backup': None}

        except Exception as e:
            logging.error(f"Error processing CSV file {csv_file}: {e}")
            return {'migrated': 0, 'backup': backup_file, 'error': str(e)}

    def _populate_jumper_tables(self, circuit_name):
        self._current_circuit_name = circuit_name  # Add this line
        main_rows_with_id = self.db.fetchall(f"SELECT id, * FROM {circuit_name}")
        if not main_rows_with_id:
            return

        old_jumpers = self.db.fetchall("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ?", (f"{circuit_name}_jumper%",))
        for table in old_jumpers:
            self.db.execute(f"DROP TABLE IF EXISTS {table['name']}")
        self.db.commit()

        max_length = 0
        for r in main_rows_with_id:
            try:
                max_length = max(max_length, int(dict(r).get('length', 0) or 0))
            except (ValueError, TypeError):
                continue
        max_jumper_count = max_length // 2

        for jumper_num in range(1, max_jumper_count + 1):
            jumper_table_name = f"{circuit_name}_jumper{jumper_num}"
            self._create_jumper_table(jumper_table_name)

            filtered_rows = [
                row for row in main_rows_with_id
                if int(dict(row).get('length', 0) or 0) >= 2 * jumper_num
            ]

            # Sort rows based on the correct sorting key
            sort_key_func = self._get_sort_key_function(jumper_num)
            sorted_rows = natsorted(filtered_rows, key=lambda r: sort_key_func(dict(r)))

            # Deduplication based on sort key + serial
            seen = set()
            unique_rows = []
            for row in sorted_rows:
                rdict = dict(row)
                sort_key = sort_key_func(rdict)
                
                # Get serial for deduplication
                length = int(rdict.get('length', 0) or 0)
                is_last = (jumper_num == length // 2)
                has_z = (rdict.get('z_location') or '').strip() not in ('', 'N/A')

                if jumper_num == 1:
                    # Special rule for CSW circuits for serial selection
                    circuit_name = getattr(self, '_current_circuit_name', '')
                    if 'csw' in circuit_name.lower():
                        # CSW: Single jumper uses A serial, multi-jumper uses Port 1 serial
                        if length == 2:  # Single jumper
                            serial = rdict.get('a_jumper_serial', '')
                        else:  # Multi-jumper
                            serial = rdict.get('port_1_jumper_serial', '')
                    else:
                        # Universal rule for all other circuits
                        if has_z:
                            serial = rdict.get('a_jumper_serial', '')
                        else:
                            serial = rdict.get('port_1_jumper_serial', '')
                elif is_last and has_z:
                    serial = rdict.get('z_jumper_serial', '')
                else:
                    if jumper_num == 2:
                        serial = rdict.get('port_2_jumper_serial', '')
                    elif jumper_num == 3:
                        serial = rdict.get('port_4_jumper_serial', '')
                    elif jumper_num == 4:
                        serial = rdict.get('port_7_jumper_serial', '')
                    else:
                        p_num = (jumper_num - 1) * 2
                        serial = rdict.get(f'port_{p_num}_jumper_serial', '')

                dedup_key = sort_key + (str(serial or ''),)
                if dedup_key not in seen:
                    seen.add(dedup_key)
                    unique_rows.append(row)

            for row in unique_rows:
                self.db.execute(f"INSERT INTO {jumper_table_name} (circuit_id) VALUES (?)", (row['id'],))
            self.db.commit()

    def _get_sort_key_function(self, jumper_num):
        def sort_key(r):
            def safe(val): return val or ""
            
            length = int(r.get('length', 0) or 0)
            is_last_jumper = (jumper_num == length // 2)
            has_z_data = (r.get('z_location') or '').strip() not in ('', 'N/A')

            if jumper_num == 1:
                # Special rule for CSW circuits
                circuit_name = getattr(self, '_current_circuit_name', '')
                if 'csw' in circuit_name.lower():
                    # CSW: Single jumper (length=2) sorts by A location, multi-jumper sorts by Port 1 location
                    if length == 2:  # Single jumper
                        return (safe(r.get('a_location')), safe(r.get('a_device')), safe(r.get('a_interface')))
                    else:  # Multi-jumper
                        return (safe(r.get('port_1_location')), safe(r.get('port_1_container')), safe(r.get('port_1_cassette')), safe(r.get('port_1')))
                else:
                    # Universal rule for all other circuits: Z data exists = A location, doesn't exist = Port 1 location
                    if has_z_data:
                        return (safe(r.get('a_location')), safe(r.get('a_device')), safe(r.get('a_interface')))
                    else:
                        return (safe(r.get('port_1_location')), safe(r.get('port_1_container')), safe(r.get('port_1_cassette')), safe(r.get('port_1')))
            
            elif is_last_jumper and has_z_data:
                return (safe(r.get('z_location')), safe(r.get('z_device')), safe(r.get('z_interface')))
            
            else:
                if jumper_num == 2:
                    p_num = 2
                elif jumper_num == 3:
                    p_num = 4
                elif jumper_num == 4:
                    p_num = 7
                else:
                    p_num = (jumper_num - 1) * 2
                
                return (safe(r.get(f'port_{p_num}_location')), 
                        safe(r.get(f'port_{p_num}_container')), 
                        safe(r.get(f'port_{p_num}_cassette')), 
                        safe(r.get(f'port_{p_num}')))
        
        return sort_key

    def _discover_jumper_tables(self):
        self.circuit_jumper_tables.clear()
        circuits = self.get_available_circuits()
        for circuit in circuits:
            jumper_tables = self.db.fetchall(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ? ORDER BY name",
                (f"{circuit}_jumper%",)
            )
            self.circuit_jumper_tables[circuit] = [jt['name'] for jt in jumper_tables]

    def get_available_circuits(self):
        tables = self.db.fetchall("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '%_jumper%' AND name != 'scan_progress' AND name != 'issue_tracking'")
        return sorted([table['name'] for table in tables])

    def get_jumper_tables_for_circuit(self, circuit_name):
        return self.circuit_jumper_tables.get(circuit_name, [])

    def get_main_row(self, circuit_name, circuit_id):
        return self.db.fetchone(f"SELECT * FROM {circuit_name} WHERE id = ?", (circuit_id,))

    def get_ordered_jumper_records(self, jumper_table_name):
        return self.db.fetchall(f"SELECT id, circuit_id FROM {jumper_table_name} ORDER BY id")

    def delete_circuit_data(self, circuit_name):
        self.db.execute(f'DROP TABLE IF EXISTS {circuit_name}')
        jumper_tables = self.db.fetchall("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ?", (f"{circuit_name}_jumper%",))
        for table in jumper_tables:
            self.db.execute(f'DROP TABLE IF EXISTS {table["name"]}')
        self.db.execute("DELETE FROM scan_progress WHERE circuit_name = ?", (circuit_name,))
        self.db.commit()
        logging.info(f"Deleted all data for circuit: {circuit_name}")

    def clear_all_circuits(self):
        """Clear all circuit data from the database"""
        try:
            # Get all table names that contain circuit data
            tables = self.db.fetchall("SELECT name FROM sqlite_master WHERE type='table' AND name NOT IN ('scan_progress', 'issue_tracking')")
            
            for table in tables:
                table_name = table[0]
                logging.info(f"Dropping table: {table_name}")
                self.db.execute(f"DROP TABLE IF EXISTS {table_name}")
            
            self.db.commit()
            logging.info("All circuit data cleared from database")
        except Exception as e:
            logging.error(f"Error clearing circuit data: {e}")

    def _migrate_scan_progress_for_updated_circuit(self, circuit_name):
        """Migrate scan progress when circuit is updated by matching locations"""
        logging.info(f"Migrating scan progress for updated circuit: {circuit_name}")
        
        # Get old scan progress before rebuilding
        old_progress = self.db.fetchall(
            "SELECT jumper_table, current_index, scanned_serials FROM scan_progress WHERE circuit_name = ?",
            (circuit_name,)
        )
        
        if not old_progress:
            logging.info(f"No existing scan progress found for {circuit_name}")
            return None
        
        # Store old progress data with location matching
        migration_data = {}
        
        for row in old_progress:
            jumper_table = row['jumper_table']
            try:
                scanned_serials = json.loads(row['scanned_serials']) if row['scanned_serials'] else {}
                
                # Get old records with their location data
                old_records = self.db.fetchall(f"SELECT id, circuit_id FROM {jumper_table} ORDER BY id")
                
                # Extract jumper number from table name
                jumper_num = int(jumper_table.split('_jumper')[1])
                location_to_status = {}
                
                for idx, record in enumerate(old_records):
                    if str(idx) in scanned_serials:
                        # Get the main row for this record
                        main_row = self.db.fetchone(f"SELECT * FROM {circuit_name} WHERE id = ?", (record['circuit_id'],))
                        if main_row:
                            # Generate location key for this record
                            location_key = self._get_location_key_for_migration(dict(main_row), jumper_num, circuit_name)
                            if location_key:
                                location_to_status[location_key] = scanned_serials[str(idx)]
                
                if location_to_status:
                    migration_data[jumper_table] = location_to_status
                    logging.info(f"Prepared migration for {jumper_table}: {len(location_to_status)} scanned locations")
                
            except Exception as e:
                logging.error(f"Error preparing migration data for {jumper_table}: {e}")
        
        # Clean up old progress (circuit will be rebuilt)
        self.db.execute("DELETE FROM scan_progress WHERE circuit_name = ?", (circuit_name,))
        self.db.commit()
        
        return migration_data if migration_data else None

    def _get_location_key_for_migration(self, main_row, jumper_num, circuit_name):
        """Generate a unique location key for matching scan progress"""
        try:
            length = int(main_row.get('length', 0) or 2)
            is_last_jumper = (jumper_num == length // 2)
            has_z_data = main_row.get('z_location') and str(main_row.get('z_location', '')).strip().upper() not in ('', 'N/A')
            
            if jumper_num == 1:
                # Special rule for CSW circuits
                if 'csw' in circuit_name.lower():
                    if length == 2:  # Single jumper
                        return f"A|{main_row.get('a_location', '')}|{main_row.get('a_device', '')}|{main_row.get('a_interface', '')}"
                    else:  # Multi-jumper
                        return f"P1|{main_row.get('port_1_location', '')}|{main_row.get('port_1_container', '')}|{main_row.get('port_1_cassette', '')}|{main_row.get('port_1', '')}"
                else:
                    # Universal rule
                    if has_z_data:
                        return f"A|{main_row.get('a_location', '')}|{main_row.get('a_device', '')}|{main_row.get('a_interface', '')}"
                    else:
                        return f"P1|{main_row.get('port_1_location', '')}|{main_row.get('port_1_container', '')}|{main_row.get('port_1_cassette', '')}|{main_row.get('port_1', '')}"
            
            elif is_last_jumper and has_z_data:
                return f"Z|{main_row.get('z_location', '')}|{main_row.get('z_device', '')}|{main_row.get('z_interface', '')}"
            
            else:
                if jumper_num == 2:
                    p_num = 2
                elif jumper_num == 3:
                    p_num = 4
                elif jumper_num == 4:
                    p_num = 7
                else:
                    p_num = (jumper_num - 1) * 2
                
                return f"P{p_num}|{main_row.get(f'port_{p_num}_location', '')}|{main_row.get(f'port_{p_num}_container', '')}|{main_row.get(f'port_{p_num}_cassette', '')}|{main_row.get(f'port_{p_num}', '')}"
        
        except Exception as e:
            logging.error(f"Error generating location key for jumper {jumper_num}: {e}")
            return None

    def _restore_migrated_progress(self, circuit_name, migration_data):
        """Restore scan progress after circuit rebuild using location matching"""
        if not migration_data:
            return 0
        
        logging.info(f"Restoring migrated scan progress for {circuit_name}")
        total_migrated = 0
        
        for jumper_table, location_to_status in migration_data.items():
            if not location_to_status:
                continue
            
            # Check if the jumper table exists in the rebuilt circuit
            table_exists = self.db.fetchone(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?", 
                (jumper_table,)
            )
            
            if not table_exists:
                logging.warning(f"Jumper table {jumper_table} no longer exists after rebuild")
                continue
            
            # Get new records and match with old progress
            new_records = self.db.fetchall(f"SELECT id, circuit_id FROM {jumper_table} ORDER BY id")
            jumper_num = int(jumper_table.split('_jumper')[1])
            
            new_scanned_serials = {}
            matched_locations = 0
            
            for idx, record in enumerate(new_records):
                main_row = self.db.fetchone(f"SELECT * FROM {circuit_name} WHERE id = ?", (record['circuit_id'],))
                if main_row:
                    location_key = self._get_location_key_for_migration(dict(main_row), jumper_num, circuit_name)
                    
                    if location_key and location_key in location_to_status:
                        new_scanned_serials[idx] = location_to_status[location_key]
                        matched_locations += 1
            
            if new_scanned_serials:
                # Save the migrated progress
                scanned_serials_json = json.dumps(new_scanned_serials)
                self.db.execute(
                    '''INSERT OR REPLACE INTO scan_progress 
                       (circuit_name, jumper_table, current_index, scanned_serials)
                       VALUES (?, ?, ?, ?)''',
                    (circuit_name, jumper_table, 0, scanned_serials_json)
                )
                total_migrated += matched_locations
                
                logging.info(f"Migrated {matched_locations} scan results for {jumper_table}")
        
        self.db.commit()
        logging.info(f"Migration complete: {total_migrated} total scan results preserved")
        return total_migrated

    def backup_scan_progress(self, circuit_name=None):
        """Create a backup of scan progress"""
        try:
            backup_dir = os.path.join(self.output_path, 'scan_backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if circuit_name:
                backup_file = os.path.join(backup_dir, f"scan_progress_backup_{circuit_name}_{timestamp}.json")
                query = "SELECT * FROM scan_progress WHERE circuit_name = ?"
                params = (circuit_name,)
            else:
                backup_file = os.path.join(backup_dir, f"scan_progress_backup_all_{timestamp}.json")
                query = "SELECT * FROM scan_progress"
                params = ()
            
            # Export scan progress
            all_progress = self.db.fetchall(query, params)
            backup_data = {
                'timestamp': timestamp,
                'circuit_name': circuit_name,
                'progress_data': [dict(row) for row in all_progress]
            }
            
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            logging.info(f"Scan progress backed up to: {backup_file}")
            return backup_file
            
        except Exception as e:
            logging.error(f"Failed to backup scan progress: {e}")
            return None
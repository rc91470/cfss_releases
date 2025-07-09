import json
import logging

class ScanController:
    """Manages the state of a scanning session for a single jumper table."""
    def __init__(self, data_manager):
        self.db = data_manager
        self.circuit_name = None
        self.jumper_table = None
        self.total_rows = 0
        self.current_index = 0
        self.scanned_serials = {}

    def load_state(self, circuit_name, jumper_table, total_rows):
        """Loads the scan progress for a given circuit and jumper table."""
        self.circuit_name = circuit_name
        self.jumper_table = jumper_table
        self.total_rows = total_rows
        self.reset_state() # Start fresh before loading

        if not circuit_name or not jumper_table:
            return

        result = self.db.fetchone(
            "SELECT current_index, scanned_serials FROM scan_progress WHERE circuit_name = ? AND jumper_table = ?",
            (self.circuit_name, self.jumper_table)
        )
        if result:
            self.current_index = min(max(result['current_index'] or 0, 0), self.total_rows - 1) if self.total_rows > 0 else 0
            try:
                raw_scanned = json.loads(result['scanned_serials']) if result['scanned_serials'] else {}
                self.scanned_serials = {int(k): v for k, v in raw_scanned.items()}
            except (json.JSONDecodeError, TypeError) as e:
                logging.error(f"JSON decode error for scanned_serials: {e}")
                self.scanned_serials = {}
            logging.info(f"Loaded scan state for {self.circuit_name}/{self.jumper_table}")
        else:
            logging.info(f"No scan state found for {self.circuit_name}/{self.jumper_table}. Initializing.")

    def save_state(self):
        """Saves the current scan progress to the database."""
        if not self.circuit_name or not self.jumper_table:
            return
        
        scanned_serials_json = json.dumps(self.scanned_serials)
        self.db.execute(
            '''
            INSERT OR REPLACE INTO scan_progress (circuit_name, jumper_table, current_index, scanned_serials)
            VALUES (?, ?, ?, ?)
            ''',
            (self.circuit_name, self.jumper_table, self.current_index, scanned_serials_json)
        )
        self.db.commit()
        logging.info(f"Saved scan state for {self.circuit_name}/{self.jumper_table}")

    def reset_state(self):
        """Resets the scan progress for the current table."""
        self.current_index = 0
        self.scanned_serials = {}

    def reset_all_states(self):
        """Resets all scan progress in the database."""
        self.db.execute("DELETE FROM scan_progress")
        self.db.commit()
        self.reset_state()

    def next_record(self):
        if self.current_index < self.total_rows - 1:
            self.current_index += 1
            return True
        return False

    def previous_record(self):
        if self.current_index > 0:
            self.current_index -= 1
            return True
        return False

    def record_scan_result(self, result):
        """Records the result of a scan for the current index."""
        self.scanned_serials[self.current_index] = result

    def get_current_status(self):
        """Gets the scan status of the current record."""
        return self.scanned_serials.get(self.current_index)

    def get_all_scan_data(self):
        """Returns the entire dictionary of scanned serials for report generation."""
        return self.scanned_serials

    def get_progress_stats(self):
        """Calculates and returns progress statistics."""
        if self.total_rows == 0:
            return {'match': 0, 'non_match': 0, 'skipped': 0, 'scanned': 0, 'total': 0, 'percentage': 0}

        stats = {'match': 0, 'non_match': 0, 'skipped': 0}
        for status in self.scanned_serials.values():
            if status is True:
                stats['match'] += 1
            elif status is False:
                stats['non_match'] += 1
            else: # is a string reason
                stats['skipped'] += 1
        
        stats['total'] = self.total_rows
        stats['scanned'] = stats['match'] + stats['non_match'] + stats['skipped']
        stats['percentage'] = (stats['scanned'] / self.total_rows * 100) if self.total_rows > 0 else 0
        return stats
    
        # Add these missing methods to your ScanController class:
    
    def get_current_index(self):
        """Returns the current index position."""
        return self.current_index
    
    def set_current_index(self, index):
        """Sets the current index position."""
        if 0 <= index < self.total_rows:
            self.current_index = index
            self.save_state()
    
    def record_scan(self, index, result):
        """Records the result of a scan for the given index."""
        self.scanned_serials[index] = result
        self.save_state()
    
    def next_record(self, total_records=None):
        """Moves to the next record."""
        if total_records is None:
            total_records = self.total_rows
        
        if self.current_index < total_records - 1:
            self.current_index += 1
            self.save_state()
            return True
        return False
    
    def reset_scan(self):
        """Resets the scan progress for the current jumper table."""
        if self.circuit_name and self.jumper_table:
            self.db.execute(
                "DELETE FROM scan_progress WHERE circuit_name = ? AND jumper_table = ?",
                (self.circuit_name, self.jumper_table)
            )
            self.db.commit()
        self.reset_state()
    
    def reset_all_circuits(self):
        """Resets all scan progress in the database."""
        self.db.execute("DELETE FROM scan_progress")
        self.db.commit()
        self.reset_state()
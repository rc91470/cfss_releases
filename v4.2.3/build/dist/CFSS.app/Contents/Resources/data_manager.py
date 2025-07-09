import sqlite3
import logging

class DataManager:
    """Handles all database interactions for the CFSS application."""
    def __init__(self, db_path):
        """Initializes the DataManager and connects to the database."""
        try:
            self.conn = sqlite3.connect(db_path)
            self.conn.row_factory = sqlite3.Row  # Access columns by name
            self.cursor = self.conn.cursor()
            logging.info(f"Database connection established to {db_path}")
        except sqlite3.Error as e:
            logging.error(f"Database connection failed: {e}")
            raise

    def execute(self, query, params=()):
        """Executes a query that doesn't return data (e.g., INSERT, UPDATE, DELETE)."""
        try:
            self.cursor.execute(query, params)
            return self.cursor
        except sqlite3.Error as e:
            logging.error(f"Query failed: {query} | Params: {params} | Error: {e}")
            raise

    def fetchone(self, query, params=()):
        """Executes a query and fetches a single result."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Fetchone query failed: {query} | Params: {params} | Error: {e}")
            return None

    def fetchall(self, query, params=()):
        """Executes a query and fetches all results."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Fetchall query failed: {query} | Params: {params} | Error: {e}")
            return []

    def commit(self):
        """Commits the current transaction."""
        try:
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database commit failed: {e}")

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            logging.info("Database connection closed.")

    def get_table_columns(self, table_name):
        """Retrieves column names for a given table."""
        result = self.fetchall(f"PRAGMA table_info({table_name})")
        return [row['name'] for row in result]
"""
Database manager for SQLite operations
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from .schema import CREATE_TABLES, INITIAL_DATA


class DatabaseManager:
    def __init__(self, db_path: str = "database/cafe_manager.db"):
        """Initialize database manager"""
        self.db_path = db_path
        self.ensure_database_directory()
        self.init_database()
    
    def ensure_database_directory(self):
        """Create database directory if it doesn't exist"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enables column access by name
        return conn
    
    def init_database(self):
        """Initialize database with tables and initial data"""
        with self.get_connection() as conn:
            # Create tables
            for table_name, create_sql in CREATE_TABLES.items():
                conn.execute(create_sql)
                print(f"✓ Created table: {table_name}")
            
            # Insert initial data if tables are empty
            self.insert_initial_data(conn)
            conn.commit()
    
    def insert_initial_data(self, conn: sqlite3.Connection):
        """Insert initial data if tables are empty"""
        # Insert pricing plans
        cursor = conn.execute("SELECT COUNT(*) FROM pricing_plans")
        if cursor.fetchone()[0] == 0:
            for plan in INITIAL_DATA['pricing_plans']:
                conn.execute("""
                    INSERT INTO pricing_plans 
                    (name, hourly_rate, minimum_charge, is_default, is_active)
                    VALUES (?, ?, ?, ?, ?)
                """, plan)
            print("✓ Inserted initial pricing plans")
        
        # Insert sample PCs
        cursor = conn.execute("SELECT COUNT(*) FROM pcs")
        if cursor.fetchone()[0] == 0:
            for pc in INITIAL_DATA['pcs']:
                conn.execute("""
                    INSERT INTO pcs (name, ip_address, mac_address, location)
                    VALUES (?, ?, ?, ?)
                """, pc)
            print("✓ Inserted sample PCs")
    
    def execute_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Execute SELECT query and return results"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute INSERT/UPDATE/DELETE query and return affected rows"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    def get_last_insert_id(self) -> int:
        """Get the ID of the last inserted row"""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT last_insert_rowid()")
            return cursor.fetchone()[0]


# Global database instance
db_manager = DatabaseManager()

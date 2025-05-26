"""
PC model for managing computer workstations
"""
from datetime import datetime
from typing import Optional, List
from core.database.manager import db_manager


class PC:
    def __init__(self, id: int = None, name: str = "", ip_address: str = "",
                 mac_address: str = "", location: str = "", status: str = "offline",
                 is_active: bool = True, last_seen: datetime = None):
        self.id = id
        self.name = name
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.location = location
        self.status = status
        self.is_active = is_active
        self.last_seen = last_seen
    
    @classmethod
    def create(cls, name: str, ip_address: str, mac_address: str = "", 
               location: str = "") -> 'PC':
        """Create new PC in database"""
        query = """
            INSERT INTO pcs (name, ip_address, mac_address, location)
            VALUES (?, ?, ?, ?)
        """
        db_manager.execute_update(query, (name, ip_address, mac_address, location))
        pc_id = db_manager.get_last_insert_id()
        
        return cls(id=pc_id, name=name, ip_address=ip_address, 
                  mac_address=mac_address, location=location)
    
    @classmethod
    def get_by_id(cls, pc_id: int) -> Optional['PC']:
        """Get PC by ID"""
        query = "SELECT * FROM pcs WHERE id = ? AND is_active = 1"
        rows = db_manager.execute_query(query, (pc_id,))
        
        if rows:
            row = rows[0]
            return cls(
                id=row['id'],
                name=row['name'],
                ip_address=row['ip_address'],
                mac_address=row['mac_address'],
                location=row['location'],
                status=row['status'],
                is_active=bool(row['is_active']),
                last_seen=row['last_seen']
            )
        return None
    
    @classmethod
    def get_all(cls) -> List['PC']:
        """Get all active PCs"""
        query = "SELECT * FROM pcs WHERE is_active = 1 ORDER BY name"
        rows = db_manager.execute_query(query)
        
        pcs = []
        for row in rows:
            pcs.append(cls(
                id=row['id'],
                name=row['name'],
                ip_address=row['ip_address'],
                mac_address=row['mac_address'],
                location=row['location'],
                status=row['status'],
                is_active=bool(row['is_active']),
                last_seen=row['last_seen']
            ))
        return pcs
    
    def update_status(self, status: str) -> bool:
        """Update PC status"""
        query = """
            UPDATE pcs 
            SET status = ?, last_seen = CURRENT_TIMESTAMP 
            WHERE id = ?
        """
        rows_affected = db_manager.execute_update(query, (status, self.id))
        if rows_affected > 0:
            self.status = status
            self.last_seen = datetime.now()
            return True
        return False
    
    def is_available(self) -> bool:
        """Check if PC is available for use"""
        return self.status in ['offline', 'idle'] and self.is_active
    
    def __str__(self):
        return f"PC({self.name}: {self.ip_address}, Status: {self.status})"

"""
User model for managing customers
"""
from datetime import datetime
from typing import Optional, List
from core.database.manager import db_manager


class User:
    def __init__(self, id: int = None, username: str = "", full_name: str = "", 
                 email: str = "", phone: str = "", balance: float = 0.0, 
                 is_active: bool = True):
        self.id = id
        self.username = username
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.balance = balance
        self.is_active = is_active
    
    @classmethod
    def create(cls, username: str, full_name: str, email: str = "", 
               phone: str = "", initial_balance: float = 0.0) -> 'User':
        """Create new user in database"""
        query = """
            INSERT INTO users (username, full_name, email, phone, balance)
            VALUES (?, ?, ?, ?, ?)
        """
        db_manager.execute_update(query, (username, full_name, email, phone, initial_balance))
        user_id = db_manager.get_last_insert_id()
        
        return cls(id=user_id, username=username, full_name=full_name, 
                  email=email, phone=phone, balance=initial_balance)
    
    @classmethod
    def get_by_id(cls, user_id: int) -> Optional['User']:
        """Get user by ID"""
        query = "SELECT * FROM users WHERE id = ? AND is_active = 1"
        rows = db_manager.execute_query(query, (user_id,))
        
        if rows:
            row = rows[0]
            return cls(
                id=row['id'],
                username=row['username'],
                full_name=row['full_name'],
                email=row['email'],
                phone=row['phone'],
                balance=float(row['balance']),
                is_active=bool(row['is_active'])
            )
        return None
    
    @classmethod
    def get_by_username(cls, username: str) -> Optional['User']:
        """Get user by username"""
        query = "SELECT * FROM users WHERE username = ? AND is_active = 1"
        rows = db_manager.execute_query(query, (username,))
        
        if rows:
            row = rows[0]
            return cls(
                id=row['id'],
                username=row['username'],
                full_name=row['full_name'],
                email=row['email'],
                phone=row['phone'],
                balance=float(row['balance']),
                is_active=bool(row['is_active'])
            )
        return None
    
    @classmethod
    def get_all(cls) -> List['User']:
        """Get all active users"""
        query = "SELECT * FROM users WHERE is_active = 1 ORDER BY full_name"
        rows = db_manager.execute_query(query)
        
        users = []
        for row in rows:
            users.append(cls(
                id=row['id'],
                username=row['username'],
                full_name=row['full_name'],
                email=row['email'],
                phone=row['phone'],
                balance=float(row['balance']),
                is_active=bool(row['is_active'])
            ))
        return users
    
    def update_balance(self, amount: float, description: str = "") -> bool:
        """Update user balance (positive for add, negative for deduct)"""
        new_balance = self.balance + amount
        if new_balance < 0:
            return False  # Insufficient balance
        
        # Update user balance
        query = "UPDATE users SET balance = ? WHERE id = ?"
        rows_affected = db_manager.execute_update(query, (new_balance, self.id))
        
        if rows_affected > 0:
            # Record transaction
            trans_type = "credit" if amount > 0 else "debit"
            trans_query = """
                INSERT INTO transactions (user_id, amount, transaction_type, description)
                VALUES (?, ?, ?, ?)
            """
            db_manager.execute_update(trans_query, (self.id, abs(amount), trans_type, description))
            
            self.balance = new_balance
            return True
        return False
    
    def save(self) -> bool:
        """Save user changes to database"""
        if self.id:
            # Update existing user
            query = """
                UPDATE users 
                SET username = ?, full_name = ?, email = ?, phone = ?, 
                    balance = ?, is_active = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            rows_affected = db_manager.execute_update(
                query, (self.username, self.full_name, self.email, self.phone, 
                       self.balance, self.is_active, self.id)
            )
            return rows_affected > 0
        return False
    
    def __str__(self):
        return f"User({self.username}: {self.full_name}, Balance: ${self.balance:.2f})"

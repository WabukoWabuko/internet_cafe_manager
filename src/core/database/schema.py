"""
Database schema definitions for Internet Cafe Manager
"""

CREATE_TABLES = {
    'users': '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            full_name VARCHAR(100) NOT NULL,
            email VARCHAR(100),
            phone VARCHAR(20),
            balance DECIMAL(10,2) DEFAULT 0.00,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''',
    
    'pcs': '''
        CREATE TABLE IF NOT EXISTS pcs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) UNIQUE NOT NULL,
            ip_address VARCHAR(15) UNIQUE NOT NULL,
            mac_address VARCHAR(17),
            location VARCHAR(100),
            status VARCHAR(20) DEFAULT 'offline',
            is_active BOOLEAN DEFAULT 1,
            last_seen TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''',
    
    'sessions': '''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            pc_id INTEGER NOT NULL,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP,
            duration_minutes INTEGER DEFAULT 0,
            cost DECIMAL(10,2) DEFAULT 0.00,
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (pc_id) REFERENCES pcs (id)
        )
    ''',
    
    'transactions': '''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_id INTEGER,
            amount DECIMAL(10,2) NOT NULL,
            transaction_type VARCHAR(20) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        )
    ''',
    
    'pricing_plans': '''
        CREATE TABLE IF NOT EXISTS pricing_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) UNIQUE NOT NULL,
            hourly_rate DECIMAL(10,2) NOT NULL,
            minimum_charge DECIMAL(10,2) DEFAULT 0.00,
            is_default BOOLEAN DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''',
    
    'system_logs': '''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action VARCHAR(100) NOT NULL,
            user_id INTEGER,
            pc_id INTEGER,
            details TEXT,
            ip_address VARCHAR(15),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (pc_id) REFERENCES pcs (id)
        )
    '''
}

INITIAL_DATA = {
    'pricing_plans': [
        ('Standard Rate', 2.00, 0.50, 1, 1),  # $2/hour, 50¢ minimum, default, active
        ('Student Rate', 1.50, 0.50, 0, 1),   # $1.50/hour, 50¢ minimum
        ('Premium Rate', 3.00, 1.00, 0, 1)    # $3/hour, $1 minimum
    ],
    'pcs': [
        ('PC-001', '192.168.1.101', '00:11:22:33:44:55', 'Front Row Left'),
        ('PC-002', '192.168.1.102', '00:11:22:33:44:56', 'Front Row Center'),
        ('PC-003', '192.168.1.103', '00:11:22:33:44:57', 'Front Row Right'),
        ('PC-004', '192.168.1.104', '00:11:22:33:44:58', 'Back Row Left'),
        ('PC-005', '192.168.1.105', '00:11:22:33:44:59', 'Back Row Right')
    ]
}

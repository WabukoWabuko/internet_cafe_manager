#!/usr/bin/env python3
"""
Internet Cafe Manager - Main Entry Point
"""

def main():
    print("🏪 Internet Cafe Manager v1.0")
    print("=" * 40)
    
    try:
        # Import here to test database connection
        from src.core.database.manager import db_manager
        print("✅ Database connection successful")
        
        from src.models.user import User
        from src.models.pc import PC
        print("✅ Models imported successfully")
        
        # Quick test
        pcs = PC.get_all()
        users = User.get_all()
        print(f"📊 Found {len(pcs)} PCs and {len(users)} users in database")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print("\n🚀 System ready!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test database setup and models
"""
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Now import using absolute imports
from core.database.manager import db_manager
from models.user import User
from models.pc import PC

def test_database():
    print("🔧 Testing Database Setup...")
    
    # Test PC operations
    print("\n📺 Testing PC Operations:")
    pcs = PC.get_all()
    print(f"Found {len(pcs)} PCs:")
    for pc in pcs:
        print(f"  - {pc}")
    
    # Test User operations
    print("\n👤 Testing User Operations:")
    
    # Create a test user
    test_user = User.create(
        username="testuser",
        full_name="Test User",
        email="test@example.com",
        phone="123-456-7890",
        initial_balance=10.00
    )
    print(f"Created user: {test_user}")
    
    # Add money to user account
    success = test_user.update_balance(5.00, "Initial top-up")
    print(f"Balance update success: {success}")
    print(f"New balance: ${test_user.balance:.2f}")
    
    # Get all users
    all_users = User.get_all()
    print(f"\nAll users ({len(all_users)}):")
    for user in all_users:
        print(f"  - {user}")
    
    print("\n✅ Database test completed successfully!")

if __name__ == "__main__":
    test_database()

#!/usr/bin/env python3
"""
Test XML configuration system
"""
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.config.xml_manager import config_manager
from core.config.settings import settings

def test_xml_configuration():
    print("🔧 Testing XML Configuration System...")
    
    # Test 1: Check if config files were created
    print("\n📁 Testing Config File Creation:")
    config_files = [
        "config/settings.xml",
        "config/pc_profiles.xml", 
        "config/pricing.xml"
    ]
    
    for file_path in config_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path} - EXISTS")
        else:
            print(f"  ❌ {file_path} - MISSING")
    
    # Test 2: Load and display settings
    print("\n⚙️ Testing Settings Loading:")
    print(f"  Cafe Name: {settings.cafe_name}")
    print(f"  Currency: {settings.currency} ({settings.get_currency_symbol()})")
    print(f"  Server Port: {settings.server_port}")
    print(f"  Theme: {settings.theme}")
    print(f"  Auto Logout: {settings.auto_logout}")
    print(f"  Supabase Sync: {settings.sync_enabled}")
    
    # Test 3: Test PC Profiles
    print("\n💻 Testing PC Profiles:")
    pc_profiles = settings.get_pc_profiles()
    print(f"  Found {len(pc_profiles)} PC profiles:")
    for profile in pc_profiles:
        print(f"    - {profile['name']} ({profile['type']})")
        print(f"      Max Session: {profile['time_limits']['max_session_hours']}h")
        print(f"      Allow Games: {profile['software']['allow_games']}")
    
    # Test 4: Test Pricing Plans
    print("\n💰 Testing Pricing Plans:")
    pricing_plans = settings.get_pricing_plans()
    print(f"  Found {len(pricing_plans)} pricing plans:")
    for plan in pricing_plans:
        rate = plan['hourly_rate']
        minimum = plan['minimum_charge']
        default = plan['is_default']
        active = plan['is_active']
        formatted_rate = settings.format_currency(rate)
        formatted_min = settings.format_currency(minimum)
        
        status = []
        if default:
            status.append("DEFAULT")
        if active:
            status.append("ACTIVE")
        
        print(f"    - {plan['name']}: {formatted_rate}/hour (min: {formatted_min}) {status}")
    
    # Test 5: Test Default Pricing Plan
    print("\n🎯 Testing Default Pricing Plan:")
    default_plan = settings.get_default_pricing_plan()
    if default_plan:
        print(f"  Default Plan: {default_plan['name']}")
        print(f"  Rate: {settings.format_currency(default_plan['hourly_rate'])}/hour")
    else:
        print("  ❌ No default pricing plan found!")
    
    # Test 6: Test Settings Update
    print("\n🔄 Testing Settings Update:")
    original_name = settings.cafe_name
    success = settings.update_cafe_name("Test Internet Cafe")
    new_name = settings.cafe_name
    
    print(f"  Original name: {original_name}")
    print(f"  Update success: {success}")
    print(f"  New name: {new_name}")
    
    # Restore original name
    settings.update_cafe_name(original_name)
    print(f"  Restored name: {settings.cafe_name}")
    
    # Test 7: Test Currency Formatting
    print("\n💱 Testing Currency Formatting:")
    test_amounts = [1.0, 2.50, 15.99, 100.00]
    for amount in test_amounts:
        formatted = settings.format_currency(amount)
        print(f"  {amount} -> {formatted}")
    
    # Test 8: Test Profile Filtering
    print("\n🔍 Testing Profile Filtering:")
    gaming_profiles = settings.get_pc_profiles_by_type("gaming")
    office_profiles = settings.get_pc_profiles_by_type("office")
    basic_profiles = settings.get_pc_profiles_by_type("basic")
    
    print(f"  Gaming profiles: {len(gaming_profiles)}")
    print(f"  Office profiles: {len(office_profiles)}")
    print(f"  Basic profiles: {len(basic_profiles)}")
    
    # Test 9: Test Supabase Configuration
    print("\n☁️ Testing Supabase Configuration:")
    print(f"  URL: {settings.supabase_url}")
    print(f"  Configured: {settings.is_supabase_configured()}")
    
    print("\n✅ XML Configuration test completed successfully!")

def test_raw_xml_operations():
    print("\n🔧 Testing Raw XML Operations...")
    
    # Test direct XML manager operations
    raw_settings = config_manager.get_settings()
    print(f"Raw settings sections: {list(raw_settings.keys())}")
    
    # Test setting update
    success = config_manager.update_setting("general", "test_key", "test_value")
    print(f"Direct update success: {success}")
    
    # Verify update
    updated_settings = config_manager.get_settings()
    test_value = updated_settings.get('general', {}).get('test_key')
    print(f"Retrieved test value: {test_value}")
    
    print("✅ Raw XML operations test completed!")

if __name__ == "__main__":
    test_xml_configuration()
    test_raw_xml_operations()

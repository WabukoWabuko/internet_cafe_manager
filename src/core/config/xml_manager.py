"""
XML Configuration Manager for Internet Cafe Manager
"""
import xml.etree.ElementTree as ET
import os
from typing import Dict, Any, Optional, List


class XMLConfigManager:
    def __init__(self, config_dir: str = "config"):
        """Initialize XML configuration manager"""
        self.config_dir = config_dir
        self.ensure_config_directory()
        self.settings_file = os.path.join(config_dir, "settings.xml")
        self.pc_profiles_file = os.path.join(config_dir, "pc_profiles.xml")
        self.pricing_file = os.path.join(config_dir, "pricing.xml")
        
        # Initialize config files if they don't exist
        self.init_config_files()
    
    def ensure_config_directory(self):
        """Create config directory if it doesn't exist"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            print(f"✓ Created config directory: {self.config_dir}")
    
    def init_config_files(self):
        """Initialize configuration files with default values"""
        if not os.path.exists(self.settings_file):
            self.create_default_settings()
        
        if not os.path.exists(self.pc_profiles_file):
            self.create_default_pc_profiles()
        
        if not os.path.exists(self.pricing_file):
            self.create_default_pricing()
    
    def create_default_settings(self):
        """Create default settings.xml file"""
        root = ET.Element("cafe_settings")
        
        # General settings
        general = ET.SubElement(root, "general")
        ET.SubElement(general, "cafe_name").text = "My Internet Cafe"
        ET.SubElement(general, "currency").text = "USD"
        ET.SubElement(general, "timezone").text = "UTC"
        ET.SubElement(general, "language").text = "en"
        ET.SubElement(general, "theme").text = "dark"
        
        # Network settings
        network = ET.SubElement(root, "network")
        ET.SubElement(network, "server_port").text = "8080"
        ET.SubElement(network, "broadcast_interval").text = "30"
        ET.SubElement(network, "timeout").text = "5"
        ET.SubElement(network, "max_connections").text = "50"
        
        # Database settings
        database = ET.SubElement(root, "database")
        ET.SubElement(database, "backup_interval").text = "24"
        ET.SubElement(database, "auto_cleanup").text = "true"
        ET.SubElement(database, "keep_logs_days").text = "30"
        
        # Supabase settings (cloud sync)
        supabase = ET.SubElement(root, "supabase")
        ET.SubElement(supabase, "url").text = "your_supabase_url"
        ET.SubElement(supabase, "key").text = "your_api_key"
        ET.SubElement(supabase, "sync_enabled").text = "false"
        ET.SubElement(supabase, "sync_interval").text = "300"
        
        # Business settings
        business = ET.SubElement(root, "business")
        ET.SubElement(business, "auto_logout").text = "true"
        ET.SubElement(business, "warning_minutes").text = "5"
        ET.SubElement(business, "grace_period").text = "2"
        ET.SubElement(business, "minimum_session").text = "15"
        
        self._write_xml_file(root, self.settings_file)
        print("✓ Created default settings.xml")
    
    def create_default_pc_profiles(self):
        """Create default pc_profiles.xml file"""
        root = ET.Element("pc_profiles")
        
        # Sample PC configurations
        pc_configs = [
            {"name": "Gaming-001", "type": "gaming", "specs": "High-end gaming PC"},
            {"name": "Office-001", "type": "office", "specs": "Standard office PC"},
            {"name": "Basic-001", "type": "basic", "specs": "Basic browsing PC"}
        ]
        
        for config in pc_configs:
            pc = ET.SubElement(root, "pc_profile")
            ET.SubElement(pc, "name").text = config["name"]
            ET.SubElement(pc, "type").text = config["type"]
            ET.SubElement(pc, "specs").text = config["specs"]
            
            # Software restrictions
            software = ET.SubElement(pc, "software")
            ET.SubElement(software, "allow_games").text = "true" if config["type"] == "gaming" else "false"
            ET.SubElement(software, "allow_downloads").text = "false"
            ET.SubElement(software, "allow_installs").text = "false"
            
            # Time restrictions
            time_limits = ET.SubElement(pc, "time_limits")
            ET.SubElement(time_limits, "max_session_hours").text = "8" if config["type"] == "gaming" else "4"
            ET.SubElement(time_limits, "idle_timeout").text = "10"
        
        self._write_xml_file(root, self.pc_profiles_file)
        print("✓ Created default pc_profiles.xml")
    
    def create_default_pricing(self):
        """Create default pricing.xml file"""
        root = ET.Element("pricing_plans")
        
        # Default pricing plans
        plans = [
            {"name": "Standard", "rate": "2.00", "minimum": "0.50", "default": "true"},
            {"name": "Student", "rate": "1.50", "minimum": "0.50", "default": "false"},
            {"name": "Gaming", "rate": "3.00", "minimum": "1.00", "default": "false"},
            {"name": "Premium", "rate": "4.00", "minimum": "1.00", "default": "false"}
        ]
        
        for plan in plans:
            pricing = ET.SubElement(root, "pricing_plan")
            ET.SubElement(pricing, "name").text = plan["name"]
            ET.SubElement(pricing, "hourly_rate").text = plan["rate"]
            ET.SubElement(pricing, "minimum_charge").text = plan["minimum"]
            ET.SubElement(pricing, "is_default").text = plan["default"]
            ET.SubElement(pricing, "is_active").text = "true"
            
            # Time-based pricing (optional)
            time_based = ET.SubElement(pricing, "time_based")
            ET.SubElement(time_based, "peak_hours").text = "18:00-22:00"
            ET.SubElement(time_based, "peak_multiplier").text = "1.5"
            ET.SubElement(time_based, "weekend_multiplier").text = "1.2"
        
        self._write_xml_file(root, self.pricing_file)
        print("✓ Created default pricing.xml")
    
    def _write_xml_file(self, root: ET.Element, filepath: str):
        """Write XML element to file with proper formatting"""
        # Create formatted XML string
        self._indent_xml(root)
        tree = ET.ElementTree(root)
        tree.write(filepath, encoding='utf-8', xml_declaration=True)
    
    def _indent_xml(self, elem, level=0):
        """Add proper indentation to XML for readability"""
        indent = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = indent + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = indent
            for elem in elem:
                self._indent_xml(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = indent
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = indent
    
    def get_settings(self) -> Dict[str, Any]:
        """Load and return all settings from settings.xml"""
        try:
            tree = ET.parse(self.settings_file)
            root = tree.getroot()
            
            settings = {}
            for section in root:
                section_dict = {}
                for item in section:
                    # Convert string values to appropriate types
                    value = item.text
                    if value.lower() in ['true', 'false']:
                        value = value.lower() == 'true'
                    elif value.isdigit():
                        value = int(value)
                    elif self._is_float(value):
                        value = float(value)
                    
                    section_dict[item.tag] = value
                settings[section.tag] = section_dict
            
            return settings
        except Exception as e:
            print(f"Error loading settings: {e}")
            return {}
    
    def update_setting(self, section: str, key: str, value: str) -> bool:
        """Update a specific setting in settings.xml"""
        try:
            tree = ET.parse(self.settings_file)
            root = tree.getroot()
            
            # Find the section
            section_elem = root.find(section)
            if section_elem is None:
                # Create section if it doesn't exist
                section_elem = ET.SubElement(root, section)
            
            # Find or create the key
            key_elem = section_elem.find(key)
            if key_elem is None:
                key_elem = ET.SubElement(section_elem, key)
            
            key_elem.text = str(value)
            
            self._write_xml_file(root, self.settings_file)
            return True
            
        except Exception as e:
            print(f"Error updating setting: {e}")
            return False
    
    def get_pc_profiles(self) -> List[Dict[str, Any]]:
        """Load and return all PC profiles"""
        try:
            tree = ET.parse(self.pc_profiles_file)
            root = tree.getroot()
            
            profiles = []
            for pc_profile in root.findall('pc_profile'):
                profile = {}
                for child in pc_profile:
                    if child.tag in ['software', 'time_limits']:
                        # Handle nested elements
                        nested_dict = {}
                        for nested_child in child:
                            value = nested_child.text
                            if value.lower() in ['true', 'false']:
                                value = value.lower() == 'true'
                            elif value.isdigit():
                                value = int(value)
                            nested_dict[nested_child.tag] = value
                        profile[child.tag] = nested_dict
                    else:
                        profile[child.tag] = child.text
                profiles.append(profile)
            
            return profiles
        except Exception as e:
            print(f"Error loading PC profiles: {e}")
            return []
    
    def get_pricing_plans(self) -> List[Dict[str, Any]]:
        """Load and return all pricing plans"""
        try:
            tree = ET.parse(self.pricing_file)
            root = tree.getroot()
            
            plans = []
            for pricing_plan in root.findall('pricing_plan'):
                plan = {}
                for child in pricing_plan:
                    if child.tag == 'time_based':
                        # Handle time-based pricing
                        time_based = {}
                        for nested_child in child:
                            value = nested_child.text
                            if self._is_float(value):
                                value = float(value)
                            time_based[nested_child.tag] = value
                        plan[child.tag] = time_based
                    else:
                        value = child.text
                        if value.lower() in ['true', 'false']:
                            value = value.lower() == 'true'
                        elif self._is_float(value):
                            value = float(value)
                        plan[child.tag] = value
                plans.append(plan)
            
            return plans
        except Exception as e:
            print(f"Error loading pricing plans: {e}")
            return []
    
    def _is_float(self, value: str) -> bool:
        """Check if string can be converted to float"""
        try:
            float(value)
            return True
        except ValueError:
            return False


# Global configuration manager instance
config_manager = XMLConfigManager()

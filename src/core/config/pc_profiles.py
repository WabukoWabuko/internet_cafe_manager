"""
PC Profiles XML Manager
"""
import xml.etree.ElementTree as ET
import os
from typing import List, Dict, Any, Optional


class PCProfileManager:
    def __init__(self, profiles_file: str = "config/pc_profiles.xml"):
        self.profiles_file = profiles_file
        self.ensure_config_directory()
        self.profiles = []
        self.load_profiles()
    
    def ensure_config_directory(self):
        """Create config directory if it doesn't exist"""
        config_dir = os.path.dirname(self.profiles_file)
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir)
    
    def create_default_profiles(self):
        """Create default PC profiles file"""
        default_profiles = """<?xml version="1.0" encoding="UTF-8"?>
<pc_profiles>
    <pc>
        <name>PC-001</name>
        <ip_address>192.168.1.101</ip_address>
        <mac_address>00:11:22:33:44:55</mac_address>
        <location>Front Row Left</location>
        <specs>
            <cpu>Intel i5-10400</cpu>
            <ram>8GB</ram>
            <storage>256GB SSD</storage>
            <gpu>GTX 1650</gpu>
        </specs>
        <software>
            <os>Windows 10</os>
            <games>Steam, Epic Games</games>
            <office>Microsoft Office</office>
        </software>
        <restrictions>
            <max_session_hours>8</max_session_hours>
            <allowed_categories>gaming,office,internet</allowed_categories>
        </restrictions>
    </pc>
    <pc>
        <name>PC-002</name>
        <ip_address>192.168.1.102</ip_address>
        <mac_address>00:11:22:33:44:56</mac_address>
        <location>Front Row Center</location>
        <specs>
            <cpu>Intel i5-10400</cpu>
            <ram>8GB</ram>
            <storage>256GB SSD</storage>
            <gpu>GTX 1650</gpu>
        </specs>
        <software>
            <os>Windows 10</os>
            <games>Steam, Epic Games</games>
            <office>Microsoft Office</office>
        </software>
        <restrictions>
            <max_session_hours>8</max_session_hours>
            <allowed_categories>gaming,office,internet</allowed_categories>
        </restrictions>
    </pc>
    <pc>
        <name>PC-003</name>
        <ip_address>192.168.1.103</ip_address>
        <mac_address>00:11:22:33:44:57</mac_address>
        <location>Front Row Right</location>
        <specs>
            <cpu>Intel i7-10700</cpu>
            <ram>16GB</ram>
            <storage>512GB SSD</storage>
            <gpu>RTX 3060</gpu>
        </specs>
        <software>
            <os>Windows 10</os>
            <games>Steam, Epic Games, Battle.net</games>
            <office>Microsoft Office</office>
            <creative>Adobe Suite</creative>
        </software>
        <restrictions>
            <max_session_hours>12</max_session_hours>
            <allowed_categories>gaming,office,internet,creative</allowed_categories>
        </restrictions>
    </pc>
</pc_profiles>"""
        
        try:
            with open(self.profiles_file, 'w', encoding='utf-8') as f:
                f.write(default_profiles)
            print(f"✅ Created default PC profiles: {self.profiles_file}")
        except Exception as e:
            print(f"❌ Error creating PC profiles: {e}")
    
    def load_profiles(self) -> bool:
        """Load PC profiles from XML file"""
        try:
            if not os.path.exists(self.profiles_file):
                self.create_default_profiles()
            
            tree = ET.parse(self.profiles_file)
            root = tree.getroot()
            
            self.profiles = []
            for pc_element in root.findall('pc'):
                profile = self._parse_pc_profile(pc_element)
                self.profiles.append(profile)
            
            print(f"✅ Loaded {len(self.profiles)} PC profiles")
            return True
            
        except Exception as e:
            print(f"❌ Error loading PC profiles: {e}")
            return False
    
    def _parse_pc_profile(self, pc_element: ET.Element) -> Dict[str, Any]:
        """Parse single PC profile from XML element"""
        profile = {}
        
        # Basic info
        profile['name'] = pc_element.find('name').text if pc_element.find('name') is not None else ""
        profile['ip_address'] = pc_element.find('ip_address').text if pc_element.find('ip_address') is not None else ""
        profile['mac_address'] = pc_element.find('mac_address').text if pc_element.find('mac_address') is not None else ""
        profile['location'] = pc_element.find('location').text if pc_element.find('location') is not None else ""
        
        # Specs
        specs_element = pc_element.find('specs')
        if specs_element is not None:
            profile['specs'] = {}
            for spec in specs_element:
                profile['specs'][spec.tag] = spec.text
        
        # Software
        software_element = pc_element.find('software')
        if software_element is not None:
            profile['software'] = {}
            for software in software_element:
                profile['software'][software.tag] = software.text
        
        # Restrictions
        restrictions_element = pc_element.find('restrictions')
        if restrictions_element is not None:
            profile['restrictions'] = {}
            for restriction in restrictions_element:
                if restriction.tag == 'max_session_hours':
                    profile['restrictions'][restriction.tag] = int(restriction.text)
                else:
                    profile['restrictions'][restriction.tag] = restriction.text
        
        return profile
    
    def get_profile(self, pc_name: str) -> Optional[Dict[str, Any]]:
        """Get PC profile by name"""
        for profile in self.profiles:
            if profile.get('name') == pc_name:
                return profile
        return None
    
    def get_all_profiles(self) -> List[Dict[str, Any]]:
        """Get all PC profiles"""
        return self.profiles.copy()
    
    def add_profile(self, profile: Dict[str, Any]) -> bool:
        """Add new PC profile"""
        # Check if PC name already exists
        if self.get_profile(profile.get('name', '')):
            print(f"❌ PC profile '{profile.get('name')}' already exists")
            return False
        
        self.profiles.append(profile)
        return self.save_profiles()
    
    def update_profile(self, pc_name: str, updated_profile: Dict[str, Any]) -> bool:
        """Update existing PC profile"""
        for i, profile in enumerate(self.profiles):
            if profile.get('name') == pc_name:
                self.profiles[i] = updated_profile
                return self.save_profiles()
        return False
    
    def save_profiles(self) -> bool:
        """Save PC profiles to XML file"""
        try:
            root = ET.Element('pc_profiles')
            
            for profile in self.profiles:
                pc_element = ET.SubElement(root, 'pc')
                self._profile_to_xml(pc_element, profile)
            
            tree = ET.ElementTree(root)
            ET.indent(tree, space="    ", level=0)
            tree.write(self.profiles_file, encoding='utf-8', xml_declaration=True)
            print(f"✅ PC profiles saved to {self.profiles_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving PC profiles: {e}")
            return False
    
    def _profile_to_xml(self, pc_element: ET.Element, profile: Dict[str, Any]):
        """Convert profile dictionary to XML elements"""
        # Basic info
        for key in ['name', 'ip_address', 'mac_address', 'location']:
            if key in profile:
                elem = ET.SubElement(pc_element, key)
                elem.text = str(profile[key])
        
        # Specs
        if 'specs' in profile:
            specs_elem = ET.SubElement(pc_element, 'specs')
            for key, value in profile['specs'].items():
                spec_elem = ET.SubElement(specs_elem, key)
                spec_elem.text = str(value)
        
        # Software
        if 'software' in profile:
            software_elem = ET.SubElement(pc_element, 'software')
            for key, value in profile['software'].items():
                soft_elem = ET.SubElement(software_elem, key)
                soft_elem.text = str(value)
        
        # Restrictions
        if 'restrictions' in profile:
            restrictions_elem = ET.SubElement(pc_element, 'restrictions')
            for key, value in profile['restrictions'].items():
                restrict_elem = ET.SubElement(restrictions_elem, key)
                restrict_elem.text = str(value)


# Global PC profile manager
pc_profile_manager = PCProfileManager()

"""
Settings wrapper for easy access to configuration values
"""
from typing import Any, Dict, List
from .xml_manager import config_manager


class Settings:
    """Easy access to application settings"""
    
    def __init__(self):
        self._settings = None
        self._pc_profiles = None
        self._pricing_plans = None
        self.reload()
    
    def reload(self):
        """Reload all settings from XML files"""
        self._settings = config_manager.get_settings()
        self._pc_profiles = config_manager.get_pc_profiles()
        self._pricing_plans = config_manager.get_pricing_plans()
    
    # General Settings
    @property
    def cafe_name(self) -> str:
        return self._settings.get('general', {}).get('cafe_name', 'My Internet Cafe')
    
    @property
    def currency(self) -> str:
        return self._settings.get('general', {}).get('currency', 'USD')
    
    @property
    def timezone(self) -> str:
        return self._settings.get('general', {}).get('timezone', 'UTC')
    
    @property
    def language(self) -> str:
        return self._settings.get('general', {}).get('language', 'en')
    
    @property
    def theme(self) -> str:
        return self._settings.get('general', {}).get('theme', 'dark')
    
    # Network Settings
    @property
    def server_port(self) -> int:
        return self._settings.get('network', {}).get('server_port', 8080)
    
    @property
    def broadcast_interval(self) -> int:
        return self._settings.get('network', {}).get('broadcast_interval', 30)
    
    @property
    def network_timeout(self) -> int:
        return self._settings.get('network', {}).get('timeout', 5)
    
    @property
    def max_connections(self) -> int:
        return self._settings.get('network', {}).get('max_connections', 50)
    
    # Database Settings
    @property
    def backup_interval(self) -> int:
        return self._settings.get('database', {}).get('backup_interval', 24)
    
    @property
    def auto_cleanup(self) -> bool:
        return self._settings.get('database', {}).get('auto_cleanup', True)
    
    @property
    def keep_logs_days(self) -> int:
        return self._settings.get('database', {}).get('keep_logs_days', 30)
    
    # Supabase Settings
    @property
    def supabase_url(self) -> str:
        return self._settings.get('supabase', {}).get('url', '')
    
    @property
    def supabase_key(self) -> str:
        return self._settings.get('supabase', {}).get('key', '')
    
    @property
    def sync_enabled(self) -> bool:
        return self._settings.get('supabase', {}).get('sync_enabled', False)
    
    @property
    def sync_interval(self) -> int:
        return self._settings.get('supabase', {}).get('sync_interval', 300)
    
    # Business Settings
    @property
    def auto_logout(self) -> bool:
        return self._settings.get('business', {}).get('auto_logout', True)
    
    @property
    def warning_minutes(self) -> int:
        return self._settings.get('business', {}).get('warning_minutes', 5)
    
    @property
    def grace_period(self) -> int:
        return self._settings.get('business', {}).get('grace_period', 2)
    
    @property
    def minimum_session(self) -> int:
        return self._settings.get('business', {}).get('minimum_session', 15)
    
    # PC Profiles
    def get_pc_profiles(self) -> List[Dict[str, Any]]:
        """Get all PC profiles"""
        return self._pc_profiles or []
    
    def get_pc_profile_by_name(self, name: str) -> Dict[str, Any]:
        """Get specific PC profile by name"""
        for profile in self._pc_profiles or []:
            if profile.get('name') == name:
                return profile
        return {}
    
    def get_pc_profiles_by_type(self, pc_type: str) -> List[Dict[str, Any]]:
        """Get PC profiles by type (gaming, office, basic)"""
        return [p for p in self._pc_profiles or [] if p.get('type') == pc_type]
    
    # Pricing Plans
    def get_pricing_plans(self) -> List[Dict[str, Any]]:
        """Get all pricing plans"""
        return self._pricing_plans or []
    
    def get_default_pricing_plan(self) -> Dict[str, Any]:
        """Get the default pricing plan"""
        for plan in self._pricing_plans or []:
            if plan.get('is_default', False):
                return plan
        # Return first plan if no default found
        return self._pricing_plans[0] if self._pricing_plans else {}
    
    def get_pricing_plan_by_name(self, name: str) -> Dict[str, Any]:
        """Get specific pricing plan by name"""
        for plan in self._pricing_plans or []:
            if plan.get('name') == name:
                return plan
        return {}
    
    def get_active_pricing_plans(self) -> List[Dict[str, Any]]:
        """Get only active pricing plans"""
        return [p for p in self._pricing_plans or [] if p.get('is_active', True)]
    
    # Update methods
    def update_setting(self, section: str, key: str, value: Any) -> bool:
        """Update a setting and reload configuration"""
        success = config_manager.update_setting(section, key, str(value))
        if success:
            self.reload()
        return success
    
    def update_cafe_name(self, name: str) -> bool:
        """Update cafe name"""
        return self.update_setting('general', 'cafe_name', name)
    
    def update_server_port(self, port: int) -> bool:
        """Update server port"""
        return self.update_setting('network', 'server_port', port)
    
    def enable_supabase_sync(self, url: str, key: str) -> bool:
        """Enable Supabase synchronization"""
        success1 = self.update_setting('supabase', 'url', url)
        success2 = self.update_setting('supabase', 'key', key)
        success3 = self.update_setting('supabase', 'sync_enabled', 'true')
        return all([success1, success2, success3])
    
    def disable_supabase_sync(self) -> bool:
        """Disable Supabase synchronization"""
        return self.update_setting('supabase', 'sync_enabled', 'false')
    
    # Utility methods
    def is_supabase_configured(self) -> bool:
        """Check if Supabase is properly configured"""
        return bool(self.supabase_url and self.supabase_key and self.sync_enabled)
    
    def get_currency_symbol(self) -> str:
        """Get currency symbol based on currency code"""
        symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'INR': '₹',
            'CAD': 'C$',
            'AUD': 'A$'
        }
        return symbols.get(self.currency, self.currency)
    
    def format_currency(self, amount: float) -> str:
        """Format amount with currency symbol"""
        symbol = self.get_currency_symbol()
        return f"{symbol}{amount:.2f}"
    
    def __str__(self):
        return f"Settings(cafe='{self.cafe_name}', port={self.server_port})"


# Global settings instance
settings = Settings()

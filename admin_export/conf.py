"""
Configuration module for Django Admin Export Package.

This module provides centralized configuration management and default values
for all export-related settings.
"""

from django.conf import settings
from typing import Dict, Any, Optional


class ExportConfig:
    """Configuration class for export settings."""
    
    # Default configuration values
    DEFAULTS = {
        # CSV export settings
        'CSV_DELIMITER': ',',
        'CSV_ENCODING': 'utf-8',
        'CSV_INCLUDE_BOM': True,
        
        # Excel export settings
        'EXCEL_SHEET_NAME': 'Sheet1',
        'EXCEL_HEADER_STYLE': {
            'font_bold': True,
            'background_color': 'CCCCCC',
            'alignment': 'center'
        },
        'EXCEL_AUTO_COLUMN_WIDTH': True,
        'EXCEL_MAX_COLUMN_WIDTH': 50,
        'EXCEL_MIN_COLUMN_WIDTH': 10,
        
        # General export settings
        'MAX_EXPORT_ROWS': 10000,
        'ENABLE_PROGRESS': True,
        'DEFAULT_FILENAME': 'export',
        'INCLUDE_META_FIELDS': False,
        
        # Logging and monitoring
        'ENABLE_LOGGING': True,
        'LOG_LEVEL': 'INFO',
        'LOG_EXPORT_ACTIVITY': True,
        
        # Security and permissions
        'ENABLE_PERMISSION_CHECKING': True,
        'ALLOW_BULK_EXPORT': True,
        'MAX_BULK_EXPORT_SIZE': 100000,
        
        # Performance settings
        'CHUNK_SIZE': 1000,
        'ENABLE_ASYNC_EXPORT': False,
        'EXPORT_TIMEOUT': 300,  # 5 minutes
        
        # File handling
        'TEMP_FILE_CLEANUP': True,
        'TEMP_FILE_RETENTION': 3600,  # 1 hour
        
        # Internationalization
        'DEFAULT_LANGUAGE': 'en',
        'ENABLE_TRANSLATIONS': True,
        
        # Custom formatters
        'CUSTOM_FORMATTERS': {},
        'FORMATTER_PRIORITY': ['csv', 'xlsx', 'json'],
    }
    
    def __init__(self):
        """Initialize configuration with Django settings."""
        self._config = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from Django settings."""
        for key, default_value in self.DEFAULTS.items():
            setting_key = f'EXPORT_{key}'
            self._config[key] = getattr(settings, setting_key, default_value)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def get_csv_delimiter(self) -> str:
        """Get CSV delimiter setting."""
        return self.get('CSV_DELIMITER')
    
    def get_excel_sheet_name(self) -> str:
        """Get Excel sheet name setting."""
        return self.get('EXCEL_SHEET_NAME')
    
    def get_max_export_rows(self) -> int:
        """Get maximum export rows setting."""
        return self.get('MAX_EXPORT_ROWS')
    
    def is_progress_enabled(self) -> bool:
        """Check if progress tracking is enabled."""
        return self.get('ENABLE_PROGRESS')
    
    def is_logging_enabled(self) -> bool:
        """Check if logging is enabled."""
        return self.get('ENABLE_LOGGING')
    
    def get_log_level(self) -> str:
        """Get logging level."""
        return self.get('LOG_LEVEL')
    
    def is_permission_checking_enabled(self) -> bool:
        """Check if permission checking is enabled."""
        return self.get('ENABLE_PERMISSION_CHECKING')
    
    def get_chunk_size(self) -> int:
        """Get chunk size for processing large datasets."""
        return self.get('CHUNK_SIZE')
    
    def is_async_export_enabled(self) -> bool:
        """Check if async export is enabled."""
        return self.get('ENABLE_ASYNC_EXPORT')
    
    def get_export_timeout(self) -> int:
        """Get export timeout in seconds."""
        return self.get('EXPORT_TIMEOUT')
    
    def get_header_style(self) -> Dict[str, Any]:
        """Get Excel header style configuration."""
        return self.get('EXCEL_HEADER_STYLE')
    
    def is_auto_column_width_enabled(self) -> bool:
        """Check if auto column width is enabled."""
        return self.get('EXCEL_AUTO_COLUMN_WIDTH')
    
    def get_max_column_width(self) -> int:
        """Get maximum column width."""
        return self.get('EXCEL_MAX_COLUMN_WIDTH')
    
    def get_min_column_width(self) -> int:
        """Get minimum column width."""
        return self.get('EXCEL_MIN_COLUMN_WIDTH')
    
    def get_custom_formatters(self) -> Dict[str, Any]:
        """Get custom formatter configurations."""
        return self.get('CUSTOM_FORMATTERS')
    
    def get_formatter_priority(self) -> list:
        """Get formatter priority list."""
        return self.get('FORMATTER_PRIORITY')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self._config.copy()
    
    def update(self, updates: Dict[str, Any]):
        """Update configuration with new values."""
        self._config.update(updates)
    
    def reset_to_defaults(self):
        """Reset configuration to default values."""
        self._config = self.DEFAULTS.copy()


# Global configuration instance
config = ExportConfig()


def get_config() -> ExportConfig:
    """Get the global configuration instance."""
    return config


def get_setting(key: str, default: Any = None) -> Any:
    """Get a specific configuration setting."""
    return config.get(key, default)


# Convenience functions for common settings
def get_csv_delimiter() -> str:
    """Get CSV delimiter setting."""
    return config.get_csv_delimiter()


def get_excel_sheet_name() -> str:
    """Get Excel sheet name setting."""
    return config.get_excel_sheet_name()


def get_max_export_rows() -> int:
    """Get maximum export rows setting."""
    return config.get_max_export_rows()


def is_progress_enabled() -> bool:
    """Check if progress tracking is enabled."""
    return config.is_progress_enabled()


def is_logging_enabled() -> bool:
    """Check if logging is enabled."""
    return config.is_logging_enabled()


def get_log_level() -> str:
    """Get logging level."""
    return config.get_log_level()


def is_permission_checking_enabled() -> bool:
    """Check if permission checking is enabled."""
    return config.is_permission_checking_enabled()


def get_chunk_size() -> int:
    """Get chunk size for processing large datasets."""
    return config.get_chunk_size()


def is_async_export_enabled() -> bool:
    """Check if async export is enabled."""
    return config.is_async_export_enabled()


def get_export_timeout() -> int:
    """Get export timeout in seconds."""
    return config.get_export_timeout() 
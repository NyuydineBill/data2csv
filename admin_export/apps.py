from django.apps import AppConfig
from django.conf import settings


class AdminExportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_export'
    verbose_name = 'Admin Export'
    
    def ready(self):
        """Initialize the app when Django starts."""
        # Import signals if they exist
        try:
            import admin_export.signals
        except ImportError:
            pass
        
        # Set default configuration if not already set
        self._set_default_config()
    
    def _set_default_config(self):
        """Set default configuration values if not already configured."""
        defaults = {
            'EXPORT_CSV_DELIMITER': ',',
            'EXPORT_EXCEL_SHEET_NAME': 'Sheet1',
            'EXPORT_MAX_ROWS': 10000,
            'EXPORT_ENABLE_PROGRESS': True,
            'EXPORT_DEFAULT_FILENAME': 'export',
            'EXPORT_INCLUDE_META_FIELDS': False,
            'EXPORT_ENABLE_LOGGING': True,
            'EXPORT_LOG_LEVEL': 'INFO',
        }
        
        for key, default_value in defaults.items():
            if not hasattr(settings, key):
                setattr(settings, key, default_value)

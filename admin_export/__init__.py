"""
Django Admin Export Package

A comprehensive Django app that enhances the Django admin interface by providing
custom admin actions for exporting data to CSV, Excel, and JSON formats.

Features:
- Easy-to-use mixin for ModelAdmin classes
- Support for CSV, Excel, and JSON exports
- Customizable field selection and formatting
- Built-in error handling and logging
- Progress tracking for large exports
- Internationalization support
- Backward compatibility with legacy functions

Usage:
    from admin_export.admin import ExportMixin
    
    @admin.register(YourModel)
    class YourModelAdmin(ExportMixin, admin.ModelAdmin):
        export_fields = ['name', 'email', 'created_at']
        export_exclude_fields = ['password']
        export_field_labels = {'name': 'Full Name'}
"""

__version__ = '1.0.10'
__author__ = 'Nyuydine Bill'
__email__ = 'billleynyuy@gmail.com'
__license__ = 'MIT'

# Public API
from .admin import ExportMixin, export_to_csv, export_to_excel
from .utils import get_formatter, validate_export_config
from .forms import ExportConfigurationForm, BulkExportForm
from .exceptions import ExportError

__all__ = [
    'ExportMixin',
    'export_to_csv',
    'export_to_excel',
    'get_formatter',
    'validate_export_config',
    'ExportConfigurationForm',
    'BulkExportForm',
    'ExportError',
]

# Version info
VERSION = __version__
VERSION_INFO = tuple(int(x) for x in __version__.split('.'))

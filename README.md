# Django Admin Export Package

[![PyPI version](https://badge.fury.io/py/django-admin-export.svg)](https://badge.fury.io/py/django-admin-export)
[![Python versions](https://img.shields.io/pypi/pyversions/django-admin-export.svg)](https://pypi.org/project/django-admin-export/)
[![Django versions](https://img.shields.io/pypi/djversions/django-admin-export.svg)](https://pypi.org/project/django-admin-export/)
[![License](https://img.shields.io/pypi/l/django-admin-export.svg)](https://pypi.org/project/django-admin-export/)

A comprehensive Django app that enhances the Django admin interface by providing advanced export functionality for CSV, Excel, and JSON formats. Built with modern Python practices, comprehensive error handling, and extensive customization options.

## ✨ Features

- **Multiple Export Formats**: Support for CSV, Excel (XLSX), and JSON exports
- **Easy Integration**: Simple mixin-based approach for ModelAdmin classes
- **Field Customization**: Select specific fields, exclude unwanted ones, and customize labels
- **Advanced Formatting**: Automatic column sizing, header styling, and data type handling
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Progress Tracking**: Built-in progress indicators for large exports
- **Internationalization**: Full i18n support with Django's translation system
- **Backward Compatibility**: Legacy function support for existing implementations
- **Logging & Monitoring**: Built-in logging and audit trails
- **Configuration Options**: Extensive customization through Django settings

## 🚀 Quick Start

### Installation

```bash
pip install django-admin-export
```

### Basic Usage

Add the app to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... other apps
    'admin_export',
]
```

Use the `ExportMixin` in your ModelAdmin:

```python
from django.contrib import admin
from admin_export.admin import ExportMixin
from .models import Product

@admin.register(Product)
class ProductAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'created_at')
    
    # Export configuration
    export_fields = ['name', 'price', 'quantity', 'created_at']
    export_exclude_fields = ['id', 'updated_at']
    export_field_labels = {
        'name': 'Product Name',
        'price': 'Price (USD)',
        'quantity': 'Stock Quantity'
    }
    export_filename = 'products_export'
```

## 📚 Advanced Usage

### Custom Field Selection

```python
@admin.register(Product)
class ProductAdmin(ExportMixin, admin.ModelAdmin):
    # Export only specific fields
    export_fields = ['name', 'price', 'category__name', 'supplier__company_name']
    
    # Exclude sensitive fields
    export_exclude_fields = ['password', 'api_key', 'internal_notes']
    
    # Custom field labels
    export_field_labels = {
        'name': 'Product Name',
        'category__name': 'Category',
        'supplier__company_name': 'Supplier Company'
    }
```

### Format-Specific Configuration

```python
@admin.register(Product)
class ProductAdmin(ExportMixin, admin.ModelAdmin):
    # Enable only specific formats
    enable_csv_export = True
    enable_excel_export = True
    enable_json_export = False
    
    # Custom Excel sheet name
    export_filename = 'product_catalog'
    
    # Limit export size
    export_max_rows = 5000
```

### Advanced Excel Styling

The package automatically applies professional styling to Excel exports:
- Bold headers with gray background
- Auto-adjusted column widths
- Proper data type handling
- Clean, readable formatting

## ⚙️ Configuration

### Django Settings

Add these to your Django settings for global configuration:

```python
# Export configuration
EXPORT_CSV_DELIMITER = ','  # CSV delimiter
EXPORT_EXCEL_SHEET_NAME = 'Data Export'  # Default Excel sheet name
EXPORT_MAX_ROWS = 10000  # Maximum rows per export
EXPORT_ENABLE_PROGRESS = True  # Enable progress tracking
EXPORT_DEFAULT_FILENAME = 'export'  # Default filename prefix
EXPORT_INCLUDE_META_FIELDS = False  # Include Django meta fields
EXPORT_ENABLE_LOGGING = True  # Enable export logging
EXPORT_LOG_LEVEL = 'INFO'  # Log level for exports
```

### Model-Specific Configuration

```python
@admin.register(Product)
class ProductAdmin(ExportMixin, admin.ModelAdmin):
    # Basic export settings
    export_fields = ['name', 'price', 'category', 'created_at']
    export_exclude_fields = ['id', 'updated_at', 'deleted_at']
    
    # Custom labels and formatting
    export_field_labels = {
        'name': 'Product Name',
        'price': 'Price (USD)',
        'category': 'Product Category',
        'created_at': 'Date Added'
    }
    
    # File naming
    export_filename = 'product_catalog'
    
    # Export limits
    export_max_rows = 5000
    
    # Format selection
    enable_csv_export = True
    enable_excel_export = True
    enable_json_export = False
```

## 🔧 API Reference

### ExportMixin

The main mixin class that provides export functionality.

#### Attributes

- `export_fields`: List of field names to export (None = all fields)
- `export_exclude_fields`: List of field names to exclude
- `export_field_labels`: Dictionary mapping field names to custom labels
- `export_filename`: Custom filename for exports
- `export_max_rows`: Maximum rows to export
- `enable_csv_export`: Enable CSV export (default: True)
- `enable_excel_export`: Enable Excel export (default: True)
- `enable_json_export`: Enable JSON export (default: False)

#### Methods

- `get_export_fields(request)`: Get list of fields to export
- `get_export_field_labels(request)`: Get custom field labels
- `get_export_filename(request, format_type)`: Generate export filename
- `get_export_queryset(request, queryset)`: Get queryset for export
- `export_to_csv(request, queryset)`: Export to CSV
- `export_to_excel(request, queryset)`: Export to Excel
- `export_to_json(request, queryset)`: Export to JSON

### Utility Functions

```python
from admin_export.utils import get_formatter, validate_export_config

# Get formatter for specific format
formatter = get_formatter('csv', delimiter=';', include_headers=True)

# Validate export configuration
config = validate_export_config({
    'format': 'xlsx',
    'max_rows': 5000,
    'sheet_name': 'Custom Sheet'
})
```

### Forms

```python
from admin_export.forms import ExportConfigurationForm, BulkExportForm

# Export configuration form
form = ExportConfigurationForm(
    model_fields=Product._meta.fields,
    initial={'format': 'csv', 'max_rows': 1000}
)

# Bulk export form
bulk_form = BulkExportForm(available_models=[
    ('app.Product', 'Products'),
    ('app.Category', 'Categories')
])
```

## 🧪 Testing

Run the test suite:

```bash
python manage.py test admin_export
```

Or use pytest:

```bash
pytest tests/
```

## 📖 Examples

### Basic Product Export

```python
from django.contrib import admin
from admin_export.admin import ExportMixin
from .models import Product

@admin.register(Product)
class ProductAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'created_at')
    list_filter = ('category', 'created_at', 'is_active')
    search_fields = ('name', 'description')
    
    # Export configuration
    export_fields = ['name', 'price', 'category', 'stock', 'created_at']
    export_exclude_fields = ['id', 'updated_at', 'deleted_at']
    export_field_labels = {
        'name': 'Product Name',
        'price': 'Price (USD)',
        'category': 'Category',
        'stock': 'Stock Level',
        'created_at': 'Date Added'
    }
    export_filename = 'product_inventory'
```

### User Management Export

```python
from django.contrib.auth.admin import UserAdmin
from admin_export.admin import ExportMixin

class CustomUserAdmin(ExportMixin, UserAdmin):
    # Export configuration
    export_fields = ['username', 'email', 'first_name', 'last_name', 'date_joined', 'is_active']
    export_exclude_fields = ['password', 'last_login', 'groups', 'user_permissions']
    export_field_labels = {
        'username': 'Username',
        'email': 'Email Address',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'date_joined': 'Registration Date',
        'is_active': 'Account Status'
    }
    export_filename = 'user_management'
    
    # Enable only CSV and Excel
    enable_csv_export = True
    enable_excel_export = True
    enable_json_export = False

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
```

### Advanced Export with Custom Logic

```python
@admin.register(Order)
class OrderAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'total_amount', 'status', 'created_at')
    
    def get_export_fields(self, request):
        """Dynamic field selection based on user permissions."""
        if request.user.is_superuser:
            return ['order_number', 'customer', 'total_amount', 'status', 'created_at', 'notes']
        else:
            return ['order_number', 'customer', 'total_amount', 'status', 'created_at']
    
    def get_export_queryset(self, request, queryset):
        """Filter queryset based on user permissions."""
        if not request.user.is_superuser:
            return queryset.filter(status__in=['confirmed', 'shipped'])
        return queryset
    
    def export_to_excel(self, request, queryset):
        """Custom Excel export with additional formatting."""
        response = super().export_to_excel(request, queryset)
        
        # Add custom logic here if needed
        return response
```

## 🔒 Security & Permissions

The package respects Django's permission system:

- Users can only export data they have permission to view
- Export actions are automatically filtered based on user permissions
- Sensitive fields can be excluded from exports
- Audit logging tracks all export activities

## 🌍 Internationalization

Full support for Django's internationalization system:

```python
from django.utils.translation import gettext_lazy as _

@admin.register(Product)
class ProductAdmin(ExportMixin, admin.ModelAdmin):
    export_field_labels = {
        'name': _('Product Name'),
        'price': _('Price'),
        'category': _('Category'),
    }
```

## 🐛 Troubleshooting

### Common Issues

1. **Export fails silently**: Check Django logs and ensure proper error handling
2. **Large exports timeout**: Adjust `EXPORT_MAX_ROWS` setting
3. **Field not found errors**: Verify field names in `export_fields`
4. **Permission denied**: Check user permissions for the model

### Debug Mode

Enable debug logging:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'admin_export': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/NyuydineBill/data2csv.git
cd data2csv
pip install -e ".[dev]"
python manage.py test
```

### Code Style

We use:
- [Black](https://black.readthedocs.io/) for code formatting
- [Flake8](https://flake8.pycqa.org/) for linting
- [isort](https://pycqa.github.io/isort/) for import sorting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django community for the excellent framework
- OpenPyXL team for Excel support
- All contributors and users of this package

## 📞 Support

- **Documentation**: [GitHub README](https://github.com/NyuydineBill/data2csv#readme)
- **Issues**: [GitHub Issues](https://github.com/NyuydineBill/data2csv/issues)
- **Email**: billleynyuy@gmail.com

---

**Made with ❤️ by Nyuydine Bill**
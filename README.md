```markdown
# Django Admin Export Package

Django Admin Export Package is a Django app that enhances the Django admin interface by providing custom admin actions for exporting selected items to CSV or Excel format.

## Installation

You can install Django Admin Export Package via pip:

```bash
pip install -i https://test.pypi.org/simple/ django-admin-export
```

Make sure to add `'admin_export'` to your `INSTALLED_APPS` in your Django project's settings file.

## Usage

### Registering Admin Actions

To use the export functionality in the Django admin interface, follow these steps:

1. Import the `export_to_csv` and `export_to_excel` functions from `admin_export.admin`.
2. Register these functions as admin actions for the desired models in your `admin.py` file.

```python
from django.contrib import admin
from .models import Product
from admin_export.admin import export_to_csv, export_to_excel

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')
    actions = [export_to_csv, export_to_excel]
```

### Exporting Data

In the Django admin interface, navigate to the list view of a model and select the objects you want to export.
From the "Actions" dropdown menu, select "Export selected items to CSV" or "Export selected items to Excel" to download the exported file.

## Configuration Options

Django Admin Export Package supports the following configuration options:

- `EXPORT_CSV_DELIMITER`: Customize the delimiter used in the exported CSV file (default is `,`).
- `EXPORT_EXCEL_SHEET_NAME`: Customize the name of the Excel worksheet in the exported Excel file (default is "Sheet1").

You can override these options in your Django project's settings file.

## Troubleshooting

If you encounter any issues while using Django Admin Export Package, refer to the following troubleshooting tips:

- **Error: Failed to import test module**: This error may occur if your test file is not located in the same directory as your Django app. Make sure to place your test file in the correct location and adjust the import statements accordingly.

## Contributing

Contributions to Django Admin Export Package are welcome! To contribute, follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Make your changes and write tests for them.
4. Submit a pull request with your changes.

## License

Django Admin Export Package is released under the MIT License. See the [LICENSE](https://github.com/NyuydineBill/django-admin-export/blob/main/LICENSE) file for details.

## Feedback and Support

For questions, feedback, or support requests, please contact the maintainers of Django Admin Export Package at [billleynyuy@gmail.com](mailto:billleynyuy@gmail.com).

Feel free to customize this documentation template to fit the specific features and configuration options of your package. Let me know if you need further assistance or if you have any questions!
```

You can copy this markdown text and paste it into your documentation file. Feel free to customize it further according to your needs. Let me know if you need any further assistance!
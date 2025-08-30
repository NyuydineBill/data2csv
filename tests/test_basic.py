"""Basic tests for Django Admin Export Package."""

from django.test import TestCase
from admin_export.exceptions import ExportError
from admin_export.utils import get_formatter, validate_export_config, get_export_filename


class ExportExceptionsTestCase(TestCase):
    """Tests for custom export exceptions."""
    
    def test_export_error_inheritance(self):
        """Tests that export exceptions inherit from base ExportError."""
        from admin_export.exceptions import (
            ExportError, ExportFormatError, ExportPermissionError,
            ExportLimitError, ExportFieldError, ExportQuerysetError
        )
        
        self.assertTrue(issubclass(ExportFormatError, ExportError))
        self.assertTrue(issubclass(ExportPermissionError, ExportError))
        self.assertTrue(issubclass(ExportLimitError, ExportError))
        self.assertTrue(issubclass(ExportFieldError, ExportError))
        self.assertTrue(issubclass(ExportQuerysetError, ExportError))
    
    def test_export_error_instantiation(self):
        """Tests that export exceptions can be instantiated."""
        from admin_export.exceptions import ExportError, ExportFormatError
        
        error = ExportError("Test error")
        self.assertEqual(str(error), "Test error")
        
        format_error = ExportFormatError("Format error")
        self.assertEqual(str(format_error), "Format error")


class ExportUtilsTestCase(TestCase):
    """Tests for export utility functions."""
    
    def test_get_formatter_csv(self):
        """Tests getting CSV formatter."""
        formatter = get_formatter('csv', delimiter=';')
        self.assertEqual(formatter.delimiter, ';')
        self.assertTrue(formatter.include_headers)
    
    def test_get_formatter_excel(self):
        """Tests getting Excel formatter."""
        formatter = get_formatter('xlsx', sheet_name='Custom Sheet')
        self.assertEqual(formatter.sheet_name, 'Custom Sheet')
    
    def test_get_formatter_json(self):
        """Tests getting JSON formatter."""
        formatter = get_formatter('json')
        self.assertTrue(formatter.include_headers)
    
    def test_get_formatter_invalid(self):
        """Tests getting formatter with invalid format."""
        with self.assertRaises(ValueError):
            get_formatter('invalid_format')
    
    def test_validate_export_config(self):
        """Tests export configuration validation."""
        config = {'format': 'xlsx', 'max_rows': 5000}
        validated = validate_export_config(config)
        
        self.assertIn('include_headers', validated)
        self.assertIn('delimiter', validated)
        self.assertIn('sheet_name', validated)
        
        self.assertIsNone(validated['delimiter'])
    
    def test_get_export_filename(self):
        """Tests export filename generation."""
        filename = get_export_filename('products', 'csv')
        self.assertEqual(filename, 'products.csv')
        
        filename = get_export_filename('products', 'xlsx', '20231201_120000')
        self.assertEqual(filename, 'products_20231201_120000.xlsx')


class ExportMixinBasicTestCase(TestCase):
    """Test case for basic ExportMixin functionality without database."""
    
    def test_export_mixin_import(self):
        """Test that ExportMixin can be imported."""
        from admin_export.admin import ExportMixin
        self.assertTrue(ExportMixin)
    
    def test_export_mixin_attributes(self):
        """Test that ExportMixin has expected attributes."""
        from admin_export.admin import ExportMixin
        
        # Check that the mixin has expected attributes
        self.assertTrue(hasattr(ExportMixin, 'export_fields'))
        self.assertTrue(hasattr(ExportMixin, 'export_exclude_fields'))
        self.assertTrue(hasattr(ExportMixin, 'export_field_labels'))
        self.assertTrue(hasattr(ExportMixin, 'export_filename'))
        self.assertTrue(hasattr(ExportMixin, 'export_max_rows'))
        self.assertTrue(hasattr(ExportMixin, 'enable_csv_export'))
        self.assertTrue(hasattr(ExportMixin, 'enable_excel_export'))
        self.assertTrue(hasattr(ExportMixin, 'enable_json_export'))
    
    def test_export_mixin_methods(self):
        """Test that ExportMixin has expected methods."""
        from admin_export.admin import ExportMixin
        
        # Check that the mixin has expected methods
        self.assertTrue(hasattr(ExportMixin, 'get_export_fields'))
        self.assertTrue(hasattr(ExportMixin, 'get_export_field_labels'))
        self.assertTrue(hasattr(ExportMixin, 'get_export_filename'))
        self.assertTrue(hasattr(ExportMixin, 'get_export_queryset'))
        self.assertTrue(hasattr(ExportMixin, 'export_to_csv'))
        self.assertTrue(hasattr(ExportMixin, 'export_to_excel'))
        self.assertTrue(hasattr(ExportMixin, 'export_to_json'))
        self.assertTrue(hasattr(ExportMixin, 'get_field_value'))
        self.assertTrue(hasattr(ExportMixin, 'get_export_actions'))
        self.assertTrue(hasattr(ExportMixin, 'get_actions'))


class LegacyFunctionsTestCase(TestCase):
    """Test case for legacy export functions."""
    
    def test_legacy_functions_import(self):
        """Test that legacy functions can be imported."""
        from admin_export.admin import export_to_csv, export_to_excel
        
        self.assertTrue(export_to_csv)
        self.assertTrue(export_to_excel)
    
    def test_legacy_functions_attributes(self):
        """Test that legacy functions have expected attributes."""
        from admin_export.admin import export_to_csv, export_to_excel
        
        # Check that functions have short_description
        self.assertTrue(hasattr(export_to_csv, 'short_description'))
        self.assertTrue(hasattr(export_to_excel, 'short_description'))
        
        # Check descriptions
        self.assertIn('CSV', export_to_csv.short_description)
        self.assertIn('Excel', export_to_excel.short_description) 
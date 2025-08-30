from django.test import TestCase, RequestFactory, override_settings
from django.contrib.auth.models import User
from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpResponse
from django.db import models
from admin_export.admin import ExportMixin
from admin_export.exceptions import ExportError
from admin_export.utils import get_formatter, validate_export_config
import csv
import json
from io import BytesIO
from openpyxl import load_workbook


class TestProduct(models.Model):
    """Test model for export functionality."""
    name = models.CharField(max_length=100, verbose_name="Product Name")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'admin_export'
        db_table = 'test_admin_export_product'


class TestProductAdmin(ExportMixin, ModelAdmin):
    """Test admin with export functionality."""
    model = TestProduct
    
    export_fields = ['name', 'price', 'category', 'is_active', 'created_at']
    export_exclude_fields = ['id']
    export_field_labels = {
        'name': 'Product Name',
        'price': 'Price (USD)',
        'category': 'Product Category'
    }
    export_filename = 'test_products'
    export_max_rows = 100


class ExportMixinBasicTestCase(TestCase):
    """Basic tests for ExportMixin without database."""
    
    def setUp(self):
        """Sets up test environment."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='test@example.com'
        )
        self.admin_site = AdminSite()
        self.admin = TestProductAdmin(TestProduct, self.admin_site)
        
        self.request = self.factory.get('/admin/')
        self.request.user = self.user
        setattr(self.request, 'session', {})
        messages = FallbackStorage(self.request)
        setattr(self.request, '_messages', messages)
    
    def test_get_export_fields(self):
        """Tests getting export fields."""
        fields = self.admin.get_export_fields(self.request)
        expected_fields = ['name', 'price', 'category', 'is_active', 'created_at']
        self.assertEqual(fields, expected_fields)
    
    def test_get_export_field_labels(self):
        """Tests getting export field labels."""
        labels = self.admin.get_export_field_labels(self.request)
        expected_labels = {
            'name': 'Product Name',
            'price': 'Price (USD)',
            'category': 'Product Category',
            'is_active': 'is active',
            'created_at': 'created at'
        }
        self.assertEqual(labels, expected_labels)
    
    def test_get_export_filename(self):
        """Tests generating export filename."""
        filename = self.admin.get_export_filename(self.request, 'csv')
        self.assertTrue(filename.startswith('test_products'))
        self.assertTrue(filename.endswith('.csv'))
    
    def test_get_export_actions(self):
        """Tests getting export action names."""
        actions = self.admin.get_export_actions()
        expected_actions = ['export_to_csv', 'export_to_excel']
        self.assertEqual(actions, expected_actions)
        
        self.admin.enable_json_export = True
        actions = self.admin.get_export_actions()
        expected_actions = ['export_to_csv', 'export_to_excel', 'export_to_json']
        self.assertEqual(actions, expected_actions)
    
    def test_get_actions(self):
        """Tests that export actions are added to admin actions."""
        actions = self.admin.get_actions(self.request)
        
        self.assertIn('export_to_csv', actions)
        self.assertIn('export_to_excel', actions)
        
        csv_action = actions['export_to_csv']
        self.assertEqual(csv_action[2], 'Export selected items to CSV')
        
        excel_action = actions['export_to_excel']
        self.assertEqual(excel_action[2], 'Export selected items to Excel')
    
    def test_export_configuration(self):
        """Tests export configuration attributes."""
        self.assertEqual(self.admin.export_fields, ['name', 'price', 'category', 'is_active', 'created_at'])
        self.assertEqual(self.admin.export_exclude_fields, ['id'])
        self.assertEqual(self.admin.export_filename, 'test_products')
        self.assertEqual(self.admin.export_max_rows, 100)
        self.assertTrue(self.admin.enable_csv_export)
        self.assertTrue(self.admin.enable_excel_export)
        self.assertFalse(self.admin.enable_json_export)


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
        from admin_export.utils import get_export_filename
        
        filename = get_export_filename('products', 'csv')
        self.assertEqual(filename, 'products.csv')
        
        filename = get_export_filename('products', 'xlsx', '20231201_120000')
        self.assertEqual(filename, 'products_20231201_120000.xlsx')


class ExportErrorTestCase(TestCase):
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


class ExportMixinIntegrationTestCase(TestCase):
    """Integration tests for ExportMixin with mock data."""
    
    def setUp(self):
        """Sets up test environment with mock data."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='test@example.com'
        )
        self.admin_site = AdminSite()
        self.admin = TestProductAdmin(TestProduct, self.admin_site)
        
        self.request = self.factory.get('/admin/')
        self.request.user = self.user
        setattr(self.request, 'session', {})
        messages = FallbackStorage(self.request)
        setattr(self.request, '_messages', messages)
        
        self.mock_queryset = [
            {
                'name': 'Product 1',
                'price': 10.00,
                'category': 'Electronics',
                'is_active': True,
                'created_at': '2023-01-01 10:00:00'
            },
            {
                'name': 'Product 2',
                'price': 25.50,
                'category': 'Books',
                'is_active': False,
                'created_at': '2023-01-02 11:00:00'
            }
        ]
    
    def test_export_mixin_methods_exist(self):
        """Tests that all required methods exist on the ExportMixin."""
        required_methods = [
            'get_export_fields',
            'get_export_field_labels',
            'get_export_filename',
            'get_export_queryset',
            'export_to_csv',
            'export_to_excel',
            'export_to_json',
            'get_field_value',
            'get_export_actions',
            'get_actions'
        ]
        
        for method_name in required_methods:
            self.assertTrue(hasattr(self.admin, method_name), f"Method {method_name} not found")
    
    def test_export_mixin_attributes(self):
        """Tests that all required attributes exist on the ExportMixin."""
        required_attributes = [
            'export_fields',
            'export_exclude_fields',
            'export_field_labels',
            'export_filename',
            'export_max_rows',
            'enable_csv_export',
            'enable_excel_export',
            'enable_json_export'
        ]
        
        for attr_name in required_attributes:
            self.assertTrue(hasattr(self.admin, attr_name), f"Attribute {attr_name} not found")
    
    def test_export_mixin_default_values(self):
        """Tests default values for ExportMixin attributes."""
        self.assertEqual(self.admin.export_fields, ['name', 'price', 'category', 'is_active', 'created_at'])
        self.assertEqual(self.admin.export_exclude_fields, ['id'])
        self.assertEqual(self.admin.export_filename, 'test_products')
        self.assertEqual(self.admin.export_max_rows, 100)
        self.assertTrue(self.admin.enable_csv_export)
        self.assertTrue(self.admin.enable_excel_export)
        self.assertFalse(self.admin.enable_json_export)
    
    def test_export_mixin_configuration(self):
        """Tests ExportMixin configuration methods."""
        fields = self.admin.get_export_fields(self.request)
        self.assertEqual(fields, ['name', 'price', 'category', 'is_active', 'created_at'])
        
        labels = self.admin.get_export_field_labels(self.request)
        expected_labels = {
            'name': 'Product Name',
            'price': 'Price (USD)',
            'category': 'Product Category',
            'is_active': 'is active',
            'created_at': 'created at'
        }
        self.assertEqual(labels, expected_labels)
        
        filename = self.admin.get_export_filename(self.request, 'csv')
        self.assertTrue(filename.startswith('test_products'))
        self.assertTrue(filename.endswith('.csv'))
        
        actions = self.admin.get_export_actions()
        expected_actions = ['export_to_csv', 'export_to_excel']
        self.assertEqual(actions, expected_actions) 
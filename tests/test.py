from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Product
from admin_export.admin import export_to_csv, export_to_excel
from io import BytesIO
import csv
from openpyxl import load_workbook


class ExportTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product1 = Product.objects.create(name='Product 1', price=10.00, quantity=5)
        self.product2 = Product.objects.create(name='Product 2', price=15.00, quantity=3)

    def test_export_to_csv(self):
        # Simulate exporting selected products to CSV
        queryset = Product.objects.all()
        response = export_to_csv(modeladmin=None, request=None, queryset=queryset)

        # Check response content type
        self.assertEqual(response['Content-Type'], 'text/csv')

        # Read CSV data from response
        csv_data = response.content.decode('utf-8')
        csv_reader = csv.reader(csv_data.splitlines())
        rows = list(csv_reader)

        # Check CSV content
        self.assertEqual(len(rows), 3)  # Header + 2 rows of data
        self.assertEqual(rows[0], ['id', 'name', 'price', 'quantity'])  # Header row
        self.assertEqual(rows[1][1:], ['Product 1', '10.00', '5'])  # First row of data
        self.assertEqual(rows[2][1:], ['Product 2', '15.00', '3'])  # Second row of data

    def test_export_to_excel(self):
        # Simulate exporting selected products to Excel
        queryset = Product.objects.all()
        response = export_to_excel(modeladmin=None, request=None, queryset=queryset)

        # Check response content type
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # Read Excel data from response
        excel_data = BytesIO(response.content)
        workbook = load_workbook(excel_data)
        worksheet = workbook.active

        # Check Excel content
        self.assertEqual(worksheet['A1'].value, 'id')
        self.assertEqual(worksheet['B1'].value, 'name')
        self.assertEqual(worksheet['C1'].value, 'price')
        self.assertEqual(worksheet['D1'].value, 'quantity')
        self.assertEqual(worksheet['B2'].value, 'Product 1')
        self.assertEqual(worksheet['C2'].value, 10.00)
        self.assertEqual(worksheet['D2'].value, 5)
        self.assertEqual(worksheet['B3'].value, 'Product 2')
        self.assertEqual(worksheet['C3'].value, 15.00)
        self.assertEqual(worksheet['D3'].value, 3)

"""
Basic Usage Examples for Django Admin Export Package

This file demonstrates how to use the ExportMixin in your Django admin classes.
"""

from django.contrib import admin
from django.db import models
from admin_export.admin import ExportMixin


# Example Model
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Product Name")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    stock_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.name


# Basic ExportMixin Usage
@admin.register(Product)
class ProductAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock_quantity', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'category')
    list_editable = ('price', 'stock_quantity', 'is_active')
    
    # Export Configuration
    export_fields = ['name', 'price', 'category', 'stock_quantity', 'is_active', 'created_at']
    export_exclude_fields = ['id', 'description', 'updated_at']
    export_field_labels = {
        'name': 'Product Name',
        'price': 'Price (USD)',
        'category': 'Product Category',
        'stock_quantity': 'Stock Level',
        'is_active': 'Active Status',
        'created_at': 'Date Added'
    }
    export_filename = 'product_catalog'
    export_max_rows = 5000


# Advanced ExportMixin Usage with Custom Logic
class AdvancedProductAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock_quantity', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'category')
    
    # Export Configuration
    export_fields = ['name', 'price', 'category', 'stock_quantity', 'is_active', 'created_at']
    export_exclude_fields = ['id', 'description', 'updated_at']
    export_field_labels = {
        'name': 'Product Name',
        'price': 'Price (USD)',
        'category': 'Product Category',
        'stock_quantity': 'Stock Level',
        'is_active': 'Active Status',
        'created_at': 'Date Added'
    }
    export_filename = 'advanced_product_catalog'
    export_max_rows = 10000
    
    # Enable only specific export formats
    enable_csv_export = True
    enable_excel_export = True
    enable_json_export = False
    
    def get_export_fields(self, request):
        """Dynamic field selection based on user permissions."""
        if request.user.is_superuser:
            # Superusers get all fields
            return self.export_fields
        elif request.user.has_perm('app.can_export_sensitive_data'):
            # Users with special permission get most fields
            return ['name', 'price', 'category', 'stock_quantity', 'is_active', 'created_at']
        else:
            # Regular users get limited fields
            return ['name', 'category', 'is_active', 'created_at']
    
    def get_export_queryset(self, request, queryset):
        """Filter queryset based on user permissions."""
        if not request.user.is_superuser:
            # Regular users can only export active products
            return queryset.filter(is_active=True)
        return queryset
    
    def export_to_excel(self, request, queryset):
        """Custom Excel export with additional formatting."""
        # Call parent method first
        response = super().export_to_excel(request, queryset)
        
        # Add custom logic here if needed
        # For example, you could add additional sheets or formatting
        
        return response


# Example with Related Fields
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class ProductWithCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


@admin.register(ProductWithCategory)
class ProductWithCategoryAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at')
    
    # Export with related field data
    export_fields = ['name', 'category__name', 'price', 'created_at']
    export_field_labels = {
        'name': 'Product Name',
        'category__name': 'Category Name',
        'price': 'Price',
        'created_at': 'Created Date'
    }
    export_filename = 'products_with_categories'


# Example with Custom Export Logic
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
    
    def __str__(self):
        return f"Order {self.order_number}"


@admin.register(Order)
class OrderAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'customer_name')
    
    # Export Configuration
    export_fields = ['order_number', 'customer_name', 'total_amount', 'status', 'created_at']
    export_exclude_fields = ['id', 'notes']
    export_field_labels = {
        'order_number': 'Order #',
        'customer_name': 'Customer',
        'total_amount': 'Total Amount (USD)',
        'status': 'Order Status',
        'created_at': 'Order Date'
    }
    export_filename = 'order_summary'
    
    def get_export_queryset(self, request, queryset):
        """Filter orders based on user permissions."""
        if not request.user.is_superuser:
            # Regular users can only export confirmed and shipped orders
            return queryset.filter(status__in=['confirmed', 'shipped'])
        return queryset
    
    def export_to_csv(self, request, queryset):
        """Custom CSV export with additional formatting."""
        # Call parent method first
        response = super().export_to_csv(request, queryset)
        
        # Add custom logic here if needed
        # For example, you could add summary statistics
        
        return response


# Example with Bulk Export
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
    
    def __str__(self):
        return self.name


@admin.register(Customer)
class CustomerAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'email', 'phone')
    
    # Export Configuration
    export_fields = ['name', 'email', 'phone', 'is_active', 'created_at']
    export_exclude_fields = ['id']
    export_field_labels = {
        'name': 'Customer Name',
        'email': 'Email Address',
        'phone': 'Phone Number',
        'is_active': 'Active Status',
        'created_at': 'Registration Date'
    }
    export_filename = 'customer_database'
    
    # Enable all export formats
    enable_csv_export = True
    enable_excel_export = True
    enable_json_export = True
    
    def get_export_fields(self, request):
        """Dynamic field selection based on user permissions."""
        if request.user.is_superuser:
            return self.export_fields
        else:
            # Regular users can't export phone numbers
            return ['name', 'email', 'is_active', 'created_at']


# Example with Custom Field Processing
class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=20, unique=True)
    quantity = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory Items"
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    @property
    def stock_status(self):
        """Calculate stock status based on quantity and reorder level."""
        if self.quantity <= 0:
            return "Out of Stock"
        elif self.quantity <= self.reorder_level:
            return "Low Stock"
        else:
            return "In Stock"
    
    @property
    def total_value(self):
        """Calculate total inventory value."""
        return self.quantity * self.unit_cost


@admin.register(InventoryItem)
class InventoryItemAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('name', 'sku', 'quantity', 'reorder_level', 'unit_cost', 'stock_status', 'total_value')
    list_filter = ('stock_status', 'last_updated')
    search_fields = ('name', 'sku')
    
    # Export Configuration with computed fields
    export_fields = ['name', 'sku', 'quantity', 'reorder_level', 'unit_cost', 'stock_status', 'total_value']
    export_field_labels = {
        'name': 'Item Name',
        'sku': 'SKU',
        'quantity': 'Current Stock',
        'reorder_level': 'Reorder Level',
        'unit_cost': 'Unit Cost (USD)',
        'stock_status': 'Stock Status',
        'total_value': 'Total Value (USD)'
    }
    export_filename = 'inventory_report'
    
    def get_field_value(self, obj, field_name):
        """Custom field value processing for computed fields."""
        if field_name == 'stock_status':
            return obj.stock_status
        elif field_name == 'total_value':
            return f"${obj.total_value:.2f}"
        else:
            return super().get_field_value(obj, field_name) 
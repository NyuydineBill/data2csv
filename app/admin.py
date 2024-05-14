from django.contrib import admin
from .models import Product
from admin_export.admin import export_to_csv

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.

    Attributes:
        list_display (tuple): A tuple of model fields to display in the list view.
        actions (list): A list of actions available in the admin interface.
    """
    list_display = ('name', 'price', 'quantity')
    actions = [export_to_csv]

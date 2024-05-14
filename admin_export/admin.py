from django.contrib import admin
from django.http import HttpResponse
import csv
from openpyxl import Workbook

def export_to_csv(modeladmin, request, queryset):
    """
    Export selected items to CSV format.

    Args:
        modeladmin (admin.ModelAdmin): The admin instance for the model.
        request (HttpRequest): The HTTP request object.
        queryset (QuerySet): The queryset containing the selected objects.

    Returns:
        HttpResponse: HTTP response containing the exported CSV data.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

    writer = csv.writer(response)
    # Write header row
    writer.writerow([field.name for field in queryset.model._meta.fields])
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field.name) for field in queryset.model._meta.fields])
    return response

def export_to_excel(modeladmin, request, queryset):
    """
    Export selected items to Excel format.

    Args:
        modeladmin (admin.ModelAdmin): The admin instance for the model.
        request (HttpRequest): The HTTP request object.
        queryset (QuerySet): The queryset containing the selected objects.

    Returns:
        HttpResponse: HTTP response containing the exported Excel data.
    """
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'

    workbook = Workbook()
    worksheet = workbook.active

    # Write header row
    fields = [field.name for field in queryset.model._meta.fields]
    worksheet.append(fields)

    # Write data rows
    for obj in queryset:
        row = [getattr(obj, field) for field in fields]
        worksheet.append(row)

    workbook.save(response)
    return response

export_to_csv.short_description = "Export selected items to CSV"
export_to_excel.short_description = "Export selected items to Excel"

# Register your models and apply the custom actions
admin.site.add_action(export_to_csv)
admin.site.add_action(export_to_excel)

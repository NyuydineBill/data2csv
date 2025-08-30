from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class ExportConfigurationForm(forms.Form):
    """Form for configuring export options."""
    
    EXPORT_FORMATS = [
        ('csv', 'CSV'),
        ('xlsx', 'Excel'),
        ('json', 'JSON'),
    ]
    
    format = forms.ChoiceField(
        choices=EXPORT_FORMATS,
        label=_("Export Format"),
        initial='csv',
        help_text=_("Choose the format for your export")
    )
    
    include_headers = forms.BooleanField(
        label=_("Include Headers"),
        initial=True,
        help_text=_("Include column headers in the export")
    )
    
    delimiter = forms.ChoiceField(
        choices=[
            (',', 'Comma (,)'),
            (';', 'Semicolon (;)'),
            ('\t', 'Tab'),
            ('|', 'Pipe (|)'),
        ],
        label=_("CSV Delimiter"),
        initial=getattr(settings, 'EXPORT_CSV_DELIMITER', ','),
        help_text=_("Choose the delimiter for CSV exports"),
        required=False
    )
    
    max_rows = forms.IntegerField(
        label=_("Maximum Rows"),
        initial=getattr(settings, 'EXPORT_MAX_ROWS', 10000),
        min_value=1,
        max_value=100000,
        help_text=_("Maximum number of rows to export")
    )
    
    filename = forms.CharField(
        label=_("Custom Filename"),
        max_length=100,
        required=False,
        help_text=_("Custom filename (without extension)")
    )
    
    def __init__(self, *args, **kwargs):
        model_fields = kwargs.pop('model_fields', [])
        super().__init__(*args, **kwargs)
        
        if model_fields:
            # Add field selection
            field_choices = [(field.name, field.verbose_name or field.name) for field in model_fields]
            self.fields['selected_fields'] = forms.MultipleChoiceField(
                choices=field_choices,
                label=_("Fields to Export"),
                initial=[field.name for field in model_fields],
                help_text=_("Select which fields to include in the export"),
                widget=forms.CheckboxSelectMultiple
            )
    
    def clean(self):
        cleaned_data = super().clean()
        format_type = cleaned_data.get('format')
        
        # Only show delimiter for CSV
        if format_type != 'csv':
            cleaned_data['delimiter'] = None
        
        return cleaned_data


class BulkExportForm(forms.Form):
    """Form for bulk export operations."""
    
    models = forms.MultipleChoiceField(
        choices=[],
        label=_("Models to Export"),
        help_text=_("Select which models to export"),
        widget=forms.CheckboxSelectMultiple
    )
    
    format = forms.ChoiceField(
        choices=[
            ('csv', 'CSV'),
            ('xlsx', 'Excel'),
            ('json', 'JSON'),
        ],
        label=_("Export Format"),
        initial='csv'
    )
    
    include_related = forms.BooleanField(
        label=_("Include Related Data"),
        initial=False,
        help_text=_("Include related model data in exports")
    )
    
    def __init__(self, *args, **kwargs):
        available_models = kwargs.pop('available_models', [])
        super().__init__(*args, **kwargs)
        
        if available_models:
            self.fields['models'].choices = available_models 
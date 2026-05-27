from django.contrib import admin
from .models import DataSource, EmissionRecord

@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'source_type', 'uploaded_at', 'uploaded_by']

@admin.register(EmissionRecord)
class EmissionRecordAdmin(admin.ModelAdmin):
    list_display = ['source', 'category', 'quantity', 'unit', 'status', 'created_at']
    list_filter = ['status', 'source__source_type']
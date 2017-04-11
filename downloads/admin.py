from django.contrib import admin
from downloads.models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'timestamp',)
    fieldsets = [
        (None,                  {'fields':  ('name,
                                             'document',)
    ]
    ordering = ['timestamp']
    list_filter = ['timestamp']

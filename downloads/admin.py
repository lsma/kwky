from django.contrib import admin
from downloads.models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    def view_on_site(self, obj):
        return obj.get_absolute_url()
    list_display = ('name',
                    'timestamp',)
    ordering = ['-timestamp']
    list_filter = ['timestamp']

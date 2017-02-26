from django.contrib import admin
from .models import Event

class DefaultAdminModel(admin.ModelAdmin):
    empty_value_display = 'N/A'

@admin.register(Event)
class ProgramAdmin(DefaultAdminModel):
    list_display = ('__str__',
                    'event_start',
                    'begin',
                    'expire',
                    'weight',)
    ordering = ['weight']

from django.contrib import admin
from django.core.urlresolvers import reverse
from .models import StaffProfile, StaffLink, Program, ProgramLink, Showtime

class StaffLinkInline(admin.TabularInline):
    model = StaffLink
    extra = 0

class ProgramLinkInline(admin.TabularInline):
    model = ProgramLink
    extra = 0

class ShowtimeInline(admin.TabularInline):
    model = Showtime
    extra = 0

class DefaultAdminModel(admin.ModelAdmin):
    empty_value_display = 'N/A'


@admin.register(Program)
class ProgramAdmin(DefaultAdminModel):
    list_display = ('abbr', 'title')
    inlines = [ShowtimeInline, ProgramLinkInline]

@admin.register(StaffProfile)
class StaffProfileAdmin(DefaultAdminModel):
    def view_on_site(self, obj):
        return obj.get_absolute_url()

    ordering = ['org_rank']
    list_display = ('__str__',
                    'job_title',
                    'org_rank',
                    'email',
                    'phone',)
    fieldsets = [
        (None,                  {'fields':  (('first_name',
                                              'last_name',),
                                             ('job_title',
                                              'org_rank'),
                                             'program',)
                                }),
        ('Contact',             {'fields':  (('email','phone'),),
                                 'classes': ('collapse'),
                                }),
        ('Biography',           {'fields':  ('picture','bio'),
                                 'classes': ('collapse'),
                                }),
    ]

    inlines = [StaffLinkInline]



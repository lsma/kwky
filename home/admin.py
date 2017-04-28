from django.contrib import admin

from home.models import Slide, Card

class DefaultAdminModel(admin.ModelAdmin):
    empty_value_display = 'N/A'

@admin.register(Slide)
class SlideAdmin(DefaultAdminModel):
    def view_on_site(self, obj):
        return '/'
    list_display = ('title',
                    'url',
                    'weight',
                    'is_active',
                    'begin',
                    'expire',)
    fieldsets = [
        (None,                  {'fields':  (('title', 'url'),
                                             'image',)
                                }),
        ('Display',         {'fields':  ('weight',
                                         ('begin','expire'),)
                                }),
    ]
    ordering = ['begin', 'weight']


@admin.register(Card)
class CardAdmin(DefaultAdminModel):
    def view_on_site(self, obj):
        return '/'
    list_display = ('id',
                    'title',
                    'image',
                    'content',
                    'button',
                    'weight',
                    'is_active',
                    'begin',
                    'expire',)
    fieldsets = [
        (None,                  {'fields':  ('title',
                                             'image',
                                             'content',
                                             'button',)
                                }),
        ('Display',         {'fields':  ('weight',
                                         ('begin','expire'),)
                                }),
    ]
    ordering = ['begin', 'weight']
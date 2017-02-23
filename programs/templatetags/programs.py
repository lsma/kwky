from django import template
from programs.models import Program

register = template.Library()

@register.inclusion_tag('template_menu.html')
def program_menu():
    programs = Program.objects.order_by('title')
    return {'programs': programs}
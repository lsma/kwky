from django import template
from events.models import Event

register = template.Library()

@register.inclusion_tag('event_submenu.html')
def event_menu():
    events = Event.objects.order_by('weight')
    return {'events': events}
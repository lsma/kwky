import datetime, calendar

from markdown import markdown as md

from django import template
from django.utils import timezone
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

from events.models import Event

MIN_TIME = datetime.datetime(datetime.MINYEAR, 1, 1)
MAX_TIME = datetime.datetime(datetime.MAXYEAR, 12, calendar.monthrange(datetime.MAXYEAR,12)[1])

register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def markdown(value, autoescape=True):
    """Converts markdown text into html"""
    #if autoescape:
    #    esc = conditional_escape
    #else:
    #    esc = lambda x: x
    return mark_safe(md(conditional_escape(value)))

@register.simple_tag
def current_events():
    now = timezone.now()
    return Event.objects.filter(expire__range=(now, MAX_TIME),
                                begin__range=(MIN_TIME, now),
                               ).order_by('weight')

@register.inclusion_tag('event_submenu.html')
def event_menu():
    return {'events': current_events()}

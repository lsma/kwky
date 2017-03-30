import datetime, calendar

from markdown import markdown as md

from django import template
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

@register.inclusion_tag('event_submenu.html')
def event_menu():
    now = timezone.now()
    events = Event.objects.filter(expire__range=(now, MAX_TIME),
                                  begin__range=(MIN_TIME, now),
                           ).order_by('weight')
    return {'events': events}

@register.simple_tag
def current_events():
    return Event.objects.filter(expire__range=(now, MAX_TIME),
                                begin__range=(MIN_TIME, now),
                               ).order_by('weight')
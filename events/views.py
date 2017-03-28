import datetime, calendar

from django.utils import timezone
from django.shortcuts import render, get_object_or_404

from .models import Event

MIN_TIME = datetime.datetime(datetime.MINYEAR, 1, 1)
MAX_TIME = datetime.datetime(datetime.MAXYEAR, 12, calendar.monthrange(datetime.MAXYEAR,12)[1])

def event_index(request):
    now = timezone.now()
    events = Event.objects.filter(expire__range=(now, MAX_TIME),
                                  begin__range=(MIN_TIME, now),
                           ).order_by('weight')
    context = {'event_list': events}
    return render(request, 'events/event_index.html', context)


def event_detail(request, url):
    event = get_object_or_404(Event, url__iexact=url)
    context = {'event': event}
    return render(request, 'events/event_detail.html', context)
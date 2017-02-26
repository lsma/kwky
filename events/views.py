from django.shortcuts import render, get_object_or_404

from .models import Event

def event_index(request):
    events = Event.objects.order_by('title')
    context = {'event_list': events}
    return render(request, 'events/event_index.html', context)


def event_detail(request, url):
    event = get_object_or_404(Event, url__iexact=url)
    context = {'event': event}
    return render(request, 'events/event_detail.html', context)
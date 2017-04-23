import datetime

from django.utils import timezone
from django.shortcuts import render

from home.models import Slide, Card

MIN_TIME = datetime.datetime.min # (datetime.MINYEAR, 1, 1)
MAX_TIME = datetime.datetime.max # (datetime.MAXYEAR, 12, calendar.monthrange(datetime.MAXYEAR,12)[1])

def homepage(request):
    now = timezone.now()

    slides = Slide.objects.none().union(
        # Slides with both a publish date and an expire date
        Slide.objects.filter(expire__isnull=False, begin__isnull=False).filter(expire__range=(now, MAX_TIME), begin__range=(MIN_TIME, now)),

        # Slides with only an expiration date
        Slide.objects.filter(expire__isnull=False, begin__isnull=True).filter(expire__range=(now, MAX_TIME)),

        # Slides with only a publish date
        Slide.objects.filter(expire__isnull=True, begin__isnull=False).filter(begin__range=(MIN_TIME, now)),

        # Slides with neither (show all)
        Slide.objects.filter(expire__isnull=True, begin__isnull=True),
    ).order_by('weight')

    cards = Card.objects.filter(expire__isnull=True, begin__isnull=True).union(#Card.objects.none().union(
        # Same as above
        Card.objects.filter(expire__isnull=False, begin__isnull=False).filter(expire__range=(now, MAX_TIME), begin__range=(MIN_TIME, now)),
        Card.objects.filter(expire__isnull=False, begin__isnull=True).filter(expire__range=(now, MAX_TIME)),
        Card.objects.filter(expire__isnull=True, begin__isnull=False).filter(begin__range=(MIN_TIME, now)),
        Card.objects.filter(expire__isnull=True, begin__isnull=True)
    ).order_by('weight')

    #cards = Card.objects.filter(expire__isnull=True, begin__isnull=True)

    context = {"slides": slides, "cards": cards}
    return render(request, 'home/homepage.html', context)

def contact(request, slug):
    return render(request, 'home/contact.html', {})

from django.utils import timezone
from django.db import models


class Event(models.Model):
    # Main info
    url = models.SlugField(max_length=128)
    title = models.CharField(max_length=128)
    contents = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='event/', null=True, blank=True)

    # Address of Event
    location = models.CharField('Name of venue', max_length=256, blank=True)
    address = models.CharField('Exact address of venue', max_length=256, blank=True)

    # EventBrite EID
    eid = models.CharField('EventBrite EID', max_length=24, blank=True)

    # When the event will take place
    event_start = models.DateTimeField()
    event_end  = models.DateTimeField()


    # When the event will be visible on the site
    begin = models.DateTimeField('When to publish')
    expire = models.DateTimeField('When to remove')

    # How high up on the event index should this page be displayed
    weight = models.PositiveIntegerField()


    homepage_slide = models.ImageField(upload_to='slides/', null=True, blank=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('event_detail', args=[self.url.lower()])

    def is_active(self):
        now = timezone.now()
        return (self.begin <= now <= self.expire)
    is_active.admin_order_field = 'event_start'
    is_active.boolean = True
    is_active.short_description = 'Event is live?'

    class Meta:
        get_latest_by = 'event_start'
        ordering = ['begin', 'weight']












import datetime

from django.utils import timezone
from django.db import models

MIN_TIME = datetime.datetime.min.replace(tzinfo=timezone.get_default_timezone())
MAX_TIME = datetime.datetime.max.replace(tzinfo=timezone.get_default_timezone())

class Slide(models.Model):
    # Main Info
    title = models.CharField(max_length=128)
    image = models.ImageField("Slide Image", help_text="Recomended 1750px by 675px", upload_to='home/')
    url = models.URLField("Slide Link")

    # Ordering
    weight = models.PositiveIntegerField()

    # Publishing
    begin = models.DateTimeField('When to publish', null=True, blank=True)
    expire = models.DateTimeField('When to remove', null=True, blank=True)

    def get_absolute_url(self):
        return self.url

    def is_active(self):
        now = timezone.now()
        return (self.begin <= now <= self.expire)
    is_active.admin_order_field = 'event_start'
    is_active.boolean = True
    is_active.short_description = 'Slide is live?'

    class Meta:
        get_latest_by = 'begin'
        ordering = ['begin']

class Card(models.Model):
    # Main Info
    title = models.CharField(max_length=128, blank=True)
    image = models.ImageField(help_text="Recomended 1750px by 675px", upload_to='home/', null=True, blank=True)
    content = models.TextField(blank=True)
    button = models.URLField("Link", blank=True)

    # Ordering
    weight = models.PositiveIntegerField()

    # Publishing
    begin = models.DateTimeField('When to publish', null=True, blank=True)
    expire = models.DateTimeField('When to remove', null=True, blank=True)

    def is_active(self):
        now = timezone.now()
        return ((self.begin if self.begin else MIN_TIME) <= now <= (self.expire if self.expire else MAX_TIME))
    is_active.admin_order_field = 'event_start'
    is_active.boolean = True
    is_active.short_description = 'Card is live?'

    class Meta:
        get_latest_by = 'begin'
        ordering = ['begin']

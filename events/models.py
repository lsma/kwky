from django.db import models

#
#  ***************
#  *             *  Title
#  *    Image    *  Location
#  *             *  Date
#  ***************
#
#  Description.... *********
#  ............... *       *
#  ............... *Tickets*
#  ............... *       *
#  ............... *********
#  ............... *****>>>*
#  ...............


class Event(models.Model):
    # Main info
    url = models.SlugField(max_length=128)
    title = models.CharField(max_length=128)
    contents = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='event/', null=True, blank=True)

    # Address of Event
    location = models.CharField(max_length=128)
    address = models.CharField(max_length=128, blank=True)

    # When the event will take place
    event_start = models.DateTimeField()
    event_end  = models.DateTimeField()


    # When the event will be visible on the site
    begin = models.DateTimeField()
    expire = models.DateTimeField()

    # How high up on the event index should this page be displayed
    weight = models.PositiveIntegerField()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('event_detail', args=[self.url.lower()])

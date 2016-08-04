from datetime import datetime, date

from django.db import models


class Program(models.Model):
    DAY_CHOICES = (('S','Sun'),
                   ('M','Mon'),
                   ('T','Tue'),
                   ('W','Wed'),
                   ('H','Thu'),
                   ('F','Fri'),
                   ('A','Sat'),
                   ('D','Weekday'),
                   ('E','Weekends'),
                   ('X','Every Day'),
                   (None, 'Day of Week'))
    title = models.CharField(max_length=128)
    abbr = models.SlugField('Program ID', max_length=3)
    air_days = models.CharField(max_length=1, choices=DAY_CHOICES)
    picture = models.ImageField(upload_to='program/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_url_comp(self):
        return self.abbr.lower()
    
class StaffProfile(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    job_title = models.CharField(max_length=64)
    org_rank = models.PositiveIntegerField('Orginizational Weight',
        help_text='Staff members who are more important (eg General ' + \
                  'Manager should recieve lower values, while those ' + \
                  'in lower positions (eg Office Assistant) should ' + \
                  'recieve a higher value here.')
    picture = models.ImageField(upload_to='staff/')
    email = models.EmailField('Contact Email')
    phone = models.CharField('Phone Number',max_length=14)
    bio = models.TextField()
    program = models.ForeignKey(
        Program,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return '{} {}'.format(self.first_name.capitalize(),
                              self.last_name.capitalize(),)
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('staff_detail', args=[self.first_name,self.last_name])


class Link(models.Model):
    display_text = models.CharField(max_length=128)
    href = models.URLField('Link URL')
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)

    def __str__(self):
        return '[{}]({})'.format(self.display_text, self.href)

class Showtime(models.Model):
    start_time = models.TimeField()
    duration = models.DurationField()
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}:{}'.format(self.start_time,
                                 self.get_end_time(),
                                 self.duration)

    def get_end_time(self):
        return (datetime.combine(date.min, self.start_time) + self.duration).time()
    


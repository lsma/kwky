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
    air_days = models.TextField(choices=DAY_CHOICES)
    

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


class Link(models.Model):
    display_text = models.CharField(max_length=128)
    href = models.URLField('Link URL')
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)

class Showtime(models.Model):
    start_time = models.TimeField()
    duration = models.DurationField()
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    


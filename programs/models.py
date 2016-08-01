from django.db import models

class StaffProfile(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    job_title = models.CharField(max_length=64)
    picture = models.ImageField(upload_to='staff/')
    bio = models.CharField(max_length=1048)
    program = models.ForeignKey(
        Program,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )


class Link(models.Model):
    display_text = models.CharField(max_length=128)
    href = models.URLField('Link URL')
    staff = models.ForeignKey(Host, on_delete=models.CASCADE)

class Showtime(models.Model):
    start_time = TimeField()
    duration = DurationField()
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    

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
    abbr = SlugField('Program ID', max_length=3)
    air_days = TextField(choices=DAY_CHOICES)
    

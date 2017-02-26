from datetime import datetime, date

from django.db import models


class Program(models.Model):
    title = models.CharField(max_length=128)
    abbr = models.SlugField('Program ID', max_length=3)
    picture = models.ImageField(upload_to='program/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('program_detail', args=[self.abbr.lower()])

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
        related_name='hosts',
    )

    def __str__(self):
        return '{} {}'.format(self.first_name.capitalize(),
                              self.last_name.capitalize(),)

    def get_full_name(self):
        return "{} {}".format(self.first_name.capitalize(),
                              self.last_name.capitalize())

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('staff_detail', args=[self.last_name.lower(),
                                             self.first_name.lower()])


class StaffLink(models.Model):
    display_text = models.CharField(max_length=128)
    href = models.URLField('Link URL')
    staff = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name='links',
    )

    def __str__(self):
        return '<a href="{}">{}</a>'.format(self.href, self.display_text)

class ProgramLink(models.Model):
    display_text = models.CharField(max_length=128)
    href = models.URLField('Link URL')
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name='links',
    )

    def __str__(self):
        return '<a href="{}">{}</a>'.format(self.href, self.display_text)

class Showtime(models.Model):
    on_sun = models.BooleanField('Sunday',      default=False)
    on_mon = models.BooleanField('Monday',      default=False)
    on_tue = models.BooleanField('Tuesday',     default=False)
    on_wed = models.BooleanField('Wednesday',   default=False)
    on_thu = models.BooleanField('Thursday',    default=False)
    on_fri = models.BooleanField('Friday',      default=False)
    on_sat = models.BooleanField('Saturday',    default=False)
    start_time = models.TimeField()
    duration = models.DurationField()
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name='showtimes',
    )

    def __str__(self):
        #return '{}-{}'.format(self.start_time,
        #                      self.get_end_time())
        return '{} from {} to {}'.format(', '.join(self.get_days()),
                                         self.start_time.strftime('%I:%M%p'),
                                         self.get_end_time().strftime('%I:%M%p'))

    def get_days(self):
        s = []
        if self.on_sun: s.append('Sunday')
        if self.on_mon: s.append('Monday')
        if self.on_tue: s.append('Tuesday')
        if self.on_wed: s.append('Wednesday')
        if self.on_thu: s.append('Thursday')
        if self.on_fri: s.append('Friday')
        if self.on_sat: s.append('Saturday')
        return s

    def get_end_time(self):
        return (datetime.combine(date.min, self.start_time) + self.duration).time()



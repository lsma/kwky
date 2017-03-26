from datetime import datetime, date
import string

from django.db import models
from django.core.urlresolvers import reverse

from programs import services


class Program(models.Model):
    title = models.CharField(max_length=128)
    abbr = models.SlugField('Program ID', max_length=3)
    picture = models.ImageField(upload_to='program/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pretty_showtimes = models.TextField(blank=True, editable=False) # the pretty version of the showtimes

    def save(self, *args, **kwargs):
        """
        Override normal save in order to compute the "pretty_showtimes" field.
        The computation of the "pretty" version of the showtimes is a bit heavy,
        and doesn't need to be done every time a view is called.  It only needs
        changing when a showtime is edited, so this is the best place for it.
        """
        self.pretty_showtimes = '\n'.join(services.render_showtimes(
            services.merge_showtimes(
                [(s.get_weekdays_tuple(),
                  s.start_time,
                  s.duration) for s in self.showtimes.all()]
            ),
            timeformat  = '{0:%-I}:{0:%M}{0:%p}',
            entryformat = '{days} at {times}',
        ))
        super(Program, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('program_detail', args=[self.abbr.lower()])

    class Meta:
        ordering = ['title']

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
    email = models.EmailField('Contact Email',blank=True)
    phone = models.CharField('Phone Number',max_length=14,blank=True)
    bio = models.TextField(blank=True)
    slug = models.SlugField(max_length=48, editable=False)
    program = models.ForeignKey(
        Program,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='hosts',
    )

    def save(self, *args, **kwargs):
        s = self.first_name.lower()+' '+self.last_name.lower()
        s = ''.join(e for e in s if (e.isalnum() or e.isspace()))
        s = s.translate(str.maketrans(string.whitespace, '_' * len(string.whitespace)))
        self.slug = s
        super(StaffProfile, self).save(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(self.first_name.capitalize(),
                              self.last_name.capitalize(),)

    def get_full_name(self):
        return "{} {}".format(self.first_name.capitalize(),
                              self.last_name.capitalize())

    def get_absolute_url(self):
        return reverse('staff_detail', args=[self.slug])

    class Meta:
        ordering = ['org_rank', 'last_name']


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

    class Meta:
        order_with_respect_to = 'staff'

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

    class Meta:
        order_with_respect_to = 'program'

class Showtime(models.Model):
    on_mon = models.BooleanField('Monday',      default=False)
    on_tue = models.BooleanField('Tuesday',     default=False)
    on_wed = models.BooleanField('Wednesday',   default=False)
    on_thu = models.BooleanField('Thursday',    default=False)
    on_fri = models.BooleanField('Friday',      default=False)
    on_sat = models.BooleanField('Saturday',    default=False)
    on_sun = models.BooleanField('Sunday',      default=False)
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
        """Returns a list of the days this showtime covers"""
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

    def get_weekdays_tuple(self):
        """Returns a 7 item tuple of booleans signifying which days this
        showtime includes (ISO 8601).  For example, Mon-Fri would be:
        (1,1,1,1,1,0,0).  To get a simple list the days, try get_days"""
        return (self.on_mon, self.on_tue, self.on_wed,
                self.on_thu, self.on_fri, self.on_sat, self.on_sun)




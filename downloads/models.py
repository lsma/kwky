from django.db import models

class Document(models.Model):
    def __str__(self):
        return 'downloads/{}'.format(self.name)

    def get_filename(self, f):
        return str(self)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('downloads_get', args=[self.name])

    name = models.SlugField('URL Name', max_length=128, primary_key=True)
    document = models.FileField(upload_to=get_filename)
    timestamp = models.DateTimeField('Created', auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
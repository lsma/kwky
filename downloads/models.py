from django.db import models

class Document(models.Model):
    def __str__(self, f):
        return 'downloads/{}'.format(self.name)

    name = models.CharField('URL Name', max_length=128, primary_key=True)
    document = models.FileField(upload_to=__str__)
    timestamp = models.DateTimeField('Created', auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
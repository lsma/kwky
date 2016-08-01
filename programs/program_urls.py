from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.program_index, name='program_index'),
    url(r'^(?P<prog_id>[a-z][a-z][a-z])/$', 
        views.program_detail, name='program_detail'),
    url(r'^(?P<prog_id>[a-z][a-z][a-z])/(?P<archive_year>\d\d)/$', 
        views.program_archive, name='program_archive'),
]

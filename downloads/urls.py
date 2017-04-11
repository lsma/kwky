from django.conf.urls import url

from downloads import views

urlpatterns = [
    url(r'^(?P<url>\w+)/$', views.downloads_get, name='downloads_get'),
]
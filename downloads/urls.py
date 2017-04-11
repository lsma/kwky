from django.conf.urls import url

from downloads import views

urlpatterns = [
    url(r'^(?P<name>\w+)/$', views.downloads_get, name='downloads_get'),
]
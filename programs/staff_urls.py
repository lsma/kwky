from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.staff_index, name='staff_index'),
    url(r'^(?P<fn>[a-z]+)_(?P<ln>[a-z]+)/$', views.staff_detail, name='staff_detail'),
]

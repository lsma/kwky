from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.staff_index, name='staff_index'),
    url(r'^(?i)(?P<slug>[a-z_]+)/$', views.staff_detail, name='staff_detail'),
]

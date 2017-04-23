from django.conf.urls import url

from home import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^contact/$', views.contact, name='contact'),
]

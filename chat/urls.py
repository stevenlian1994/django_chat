# chat/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login_and_registration, name='index'),
    url(r"^register$", views.register),
    url(r"^login$", views.login),
    url(r"^logout$", views.logout),
    url(r'^chat/$', views.index, name='find_room'),
    url(r'^chat/(?P<room_name>[^/]+)/$', views.room, name='room'),


]
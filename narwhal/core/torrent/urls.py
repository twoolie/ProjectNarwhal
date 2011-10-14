from django.conf import settings
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
        url(r'^$', views.torrent_list, name='index'),
        url(r'^t/([\w-]+)$', views.torrent, name='index'),
    )
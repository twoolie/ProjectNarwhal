from django.conf import settings
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
        url(r'^user/(?P<username>[\w.@+-]+)?$', views.profile, name='profile'),
        url(r'^user-card/(?P<username>[\w.@+-]+)?$', views.user_card, name='user-card'),
    )
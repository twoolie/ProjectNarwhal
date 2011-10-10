from django.conf import settings
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('', 
        url(r'$^', views.announce, name='announce'),
        url(r'$^', views.scrape, name='scrape'),
    )
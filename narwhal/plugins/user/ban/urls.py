from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^ban/[\w.@+-]+$'),
    url(r'^banned$'),
    url(r'^appeal$'),
)
# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from django.http import HttpResponseServerError
from django.template import loader
from django.shortcuts import RequestContext, render
from django.views.generic.simple import direct_to_template

if 'haystack' in settings.INSTALLED_APPS:
    import haystack; haystack.autodiscover() # autodiscover search indexes
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib import admin; admin.autodiscover()

handler500 = lambda request: HttpResponseServerError(loader.get_template('500.html').render(RequestContext(request)))

urlpatterns = patterns('', 
        url(r'^admin/', include(admin.site.urls)),
        
        url(r'^$', direct_to_template, {'template':'home.html'}, name='home'),
        url(r'^tracker/', include('narwhal.core.tracker.urls', namespace='tracker')),
        url(r'^torrents/', include('narwhal.core.torrent.urls', namespace='torrent')),
        url(r'^profile/', include('narwhal.core.profile.urls', namespace='profile')),
        
        url(r'^500', handler500, name='500'),
        url(r'^404', handler404, name='404'),
    )

if 'messages' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', 
        url(r'^messages/', include('messages.urls')),
    )

if 'django.contrib.admindocs' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', 
        url(r'^admin/docs/', include('django.contrib.admindocs.urls')),
    )

if 'sentry' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^sentry/', include('sentry.web.urls')),
    )

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
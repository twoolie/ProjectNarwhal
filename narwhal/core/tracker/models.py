from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if settings.TRACKER_BACKEND == 'django':
    from narwhal.core.tracker.backends.django import *

elif settings.TRACKER_BACKEND == 'xbtt':
    from backends.xbtt import *
    if 'narwhal.backends.XbttDatabaseRouter' not in settings.DATABASE_ROUTERS :
        raise ImproperlyConfigured("Xbtt requires 'narwhal.backends.XbttDatabaseRouter' in DATABASE_ROUTERS.")
    elif 'xbtt' not in settings.DATABASES \
       or not settings.DATABASES['xbtt']['ENGINE'].contains('mysql') \
       or not settings.DATABASES['xbtt']['NAME'] == 'xbtt':
        raise ImproperlyConfigured("Xbtt Database not correctly setup.")

else:
    raise ImproperlyConfigured("TRACKER_BACKEND must be one of ('django', 'xbtt').")
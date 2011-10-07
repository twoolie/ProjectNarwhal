from base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = PROJECT_ROOT/'whoosh_index'

#Not for use in production
CACHES = { 'default': { 'BACKEND': 'django.core.cache.backends.locmem.LocMemCache' } }

DATABASES = {
    'default': {
        'ENGINE': 'sqlite3',
        'NAME':   PROJECT_ROOT/'sqlite.db',
    }
#   Enable these configs to use xbtt scraper
#   'xbtt': {
#        'ENGINE': 'mysql',
#        'NAME': 'xbtt',
#        'USER': 'xbtt',
#        'PASS': 'INSERT PASS HERE',
#    }
}
from path import path
from datetime import timedelta
#from django.conf import BaseSettings
from narwhal.default_settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

TIME_ZONE = 'Australia/Adelaide'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
LANGUAGES = [
    ('en', 'English'),
]
USE_L10N = True

# Setup Filesystem paths
PROJECT_ROOT = path(__file__).parent.dirname() # get the current folder

MEDIA_ROOT = PROJECT_ROOT / 'media' # FS path for media. must be R/W for user www
MEDIA_URL = '/media/'

STATIC_ROOT = PROJECT_ROOT / 'static-root' # FS path for static content. must be R for user www 
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    PROJECT_ROOT / 'static',
)
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = SITE_NAME+"*&(*&*&^79876*&^*(&6*&6*&6*(&^*(^"

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

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'djangobb_forum.middleware.LastLoginMiddleware',
    #'djangobb_forum.middleware.UsersOnline',
    'django_authopenid.middleware.OpenIDMiddleware',
    'narwhal.core.profile.middleware.UserState',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'narwhal.context_processors.settings',
    'narwhal.context_processors.versions',
    'messages.context_processors.inbox',
    'django_authopenid.context_processors.authopenid',
    #'djangobb_forum.context_processors.forum_settings',
)

TEMPLATE_DIRS = (
    PROJECT_ROOT/'templates',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    #contrib
    'django.contrib.auth',
    'django.contrib.admin',
    # 'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    
    #libs
    'south',
    'taggit',
    'annoying',
    'haystack',
    'bootstrap',
    'registration',
    'sentry.client',
    'debug_toolbar',
    'sorl.thumbnail',
    'django_tables2',
    'django_authopenid',
    
    #apps
    'sentry',
    'messages',
    
    #narwhal core
    'narwhal.core.torrent',
    'narwhal.core.tracker',
    'narwhal.core.profile',
    
    #narwhal plugins
    'narwhal.plugins.irc.bot',
    'narwhal.plugins.book',
    'narwhal.plugins.video',
    'narwhal.plugins.video.tv',
    'narwhal.plugins.video.movie',
    'narwhal.plugins.video.anime',
    
    #djangobb_forum
)

LOGIN_REDIRECT_URL = "/"

INTERNAL_IPS = ('127.0.0.1',)
if 'debug_toolbar' in INSTALLED_APPS:
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

AUTH_PROFILE_MODULE = 'profile.Profile'

HAYSTACK_SITECONF = 'urls'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'sentry': {
            'level': 'DEBUG',
            'class': 'sentry.client.handlers.SentryHandler',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
         },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sorl.thumbnail': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': True
        }
    }
}

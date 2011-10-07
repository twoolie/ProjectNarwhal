import urllib2.HTTPError, logging
from datetime import datetime
log = logging.getLogger('django.auth')

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

__all__ = ('RedditAuthBackend', 'XbttDatabaseRouter',)

class XbttDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'xbtt':
            return 'xbtt'
    
    db_for_write = db_for_read
        
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'xbtt' and not obj2._meta.app_label == 'xbtt':
            return False
    
    def allow_syncdb(self, db, model):
        if model._meta.app_label == 'xbtt':
            if db == 'xbtt':
                return True
            else:
                return False

if 'narwhal.backends.RedditAuthBackends' in settings.AUTH_BACKENDS:
    from reddit import Reddit
    from reddit.api_exceptions import InvalidUserPass
    try:
        from django.conf.settings import JOIN_MIN_COMMENT_KARMA, JOIN_MIN_LINK_KARMA, JOIN_MIN_MEMBER_TIME, USER_AGENT
    except ImportError:
        raise ImproperlyConfigured("Could not import required settings for RedditAuthbackend")

class RedditAuthBackend(ModelBackend):
    """ Custom backend to auth against reddit and cache credentials for when reddit goes offline """
    def authenticate(self, username, password, request=None):
        
        try:
            reddit = Reddit(user_agent=USER_AGENT)
            reddit.login(username, password)
            r_user = reddit.user
            
        except urllib2.URLError:
            log.warning("Could not reach reddit. Is it down?")
            r_user = None
        except InvalidUserPass:
            log.Info(_('User "%s" tried to login without valid credentials')%username)
            return None
        except urllib2.HTTPError as e:
            log.Info(_('User "%s" tried to login without valid credentials')%username)
            return None
        
        try:
            db_user = User.objects.get(username__iexact=username)
            if not r_user and not db_user.check_password(password):
                return None
            if not db_user.is_active: #instead of deleting users, disable them.
                return None
        except User.DoesNotExist:
            #Rules for Joining
            if r_user and r_user.comment_karma >= JOIN_MIN_COMMENT_KARMA \
                      and r_user.link_karma >= JOIN_MIN_LINK_KARMA \
                      and (datetime.now() - datetime.utcfromtimestamp(r_user.created_utc)) >= JOIN_MIN_MEMBER_TIME:
                db_user = User(username=username, is_active=True)
            else:
                return None
        
        db_user.set_password(password) # Hash and store password for offline logins
        db_user.backend = self.__class__.__name__
        db_user.save()
        return db_user

from hashlib import md5
import os

from django.conf import settings
from django.db.models import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from annoying.fields import AutoOneToOneField, JSONField
from sorl.thumbnail import ImageField

class Profile(Model):
    user = AutoOneToOneField(User, related_name='profile')
    
    avatar = ImageField(upload_to='profiles/avatar/', blank=True, null=True)
    
    key = CharField(max_length=32, default=lambda: md5(os.urandom(40)).hexdigest())
    downloaded = PositiveIntegerField(default=0)
    uploaded = PositiveIntegerField(default=0)
    
    # extra_data should only be used for data that should not be 
    # searched upon, such as chat protocol addresses
    data = JSONField(default=lambda: {})
    
    #def __getattr__(self, name):
    #    try: return self.extra_data[name]
    #    except KeyError, e: raise AttributeError, e
    #def __setattr__(self, name, value):
    #    self.extra_data[name] = value
    
    def __unicode__(self):
        return self.user.username
    
    @permalink
    def get_absolute_url(self):
        return ('profile:profile', (), {'username': self.user.username} )
    
    def gravatar(self):
        if self.user.email:
            return "http://www.gravatar.com/avatar/%s.png?d=%s" % (
                md5(self.user.email.lower().strip()).hexdigest(),
                settings.PROFILE_GRAVATAR_STANDIN )
        
    def ratio(self):
        return "%.2f"% (self.total_uploaded / float(self.total_downloaded))
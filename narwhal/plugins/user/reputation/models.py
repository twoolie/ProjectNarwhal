import os
from hashlib import md5

from django.db.models import *

class Reputation(Model):
    positive = PositiveIntegerField()
    negative = PositiveIntegerField()
    
    def __unicode__(self):
        return u"%i (%i-%i)" % (self.positive-self.negative, self.positive, self.negative)
    
    def __repr__(self):
        return self.positive-self.negative
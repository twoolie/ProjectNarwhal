import os
from hashlib import md5

from django.db.models import *
from django.db.models.fields.related import ForeignKey

class Invite(Model):
    inviter = ForeignKey('auth.User', verbose_name=_('inviter'), related_name='user_invited')
    invitee = OneToOneField('auth.User', null=True, blank=True, verbose_name=_('invitee'), related_name='invited_by')
    email_address = CharField(_('email address'), max_length='100')
    code = CharField(_('invite_code'), max_length=32, default=lambda: md5(os.urandom(32)).hexdigest())
    

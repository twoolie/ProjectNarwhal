
from django.db.models import *

from django.contrib.auth.models import User

class Ban(Model):
    user     = ForeignKey(User, verbose_name=_('User'))
    start    = DateTimeField(_('Start'), auto_now=True)
    end      = DateTimeField(_('End'), null=True, blank=True)
    reason   = TextField(_('Reason'))

class Appeal(Model):
    ban      = OneToOneField(Ban, editable=False)
    message  = CharField(_('Message'), max_length=255)
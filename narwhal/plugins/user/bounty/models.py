
from django.db.models import *
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User


class Bounty(Model):
    
    title = CharField(_('Title'), max_length=255)
    description = CharField(_('Description'))
    
    backers = ManyToManyField(User, through='bounty.Backer', verbose_name=_('Backers'))

class Backer(Model):
    
    user = ForeignKey(User)
    bounty = ForeignKey(Bounty)
    
    reputation = PositiveIntegerField(_('Staked Reputation'))

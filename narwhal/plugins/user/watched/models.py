from django.db.models import *
from django.utils.translation import ugettext_lazy as _

from narwhal.plugins.user.stack.models import Stack
from narwhal.plugins.video.models import Video

class WatchedList(Stack):
    
    public_add  = BooleanField(default=False)
    public_view = BooleanField(default=False)
    
    
class Watched(Video):
    
    WATCHED = 1 ; WATCHING = 2; DROPPED =3
    WATCHED_CHOICES = ((WATCHED, _('Watched')), (WATCHING, _('Watching')), (DROPPED, _('Dropped')), )
    
    status = SmallIntegerField(choices = WATCHED_CHOICES, default=WATCHED)
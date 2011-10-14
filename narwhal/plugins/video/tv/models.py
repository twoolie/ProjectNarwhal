
from django.db.models import *
from django.utils.translation import ugettext_lazy as _

from narwhal.core.torrent.models import Category
from narwhal.plugins.video.models import Video

from annoying.functions import get_object_or_None
import conf

class Series(Video):
    """ Keeps track of series """
    
    PENDING = 1; RUNNING = 2; ENDED = 3; HIATUS = 4
    STATUS_CHOICES = ((PENDING,_('Pending')), (RUNNING,_('Running')), (ENDED,_('Ended')), (HIATUS,_('Hiatus')))
    
    category     = ForeignKey(Category, verbose_name=_('Category'), default=lambda: get_object_or_None(Category, title=conf.CATEGORY_NAME))
    description  = TextField(_('Description'), blank=True)
    
    status       = SmallIntegerField(_('Status'), max_length=1, choices=STATUS_CHOICES, default=RUNNING)
    first_aired  = DateField(_('First Aired'), null=True)
    next_aired   = DateField(_('Next Aired'), null=True, blank=True)
    metadata_url = CharField(_('IMDB URL'), max_length=255, null=True, blank=True)

class TVShow(Video):
    """ Base Class for episodic content """
    
    series = ForeignKey(Series, verbose_name=_('series'), blank=True, null=True)
    
    class Meta:
        verbose_name= _('TV Show')
from django.db.models import *
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager
from narwhal.core.torrent.models import Torrent

class Stack(Model):
    
    torrents = ManyToManyField(Torrent, verbose_name=_('Torrents'))
    
    title       = CharField(max_length=255)
    subtitle    = CharField(max_length=255)
    slug        = SlugField(max_length=100)
    
    owner       = ForeignKey()
    public_add  = BooleanField()
    public_view = BooleanField()
    
    description = TextField()
    
    tags = TaggableManager()
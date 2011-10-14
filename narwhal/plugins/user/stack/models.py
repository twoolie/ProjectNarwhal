from django.db.models import *
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from narwhal.core.torrent.models import Torrent

class Stack(Model):
    class Meta:
        ordering = ('title',)
        app_label = 'stack'
        verbose_name = _('Stack')
        verbose_name_plural = _('Stacks')
    
    torrents = ManyToManyField(Torrent, verbose_name=_('Torrents'), related_name='stacks')
    
    owner       = ForeignKey(User, verbose_name=_('Owner'), related_name='stacks')
    public_view = BooleanField(_('Public View'), help_text=_('Other users can view this stack.'))
    public_add  = BooleanField(_('Public Add'), help_text=_('Other users can add to this stack.'))
    
    title       = CharField(_('Title'), max_length=255)
    subtitle    = CharField(_('Subtile'), max_length=255)
    slug        = SlugField(_('Slug'), unique=True, max_length=100)
    
    description = TextField(_('Description'))
    
    tags = TaggableManager()
    
    def public_editable(self):
        return self.public_view and self.public_add
    public_editable.boolean=True
    
    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.subtitle)


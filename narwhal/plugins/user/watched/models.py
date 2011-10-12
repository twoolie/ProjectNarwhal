from django.db.models import *
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from narwhal.plugins.video.models import Video
from narwhal.plugins.user.stack.models import Stack

class Watched(Video):
    class Meta:
        app_label = 'stack' # put this in the stack app in admin interface
        verbose_name = _('Watched')
        verbose_name_plural = _('Watched Videos')
    
    WATCHED = 1 ; WATCHING = 2; ON_HOLD = 3; DROPPED = 4
    WATCHED_CHOICES = ((WATCHED, _('Watched')), (WATCHING, _('Watching')),
                       (ON_HOLD, _('On Hold')), (DROPPED, _('Dropped')), )
    
    user   = ForeignKey(User, verbose_name=_('User'))
    status = SmallIntegerField(_('Status'), choices=WATCHED_CHOICES, default=WATCHED)
    
    def save(self, user=None):
        if 'narwhal.plugins.user.stack' in settings.INSTALLED_APPS:
            stack, created = Stack.objects.get_or_create(title="Watchlist")
            if created:
                stack.slug = 'watchlist-'+self.user.username
                stack.public_view = False
                stack.public_add = False
                stack.owner = user
                stack.description = _('The personal watchlist stack for %(username)s.') % \
                                        {'username': user.username}
            elif not user:
                raise AttributeError("Need a user to create a stack")
    
    def __unicode__(self):
        return u'[%s] %s' % (self.torrent.title, self.get_status_for_display())
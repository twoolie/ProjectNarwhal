
from django.db.models import *
from django.core.exceptions import ImproperlyConfigured

from django.utils.translation import ugettext_lazy as _

from narwhal.plugins.video.tv.models import TVShow

if 'narwhal.plugins.video.tv' not in settings.INSTALLED_APPS:
    raise ImproperlyConfigured('plugin "video.anime" requires "video.tv"')

class Anime(TVShow):
    """ Anime is a specialisation of tv show.
        The fields on this class extend the fields of TVShow """
    
    ova = BooleanField(_('OVA'),default=False)
    omake = BooleanField(_('OMAKE'),default=False)

    class Meta:
        verbose_name= _('Anime')
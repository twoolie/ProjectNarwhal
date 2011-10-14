from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.core.exceptions import ImproperlyConfigured

from django_tables2 import *

class ImageHeadColumn(Column):
    def __init__(self, *args, **kwargs):
        image = kwargs.pop('image')
        if not image: raise ImproperlyConfigured
        super(ImageHeadColumn, self).__init__(*args, **kwargs)
        self.header = mark_safe('<img src="%s" alt="%s">'
                        %(settings.STATIC_URL+image, self.header))
    header = ""


class TorrentTable(Table):
    title      = Column(_('Title'))
    size       = Column(_('Size'))
    seeders    = ImageHeadColumn(_('Seeders'), image='img/icons/16x16/arrow1-up.png')
    leechers   = ImageHeadColumn(_('Leechers'), image='img/icons/16x16/arrow1-down.png')
    downloads  = ImageHeadColumn(_('Downloads'), image='img/icons/16x16/ok.png')
    
    def render_title(self, record):
        tags = " | ".join('<a href="torrent/tagged/%s">%s</a>' % (tag.name, tag.name) for tag in record.tags)
    
    class Meta:
        attrs = {'class':'torrent-table'}
        sortable = False
        template = 'torrent/table.html'
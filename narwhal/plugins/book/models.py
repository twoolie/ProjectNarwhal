from django.db.models import *
from django.utils.translation import ugettext_lazy as _

from narwhal.core.torrent.models import Torrent

class Book(Torrent):
    """ ``Video`` Provides a base class for all video plugins to subclass. """
    
    author = CharField(_('Author'), max_length=255)
    
    def formats(self):
        return (name.rsplit(".") for name in self.files())
    formats.verbose_name = _('Formats')
    
    def validate(self):
        super(Video, self).validate() #call default Torrent validator
        #add validators here
    
    class Meta:
        verbose_name = _('Book')
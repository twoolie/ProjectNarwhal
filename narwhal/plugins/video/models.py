from django.db.models import *
from django.utils.translation import ugettext_lazy as _

from narwhal.core.torrent.models import Torrent

class Video(Torrent):
    """ ``Video`` Provides a base class for all video plugins to subclass. """
    
    def formats(self):
        return (name.rsplit(".") for name in self.files())
    formats.verbose_name = _('Formats')
    
    def validate(self):
        super(Video, self).validate() #call default Torrent validator
        #add validators here
    
    class Meta:
        abstract = True #we add no fields here
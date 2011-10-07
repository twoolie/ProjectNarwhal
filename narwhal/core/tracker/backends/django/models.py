# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

### THIS WILL GO, RE-IMPLEMENTED AS SOMETHING FASTER: REDIS? ###

class Peer(models.Model):
    user = models.ForeignKey('auth.User', verbose_name=_('user'), null=True, related_name='connections')
    torrent = models.ForeignKey('torrent.torrent', verbose_name=_('torrent'), related_name='peers')
    peer_id = models.CharField(_('peer ID'), max_length=128, db_index=True)
    ip = models.IPAddressField(_('IP address'))
    port = models.PositiveIntegerField(_('post'))
    key = models.CharField(_('key'), max_length=255, default='')
    uploaded = models.PositiveIntegerField(_('uploaded'), default=0)
    downloaded = models.PositiveIntegerField(_('downloaded'), default=0)
    left = models.PositiveIntegerField(_('left'), default=0)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return smart_unicode(self.peer_id)

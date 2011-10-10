# -*- coding: utf-8 -*-

import django
from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

### THIS WILL GO, RE-IMPLEMENTED AS SOMETHING FASTER: REDIS? ###

class Peer(models.Model):
    user = models.ForeignKey('auth.User', verbose_name=_('User'), null=True, related_name='connections')
    torrent = models.ForeignKey('torrent.torrent', verbose_name=_('Torrent'), related_name='peers')
    peer_id = models.CharField(_('Peer ID'), max_length=128, db_index=True)
    if django.get_version() >= "1.4":
        ip = models.GenericIPAddressField(_('IP Address'))
    else:
        ip = models.IPAddressField(_('IP Address'))
    port = models.PositiveIntegerField(_('Port'))
    key = models.CharField(_('Key'), max_length=255, default='')
    uploaded = models.PositiveIntegerField(_('Uploaded'), default=0)
    downloaded = models.PositiveIntegerField(_('Downloaded'), default=0)
    left = models.PositiveIntegerField(_('Left'), default=0)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return smart_unicode(self.peer_id)

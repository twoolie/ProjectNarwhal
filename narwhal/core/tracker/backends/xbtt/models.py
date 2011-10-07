import time, datetime
from gettext import gettext as _

# Django
from django.db.models import *

# Modules
from fields import DateTimeStampField, FlagField #compat fields


class Config(Model):
    """ Xbtt Configuration values """
    name  = CharField(_('Name'), db_index=True, max_length=255)
    value = CharField(_('Value'), max_length=255)
    
    class Meta:
        managed = False
        app_label = 'xbtt'
        db_tablename = 'xbt_config'
        verbose_name = _('configuration')
        verbose_name_plural = _('configuration variables')

class Downtime(Model):
    """ Downtimes for maintennance """
    begin = DateTimeStampField(_('Begin'), db_index=True, db_column='begin')
    end   = DateTimeStampField(_('End'), db_index=True, db_column='begin')
    
    class Meta:
        managed=False
        app_label = 'xbtt'
        db_tablename = 'xbt_deny_from_hosts'
        verbose_name = _('Downtime')
        verbose_name_plural = _('Downtimes')

class Torrent(Model):
    """ Torrents being tracked """
    WAS_UPDATED=0; NEEDS_DELETION=1; WAS_UPDATED=2
    FLAG_CHOICES = ((WAS_UPDATED,_('No Changes')), (NEEDS_DELETION,_('Needs Deletion')), (WAS_UPDATED,_('Was Updated')))
    fid       = AutoField(primary_key=True, editable=False, db_column='fid')
    info_hash = CharField(_('Info Hash'), max_length=20, unique=True, db_column='info_hash')
    leechers  = PositiveIntegerField(_('Leechers'), default=0, db_column='leechers')
    seeders   = PositiveIntegerField(_('Seeders'), default=0, db_column='seeders')
    completed = PositiveIntegerField(_('Completed'), default=0, db_column='completed')
    flags     = PositiveIntegerField(_('Flags'), default=0, choices=FLAG_CHOICES, db_column='flags')
    created   = DateTimeStampField(auto_now_add=True, editable=False, db_column='ctime')
    modified  = DateTimeStampField(auto_now=False, editable=False, db_column='mtime')
    
    class Meta:
        managed=False
        app_label = 'xbtt'
        db_tablename = 'xbt_files'
        verbose_name = _('Torrent')
        verbose_name_plural = _('Torrents')

class Peer(Model):
    fid        = ForeignKey(Torrent, verbose_name=_('Torrent'), related_name='torrent',on_delete=CASCADE, db_column='fid')
    uid        = ForeignKey('xbtt.User', verbose_name=_('User'), related_name='user',on_delete=CASCADE, db_column='uid')
    active     = BooleanField(_('Is Active?'), db_column='active')
    announced  = PositiveIntegerField(_('Announced'), help_text=_('How many time has this user Announced?'), db_column='announced')
    downloaded = BigIntegerField(_('Downloaded'), help_text=_('In Bytes'), db_column='downloaded')
    left       = BigIntegerField(_('Left'), help_text=_('In Bytes'), db_column='left')
    uploaded   = BigIntegerField(_('Uploaded'), help_text=_('In Bytes'), db_column='uploaded')
    modified   = DateTimeStampField(_('Modified'), auto_now=True, editable=False, db_column='mtime')
    
    class Meta:
        managed=False
        app_label = 'xbtt'
        db_tablename = 'xbt_files_users'
        verbose_name = _('Peer')
        verbose_name_plural = _('Peers')

class User(Model):
    """ users who have been seen """
    uid        = AutoField(primary_key=True, editable=False, db_column='uid')
    tp_version = IntegerField(db_column='torrent_pass_version')
    downloaded = BigIntegerField(db_column='downloaded')
    uploaded   = BigIntegerField(db_column='uploaded')
    torrents   = ManyToManyField(Torrent, through=Peer, related_name='users')

    class Meta:
        managed=False
        app_label = 'xbtt'
        db_tablename = 'xbt_users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

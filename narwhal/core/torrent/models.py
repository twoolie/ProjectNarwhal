# -*- coding: utf-8 -*-

from hashlib import sha1

from django.db.models import *
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
from treebeard.mp_tree import MP_Node
from annoying.fields import JSONField

class Category(MP_Node):
    """Categories for Torrents"""
    parent = ForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_('Parent'))
    title = CharField(_('Title'), max_length=80)
    image = ImageField(_('Image'), upload_to='img/category', blank=True, null=True)
    count = PositiveIntegerField(editable=False, default=0)
    
    def __unicode__(self):
        return smart_unicode(self.title)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Torrent(Model):
    class Meta:
        verbose_name =_('torrent')
        verbose_name_plural =_('torrents')

    category = ForeignKey(Category)
    title = CharField(_('Title'), max_length=80)
    slug = SlugField(_('Slug'))
    user = ForeignKey('auth.User', blank=True, null=True, verbose_name=_('Author'))
    image = ImageField(_('Image'), upload_to='img/torrents', blank=True, null=True)
    description = TextField(_('Description'))
    html = TextField(editable=False, blank=True)
    added = DateTimeField(_('Added'), auto_now_add=True, editable=False)
    
    torrent = FileField(upload_to='torrent/')
    data = JSONField(editable=False)
    info_hash = CharField(_('Info hash'), max_length=40, db_index=True, editable=False)
    seeders = PositiveIntegerField(editable=False, default=0)
    leechers = PositiveIntegerField(editable=False, default=0)
    comment_count = PositiveIntegerField(editable=False, default=0)
    comments_enabled = BooleanField(_('comments enabled'), default=True)
    
    def files(self):
        if 'length' in self.data['info'].keys():
            return [ self.data['info']['name'] ]
        else:
            return [ ( "/".join(f['path']), f['length']) for f in self.data['info']['files'] ]
    
    def num_files(self):
        try:
            if 'length' in self.data['info'].keys():
                return 1
            elif 'files' in self.data['info'].keys():
                return len(self.data['info']['files'])
        except KeyError:
            pass
        raise ValueError("Torrent does not contain any files/is malformed.")
    
    def size(self):
        try:
            if 'length' in self.data['info'].keys():
                return self.data['info']['length']
            elif 'files' in self.data['info'].keys():
                return reduce(lambda a,b:a+b, (length for file, length in self.data['info']['files'].items()) )
        except KeyError:
            pass
        raise ValueError("Torrent does not contain any files/is malformed.")
    
    def __unicode__(self):
        return smart_unicode(self.title)


    def save(self, **kwargs):
        from markdown import Markdown
        md = Markdown(extensions=['footnotes'], safe_mode=True)
        self.html = md.convert(self.text)
        super(Torrent, self).save(**kwargs)

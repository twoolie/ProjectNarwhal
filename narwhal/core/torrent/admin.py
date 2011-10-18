# -*- coding: utf-8 -*-

from hashlib import sha1
from bencode import bdecode, BTFailure

from django.contrib import admin
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.admin import AdminImageMixin
from markitup.widgets import AdminMarkItUpWidget
from treebeard.admin import TreeAdmin

from forms import CategoryForm, TorrentForm
from models import Category, Torrent


class CategoryAdmin(AdminImageMixin, TreeAdmin):
    #form = CategoryForm
    list_display = ('path', 'title', 'count')
    ordering = ('path', 'title')

class TorrentAdmin(AdminImageMixin, admin.ModelAdmin):
    form = TorrentForm
    list_display = ('title', 'category', 'user', 'added', 'info_hash', 'size', 'seeders', 'leechers')
    prepopulated_fields = {'slug': ('title',) }
    fieldsets = (
        (None, {
            'fields': ( ('title', 'slug',),
                        ('comments_enabled', 'user', 'category'),
                        'description', )
        }),
        (_('Files'), {
            'fields': ( ('torrent', 'image'), ),
        }),
        #(_('Quick Stats'), {
        #    'classes': ('collapse',),
        #    'fields': ( ('size', 'files'), 
        #                ('seeders', 'leechers'),
        #                ('pub_date', 'comment_count'), )
        #}),
    )
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'description':
            kwargs['widget'] = AdminMarkItUpWidget()
        return super(TorrentAdmin, self).formfield_for_dbfield(db_field, **kwargs)
    

admin.site.register(Category, CategoryAdmin)
admin.site.register(Torrent, TorrentAdmin)

# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.admin import AdminImageMixin
from treebeard.admin import TreeAdmin

from forms import CategoryForm, TorrentForm
from models import Category, Torrent


class CategoryAdmin(AdminImageMixin, TreeAdmin):
    #form = CategoryForm
    list_display = ('path', 'title', 'count')
    ordering = ('path', 'title')

class TorrentAdmin(AdminImageMixin, admin.ModelAdmin):
    #form = TorrentForm
    list_display = ('title', 'category', 'user', 'added', 'info_hash', 'size', 'seeders', 'leechers')
    prepopulated_fields = {'slug': ('title',) }
    fieldsets = (
        (None, {
            'fields': ( ('title', 'slug'),
                        ('user', 'comments_enabled'),
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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Torrent, TorrentAdmin)

# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.admin import AdminImageMixin
from treebeard.admin import TreeAdmin

from models import Profile


class ProfileAdmin(AdminImageMixin, admin.ModelAdmin):
    search_fields = ('user__username', 'extra_data')
    list_display = (#'user__username', 'user__date_joined', 
                    'user', 'uploaded', 'downloaded',)
    list_filter = ('user__is_staff',)
    fields = ('user', 'avatar', 'key', 'downloaded', 'uploaded' )
    #fieldsets = (
    #    (None, {
    #        'fields': ( ('title', 'slug'),
    #                    ('user', 'comments_enabled'),
    #                    'description', )
    #    }),
    #    (_('Files'), {
    #        'fields': ( ('torrent', 'image'), ),
    #    }),
        #(_('Quick Stats'), {
        #    'classes': ('collapse',),
        #    'fields': ( ('size', 'files'), 
        #                ('seeders', 'leechers'),
        #                ('pub_date', 'comment_count'), )
        #}),
    #)


admin.site.register(Profile, ProfileAdmin)

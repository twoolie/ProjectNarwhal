
from django.conf import settings

from haystack import site
from haystack.indexes import *
from django.contrib.comments.models import Comment

import models

#This needs to be double checked
class TorrentIndex(RealTimeSearchIndex):
    text        = CharField(document=True, use_template=True)
    description = CharField(model_attr='description')
    title       = CharField(model_attr='title')
    user        = CharField(model_attr='user__username')
    added       = DateTimeField(model_attr='added')
    category    = CharField(model_attr='category__title')
    seeders     = IntegerField(model_attr='seeders')
    leechers    = IntegerField(model_attr='leechers')
    downloaded  = IntegerField(model_attr='downloaded')
    
    if 'django.contrib.comments' in settings.INSTALLED_APPS:
        num_comments = IntegerField()
        def prepare_num_comments(self, obj):
            return Comment.objects.for_model(obj).count()

site.register(models.Torrent, TorrentIndex)

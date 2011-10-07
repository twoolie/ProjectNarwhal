from haystack.indexes import *
from haystack import site

import models

#This needs to be double checked
class TorrentIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    description = CharField(model_attr='text')
    title = CharField(model_attr='title')
    author = CharField(model_attr='user__username')
    added = DateTimeField(model_attr='added')
    category = CharField(model_attr='category__name')
    seeders = CharField(model_attr='seeders')
    leechers = CharField(model_attr='leechers')

site.register(models.Torrent, TorrentIndex)

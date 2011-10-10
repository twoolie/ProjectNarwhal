# ALL PLUGINS THAT MANAGE CATEGORIES MUST HAVE THIS FILE.
# THIS FILE ADDS THE CATEGORY ENTRY FOR THIS PLUGIN

from django.core.files import File
from django.dispatch import receiver
from django.db.models.signals import post_syncdb
from django.db.models.fields.files import FieldFile
from django.contrib.staticfiles.finders import find

from narwhal.core.torrent.models import Category
from narwhal.plugins import video

import conf

@receiver(post_syncdb, sender=Category)
def category_creator(**kwargs):
    category, created = Category.objects.get_or_create(title=conf.CATEGORY_NAME)
    if created:
        category.parent = video.category_creator()
        image = File(find(path='img/icons/film.png'))
        category.image = FieldFile(image)
        category.plugin = __name__ # inserts the name of this module as the controller for this category
        
    return category

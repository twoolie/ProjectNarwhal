# ALL PLUGINS THAT MANAGE CATEGORIES MUST HAVE THIS FILE.
# THIS FILE ADDS THE CATEGORY ENTRY FOR THIS PLUGIN

from django.dispatch import receiver
from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_lazy as _

from narwhal.core.torrent.models import Category

@receiver(post_syncdb, sender=Category)
def category_creator(**kwargs):
    category, created = Category.objects.get_or_create(title='Videos')
    if created:
        category.plugin = __name__ # inserts the name of this module as the controller for this category
    
    print "I Came"
    
    return category

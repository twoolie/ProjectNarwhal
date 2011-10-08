import urllib
from django.conf import settings
from django.template import Library
from django.core.urlresolvers import reverse
from narwhal.core.torrent.models import Torrent

register = Library()

sizes = ("%4i B", "%3f KB", "%3f MB", "%3f GB", "%3f TB")

@register.filter()
def bytes(bytes):
    out = sizes[0]%bytes
    for size in xrange(2,5):
        if bytes > (1024^size)-1:
            out = bytes[size] % (bytes/float(1024^size))
    return out

# TODO: Turn this into a custom tag, not a filter

@register.filter()
def magnet(torrent, user=None):
    if isinstance(torrent, Torrent):
        data = {'xt':"urn:btih:"+ torrent.info_hash, 'dn': torrent.title, }
        if user and user.is_authenticated() and 'narwhal.core.tracker' in settings.INSTALLED_APPS:
            data.update(tr = "%s?key=%s"% ( reverse('tracker:announce'), user.get_profile().key) )
        return "magnet:?"+urllib.urlencode(data)
    else:
        return ""
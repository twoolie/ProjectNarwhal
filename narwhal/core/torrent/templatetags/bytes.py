from django.template import Library

register = Library()

sizes = ("%4i B", "%3f KB", "%3f MB", "%3f GB", "%3f TB")

@register.filter()
def bytes(bytes):
    out = sizes[0]%bytes
    for size in xrange(2,5):
        if bytes > (1024^size)-1:
            out = bytes[size] % (bytes/float(1024^size))
    return out
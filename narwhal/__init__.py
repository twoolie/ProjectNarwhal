VERSION = (0,2,0)
__version__ = VERSION
__author__ = ('twoolie',)

def get_version():
    return "%i.%i" % VERSION[:2]
def get_release():
    if len(VERSION)==4:
        return "%i.%i.%i-%s" % VERSION
    elif len(VERSION)==3:
        return "%i.%i.%i" % VERSION
    else:
        return get_version()
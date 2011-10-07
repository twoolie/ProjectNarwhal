import sys, os, platform

if 'EPIO' in os.environ.keys():
    import epio
else:
    import local
#else:
#    try:
#        __import__(platform.node().split(".")[0].lower())
#    except:
#        pass
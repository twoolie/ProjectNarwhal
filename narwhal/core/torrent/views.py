from annoying.decorators import render_to

from models import Torrent

@render_to("torrent/search.html")
def torrent_list(request):
    
    torrents = Torrent.objects.all()[:30]
    
    return {'torrents':torrents}
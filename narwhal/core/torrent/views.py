from annoying.decorators import render_to

from models import Torrent
from tables import TorrentTable

@render_to("torrent/search.html")
def torrent_list(request):
    
    latest_torrents = Torrent.objects.order_by('-added').values()
    latest_table = TorrentTable(latest_torrents, prefix='latest-')
    
    most_downloaded = Torrent.objects.order_by('-downloaded').values()
    most_table = TorrentTable(most_downloaded, prefix='most-')
    
    return {'latest_table': latest_table,
            'most_table': most_table }
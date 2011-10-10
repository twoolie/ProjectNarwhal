# -*- coding: utf-8 -*-

from urlparse import parse_qsl

from django.conf import settings
from django.http import HttpResponse, Http404
from django.utils.datastructures import MultiValueDictKeyError
from django.core.cache import cache
from django.contrib.auth.models import User

from annoying.decorators import render_to
from bencode import bencode, bdecode

from narwhal.core.profile.models import Profile
from narwhal.core.torrent.models import Torrent
from narwhal.core.tracker.models import Peer

ERROR_INTERVAL = max(3600, settings.TRACKER_ANNOUNCE_INTERVAL)

def announce(request):
    query = dict(parse_qsl(request.META['QUERY_STRING']))
    if not query.get('info_hash'):
        raise Http404
    info_hash = query['info_hash'].encode('hex')
    
    response = {'interval': settings.TRACKER_ANNOUNCE_INTERVAL}
    
    try:
        torrent = Torrent.objects.get(info_hash=info_hash)
        
        # required fields
        ip = request.META['REMOTE_ADDR']
        port = request.GET['port']
        peer_id = request.GET['peer_id']
        event = request.GET.get('event')
        numwant = request.GET.get('numwant',50)
        
        # tracking fields
        if settings.TRACKER_ANNOUNCE_STATS:
            uploaded = request.GET['uploaded']
            downloaded = request.GET['downloaded']
            left = request.GET['left']
            compact = request.GET.get('compact', 0)
        
        # keying for keeping the trash out. DIE UNWASHED MASSES, DIE.
        key = request.GET.get('key')
        if key and (settings.TRACKER_USER_STATS or \
                (settings.TRACKER_PRIVATE and not cache.get("tracker-key-ok-"+key)) ):
            try:
                profile = Profile.objects.get(key = key)
                if settings.TRACKER_USER_STATS:
                    pass # TODO: Add stats code here
                if settings.TRACKER_PRIVATE:
                    cache.set("tracker-key-ok-"+key, True, settings.TRACKER_ANNOUNCE_INTERVAL*5)
            except Profile.DoesNotExist:
                if settings.TRACKER_PRIVATE:
                    raise ValueError('you are not allowed on this tracker')
        
        # SPEED UP WITH REDIS
        
        if 'started' in event:
            peer, created = Peer.objects.get_or_create(peer_id=peer_id, torrent=torrent)
            if created:
                if key and 'profile' in locals():
                    peer.user = profile.user_id
                peer.ip = ip
                peer.port = port
                peer.save()
        elif 'stopped' in event:
            try:
                peer = Peer.objects.get(peer_id=peer_id, torrent=torrent)
                peer.delete()
            except Peer.DoesNotExist:
                pass
        elif 'completed' in event:
            torrent.downloaded = 1
            torrent.save()
        
        if numwant:
            peers = cache.get("tracker-peers-iphandout-"+info_hash)
            if not peers:
                # The random order is expensive. by caching for the announce interval, we guarantee that 
                # a random peer list will be generated every announce period and will be served to all clients
                # looking for that info. The expiry guarantees that new results will be generated on next announce
                peers = [dict((key.replace('_', ' '), value) for key, value in peer.iteritems())
                         for peer in torrent.peers.order_by('?').values('peer_id', 'ip', 'port')[:100] ]
                cache.set("tracker-peers-iphandout-"+info_hash, peers, settings.TRACKER_ANNOUNCE_INTERVAL)
            response['peers'] = peers[:min(numwant, 100)]
            
    except MultiValueDictKeyError:
        response['failure reason'] = 'invalid request, duplicate GET keys.'
    except Torrent.DoesNotExist:
        response['failure reason'] = 'torrent not available'
    except ValueError as e:
        response['failure reason'] = e.message
    
    finally:
        if response.get('failure reason'): response['interval']=ERROR_INTERVAL
        return HttpResponse(bencode(response), content_type='text/plain')

def scrape(request):
    response = {}
    try:
        info_hash = request.GET.get('info_hash')
        if info_hash:
            info = cache.get('tracker-scrape-byhash-'+info_hash)
            if not info:
                t = Torrent.objects.only('seeders', 'leechers', 'downloaded').get(info_hash=info_hash)
                file = {'info_hash':info_hash, 'complete': t.seeders, 
                        'incomplete': t.leechers, 'downloaded': t.downloaded}
                cache.set('tracker-scrape-byhash-'+info_hash, file, settings.TRACKER_SCRAPE_INTERVAL)
            response['files'] = [file]
        
        else:
            files = cache.get('tracker-scrape')
            if not info:
                files = (Torrent.objects.filter(seeders__gt=0).order_by('-added')
                    [:settings.TRACKER_MAX_SCRAPE_RESULTS] # limit the # of returned results
                    .values('info_hash', 'seeders', 'leechers', 'downloaded'))
                files = list({'info_hash':t['info_hash'], 'complete': t['seeders'],
                              'incomplete': t['leechers'], 'downloaded': t['downloaded']}
                             for file in files)
                cache.set('tracker-scrape', files, settings.TRACKER_SCRAPE_INTERVAL)
            response['files'] =  files
        
    except MultiValueDictKeyError:
        hashes = request.GET.getlist('info_hash', None)
        files = Torrent.objects.filter(info_hash__in=hashes)[:settings.TRACKER_MAX_MULTI_SCRAPE]\
            .values('info_hash', 'seeders', 'leechers', 'downloaded')
        files = list({'info_hash':t['info_hash'], 'complete': t['seeders'], 
                      'incomplete': t['leechers'], 'downloaded': t['downloaded']}
                     for file in files)
        response['files'] = files
    except Torrent.DoesNotExist:
        response['failure reason'] = 'torrent not available'
    except ValueError as e:
        response['failure reason'] = e.message
    
    finally:
        if response.get('failure reason'): response['interval']=ERROR_INTERVAL
        return HttpResponse(bencode(response), content_type='text/plain')
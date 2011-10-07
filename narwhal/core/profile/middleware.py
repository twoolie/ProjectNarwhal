import logging

from django.conf import settings
from django.core.cache import cache

USER_TRACK_ACTIVE_KEY = 'profile-user-active-track-%d'
USER_TRACK_IDLE_KEY = 'profile-user-idle-track-%d'

class UserState:
    
    def process_request(self, request):
        try:
            if request.user.id:
                cache.set(USER_TRACK_ACTIVE_KEY % request.user.id, "True", getattr(settings, 'PROFILE_ACTIVE_TIMEOUT',60))
                cache.set(USER_TRACK_IDLE_KEY % request.user.id, "True", getattr(settings, 'PROFILE_ACTIVE_TIMEOUT',300))
        except AttributeError:
            logging.getLogger('django.request').error('user variable not available in request, make sure UserState is after auth in middleware list')

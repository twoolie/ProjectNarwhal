from django.template import Library
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.models import User
from narwhal.core.profile.models import Profile
from narwhal.core.profile.middleware import USER_TRACK_ACTIVE_KEY, USER_TRACK_IDLE_KEY
import logging

register = Library()

@register.filter()
def profilelink(user):
    if isinstance(user, User):
        try:
            return user.profile.get_absolute_url()
        except Profile.DoesNotExist:
            return ""
    elif isinstance(user, Profile):
        return user.get_absolute_url()
    else:
        return ""

@register.filter()
def active(user, state=None):
    if isinstance(user, Profile):
        id = user.user_id
    if isinstance(user, User):
        id = user.id
    if id:
        #get both keys at once to avoid 2 cache round trips
        #res = cache.get_many(USER_TRACK_ACTIVE_KEY % id, USER_TRACK_IDLE_KEY % id)
        if cache.get(USER_TRACK_ACTIVE_KEY%id):
            return "online"
        elif cache.get(USER_TRACK_IDLE_KEY % id):
            return "idle"
        elif state:
            return "offline"
        else:
            return "" #return empty string, evaluates to false
    else:
        return ""
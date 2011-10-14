
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to

from django.contrib.auth.models import User

from .forms import LoginForm


@login_required
@render_to('profile/profile.html')
def profile(request, username=None):
    if not username or username==request.user.username:
        user = request.user
    elif username:
        user = get_object_or_404(User, username=username)
    else:
        raise Http404("Could not find the requested user.")
    
    return {'user':user }

@login_required
@render_to('profile/_user-card.html')
def user_card(request, username=None):
    if username == request.user.username or (not username and request.user.is_authenticated()):
        return {'user': request.user, 'is_me':True }
    elif username:
        return {'user': get_object_or_404(User.objects.select_related('profile', depth=4),
                                          username=username), 'is_me':False}
    else:
        raise Http404("Could not find the requested user.")
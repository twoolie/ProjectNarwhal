from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from annoying.decorators import render_to

@login_required
@render_to('profile/profile.html')
def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    elif request.user.is_authenticated:
        user = request.user
    
    return {'user':user}
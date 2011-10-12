
from django.contrib.auth.decorators import login_required

from annoying.functions import get_object_or_None

from narwhal.plugins.user.stack.models import Stack

@login_required
def watchlist(request):
    
    watchlist = get_object_or_None(Stack, owner=request.user)
    
    return {'watchlist': watchlist}
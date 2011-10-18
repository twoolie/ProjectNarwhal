
## needs work

from datetime import datetime

from django.http import HttpResponseForbidden
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from .models import Ban
from django.template.loader import get_template
from django.template.context import RequestContext
from django.contrib.auth import logout

class BanMiddleware:
    
    def process_view(self, request):
        ban = Ban.objects.filter(user=request.user, start__lte=datetime.now(), end__gte=datetime.now())
        if ban:
            logout(request)
            return HttpResponseForbidden( get_template('user/ban.html').render( RequestContext(request, {'ban':ban} )) )

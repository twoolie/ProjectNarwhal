from __future__ import absolute_import


from django.conf import settings
from django.template import loader
from django.forms.util import ErrorList
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.template.context import RequestContext
from django.core.mail import send_mail, EmailMessage
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required

from .models import Invite
from .forms import InviteForm
from django.contrib.auth.models import User
from narwhal.core.profile.forms import SignupForm

class InviteUser(FormView):
    template_name = 'send_invite.html'
    form_class = InviteForm
    success_url = reverse('invite-sent')
        
    def form_valid(self, form):
        invite = Invite(inviter = self.request.user, email_address = form.cleaned_data['email_address'])
        message = EmailMessage(subject=_('You have been invited to join %(site_name)s by %(user).') %\
                                            {'site_name': settings.SITE_NAME, 'user': invite.invitee.username },
                               body = loader.get_template("invite_email.html").render(RequestContext({'invite':invite})),
                               to = invite.email_address)
        
        try:
            message.send()
            invite.save()
            return HttpResponseRedirect(self.success_url)
        
        except: 
            form.errors += ErrorList(['Could not send email to that address.'])
            return self.form_invalid(form)

class SignupFromInvite(FormView):
    template_name = 'send_invite.html'
    form_class = SignupForm
    success_url = reverse('login')
    
    def get(self, request, *args, **kwargs):
        
        try:
            self.invite = Invite.objects.get(invitee__exact=None, code = request.GET['key'])
        except KeyError, Invite.DoesNotExist:
            raise Http404
        super(SignupFromInvite, self).get(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = User.objects.create_user(username = form.cleaned_data['username'],
                                        password = form.cleaned_data['password'],
                                        email    = self.invite.email_address )
        user.save()
        self.invite.invitee = user
        self.invite.save()
        
        return HttpResponseRedirect(self.success_url)
    
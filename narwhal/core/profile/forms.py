
from django.forms import *
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from bootstrap.forms import BootstrapForm

class LoginForm(BootstrapForm):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    
    username = CharField(label=_("Username"), max_length=30)
    password = CharField(label=_("Password"), widget=PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise ValidationError(_("This account is inactive."))
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise ValidationError(
                _("Your Web browser doesn't appear to have cookies enabled. "
                  "Cookies are required for logging in."))

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

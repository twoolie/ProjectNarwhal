
from datetime import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

#from narwhal.core.profile import profile_data_fields
from narwhal.core.profile.models import Profile

import conf # plugin specific settings
from models import Invite

class Inviter(Profile):
    def can_send_invites(self, *args, **kwargs):
        if not (datetime.now() - self.user.date_joined >= conf.MIN_MEMBER_AGE):
            return False
        if 'narwhal.plugins.user.reputation' in settings.INSTALLED_APPS \
          and (self.user.profile.data.get('reputation', 0) < conf.MIN_REPUTAION):
            return False
        if self.ratio < conf.MIN_RATIO:
            return False
        if not self.data.get('invites_left', 0) > 0:
            return False
        return True
    
    class Meta:
        abstract=True # We add no fields

#invites do not need to be indexable, so we leave them in the json
#profile_data_fields['general']['invites_left'] = _('Invites Remaining')
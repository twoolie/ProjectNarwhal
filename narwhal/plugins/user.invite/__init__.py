from gettext import gettext as _
from datetime import datetime

from django.core.urlresolvers import reverse

from narwhal.core.profile import profile_data_fields

import conf
from models import Invite

def can_send_invites(user, *args, **kwargs):
    if not (datetime.now() - user.date_joined >= conf.MIN_MEMBER_AGE):
        return False
    if 'narwhal.plugins.user.reputation' in settings.INSTALLED_APPS \
      and (user.profile.data.get('reputation', 0) < conf.MIN_REPUTAION):
        return False
    if user.profile.ratio < conf.MIN_RATIO:
        return False
    if not user.profile.data.get('invites_left', 0) > 0:
        return False
    return True

profile_data_fields['general']['invites_left'] = _('Invites Remaining')
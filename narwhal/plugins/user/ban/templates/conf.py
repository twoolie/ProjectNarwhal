from django.conf import settings

ALLOW_APPEALS = getattr(settings, 'BAN_ALLOW_APPEALS', False)
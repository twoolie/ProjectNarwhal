from datetime import timedelta
from django.conf import settings

MIN_MEMBER_AGE = getattr(settings, 'INVITE_MEMBER_AGE', timedelta(days=3*30) ) # 3 months
MIN_REPUTAION = getattr(settings, 'INVITE_MIN_REPUTAION', 300)
MIN_RATIO = getattr(settings, 'INVITE_MIN_RATIO', 1.0)

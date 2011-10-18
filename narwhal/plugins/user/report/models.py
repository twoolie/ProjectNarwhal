import os
from hashlib import md5

from django.db.models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.generic import ContentType, GenericForeignKey

class Report(Model):
    RULES_VIOLATION = 1; INAPPROPRIATE = 2; WRONG_CATEGORY = 3; BAD_CONTENT = 4;
    REASON_CHOICES = ((RULES_VIOLATION, _('Rules Violation')), (INAPPROPRIATE, _('Inappropriate')),
                      (WRONG_CATEGORY, _('Wrong Category')), (BAD_CONTENT, _('Bad Content')) )
    
    content_type = ForeignKey(ContentType)
    object_id    = PositiveIntegerField()
    content      = GenericForeignKey('content_type', 'object_id', verbose_name = 'Content')
    
    reporter     = ForeignKey('auth.User', verbose_name=_('Reporter'), related_name='invites_sent')
    reason       = PositiveIntegerField(_('Reason'), choices=REASON_CHOICES)
    title        = CharField(_('Title'), max_length=255)
    extra_desc   = TextField(_('Extra Description'), blank=True, null=True)
    

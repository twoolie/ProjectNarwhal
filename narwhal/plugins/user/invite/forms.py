
from django.forms import *
from bootstrap.forms import *

from models import Invite

class InviteForm(BootstrapForm):
    
    email_address = EmailField()


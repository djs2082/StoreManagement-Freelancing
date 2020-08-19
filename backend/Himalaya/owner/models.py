from django.db import models
from django.db import models
from django.conf import settings
from rest_framework.authtoken.models import Token
import datetime
from django.utils.timezone import now,localtime
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
	if created:
		Token.objects.create(user=instance)


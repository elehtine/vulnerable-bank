from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

class Message(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    text = models.TextField()

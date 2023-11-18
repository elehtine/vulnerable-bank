from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    iban = models.CharField(max_length=30, unique=True)
    balance = models.IntegerField()

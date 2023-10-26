from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=User.objects.get(username="admin").pk,
    )
    iban = models.CharField(max_length=30, unique=True)
    balance = models.IntegerField()

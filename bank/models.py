from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    iban = models.CharField(max_length=30, unique=True)
    balance = models.IntegerField()

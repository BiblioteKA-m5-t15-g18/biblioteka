from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField()
    password = models.CharField(max_length=120)
    address = models.CharField(max_length=255, null=True)
    staff = models.BooleanField(default=False)
    block = models.BooleanField(default=False)
    timeBlock = models.DateTimeField(null=True, blank=True)

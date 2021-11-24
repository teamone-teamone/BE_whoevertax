from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(verbose_name="email id",
                              max_length=64, unique=True)
    nickname = models.CharField(max_length=30, default="")
    date_joined = models.DateTimeField(default=timezone.now)

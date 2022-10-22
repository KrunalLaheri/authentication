from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    username = None
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class UserToken(models.Model):
    user_id = models.IntegerField()
    refresh_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

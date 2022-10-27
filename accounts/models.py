from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    username = None
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    is_student = models.BooleanField()
    is_teacher = models.BooleanField()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Student(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    admission_date = models.DateField()


class Teacher(models.Model):
    teacher = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    joining_date = models.DateField()


class UserToken(models.Model):
    user_id = models.IntegerField()
    refresh_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()


class Reset(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)

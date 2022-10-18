from dataclasses import field
from pyexpat import model
from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

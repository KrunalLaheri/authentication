from rest_framework.serializers import ModelSerializer
from .models import User,Student,Teacher


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'is_staff', 'is_superuser', 'password','is_student','is_teacher']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'write_only': True},
            'is_superuser': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ['student', 'name', 'admission_date']

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['teacher', 'name', 'joining_date']

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance




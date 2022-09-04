from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, Doctor, Patient


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["id"] = self.user.id
        data["email"] = self.user.email
        data["role"] = self.user.role
        return data


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "role",
            "first_name",
            "last_name",
            "password",
        )
        validators = [
            UniqueTogetherValidator(queryset=CustomUser.objects.all(), fields=["email"])
        ]


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(queryset=CustomUser.objects.all(), fields=["email"])
        ]


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(queryset=CustomUser.objects.all(), fields=["email"])
        ]

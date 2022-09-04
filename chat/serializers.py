from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . import models


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = "__all__"
        validators = [
            # UniqueTogetherValidator(queryset=CustomUser.objects.all(), fields=["email"])
        ]


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Thread
        fields = "__all__"
        depth = 1
        validators = [
            # UniqueTogetherValidator(queryset=CustomUser.objects.all(), fields=["email"])
        ]


class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = "__all__"
        validators = [
            # UniqueTogetherValidator(queryset=CustomUser.objects.all(), fields=["email"])
        ]

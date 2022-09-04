from rest_framework import serializers

from auth_and_reg.serializers import UserSerializer
from . import models


class AppointmentGetSerializer(serializers.ModelSerializer):
    """Defines the serializer class for the Appointment model"""

    created_by = UserSerializer()

    class Meta:
        model = models.Appointment
        fields = "__all__"
        depth = 1


class AppointmentCreateSerializer(serializers.ModelSerializer):
    """Defines the serializer class for the Appointment model"""

    class Meta:
        model = models.Appointment
        fields = "__all__"

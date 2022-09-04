from django.shortcuts import get_object_or_404
from . import (
    models,
    serializers,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from rest_framework_simplejwt.tokens import RefreshToken


class MyTokenObtainPairView(TokenObtainPairView):
    """View for obtainig token."""

    serializer_class = serializers.MyTokenObtainPairSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """View for creating new users"""

    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)


class APISignoutView(APIView):
    """Logout view for the API"""

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # To log out on all devices, pass a "all":"1" in the body of the request
        if self.request.data.get("all"):
            # token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "All refresh tokens blacklisted"})
        refresh_token = self.request.data.get("refresh")
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "refresh token blacklisted"})


class BioUpdateView(generics.RetrieveUpdateAPIView):
    """View for updating user biodata"""

    serializer_class = None
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):

        if self.serializer_class is None:
            if self.request.user.role == "Doctor":
                self.serializer_class = serializers.DoctorSerializer
            elif self.request.user.role == "Patient":
                self.serializer_class = serializers.PatientSerializer
            else:
                return Response(
                    {"error": "User not a Patient nor Doctor"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return super().get_serializer_class()

    def get_queryset(self):
        if self.request.user.role == "Doctor":
            self.queryset = models.Doctor.objects.all()
        if self.request.user.role == "Patient":
            self.queryset = models.Patient.objects.all()
        else:
            return Response(
                {"error": "User not a Patient nor Doctor"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return super().get_queryset()

    def get_object(self):
        user = self.request.user
        if user.role == "Doctor":
            return get_object_or_404(models.Doctor, id=user)
        elif user.role == "Patient":
            return get_object_or_404(models.Patient, id=user)
        else:
            return Response(
                {"error": "User not a Patient nor Doctor"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DoctorsView(generics.ListAPIView):
    serializer_class = serializers.DoctorSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        filter = {k: v for k, v in self.request.data.items() if v is not None}
        return models.Doctor.objects.filter(**filter)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PatientsView(generics.ListAPIView):
    serializer_class = serializers.PatientSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        filter = {k: v for k, v in self.request.data.items() if v is not None}
        return models.Patient.objects.filter(**filter)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

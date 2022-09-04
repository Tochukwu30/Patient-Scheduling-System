from xmlrpc.client import ResponseError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.views import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from auth_and_reg import models as auth_and_reg_models
from . import models, serializers, pagination

# Create your views here.


class AppointmentView(generics.RetrieveUpdateAPIView):
    pass


class AppointmentListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = pagination.AppointmentsPagination
    serializer_class = serializers.AppointmentGetSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "Doctor":
            query_set = models.Appointment.objects.filter(
                doctor=auth_and_reg_models.Doctor.objects.get(id=user)
            )
        elif user.role == "Patient":
            query_set = models.Appointment.objects.filter(
                patient=auth_and_reg_models.Patient.objects.get(id=user)
            )
        else:
            query_set = models.Appointment.objects.all()
        return query_set


class CreateAppointmentView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AppointmentCreateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data["created_by"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class UpdateAppointmentView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AppointmentCreateSerializer

    def get_queryset(self):
        self.queryset = models.Appointment.objects.filter(
            id=self.request.data["id"],
        )
        return super().get_queryset()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = get_object_or_404(self.get_queryset())
        if instance.status == "scheduled":
            data = {"status": request.data["status"]}
            if request.data["status"] == "cancelled":
                data["cancelled_on"] = str(timezone.now())
            if request.data["status"] == "confirmed":
                data["confirmed_on"] = str(timezone.now())
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, "_prefetched_objects_cache", None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        return Response(
            {"error": "Cannot update a confirmed or cancelled appointment"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

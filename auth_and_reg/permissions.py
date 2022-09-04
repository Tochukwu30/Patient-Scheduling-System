from rest_framework.permissions import BasePermission


class IsDoctor(BasePermission):
    """
    Allows access only to Doctors.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == "Doctor")


class IsPatient(BasePermission):
    """
    Allows access only to Patients.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == "Patient")

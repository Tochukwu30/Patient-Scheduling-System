from rest_framework import pagination


class AppointmentsPagination(pagination.CursorPagination):
    ordering = "-created_on"

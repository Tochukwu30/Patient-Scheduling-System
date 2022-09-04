from rest_framework import pagination


class ThreadPagination(pagination.CursorPagination):
    ordering = "-updated"

from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model
from django.shortcuts import Http404
from rest_framework.views import APIView
from rest_framework import generics, status, pagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from chat.models import Thread, Message
from . import serializers
from .pagination import ThreadPagination


class ThreadView(APIView):
    serializer_class = serializers.ThreadSerializer
    # pagination_class = pagination.CursorPagination
    paginator = pagination.CursorPagination()

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_user_id = self.kwargs.get("user_id")
        self.other_user = get_user_model().objects.get(id=other_user_id)
        obj = Thread.objects.get_or_create_personal_thread(
            self.request.user, self.other_user
        )
        if obj == None:
            raise Http404
        return obj

    def get(self, request, **kwargs):
        messages = self.get_object().message_set.all().order_by("-created")
        paginated_messages = self.paginator.paginate_queryset(messages, request=request)
        serializer = serializers.MessageSerializer(paginated_messages, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, **kwargs):
        self.object = self.get_object()
        thread = self.get_object()
        data = request.data
        user = request.user
        text = data["message"]
        Message.objects.create(sender=user, thread=thread, text=text)
        return Response({}, status=status.HTTP_201_CREATED)


class ThreadListView(generics.ListAPIView):
    serializer_class = serializers.ThreadSerializer
    pagination_class = ThreadPagination
    # queryset = Thread.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        print(self.request.user)
        return Thread.objects.filter(users=self.request.user)

from django.urls import path, include
from chat.views import ThreadListView, ThreadView

app_name = "chat"
urlpatterns = [
    path("<int:user_id>/", ThreadView.as_view()),
    path("", ThreadListView.as_view()),
]

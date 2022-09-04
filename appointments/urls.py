from django.urls import path
from . import views

app_name = "appointments"
urlpatterns = [
    path("", views.AppointmentListView.as_view()),
    path("create/", views.CreateAppointmentView.as_view()),
    path("update/", views.UpdateAppointmentView.as_view()),
]

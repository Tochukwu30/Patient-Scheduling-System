from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = "auth_and_reg"
urlpatterns = [
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signout/", views.APISignoutView.as_view(), name="signout"),
    path("signup/", views.UserCreateAPIView.as_view(), name="signup"),
    path("bio/", views.BioUpdateView.as_view(), name="bio"),
    path("doctors/", views.DoctorsView.as_view(), name="doctors"),
    path("patients/", views.PatientsView.as_view(), name="patients"),
]

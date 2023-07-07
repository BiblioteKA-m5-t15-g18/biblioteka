from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema


urlpatterns = [
    path("sendmail/", views.SendEmailView.as_view()),
    path("users/", views.UserView.as_view()),
    path("users/<int:pk>/", views.UserDetailView.as_view()),
    path("users/login/", TokenObtainPairView.as_view()),
    path("users/refresh/", TokenRefreshView.as_view()),
    path("users/<int:pk>/historic/", views.UserHistoricDetailView.as_view()),
    path("users/<int:pk>/following/", views.UserFollowDetailView.as_view()),
    path("users/<int:pk>/block/", views.UserBlockView.as_view()),
]
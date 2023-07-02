from django.urls import path
from . import views

urlpatterns = [
    path("books/follow/<int:pk>/", views.FollowView.as_view()),
]

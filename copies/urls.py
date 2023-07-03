from django.urls import path
from . import views

urlpatterns = [
    path("books/copy/", views.PermissionToRentView.as_view()),
]

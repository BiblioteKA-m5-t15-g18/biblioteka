from django.urls import path
from .views import BookView
from loan.views import LoanDetailView

urlpatterns = [
    path("books/", BookView.as_view()),
    path("books/loan/<int:pk>/", LoanDetailView.as_view()),
]

from django.urls import path
from .views import BookViewSet, BookDetailView
from loan.views import LoanDetailView

urlpatterns = [
    path("books/", BookViewSet.as_view()),
    path("books/loan/<int:pk>/", LoanDetailView.as_view()),
    path("books/<int:pk>/", BookDetailView.as_view()),
]

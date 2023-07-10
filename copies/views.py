from .models import Copy
from .serializer import CopySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from django.shortcuts import get_object_or_404
from book.models import Book
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Cópias"])
class PermissionToRentView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    def perform_create(self, serializer):
        book_ret = self.request.data.get("book")
        book = get_object_or_404(Book, id=book_ret)
        serializer.save(book=book)

from rest_framework import generics
from .models import Follow
from users.models import User
from .serializer import FollowSerializer
from .permissions import IsAccountOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from book.models import Book
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Livros seguidos"])
class FollowView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser | IsAuthenticated, IsAccountOwner]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs["pk"])

        if Follow.objects.filter(user=self.request.user, book=book).exists():
            raise ValidationError("Você já está seguindo este livro.")
        else:
            serializer.save(book=book, user=self.request.user)


@extend_schema(tags=["Livros seguidos"])
class UnfollowView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser | IsAuthenticated, IsAccountOwner]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get_object(self):
        user = self.request.user
        book = self.kwargs["pk"]
        if Follow.objects.filter(user=self.request.user, book=book).exists():
            return Follow.objects.filter(user=self.request.user, book=book)
        else:
            raise ValidationError("Você não está seguindo esse livro")

from rest_framework.generics import CreateAPIView
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


class FollowView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser | IsAuthenticated, IsAccountOwner]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs["pk"])
        serializer.save(book=book, user=self.request.user)

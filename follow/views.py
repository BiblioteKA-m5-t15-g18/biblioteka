from rest_framework.generics import CreateAPIView
from .models import Follow
from books import Book
from users import User
from .serializer import FollowSerializer
from .permissions import IsAccountOwner
from rest_framework.permissions import (
    IsAdminUser,
)
from rest_framework_simplejwt.authentication import JWTAuthentication


class FollowView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner | IsAdminUser]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
    book = get_object_or_404(Book, pk=self.kwargs["pk"])
    serializer.save(book=book, user=self.request.user)